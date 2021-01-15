import multiprocessing

bind = "0.0.0.0:80"
workers = multiprocessing.cpu_count() * 2 + 1
keep_alive = 5
max_requests = 3
worker_class = "gevent"
