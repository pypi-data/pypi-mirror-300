# FullPy
# Copyright (C) 2024 Jean-Baptiste LAMY
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

__all__ = ["Node", "FixedNode", "Tree"]

from fullpy.client import *


# def merge_callbacks(done, *calls):
#   results = [None] * len(calls)
#   nb = 0
#   for i, call in enumerate(calls):
#     def done2(*args, i = i):
#       nonlocal nb
#       nb += 1
#       results[i] = args
#       if nb == len(calls):
#         done(*results)
#     call[0](done2, *call[1])

class Node(HTML):
  def __init__(self, parent = None):
    HTML.__init__(self)
    self.parent   = parent
    self.expanded = False
    self.children = None
    if parent: self.tree = parent.tree
    else:      self.tree = None
  
  def call_with_data(self, callback):
    """Calls callback() with a (icon, label, color, has_children) triple."""
    callback("icon", "node's label", None, False)
    
  def call_with_children(self, callback):
    """Calls callback() with the list of children."""
    callback([])
    
  def build(self, builder):
    def done(r):
      icon, label, color, has_children = r
      depth = 0
      node = self.parent
      while node:
        node = node.parent
        depth += 1
      self << """<div id="node_%s" class="node"><div id="node_body_%s" class="node_body%s">""" % (id(self), id(self), " selected" if self in self.tree.selections else "")
      if has_children:
        if self.expanded:
          self << """<span id="node_expander_%s" class="node_expander" style="margin-left: %sem">▼</span>""" % (id(self), depth * 2.5)
        else:
          self << """<span id="node_expander_%s" class="node_expander" style="margin-left: %sem">▶</span>""" % (id(self), depth * 2.5)
        self.bind("node_expander_%s" % id(self), "click", self.on_toggle_expand)
      else:
        self << """<span class="node_expander_empty" style="margin-left: %sem"></span>""" % (depth * 2.5)
      if color: self << """<span id="node_node_%s"><img src="%s/%s" class="node_icon"/> <span style="color: %s;">%s</span></span>""" % (id(self), webapp.static_path, icon, color, label)
      else:     self << """<span id="node_node_%s"><img src="%s/%s" class="node_icon"/> %s</span>""" % (id(self), webapp.static_path, icon, label)
      self.bind("node_body_%s" % id(self), "mousedown", self.on_mouse_down)
      #self.bind("node_body_%s" % id(self), "mouseup",   self.on_mouse_up)
      self.bind("node_body_%s" % id(self), "mousemove", self.on_mouse_move)
      self << """</div>"""
      self << """<div id="node_children_%s" class="node_children">""" % id(self)
      if has_children and self.expanded:
        if self.children is None:
          def done_children(children):
            self.children = children
            for child in self.children: self << child
          self.call_with_children(done_children)
        else:
          for child in self.children: self << child
      self << """</div></div>"""
    self.call_with_data(done)

    
  def on_toggle_expand(self, e = None):
    if self.expanded:
      self.expanded = False
      try: document["node_expander_%s" % id(self)].innerHTML = "▶"
      except KeyError: pass
      try: document["node_children_%s" % id(self)].innerHTML = ""
      except KeyError: pass
      self.tree.emit_event("node_collapsed", self)
    else:
      self.expanded = True
      try: document["node_expander_%s" % id(self)].innerHTML = "▼"
      except KeyError: return
      self.tree.emit_event("node_expanded", self)
      def done(children):
        self.children = children
        for child in children:
          child.show_at_reference("node_children_%s" % id(self), "beforeend")
      self.call_with_children(done)
      
  def on_mouse_down(self, e = None):
    if   e.ctrlKey:
      if self in self.tree.selections: self.tree.remove_selection(self)
      else:                            self.tree.add_selection   (self)
    elif e.shiftKey:
      self.tree.select_to(self)
    else:
      self.tree.set_selections({self})
    e.preventDefault()
    document["tree_%s" % id(self.tree)].focus()
    
  #def on_mouse_up(self, e = None):
  #  print(e, e.buttons)
    
  def on_mouse_move(self, e = None):
    #print(e, e.buttons)
    if e.buttons == 1:
      self.tree.select_to(self)
    e.preventDefault()
    
  def previous(self):
    children = self.parent and self.parent.children or self.tree.root_nodes
    i = children.index(self)
    if i == 0: return self.parent
    node = children[i - 1]
    while node.expanded: node = node.children[-1]
    return node
    
  def next(self):
    if self.expanded: return self.children[0]
    node = self
    while True:
      children = node.parent and node.parent.children or node.tree.root_nodes
      i = children.index(node)
      if i < len(children) - 1: return children[i + 1]
      if not node.parent: return None
      node = node.parent
      
  def update(self, update_children = True):
    def done(r):
      icon, label, color, has_children = r
      if color: document["node_node_%s" % id(self)].innerHTML = """<img src="%s/%s" class="node_icon"/> <span style="color: %s;">%s</span>""" % (webapp.static_path, icon, color, label)
      else:     document["node_node_%s" % id(self)].innerHTML = """<img src="%s/%s" class="node_icon"/> %s""" % (webapp.static_path, icon, label)
    if update_children:
      def done_children(children):
        if children != self.children:
          self.children = children
          self.show_replace("node_%s" % id(self))
        else:
          self.call_with_data(done)
      self.call_with_children(done_children)
    else:
      self.call_with_data(done)
      
  def remove(self):
    if self in self.tree.selections:
      self.tree.selections.remove(self)
      if self.tree.last_selection is self: self.tree.last_selection = None
    if self.parent: self.parent.children.remove(self)
    else:           self.tree.remove_root_node(self)
    try:    div = document["node_%s" % id(self)]
    except: div = None
    if div: div.remove()
    
    
class FixedNode(Node):
  def __init__(self, icon, label, parent = None, color = None):
    Node.__init__(self, parent)
    self.icon     = icon
    self.label    = label
    self.color    = color
    self.children = []
    if parent: parent.children.append(self)
    
  def call_with_data    (self, callback): callback((self.icon, self.label, self.color, bool(self.children)))
  def call_with_children(self, callback): callback(self.children)
  
  
class Tree(HTML):
  python_events = { "selection_changed", "node_expanded", "node_collapsed" }
  
  def __init__(self, multiselect = True, width = None, height = None):
    self.root_nodes     = []
    self.selections     = set()
    self.last_selection = None
    self.multiselect    = multiselect
    self.width          = width
    self.height         = height
    
  def build(self, builder):
    self << """<div id="tree_%s" class="tree" tabindex="0" style="%s%s">""" % (id(self), "width: %s;" % self.width if self.width else "", "height: %s;" % self.height if self.height else "")
    self << """<div id="tree_inner_%s" class="tree_inner">""" % id(self)
    for node in self.root_nodes: self << node
    self << """</div></div>"""
    self.bind("tree_%s" % id(self), "keydown", self.on_keydown)
    
  def add_root_node(self, root_node):
    self.root_nodes.append(root_node)
    root_node.tree = self
    
  def remove_root_node(self, root_node):
    self.root_nodes.remove(root_node)
    root_node.tree = None
    
  def set_selections(self, selections):
    if selections == self.selections: return
    for node in self.selections: self._deselect(node)
    self.selections = selections
    for node in selections: self._select(node)
    if not self.last_selection in selections: self.last_selection = tuple(selections)[-1]
    self.emit_event("selection_changed", self)
    
  def add_selection(self, node):
    self.selections.add(node)
    self._select(node)
    if not self.last_selection: self.last_selection = node
    self.emit_event("selection_changed", self)
    
  def remove_selection(self, node):
    self.selections.remove(node)
    self._deselect(node)
    if not self.selections: self.last_selection = None
    self.emit_event("selection_changed", self)
    
  def select_to(self, to):
    if not self.last_selection: return
    if document["node_%s" % id(to)].offsetTop < document["node_%s" % id(self.last_selection)].offsetTop: start, end = to, self.last_selection
    else: start, end = self.last_selection, to
    selections = set()
    node = start
    while node and (not node is end):
      selections.add(node)
      node = node.next()
    selections.add(end)
    if selections != self.selections: self.set_selections(selections)
    
  def _select(self, node):
    try: document["node_body_%s" % id(node)].classList.add("selected")
    except KeyError: pass
    
  def _deselect(self, node):
    try: document["node_body_%s" % id(node)].classList.remove("selected")
    except KeyError: pass
    
  def on_keydown(self, e):
    if self.last_selection:
      if   e.code == "ArrowUp":
        self.set_selections({ self.last_selection.previous() or self.last_selection })
        document["node_%s" % id(self.last_selection)].scrollIntoView({ "behavior": "auto", "block": "nearest", "inline": "nearest" })
        e.preventDefault()
      elif e.code == "ArrowDown":
        self.set_selections({ self.last_selection.next() or self.last_selection })
        document["node_%s" % id(self.last_selection)].scrollIntoView({ "behavior": "auto", "block": "nearest", "inline": "nearest" })
        e.preventDefault()
      elif e.code == "ArrowLeft":
        if self.last_selection.expanded: self.last_selection.on_toggle_expand()
        e.preventDefault()
      elif e.code == "ArrowRight":
        if not self.last_selection.expanded:
          try:             expander = document["node_expander_%s" % id(self.last_selection)]
          except KeyError: expander = None
          if expander: self.last_selection.on_toggle_expand()
        e.preventDefault()
