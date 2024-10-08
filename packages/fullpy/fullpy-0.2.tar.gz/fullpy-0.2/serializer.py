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

__all__ = ["Serializer"]

import sys, weakref
from datetime import date, datetime, timedelta

import fullpy
from fullpy.util import TRANS

normstr = locstr = ()
def _create_spc_str():
  global normstr, locstr
  class normstr(str):
    def __repr__(self): return """normstr(%s)""" % repr(str(self))
    
  class locstr(str):
    def __new__(Class, s, lang = ""): return str.__new__(Class, s)

    def __repr__(self): return """locstr(%s, %s)""" % (repr(str(self)), repr(self.lang))

    def __init__(self, s, lang = ""):
      str.__init__(self)
      self.lang = lang
      
    def __eq__(self, other):
      return isinstance(other, locstr) and str.__eq__(self, other) and (self.lang == other.lang)
    
    def __ne__(self, other):
      return (not isinstance(other, locstr)) or str.__ne__(self, other) or (self.lang != other.lang)
    
    def __hash__(self): return hash((str(self), self.lang))
    
if sys.platform == "brython": _create_spc_str()

_not_found = object()

_NUMBER = set("-+0123456789e.")


def _encode_basestring(s): return '"%s"' % s.replace('"', '\\"')

# def _scanstring(s, i):
#   e = s.find('"', i)
#   if s[e - 1] == "\\":
#     r, j = _scanstring(s, e + 1)
#     return '%s"%s' % (s[i : e - 1], r), j
#   return s[i : e], e + 1

def _scanstring(s, i, first = True):
  e = s.find('"', i)
  if s[e - 1] == "\\":
    r, j = _scanstring(s, e + 1, False)
    r = '%s"%s' % (s[i : e - 1], r)
  else:
    r = s[i : e]
    j = e + 1
  if first and (len(s) > j):
    #if   s[j] == "n": r = normstr(r); j += 1
    if s[j] == "@": r = locstr(r, s[j + 1 : j + 3]); j += 3
  return r, j

def _encode_normstring(s): return "'%s'" % s.replace("'", "\\'")

def _scan_normstring(s, i):
  e = s.find("'", i)
  if s[e - 1] == "\\":
    r, j = _scanstring(s, e + 1)
    return "%s'%s" % (s[i : e - 1], r), j
  return s[i : e], e + 1



class Serializer(object):
  def __init__(self, world = None, ignore_none = False, ignore_empty_list = False):
    # For encoding
    self.ignore_none        = ignore_none
    self.ignore_empty_list  = ignore_empty_list
    self.root_encode_func   = None
    self.class_encode_funcs = { type : self.for_python_class }
    self.root_decode_func   = None
    self.class_decode_funcs = {}
    
    # For decoding
    self._cache_storid = weakref.WeakValueDictionary()
    #self._cache_id     = weakref.WeakValueDictionary()
    self._cache_id     = {}
    self.modules_proxy = _ModuleProxy()
    
    self.set_world(world)
    
  def set_world(self, world):
    self.world = world
    if world:
      self.class_encode_funcs[world._get_by_storid(34).__class__] = self.for_ontology_class # 34 = Thing
      global normstr, locstr
      import owlready2
      normstr = owlready2.normstr
      locstr  = owlready2.locstr
    
  def get_by_storid(self, storid): return self._cache_storid.get(storid)
  
  def for_ontology_class(self, klass): return { "name" : klass.__name__, "onto" : klass.namespace.base_iri }
  
  def for_python_class(self, klass): return { "name" : "%s.%s" % (klass.__module__, klass.__name__) }
  
  def for_instance(self, klass, func_or_prop_list = None, locstr_list = None, decode_func = None):
    if   func_or_prop_list is None:
      def f(func): self.class_encode_funcs[klass] = func
      return f
    elif callable(func_or_prop_list):
      self.class_encode_funcs[klass] = func_or_prop_list
    else:
      self.class_encode_funcs[klass] = self._prop_lister(func_or_prop_list, locstr_list)
    if decode_func: self.class_decode_funcs["%s.%s" % (klass.__module__, klass.__name__)] = decode_func
    
  def for_root(self, func_or_prop_list, func_or_locstr_list = None):
    if callable(func_or_prop_list):
      self.root_encode_func = func_or_prop_list
      if func_or_locstr_list: self.root_decode_func = func_or_locstr_list
    else:
      self.root_encode_func = self._prop_lister(func_or_prop_list, func_or_locstr_list)
    
  def for_other(self, func_or_prop_list, func_or_locstr_list = None):
    if callable(func_or_prop_list):
      self.class_encode_funcs[object] = func_or_prop_list
      if func_or_locstr_list: self.class_decode_funcs["builtins.object"] = func_or_locstr_list
    else:
      self.class_encode_funcs[object] = self._prop_lister(func_or_prop_list, func_or_locstr_list)
      
  def _prop_lister(self, prop_list, locstr_list):
    if locstr_list:
      def lister(x):
        r = {}
        for prop in prop_list:
          v = getattr(x, prop, _not_found)
          if v is _not_found: continue
          if self.ignore_none       and (v is None): continue
          if self.ignore_empty_list and isinstance(v, list) and (not v): continue
          r[prop] = v
        for prop in locstr_list:
          v = getattr(x, prop, _not_found)
          if v is _not_found: continue
          if self.ignore_empty_list and isinstance(v, list) and (not v): continue
          r[prop] = TRANS.from_annotation(v)
        return r
    else:
      def lister(x):
        r = {}
        for prop in prop_list:
          v = getattr(x, prop, _not_found)
          if v is _not_found: continue
          if self.ignore_none       and (v is None): continue
          if self.ignore_empty_list and isinstance(v, list) and (not v): continue
          r[prop] = v
        return r
    return lister
  
  #@lru_cache()
  def _get_class_func(self, klass):
    for parent in klass.__mro__:
      func = self.class_encode_funcs.get(parent)
      if func: return func
      
  def encode(self, x):
    if isinstance(x, (list, tuple, set)): roots = set( id(root) for root in x)
    else:                                 roots = set([id(x)])
    return self._encode(x, { "roots" : roots, "next_id" : 1 })
  
  def _encode(self, x, dico):
    if x is None:  return "null"
    if x is False: return "false"
    if x is True:  return "true"
    if isinstance(x, normstr): return _encode_normstring(x)
    if isinstance(x, locstr): return '%s@%s' % (_encode_basestring(x), x.lang) 
    if isinstance(x, str): return _encode_basestring(x)
    if isinstance(x, (int, float)): return repr(x)
    if isinstance(x, bytes): return 'b"%s"' % x.replace(b'"', b'\\"').decode("ascii")
    if isinstance(x, list):  return "[%s]" % ",".join(self._encode(i, dico) for i in x)
    if isinstance(x, tuple): return "(%s)" % ",".join(self._encode(i, dico) for i in x)
    if isinstance(x, set):   return "set([%s])" % ",".join(self._encode(i, dico) for i in x)
    if isinstance(x, dict):  return "{%s}" % ",".join("%s:%s" % (self._encode(k, dico), self._encode(v, dico)) for (k, v) in x.items())
    if isinstance(x, datetime):  return "datetime(%s)" % ",".join(str(i) for i in x.timetuple()[:7])
    if isinstance(x, date):      return "date(%s,%s,%s)" % (x.year, x.month, x.day)
    if isinstance(x, timedelta): return "timedelta(%s,%s,%s)" % (x.days, x.seconds, x.microseconds)
    if isinstance(x, _ModuleProxy): return """onto("%s")""" % x.base_iri
    if self.world and isinstance(x, self.world.ontologies["http://anonymous/"].__class__): return """onto("%s")""" % x.base_iri
    
    storid = getattr(x, "storid", None)
    if x in dico:
      if storid: return '{"$st":%s}' % storid
      else:      return '{"$id":%s}' % dico[x]
      
    if isinstance(x, _ObjProxy):
      if storid: return '{"$st":%s}' % storid
      else:      raise ValueError("Cannot dump _ObjProxy that are not from an Owlready ontology: '%s'!" % x)
      
    if self.root_encode_func and (id(x) in dico["roots"]):
      x2 = self.root_encode_func(x)
    else:
      func = self._get_class_func(x.__class__)
      if func: x2 = func(x)
      else: raise TypeError("No method defined for dumping: '%s' of class '%s'!" % (x, x.__class__))
      
    if storid:
      dico[x] = 1
    else:
      dico[x] = xid = dico["next_id"]
      dico["next_id"] += 1
      
    if storid:
      if hasattr(x, "_get_class_possible_relations"): # Avoid import owlready, for client-side use in browser
        return '{"$st":%s,"$bases":%s%s}' % (storid, self._encode([parent for parent in x.is_a if hasattr(parent, "_get_class_possible_relations")], dico), "".join(",%s:%s" % (self._encode(k, dico), self._encode(v, dico)) for (k, v) in x2.items()))
      else:
        return '{"$st":%s,"$class":%s%s}' % (storid, self._encode_ontology_class(x.__class__, dico), "".join(",%s:%s" % (self._encode(k, dico), self._encode(v, dico)) for (k, v) in x2.items()))
    else:
      if x.__class__ is type:
        return '{"$id":%s,"$bases":%s%s}' % (xid, self._encode([parent for parent in x.__bases__ if not parent is object], dico), "".join(",%s:%s" % (self._encode(k, dico), self._encode(v, dico)) for (k, v) in x2.items()))
      else:
        return '{"$id":%s,"$class":%s%s}' % (xid, self._encode_python_class(x.__class__, dico), "".join(",%s:%s" % (self._encode(k, dico), self._encode(v, dico)) for (k, v) in x2.items()))
      
  def _encode_ontology_class(self, klass, dico):
    id = dico.get(klass)
    if id: return klass.storid      
    return self._encode(klass, dico)
  
  def _encode_python_class(self, klass, dico):
    id = dico.get(klass)
    if id: return id      
    return self._encode(klass, dico)
  
  def decode(self, s):
    r = self._decode(s, 0)[0]
    self._cache_id.clear()
    return r
  
  def _decode(self, s, i):
    if   s[i] == '"': return _scanstring(s, i + 1)
    
    elif s[i] == "'":
       r, i = _scan_normstring(s, i + 1)
       print(normstr)
       return normstr(r), i
     
    elif s[i] == "[":
      r = []
      if s[i + 1] == "]": return r, i + 2
      while s[i] != "]":
        o, i = self._decode(s, i + 1)
        r.append(o)
      return r, i + 1
    
    elif s[i] == "(":
      if s[i + 1] == ")": return (), i + 2
      r = []
      while s[i] != ")":
        o, i = self._decode(s, i + 1)
        r.append(o)
      return tuple(r), i + 1
    
    elif s.startswith("null" , i): return None,  i + 4
    elif s.startswith("true" , i): return True,  i + 4
    elif s.startswith("false", i): return False, i + 5
    
    elif s.startswith('{"$st"', i):
      storid, i = self._decode(s, i + 7)
      if self.world: r = self.world._get_by_storid(storid)
      else:          r = self._cache_storid.get(storid)
      if s[i] == "}": return r, i + 1
      
      category = s[i + 2: i + 8]
      if   category == "$class":
        klass, i = self._decode(s, i + 10)
        if not callable(klass): klass = self._cache_storid[klass]
        if   not r:                    r = self._cache_storid[storid] = klass(storid)
        elif not r.__class__ is klass: r.__class__ = klass
        while s[i] != "}":
          k, i = self._decode(s, i + 1) # + 1 for ,
          v, i = self._decode(s, i + 1) # + 1 for :
          setattr(r, k, v)
        return r, i + 1 # + 1 for }
        
      elif category == "$bases":
        bases, i = self._decode(s, i + 10)
        bases = tuple(bases) or (_OntologyObjProxy,)
        d = {}
        while s[i] != "}":
          k, i = self._decode(s, i + 1) # + 1 for ,
          v, i = self._decode(s, i + 1) # + 1 for :
          d[k] = v
          
        name = d.pop("name")
        onto = d.pop("onto")
        
        module = self.modules_proxy.get_ontology(onto)
        if not r:
          r = module.get_class(name)
          if r:
            r.namespace = module
            self._cache_storid[storid] = r          
        if r:
          #r.__name__ = name
          if r.__bases__ != bases: r.__bases__ = bases
        else:
          r = type(name, bases, {})
          if not self.world: self._cache_storid[storid] = r
          if d: r.__dict__.update(d)
          module.add_class(r)
          r.namespace = module
          
        return r, i + 1 # + 1 for }
      
    elif s.startswith('{"$id"', i):
      objid, i = self._decode(s, i + 7)
      r = self._cache_id.get(objid)
      if s[i] == "}": return r, i + 1
      
      category = s[i + 2: i + 8]
      if   category == "$class":
        klass, i = self._decode(s, i + 10)
        if not callable(klass): klass = self._cache_id[klass]
        if not r:
          d = {}
          while s[i] != "}":
            k, i = self._decode(s, i + 1) # + 1 for ,
            v, i = self._decode(s, i + 1) # + 1 for :
            d[k] = v
          if getattr(klass, "__remote_name__", None) in self.class_decode_funcs:
            r = self._cache_id[objid] = self.class_decode_funcs[klass.__remote_name__](**d)
          else:
            r = self._cache_id[objid] = klass(**d)
        else:
          while s[i] != "}":
            k, i = self._decode(s, i + 1) # + 1 for ,
            v, i = self._decode(s, i + 1) # + 1 for :
            setattr(r, k, v)
        return r, i + 1 # + 1 for }
      
      elif category == "$bases":
        bases, i = self._decode(s, i + 10)
        
        d = {}
        while s[i] != "}":
          k, i = self._decode(s, i + 1) # + 1 for ,
          v, i = self._decode(s, i + 1) # + 1 for :
          d[k] = v
          
        name0 = d.pop("name")
        module_name, name = name0.rsplit(".", 1)
        
        #if r:
        #  r.__name__  = name
        #else:
        if not r:
          module = self.modules_proxy.get_submodule(module_name)
          r = module.get_class(name)
          if r:
            self._cache_id[objid] = r
          else:
            r = self._cache_id[objid] = type(name, tuple(bases) or (_PythonObjProxy,), {})
            r.__module__      = module_name
            r.__remote_name__ = name0
            if d: r.__dict__.update(d)
            module.add_class(r)
            
        #if d: r.__dict__.update(d)
        #setattr(self.modules_proxy.get_submodule(module_name), name, r)
        #r.__remote_name__ = name0
        return r, i + 1 # + 1 for }
    
    elif s[i] == "{":
      r = {}
      if s[i + 1] == "}": return r, i + 2
      while s[i] != "}":
        k, i = self._decode(s, i + 1) # + 1 for { or ,
        v, i = self._decode(s, i + 1) # + 1 for :
        r[k] = v
      return r, i + 1 # + 1 for }
    
    elif s.startswith("datetime(", i):
      j = s.find(")", i + 9)
      return datetime(*(int(i) for i in s[i + 9 : j].split(","))), j + 1

    elif s.startswith("date(", i):
      j = s.find(")", i + 5)
      return date(*(int(i) for i in s[i + 5 : j].split(","))), j + 1

    elif s.startswith("timedelta(", i):
      j = s.find(")", i + 10)
      return timedelta(*(int(i) for i in s[i + 10 : j].split(","))), j + 1
    
    elif s.startswith("onto(", i):
      base_iri, i = _scanstring(s, i + 6)
      onto = (self.world or self.modules_proxy).get_ontology(base_iri)
      return onto, i + 1
    
    elif s[i] == "s": # set([...])
      i += 4
      r = set()
      if s[i + 1] == "]": return r, i + 3
      while s[i] != "]":
        o, i = self._decode(s, i + 1)
        r.add(o)
      return r, i + 2
    
    elif s[i] == "b":
       r, i = _scanstring(s, i + 2)
       return bytes(r, "ascii"), i
     
    if s[i] in _NUMBER:
      j = i + 1
      while (j < len(s)) and (s[j] in _NUMBER): j +=1
      try:               return int  (s[i : j]), j
      except ValueError: return float(s[i : j]), j
      
    if (s[i] == " ") or (s[i] == "\n") or (s[i] == "\t"): return self._decode(s, i + 1)
    
    raise ValueError("Decoding error at %s: '%s...'!" % (i, s[i : i + 30]))
  
  
class _ModuleProxy(type): # Inherits from type so as missing classes are treated as module, and module can be used in isinstance() of testing class membership.
  def __new__(self, name = "", package = ""): return type.__new__(self, name, (), {})
  
  def __init__(self, name = "", package = ""):
    self.__name__    = name
    self.__package__ = package
    self._classnames = set()
    
  def __repr__(self):
    if self.__package__:
      return "<module '%s.%s' (proxy)>" % (self.__package__, self.__name__)
    elif self.__name__.startswith("http:") or self.__name__.startswith("https:"):
      return "<ontology '%s' (proxy)>" % self.__name__
    else:
      return "<module '%s' (proxy)>" % self.__name__
    
  def __getattr__(self, name):
    if self.__package__: module = _ModuleProxy(name, "%s.%s" % (self.__package__, self.__name__))
    else:                module = _ModuleProxy(name, self.__name__)
    setattr(self, name, module)
    return module
  
  def __getitem__(self, name): return getattr(self, name)
  
  def get_ontology(self, base_iri):
    if (not base_iri.endswith("/")) and (not base_iri.endswith("#")): base_iri = "%s#" % base_iri
    r = getattr(self, base_iri)
    r.base_iri = base_iri
    return r
  
  def get_submodule(self, name):
    module = self
    for part in name.split("."): module = getattr(module, part)
    return module
  
  def get_class(self, name):
    if name in self._classnames:
      return getattr(self, name)
    return None
  
  def remote_class(self, module_name, klass = None):
    module = self.get_submodule(module_name)
    if klass: module.add_class(klass)
    else: return module.add_class
    
  def add_class(self, klass):
    setattr(self, klass.__name__, klass)
    self._classnames.add(klass.__name__)
    
    
def _simple_repr(x):
  if isinstance(x, _ObjProxy): return x.__simplerepr__()
  if isinstance(x, list): return "[%s]" % ", ".join(_simple_repr(i) for i in x)
  if isinstance(x, dict): return "{ %s }" % ", ".join("%s : %s" % (_simple_repr(k), _simple_repr(v)) for (k, v) in x.items())
  return repr(x)

class _ObjProxy(object):
  def __repr__(self):
    return "<%s %s>" % (self.__class__.__name__, " ".join("%s=%s" % (k, _simple_repr(v)) for k, v in self.__dict__.items() if not k.startswith("_")))

class _PythonObjProxy(_ObjProxy):
  def __init__(self, **d):
    if d: self.__dict__ = d
    
  def __simplerepr__(self): return "<%s>" % self.__class__.__name__

class _OntologyObjProxy(_ObjProxy):
  def __init__(self, storid): self.storid = storid
  
  def __simplerepr__(self): return "<%s storid=%s>" % (self.__class__.__name__, self.storid)
  
  
  
