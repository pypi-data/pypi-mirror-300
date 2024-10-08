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

import sys, time, random

from fullpy.util import *


class Session(object):
  def init(self, user, session_id, session_token, lang, test_session):
    assert session_id or session_token
    
    self._ws               = None
    self.user              = user
    self.session_id        = session_id
    self.session_token     = session_token
    self.groups            = []
    self.is_test           = test_session
    self.transferred       = False
    self.session_last_time = time.time()
    self.webapp_lang = lang or TRANS._default_lang
    #if user and user.webapp_lang: self.webapp_lang = user.webapp_lang
    #else:                         self.webapp_lang = TRANS._default_lang
    self.on_init()
    
  def on_init(self): pass
  
  def set_manager(self, manager): self.manager = manager
  
  def __repr__(self): return "<Session %s, user=%s>" % (self.session_token or self.session_id, self.user)
  
  def get_client_data(self): return None
  
  def close(self):
    if self.manager.debug: print("* Fullpy * Session closed: %s" % self, file = sys.stderr)
    for group in self.groups: self.quit_group(group)
    self.manager.sessions.pop(self.session_token or self.session_id, None)
    self.on_closed()
    
  def destroy(self):
    if self.manager.debug: print("* Fullpy * Persistent session destroyed: %s" % self, file = sys.stderr)
    self.on_destroyed()
    
  def on_connected(self, previous_session = None): pass
  def on_closed   (self): pass
  def on_destroyed(self): pass
  
  def __getattr__(self, attr):
    if attr.startswith("client_"):
      def specific_client_call(done, *args, func_name = attr[7:]):
        return self.manager._client_call(self, done, func_name, *args)
      setattr(self, attr, specific_client_call)
      return specific_client_call
    raise AttributeError(attr)
  
  def join_group(self, group):
    if group in self.groups: return False
    if group.manager is None:
      group.init()
      group.set_manager(self.manager)
    self.groups.append(group)
    group.sessions.append(self)
    return True
  
  def quit_group(self, group):
    if not group in self.groups: return False
    self.groups.remove(group)
    group.sessions.remove(self)
    if not group.sessions: group.on_empty()
    return True
  
  
class Group(object):
  def init(self):
    self.manager  = None
    self.sessions = []
    self.on_init()
    
  def on_init(self): pass
  def on_destroyed(self): pass
  
  def set_manager(self, manager): self.manager = manager
  
  def __repr__(self): return "<Group %s>" % self.name
  
  def destroy(self):
    for session in list(self.sessions): self.remove_session(session)
    self.manager.groups.pop(self.name, None)
    self.on_destroyed()
    
  def on_empty(self): pass
  
  def __getattr__(self, attr):
    if attr.startswith("client_"):
      def specific_client_call(done, *args, func_name = attr[7:]):
        return self.manager._client_call(self.sessions, done, func_name, *args)
      setattr(self, attr, specific_client_call)
      return specific_client_call
    raise AttributeError(attr)
  
  
class BaseManager(object):
  Session = Session
  Group   = Group
  
  def __init__(self, webapp, session_max_duration, session_max_memory_duration, debug = False):
    self.webapp                      = webapp
    self.serializer                  = webapp.serializer
    self.debug                       = debug
    self.sessions                    = {}
    self.session_max_duration        = session_max_duration
    self.session_max_memory_duration = session_max_memory_duration
    self.groups                      = {}
    self._last_session_time          = ""
    self._last_session_ids           = set()
    self.pending_session_ids         = set()
    self.time_ordered_sessions       = []
    self.time_ordered_session_ids    = []
    
    if self.webapp.has_session and self.webapp.persistent_session: self.destroy_timed_out_persistent_sessions(force = True)
    
  def new_session_id_for_html_page(self): return ""
  
  def server_new_session_id(self, session = None):
    session_time = int_2_base_62(int(("%f" % (time.time() - 1671000000.0)).replace(".", "")))
    session_id   = "%s%s" % (int_2_base_62(random.randint(1, 1000000000000)), session_time)
    
    # if session_time == self._last_session_time:
    #   while session_id in self._last_session_ids:
    #     session_id = "%s%s" % (int_2_base_62(random.randint(1, 1000000000000)), session_time)
    #   self._last_session_ids.add(session_id)
    # else:
    #   self._last_session_time = session_time
    #   self._last_session_ids = { session_id }
      
    # self.pending_session_ids.add(session_id)
    # self.time_ordered_session_ids.append((time.time() + 500.0, session_id))
    return session_id
  
  def server_close_session(self, session):
    session.close()
    session.destroy()
    
  def destroy_timed_out_persistent_sessions(self, exc = None, force = False):
    limit = time.time() - self.session_max_duration
    if force or (limit >= self.last_destroy_timed_out_persistent_sessions_time):
      sessions = self.webapp.world.sparql("""SELECT ?s { ?s fullpy:session_last_time ?dt . FILTER(?dt <= ??) . }""", [limit])
      for session, in sessions:
        if (session.session_token or session.session_id) in self.sessions:
          session.close()
          try: self.time_ordered_sessions.remove(session)
          except: pass
        else:
          session.set_manager(self)
        session.destroy()
      self.last_destroy_timed_out_persistent_sessions_time = time.time()
      
  def get_group(self, name):
    group = self.groups.get(name)
    if group is None:
      try:
        group = self.Group(name)
        group.set_manager(self)
        group.on_init()
      except ValueError: return None
    return group
  
  def create_session(self, session_id, session_token = "", lang = "", test_session = None):
    if test_session:
      user = self.webapp.create_test_user(test_session)
      if user:
        user.webapp_lang = lang
        session_name  = "session_%s_%s" % (session_token or session_id, user.name)
        session_token = create_session_token(session_id, user.login, user.password)
      else:
        session_name  = "session_%s" % session_id
      session = None
    else:
      session_name = "session_%s" % (session_token or session_id)
      session      = self.sessions.get(session_token or session_id) or (self.webapp.persistent_session and self.webapp.session_onto[session_name]) or None
      if session: session_id = session.session_id
      
      if self.webapp.persistent_session and session_token:
        login = session_token.split(":", 1)[0][1:]
        user  = self.webapp.world.search_one(login = login)
        
        if user is None: print("* Fullpy * Create session failed (unknown user): %s" % session_token, file = sys.stderr); return None
        session_token2 = create_session_token(session_id, user.login, user.password)

        if session_token != session_token2: print("* Fullpy * Create session failed (wrong password / expired): %s" % session_token, file = sys.stderr); return None
        if not user.webapp_lang: user.webapp_lang = lang or TRANS.default_lang
      else:
        user = None
        
    #if not session:
    #  if not session_id in self.pending_session_ids: print("* Fullpy * Create session failed (invalid session ID): %s" % session_id, file = sys.stderr); return None
    #  self.pending_session_ids.discard(session_id)
      
    if session is None:
      if self.webapp.persistent_session:
        with self.webapp.test_session_onto if test_session else self.webapp.session_onto:
          session = self.Session(session_name)
          session.init(user, session_id, session_token, lang, test_session)
        self.webapp.test_session_onto.world.save()
      else:
        session = self.Session()
        session.init(user, session_id, session_token, lang, test_session)
      if self.debug: print("* Fullpy * New session: %s" % session, file = sys.stderr)
    else:
      if self.debug: print("* Fullpy * Reuse session: %s" % session, file = sys.stderr)
    
    session.set_manager(self)
    TRANS.set_lang((session.user and session.user.webapp_lang) or session.webapp_lang or TRANS.default_lang)
    self.sessions[session_token or session_id] = session
    return session
  
  def open_session(self, session, session_id, session_token, lang = None, test_session = None):
    if (not session_id) and (not session_token):
      session_id = self.server_new_session_id()
      force_token = True
    elif test_session:
      force_token = True
    else:
      force_token = False
    new_session = self.create_session(session_id, session_token, lang, test_session)
    #if not new_session: return None, (False, "", None, "", "")
    if not new_session: return None, (False, "", None, "", self.server_new_session_id())
    if session: session.close()
    return new_session, (True, new_session.user.__class__.name if new_session.user else "", new_session.get_client_data(), new_session.webapp_lang, new_session.session_token or new_session.session_id if force_token else "")
  
  def open_session_from_user(self, user, lang = None, test_session = None):
    session_id    = self.server_new_session_id()
    session_token = create_session_token(session_id, user.login, user.password)
    return self.open_session(None, session_id, session_token, lang, test_session)[0]
  
  def _client_call(self, session_or_group, done, func_name, *args):
    raise ValueError("Server-to-client calls are not supported with this protocol!")
  
  def close_sessions(self):
    for session in list(self.sessions.values()): session.close()
    if self.webapp.has_session and self.webapp.persistent_session: self.destroy_timed_out_persistent_sessions(force = True)
    
      
