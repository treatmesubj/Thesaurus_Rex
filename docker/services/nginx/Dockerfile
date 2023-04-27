FROM nginx:bullseye

# Override the default nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# self-signed cert bad
#RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/thesr.key -out /etc/ssl/certs/thesr.crt --subj "/C=US/ST=Texas/L=Austin/O=John/OU=John/CN=jrock4503@hotmail.com"
RUN mkdir /etc/nginx/sites-available
RUN mkdir /etc/nginx/sites-enabled
COPY ./nginx/ /etc/nginx
RUN ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default 

EXPOSE 443
EXPOSE 80
