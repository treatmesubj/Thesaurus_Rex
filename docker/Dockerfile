FROM nginx:bullseye

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install thesr

RUN mkdir /app

COPY ./flask/ /app

RUN pip install /app/dist/thesr_flask_app-0.0.0-py3-none-any.whl
RUN pip install waitress

# TODO: RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/thesr.key -out /etc/ssl/certs/thesr.crt --subj "/C=US/ST=Texas/L=Austin/O=John/OU=John/CN=jrock4503@hotmail.com"
# TODO: copy file to configure nginx /etc/nginx/sites-available/default

CMD ["waitress-serve", "--host", "0.0.0.0", "--port", "8000", "url-scheme", "https", "thesr_flask_app:app"]
# nginx runs by default per nginx:bullseye dockerfile

EXPOSE 443
EXPOSE 80
