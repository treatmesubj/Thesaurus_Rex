- [Flask package setup](https://flask.palletsprojects.com/en/2.2.x/patterns/packages/)

I had to create a new Python venv just for flask because I had wack dependency issues

## Flask Dev
- $ `cd ./flask`
- $ `pip install -e .`
- $ `flask --app thesr_flask_app run -p 8000`

## [Flask + Waitress Deploy to Prod](https://flask.palletsprojects.com/en/2.2.x/tutorial/deploy/)
- create a wheel to distribute because it's the cool way
    - $ `cd ./flask`
    - $ `python setup.py bdist_wheel`
    - $ `cd ./dist`
- create a fresh new Python venv to `pip install` wheel
    - $ `python -m venv ~/.tmp_flask_venv`
    - $ `source ~/.tmp_flask_venv/bin/activate`
    - $ `pip install thesr_flask_app-0.0.0-py3-none-any.whl`
- Deploy locally on [Waitress WSGI server](https://flask.palletsprojects.com/en/2.2.x/deploying/waitress/)
    - $ `pip install waitress`
    - $ `waitress-serve --host 127.0.0.1 --port 8000 thesr_flask_app:app`

## [Nginx Reverse Proxy for Flask + Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/reverse-proxy.html)
- Create TLS/SSL crytographic certificate & key for encryption & decryption of TCP packets
    - $ `openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/thesr.key -out /etc/ssl/certs/thesr.crt --subj "/C=US/ST=Texas/L=Austin/O=John/OU=John/CN=jrock4503@hotmail.com"`
- configure nginx: `/etc/nginx/sites-available/default`
    ```
    server {
        listen 443 ssl;
        ssl_certificate /etc/ssl/certs/thesr.crt;
        ssl_certificate_key /etc/ssl/private/thesr.key;
        server_name thesr.com;
        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }

    server {
        listen 80;
        server_name thesr.com;
        return 302 https://$server_name$request_uri;
    }
    ```

# Docker stuff
- [Dockerfile](Dockerfile)
- clear up stuff
    - $ `docker ps`
    - $ `docker stop <container>`
    - $ `docker system prune --all`
- $ `docker build -t thesr_flask_img .`
- $ `docker run -itd -p 443:443 --name thesr_flask_app thesr_flask_img`
- check stuff
    - $ `docker exec -it thesr_flask_app bash`

