import os

bind = f'[::]:{os.environ.get("PORT") if "PORT" in os.environ else 8080}'

wsgi_app = 'main:app'

accesslog = '-'

capture_output = True

proxy_allow_ips = '*'

timeout = 600