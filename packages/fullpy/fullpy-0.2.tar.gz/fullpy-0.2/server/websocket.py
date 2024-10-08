# FullPy
# Copyright (C) 2022-2023 Jean-Baptiste LAMY
# LIMICS (Laboratoire d'informatique médicale et d'ingénierie des connaissances en santé), UMR_S 1142
# INSERM, France

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, datetime
import gevent, gevent.timeout

from fullpy.server.base_rpc import *

  
class BaseWebSocketManager(BaseManager):
  def __init__(self, webapp, session_max_duration, session_max_memory_duration, debug = False):
    super().__init__(webapp, session_max_duration, session_max_memory_duration, debug)
    self._call_id                  = 0
    self._call_id_2_async_callback = {}

#import gevent.lock
#DISABLE_MICROTHREAD_LOCK = gevent.lock.RLock()
    
class GUnicornWebSocketManager(BaseWebSocketManager):
  def loop(self, ws0):
    address        = "%s:%s" % (ws0.environ["REMOTE_ADDR"], ws0.environ["REMOTE_PORT"])
    new_session_id = None
    session        = getattr(ws0.handler, "session", None)
    if session:
      session.set_manager(self)
      session._ws = ws0
    else:
      if self.debug: print("* Fullpy * New websocket connection from %s" % address)
      
    try:
      while not ws0.closed:
        if hasattr(session, "initial_message"): # Initial message, from process switcher
          message = session.initial_message
          del session.initial_message
          session.on_connected()
        else:
          with gevent.Timeout(self.session_max_memory_duration): message = ws0.receive()
          
        #DISABLE_MICROTHREAD_LOCK.acquire()
        if message is None: break
        if message == "":  continue
        if session: session.current_message = message
        
        if self.debug and self.webapp.world and self.webapp.multiprocess and self.webapp.world.graph.db.in_transaction:
          import fullpy.server.gunicorn_backend
          print("\n* Fullpy * WARNING: Quadstore not saved BEFORE receiving message '%s' in process %s!\n" % (message, fullpy.server.gunicorn_backend.CURRENT_WORKER.process_id))

        func_name, call_id, data = message.split(" ", 2)
        call_id = int(call_id)
        if self.debug: print("%s Message received from %s%s: %s(%s)%s" % (datetime.datetime.now().strftime("%d/%m/%y,%H:%M"), session and session.user and ("%s@" % session.user.login) or "", address, func_name, data[1:-1], (" (callback: %s)" % call_id) if call_id else ""), file = sys.stderr)
        data = self.serializer.decode(data)
        
        if func_name == "__ok__":
          done = self._call_id_2_async_callback.pop(call_id, None)
          if done: done(session, data)
          
        else:
          if   func_name == "new_session_id":
            response = new_session_id = self.server_new_session_id(session)
          elif func_name == "open_session": # Must have called new_session_id() before!
            new_session, response = self.open_session(session, new_session_id, *data[1:])
            if (not response[0]) and (session is None):
              new_session, response = self.open_session(None, "", "", *data[2:])
            if response[0]:
              if session: del session._ws
              new_session._ws = ws0
              new_session.on_connected(session)
              session = new_session
            else:
              new_session_id = response[-1]
          else:
            response = self.webapp.rpc_funcs["server_%s" % func_name](session, *data)
            
          if call_id and (not ws0.closed): # ws0 can be closed in case of transfer to another process
            ws0.send("__ok__ %s %s" % (call_id, self.serializer.encode(response)))
            
        if session:
          if self.webapp.persistent_session:
            current_time = time.time()
            if current_time > session.session_last_time + 600:
              with session.namespace:
                session.session_last_time = current_time
              session.namespace.world.save()
          else:
            session.session_last_time = time.time()
            
        if self.debug and self.webapp.world and self.webapp.multiprocess and self.webapp.world.graph.db.in_transaction:
          import fullpy.server.gunicorn_backend
          print("\n* Fullpy * WARNING: Quadstore not saved AFTER receiving message '%s' in process %s!\n" % (message, fullpy.server.gunicorn_backend.CURRENT_WORKER.process_id))
          
        #DISABLE_MICROTHREAD_LOCK.release()
    except gevent.timeout.Timeout: pass
    finally:
      if session:
        session.close()
      try: ws0.close()
      except WebSocketError: pass
      
  def _client_call(self, session_or_group, done, func_name, *args):
    if not ((done is None) or callable(done)): raise ValueError("First argument to remote calls must be the 'done()' callable or None!")
    
    from geventwebsocket.exceptions import WebSocketError
    
    if   isinstance(session_or_group, (list, set)): sessions = session_or_group
    elif session_or_group is None:                  sessions = [session for session in self.sessions.values() if session._ws]
    else:                                           sessions = [session_or_group]
    args = self.serializer.encode(list(args))
    
    for session in sessions:
      if done:
        self._call_id += 1
        self._call_id_2_async_callback[self._call_id] = done
        call_id = self._call_id
      else:
        call_id = 0
      try:
        session._ws.send("%s %s %s" % (func_name, call_id, args))
        #if self.debug: print("Message sent to %s: '%s %s %s'" % (session.session_id or session.session_token, func_name, call_id, args), file = sys.stderr)
      except WebSocketError:
        session.close()
        try: session._ws.close()
        except WebSocketError: pass
    
  def route(self, app, path):
    middleware = _APP_2_MIDDLEWARE.get(app)
    if not middleware: middleware = _APP_2_MIDDLEWARE[app] = app.wsgi_app = GUnicornWebSocketMiddleware(app.wsgi_app)
    middleware.ws_routes[path] = self
    

_APP_2_MIDDLEWARE = {}
class GUnicornWebSocketMiddleware(object):
  def __init__(self, wsgi_app):
    self.wsgi_app  = wsgi_app
    self.ws_routes = {}
    
  def __call__(self, environ, start_response):
    if "wsgi.websocket" in environ:
      self.ws_routes[environ["PATH_INFO"]].loop(environ["wsgi.websocket"])
      return []
    else:
      return self.wsgi_app(environ, start_response)
    
