# FullPy
# Copyright (C) 2022-2024 Jean-Baptiste LAMY
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

__all__ = ["serve_forever"]

import sys, datetime, multiprocessing, gunicorn.app.base, gunicorn.workers.ggevent, flask, gevent

from fullpy.server.base_backend import _split_address
from fullpy.server import _gevent_patch_translator

CURRENT_WORKER = None

def serve_forever(webapps, address = "http://127.0.0.1:5000,http://[::1]:5000", url_prefix = "", flask_app = None, log_file = None, pid_file = None, max_nb_websockect = 5000, use_gevent = False, nb_process = 1, process_switcher_base_filename = "/tmp/fullpy_process_switcher_socket", gunicorn_options = None):
  flask_app = flask_app or flask.Flask("fullpy")
  
  address1 = address.rsplit(",", 1)[-1]
  
  for webapp in webapps:
    if webapp.has_websocket: use_gevent = True
    
  if use_gevent:
    from gevent import monkey
    if not monkey.is_module_patched("socket"):
      raise RuntimeError("Websockets require GEvent; please call gevent.monkey.patch_all() at the beginning of the program!")
    _gevent_patch_translator()
  
  addresses = _split_address(address)
  
  class StandaloneApplication(gunicorn.app.base.BaseApplication):
    def __init__(self):
      super().__init__()
      
    def load_config(self):
      self.cfg.set("workers", nb_process)
      self.cfg.set("max_requests", 2000)
      self.cfg.set("keepalive", 5)
      self.cfg.set("on_reload", on_reload)
      self.cfg.set("pre_fork", pre_fork)
      self.cfg.set("post_fork", post_fork)
      self.cfg.set("worker_exit", worker_exit)
      self.cfg.set("child_exit",  child_exit)
      
      if use_gevent:
        self.cfg.set("worker_class", "geventwebsocket.gunicorn.workers.GeventWebSocketWorker")
        self.cfg.set("worker_connections", max_nb_websockect)
        
      self.cfg.set("bind", ["%s:%s" % (host, port) for proto, host, port in addresses])
      
      if log_file:
        self.cfg.set("capture_output", True)
        self.cfg.set("errorlog", log_file)
        
      if pid_file:
        self.cfg.set("pidfile", pid_file)
        
      if gunicorn_options:
        for k, v in gunicorn_options.items(): self.cfg.set(k, v)
        
    def load(self):
      for webapp in webapps:
        webapp.start(flask_app, address1, url_prefix)
      return flask_app
    
      
  if nb_process > 1:
    if len(webapps) > 1: raise ValueError("Multiprocess is supported only with a single webapp.")

    for webapp in webapps: webapp.multiprocess = True
    
    import random, fullpy.server.gunicorn_multiprocess
    password = ("".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-,?:") for i in range(32))).encode("utf8")
    
    class FullpyWSGIServer(gunicorn.workers.ggevent.PyWSGIServer):
      def __init__(self, *args, **kargs):
        import fullpy.server.gunicorn_multiprocess
        gunicorn.workers.ggevent.PyWSGIServer.__init__(self, *args, **kargs)
        if not fullpy.server.gunicorn_multiprocess.PROCESS_SWITCHER:
          fullpy.server.gunicorn_multiprocess.ProcessSwitcher(self, webapps[0], process_switcher_base_filename, password).start()
          
    gunicorn.workers.ggevent.GeventPyWSGIWorker.server_class = FullpyWSGIServer
    
    
  def pre_fork(arbiter, worker): # in the master process
    worker.pipe_from_master, worker.pipe_to_worker = multiprocessing.Pipe(False)

    workers = list(arbiter.WORKERS.values())
    process_ids = [getattr(w, "process_id", None) for w in workers]
    for i in range(nb_process):
      if not i in process_ids:
        worker.process_id = worker.process_id_saved = i
        break
      
  def post_fork(arbiter, worker): # in the worker process
    global CURRENT_WORKER
    CURRENT_WORKER = worker
    
    print("* Fullpy * Starting process %s..." %  worker.process_id)
    for webapp in webapps: webapp.process_id = worker.process_id
    
    worker.master_listener = gevent.spawn(listen_from_master, worker)
    
  def listen_from_master(worker):
    pipe_from_master = worker.pipe_from_master
    while True:
      if pipe_from_master.poll(0.5):
        message = pipe_from_master.recv_bytes()
        if   message == b"reload":
          worker.process_id = None # No longer valid
          fullpy.server.webapp.reload_clients(False); break
        elif message == b"reload_client":
          worker.process_id = None # No longer valid
          fullpy.server.webapp.reload_clients(True); break
        elif message == b"stop": break
        else:
          print("Message inconnu du master:", message)
          break
        
  def on_reload(arbiter): # in the master process
    print("* Fullpy * Reloading...")
    client_changed = False
    for webapp in webapps:
      if webapp.compile_client(): client_changed = True
      
    workers = list(arbiter.WORKERS.values())
    message = b"reload_client" if client_changed else b"reload"
    for worker in workers:
      worker.pipe_to_worker.send_bytes(message)
      worker.process_id = None
    arbiter.kill_workers(2)
    
  def worker_exit(arbiter, worker): # in the worker process
    print("* Fullpy * End of process %s" % worker.process_id_saved)
    if not worker.process_id is None: # Not reloading ! => send reload command to client
      for webapp in webapps: webapp.reload_clients(True)
      worker.process_id = None
      
    worker.master_listener.kill(block = False)
    
    for webapp in webapps:
      webapp.close_sessions()
      if webapp.world: webapp.world.save()
      webapp.on_stopped()
      
  def child_exit(arbiter, worker): # in the master process
    worker.process_id = None

      
  StandaloneApplication().run()

