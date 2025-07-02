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

- `cd init_TLS`
- fire up docker containers
    - `docker compose up -d`
- check NGINX is all good
    - `curl localhost`
    - check that you mounted stuff correctly
- hop in certbot container and create TLS key/cert
    - `docker exec -it cerbot bash`
    - `certbot certonly --webroot`
        - webroot: `/letsencrypt`
    - congrats

- bring down the `init_TLS` docker containers
    - `docker compose down`
- clean up
    - `docker system prune --all`
    - `docker ps`
    - `cd ..`
- back up a copy of letsencrypt files
    - `cp -r letsencrypt/ ~`
- **Go Live**
    - `cd go_live`
    - `docker compose up -d`

---

- check NGINX logs (official NGINX Docker image symlinks access & error logs to stdout & stderr)
    - `docker logs {your-container-id-here} -f`

- Set Up `certbot`
    - `docker exec -it go_live-certbot-1 bash`
    - verify `certbot` works
        - `certbot renew --dry-run`
    - add a cron job for certbot to renew cert before expiry
        - `docker exec -it go_live-certbot-1 bash`
        - `apt update && apt install cron`
        - `cron` (background)
        - `apt install vim`
        - `export EDITOR='vim'`
        - `crontab /etc/cron.d/certbot`
        - `crontab -l`
    - FYI: apparently NGINX needs to be restarted to pick up the new cert
        - `docker compose down`
        - `docker compose up -d`

#### Manual Certbot Renew
- `docker container ls`
- `docker exec -it certbot bash`
- `certbot renew --dry-run`
- `certbot renew`
- `exit`
- `cp -r ~/letsencrypt ~/letsencrypt_bak`
- `cp -r Thesaurus_Rex/docker_k8s/letsencrypt/ ~`
- `cd Thesaurus_Rex/docker_k8s/go_live`
- `docker compose down`
- `docker compose up -d`

---

## Docker Compose -> K8s

- [Install Kompose](https://github.com/kubernetes/kompose)
- [Install Docker](https://docs.docker.com/engine/install/debian/)
    - [Docker user group](https://docs.docker.com/engine/install/linux-postinstall/)
        - may also need `sudo chmod 666 /var/run/docker.sock`
- [Install Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- [Install Helm](https://helm.sh/docs/intro/install/)

You need `letsencrypt/` with certs already created by Docker Compose init\_TLS cerbot above\
You can [use scp to copy certs from elsewhere](https://github.com/treatmesubj/Tips-Tricks/blob/master/networking/scp_ssh_file_copy.txt), but you'll need to re-symlink the certs in `live/` to latest in `archive/`
```
$ cd ~/Thesaurus_Rex/docker_k8s/
$ ls -1
go_live
init_TLS
letsencrypt
README.md
```

Kompose Docker Compose to K8s Helm Templates
```bash
curl -L https://github.com/kubernetes/kompose/releases/download/v1.29.0/kompose-linux-amd64 -o kompose
./kompose convert -f ./go_live/docker-compose.yml --volumes hostPath -c
mkdir helm
mv ./go_live/docker_compose/ ./helm/thesr/
rm kompose
# add `imagePullPolicy: Never` to each of ./helm/thesr/templates/*deployment.yaml
# so k8s doesn't try to pull images from external registries
```

Install k3s
```bash
# no traefik
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server --disable=traefik" K3S_KUBECONFIG_MODE="644" sh -s -
sudo systemctl status k3s.service
cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
k cluster-info
```

Build images
```bash
docker build --no-cache ./go_live/services/certbot/ -t certbot
docker build --no-cache ./go_live/services/nginx-reverse-proxy/ -t nginx-reverse-proxy
docker build --no-cache ./go_live/services/waitress-flask-wsgi/ -t waitress-flask-wsgi
```

Import images into k3s
```bash
docker image ls
docker save nginx-reverse-proxy | sudo k3s ctr images import -
docker save waitress-flask-wsgi | sudo k3s ctr images import -
docker save certbot | sudo k3s ctr images import -
sudo k3s ctr images ls
```

Helm install charts
```bash
cd ~/Thesaurus_Rex/docker_k8s/
helm upgrade --install thesr ./helm/thesr/ --dry-run
kubectl get all
# # nginx ingress controller
# https://medium.com/@alesson.viana/installing-the-nginx-ingress-controller-on-k3s-df2c68cae3c8
# https://kubernetes.github.io/ingress-nginx/deploy/
# helm upgrade --install ingress-nginx ingress-nginx \
#   --repo https://kubernetes.github.io/ingress-nginx \
#   --namespace ingress-nginx --create-namespace
# kubectl get service --namespace ingress-nginx ingress-nginx-controller --output wide --watch
```

stop everything
```bash
helm uninstall thesr
/usr/local/bin/k3s-killall.sh
sudo rm -rf /var/lib/rancher/k3s
```

restart
```bash
sudo systemctl restart k3s
cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
```

uninstall
```
https://thriveread.com/uninstall-and-remove-k3s-completely/
```

---

certbot testing
```bash
kubectl create job --from=cronjob/certbot certbot-test
kubectl exec -it certbot-<pod> -- bash
certbot renew --dry-run
```
