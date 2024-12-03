import multiprocessing


bind = '0.0.0.0:9000'
workers = multiprocessing.cpu_count() * 2 + 1
max_requests = 500
max_requests_jitter = 100
reload = True
accesslog = 'logs/gunicorn_access.log'
errorlog = 'logs/gunicorn_error.log'
access_log_format = '%(h)s %(t)s "%(r)s" %(s)s %(b)sB %(M)sms'
