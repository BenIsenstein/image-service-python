import os

bind = f'[::]:{os.environ.get("PORT") if "PORT" in os.environ else 8080}'

wsgi_app = 'main:app'

accesslog = '-'

capture_output = True

proxy_allow_ips = '*'

timeout = int(os.environ.get("TIMEOUT")) if "TIMEOUT" in os.environ else 0

workers = int(os.environ.get("WORKERS")) if "WORKERS" in os.environ else 1

print('bind: ', bind)
print('timeout: ', timeout)
print('workers: ', workers)