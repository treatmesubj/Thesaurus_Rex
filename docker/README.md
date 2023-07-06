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
          listen [::]:80;
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
- hop in certbot container and create TLS key/cert
    - $ `docker exec -it cerbot bash`
    - $ `certbot certonly --webroot`
        - webroot: `/letsencrypt`
    - congrats

- bring down the `init_TLS` docker containers
    - $ `docker compose down`
- clean up
    - $ `docker system prune --all`
    - $ `docker ps`
- back up a copy of letsencrypt files
    - $ `cp -r letsencrypt/ ~`
- **Go Live**
    - $ `cd go_live`
    - $ `docker compose up -d`

---

- check NGINX logs (official NGINX Docker image symlinks access & error logs to stdout & stderr)
    - $ `docker logs {your-container-id-here} -f`

- Set Up `certbot`
    - $ `docker exec -it go_live-certbot-1 bash`
    - verify `certbot` works
        - $ `certbot renew --dry-run`
    - add a cron job for certbot to renew cert before expiry
        - $ `docker exec -it go_live-certbot-1 bash`
        - $ `apt update && apt install cron`
        - $ `cron` (background)
        - $ `apt install vim`
        - $ `export EDITOR='vim'`
        - $ `crontab /etc/cron.d/certbot`
        - $ `crontab -l`

---

### [Kompose](https://github.com/kubernetes/kompose)

```bash
cd go_live
curl -L https://github.com/kubernetes/kompose/releases/download/v1.29.0/kompose-linux-amd64 -o kompose
./kompose convert -f docker-compose.yml -c
```
