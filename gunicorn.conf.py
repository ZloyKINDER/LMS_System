import multiprocessing

bind = "unix:/home/test/lms_project/lms.sock"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
timeout = 120
graceful_timeout = 30
accesslog = "/home/test/lms_project/logs/gunicorn-access.log"
errorlog = "/home/test/lms_project/logs/gunicorn-error.log"
loglevel = "info"