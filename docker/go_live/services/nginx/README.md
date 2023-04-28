## [Nginx Reverse Proxy for Flask + Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/reverse-proxy.html)
- Create TLS/SSL crytographic certificate & key for encryption & decryption of TCP packets
    - $ `openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/thesr.key -out /etc/ssl/certs/thesr.crt --subj "/C=US/ST=Texas/L=Austin/O=John/OU=John/CN=jrock4503@hotmail.com"`
- configure nginx: `/etc/nginx/sites-available/default`
- Apparently it's very important to include trailing `/` to protect against path traversal
    ```
    server {
        listen 443 ssl;
        ssl_certificate /etc/ssl/certs/thesr.crt;
        ssl_certificate_key /etc/ssl/private/thesr.key;
        server_name thesr.localhost;
        location / {
            proxy_pass http://localhost:8000;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }

    server {
        listen 80;
        server_name thesr.localhost;
        return 302 https://$server_name$request_uri;
    }
    ```

## Docker stuff
- clear up stuff
    - $ `docker ps`
    - $ `docker stop <container>`
    - $ `docker system prune --all`
- $ `docker build -t thesr_flask_img .`
- $ `docker run -itd -p 443:443 --name thesr_flask_app thesr_flask_img`
- check stuff
    - $ `docker exec -it thesr_flask_app bash`

