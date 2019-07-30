# Original file:
# https://github.com/benoitc/gunicorn/blob/master/examples/example_config.py
import os

#   bind - The socket to bind. A string of the form: 'HOST', 'HOST:PORT', 'unix:PATH'. An IP is a valid HOST.
host = os.getenv("host", "0.0.0.0")
port = os.getenv("port", "8000")
bind = os.getenv("bind", f"{host}:{port}")


# backlog - The number of pending connections. This refers to the number of clients that can be waiting to be served. 
backlog = 2048


# workers - The number of worker processes that this server should keep alive for handling requests. 
workers = os.getenv("workers", 3)


# worker_class - The type of workers to use. The default sync class should handle most 'normal' types of work loads. 
worker_class = 'sync'


# worker_connections - For the eventlet and gevent worker classes this limits the maximum number of simultaneous clients that a single process can handle.
worker_connections = 1000


# timeout - If a worker does not notify the master process in this number of seconds it is killed and a new worker is spawned to replace it.
timeout = 30


# keepalive - The number of seconds to wait for the next request on a Keep-Alive HTTP connection.
keepalive = 2


# spew - Install a trace function that spews every line of Python that is executed when running the server. This is the nuclear option.
spew = False


# daemon - Detach the main Gunicorn process from the controlling terminal with a standard fork/fork sequence.
daemon = False


# raw_env - Pass environment variables to the execution environment. 
raw_env = []


# pidfile - The path to a pid file to write. A path string or None to not write a pid file.
pidfile = None


# user - Switch worker processes to run as this user. 
user = None


# umask - A mask for file permissions written by Gunicorn. Note that this affects unix socket permissions.
umask = 0


# group - Switch worker process to run as this group.
group = None


# tmp_upload_dir - A directory to store temporary request data when requests are read. This will most likely be disappearing soon.
tmp_upload_dir = None


# logfile - The path to a log file to write to. A path string. "-" means log to stdout.
logfile = '-'


# loglevel - The granularity of log output. A string of "debug", "info", "warning", "error", "critical"
loglevel = 'info'


# accesslog - The Access log file to write to.
accesslog = '-'


# access_log_format - The access log format.
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'


# proc_name - A base to use with setproctitle to change the way that Gunicorn processes are reported in the system process table. This affects things like 'ps' and 'top'.
proc_name = None

# post_fork - Called just after a worker has been forked.
def post_fork(server, worker):
    server.log.info("Worker spawned (pid: %s)", worker.pid)


# pre_fork - Called just prior to forking the worker subprocess.
def pre_fork(server, worker):
    pass


# pre_exec - Called just prior to forking off a secondary master process during things like config reloading.
def pre_exec(server):
    server.log.info("Forked child, re-executing.")

# when_ready - Called just after the server is started.
def when_ready(server):
    server.log.info("Server is ready. Spawning workers")

# worker_int - Called just after a worker exited on SIGINT or SIGQUIT.
def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")

    ## get traceback info
    import threading, sys, traceback
    id2name = {th.ident: th.name for th in threading.enumerate()}
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""),
            threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))

# worker_abort - Called when a worker received the SIGABRT signal.
def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")
