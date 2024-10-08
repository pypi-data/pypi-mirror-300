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

from gevent import monkey
monkey.patch_all()

import sys, os, os.path, datetime
from owlready2 import *
from fullpy.server import *


world       = World(filename = "/tmp/demo_basic_chat.sqlite3")
chat_onto   = world.get_ontology("http://test.org/chat.owl")
fullpy_onto = get_fullpy_onto(world)

with chat_onto:
  class MyUser(fullpy_onto.User): pass
  class MySession(fullpy_onto.Session): pass
  class Message(Thing): pass
  
  class text(Message >> str, FunctionalProperty): pass
  class date(Message >> datetime.datetime, FunctionalProperty): pass
  
  
class MyWebApp(ServerSideWebapp):
  def __init__(self):
    ServerSideWebapp.__init__(self)
    self.name          = "demo_4"
    self.static_folder = os.path.join(os.path.dirname(__file__), "..", "static")
    self.css           = ["demo_4.css"]
    
    self.use_python_client(os.path.join(os.path.dirname(__file__), "client.py"))
    self.use_ontology_quadstore(world)
    self.use_session(chat_onto.MySession)
    self.use_websocket(debug = True)
    
  def get_initial_data(self, url_params):
    return [message.text for message in sorted(Message.instances(), key = lambda message: message.date)]
  
  @rpc
  def server_add_message(self, session, text):
    message = chat_onto.Message(date = datetime.datetime.now(), text = text)
    self.client_new_message(None, message.text)
    
from fullpy.server.gunicorn_backend import *
serve_forever([MyWebApp()], "http://127.0.0.1:5000")

# You can now open the following URL in your browser: http://127.0.0.1:5000/demo_4/index.html
