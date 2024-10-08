# Fullpy

# Copyright (C) 2024 Jean-Baptiste LAMY
# LIMICS (Laboratoire d'informatique mÃ©dicale et d'ingénierie des connaissances en santÃ©)
# UMR_S 1142, INSERM, France

import sys, os, socket, gevent, gevent.pywsgi, json, hashlib, random
import geventwebsocket.handler, geventwebsocket.websocket
from gunicorn.http.wsgi import WSGIErrorsWrapper, FileWrapper

#from owlready2 import *

import fullpy.server.gunicorn_backend

PROCESS_SWITCHER = None
class ProcessSwitcher(object):
  def __init__(self, gunicorn_server, webapp, base_filename, password):
    global PROCESS_SWITCHER
    PROCESS_SWITCHER = self
    
    self.gunicorn_config = fullpy.server.gunicorn_backend.CURRENT_WORKER.cfg
    self.gunicorn_server = gunicorn_server
    self.webapp          = webapp
    self.base_filename   = base_filename
    self.process_id      = fullpy.server.gunicorn_backend.CURRENT_WORKER.process_id
    self.password        = password
    self.filename        = "%s-%s" % (base_filename, self.process_id)
    
    try: os.unlink(self.filename)
    except: pass
    self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    self.socket.bind(self.filename)
    self.socket.listen()
    
  def start(self): gevent.spawn(self.run_forever)
  
  def create_key(self, rand):
    return hashlib.sha256(self.password + rand).hexdigest().encode("utf8")
  
  def switch_to_process(self, session, process = 0, message = ""):
    environ = dict(session._ws.environ)
    
    print("* Fullpy * Sending session %s from process %s to process %s..." % (session, self.process_id, process))
    
    environ.pop("wsgi.errors", None)
    environ.pop("wsgi.file_wrapper", None)
    environ.pop("wsgi.input", None)
    environ.pop("wsgi.websocket", None)
    environ["wsgi.version"] = list(environ["wsgi.version"])
    
    data = [b"N %s" % json.dumps([message, environ, session.iri]).encode("utf8")]
    
    connection = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    connection.connect("%s-%s" % (self.base_filename, process))
    rand = connection.recv(8)
    connection.send(self.create_key(rand))
    
    gevent.socket.wait_write(connection.fileno())
    fileno = session._ws.handler.socket.fileno()
    socket.send_fds(connection, data, [fileno])
    connection.close()
    
    session.transferred = True
    session._ws.closed  = True # Pretend the socket is closed, to avoid the server close it again!
    
  def run_forever(self):
    while True:
      try:
        rand = ("".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-,?:") for i in range(8))).encode("utf8")
        key  = self.create_key(rand)
        connection, address = self.socket.accept()
        connection.send(rand)
        client_key = connection.recv(len(key))
        if key != client_key:
          print("* Fullpy * Authentication error on ProcessSwitcher:", key, client_key)
          connection.close()
          continue
        
        data, filenos, flags, address = socket.recv_fds(connection, 4096, 1)
        connection.close()
        
        gevent.spawn(self.handle_request, data, filenos[0])
        
      except: sys.excepthook(*sys.exc_info())
      
  def handle_request(self, data, fileno):
    if data.startswith(b"N"):
      message, environ, session_iri = json.loads(data[2:])
      print("* Fullpy * Receiving session %s (%s:%s) in process %s..." % (session_iri, environ["REMOTE_ADDR"], environ["REMOTE_PORT"], self.process_id))
      
      environ["wsgi.errors"] = WSGIErrorsWrapper(self.gunicorn_config)
      environ["wsgi.file_wrapper"] = FileWrapper
      environ["wsgi.version"] = tuple(environ["wsgi.version"])
      
      session = self.webapp.world[session_iri]
      if not session:
        print("* Fullpy * Cannot find session %s!" % session_iri)
        return
      
      if session.user: session.user.reload()
      
      new_socket = socket.socket(fileno = fileno)
      handler = NoInitWebSocketHandler(new_socket, environ, message, session, self.gunicorn_server)
      handler.handle_one_response()
    
class NoInitWebSocketHandler(geventwebsocket.handler.WebSocketHandler):
  def __init__(self, socket, environ, initial_message, session, server):
    self.environ                 = environ
    self.session                 = session
    self.session.initial_message = initial_message
    self.application             = server.application
    
    geventwebsocket.handler.WebSocketHandler.__init__(self, socket, (environ["REMOTE_ADDR"], environ["REMOTE_PORT"]), server)
    
  def upgrade_websocket(self):
    self.websocket = self.environ["wsgi.websocket"] = geventwebsocket.websocket.WebSocket(self.environ, geventwebsocket.websocket.Stream(self), self)
    self.environ["wsgi.input"] = self.wsgi_input = gevent.pywsgi.Input(self.rfile, None, None) #self.websocket.raw_read.__self__
    return []
  
  def get_environ(self): return self.environ

  
