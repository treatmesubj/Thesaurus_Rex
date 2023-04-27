# Proper TLS/SSL CA-signed Certs
- setup domain & its nameservers in domain registrar's control panel
    - [Hover.com](https://www.hover.com/control_panel/domain)
        - nameservers for Linode VM: `ns1.linode.com, ns2.linode.com, .. ns5.linode.com`
- add NS record, A/AAAA records for hostname/IP addrs in VM control panel
    - [cloud.linode.com](https://cloud.linode.com/domains/)
- ssh to VM
- check certbot docs for requirements for your SW/OS
    - [certbot.eff.org](https://certbot.eff.org/)
- in docker-compose.yml include a shared volume for certbot to put certs in and for nginx to use
- in nginx.conf, allow letsencrypt to find files for validation
    ```
    server {
          listen 80;

          location /.well-known/acme-challenge/ {
            root /letsencrypt/;
          }

          location / {
            gzip off;
            root /usr/share/nginx/html/;
            index  index.html;
          }

        }
    ```

- $ `cd init_TLS`
- fire up docker containers
    - $ `docker compose up -d`
- check NGINX is all good
    - $ `curl localhost`
    - check that you mounted stuff correctly
- hop in certbot container
    - $ `docker exec -it cerbot bash`
    - $ `certbot certonly --webroot`
        - webroot: `/letsencrypt`
    - congrats

- bring down the `init_TLS` docker containers
- clean up
    - $ `docker system prune --all`
    - $ `docker ps`

- go live
    - $ `cd go_live`
    - $ `docker compose up -d`


