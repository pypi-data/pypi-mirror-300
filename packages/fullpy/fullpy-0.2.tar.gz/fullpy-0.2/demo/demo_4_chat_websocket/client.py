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

from fullpy.client import *

class MyWebApp(ClientSideWebapp):
  def on_started(self):
    self.open_anonymous_session()
    
  def on_session_opened(self, user_login, user_class, client_data):
    html = HTML()
    html << """<div id="message_view">"""
    for text in self.initial_data:
      html << self.message_to_html(text)
    html << """</div>"""
    html << """<div id="entry_box">"""
    html << """<table id="entry_table"><tr><td>Say&nbsp;something:</td>"""
    html << """<td id="entry_td"><input id="entry" type="text"></input></td></tr></table>"""
    html << """</div>"""
    html.bind("entry", "keypress", self.on_keypress)
    html.show()
    
  def message_to_html(self, text):
    return """<div class="message">%s</div>""" % text

  def on_keypress(self, event):
    if event.key == "Enter":
      text = document["entry"].value.strip()
      if text:
        webapp.server_add_message(None, text)
        document["entry"].value = ""
        
  @rpc
  def client_new_message(self, text):
    document["message_view"].insertAdjacentHTML("beforeend", self.message_to_html(text))
    
      
MyWebApp()
