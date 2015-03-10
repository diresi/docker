import ConfigParser
cfg = {}
cp = ConfigParser.ConfigParser()
cp.read('/home/ente/src/ente.cfg')
for section in cp.sections():
    sec_cfg = dict([(key.lower(), value) for key, value in cp.items(section)])
    cfg[section.lower()] = sec_cfg

def get_section(s):
    return cfg[s.lower()]

def get_entry(e, default=None):
    section, key = e.lower().split(".", 1)
    return cfg.get(section, {}).get(key, default)

def add_change_hook(f):
    pass

from __main__ import global_stuff
global_stuff.config_funcs = [get_section, get_entry, add_change_hook]

import ente_init
ente_init.init_io_redirect("utf-8")

import sys
sys.argv = ["run.py"]
import tasks.tasks
reload(tasks.tasks)

def start_main_thread(*a, **kw):
    import threading
    threading.Thread(target=tasks.tasks.app.worker_main).start()
    # do not join, ente needs this function to return

ente_init.set_bgthread_hook(start_main_thread)
