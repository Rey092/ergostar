"""Gunicorn configuration file."""

bind = "127.0.0.1:8000"
workers = 4
accesslog = "-"
errorlog = "-"
forwarded_allow_ips = "*"
access_log_format = (
    '%({x-forwarded-for}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
)
loglevel = "debug"
wsgi_app = "src.infra.litestar.app_landing:app"
worker_class = "uvicorn.workers.UvicornWorker"
