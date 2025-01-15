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
- [Install Kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
    - easiest to first [install Go](https://go.dev/doc/install)
        - put Go bins on `$PATH`; [my bashrc](https://github.com/treatmesubj/Tips-Tricks/blob/master/configs/Linux/Bash/.bashrc_john.sh)
    - then, `go install sigs.k8s.io/kind@v0.20.0`
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
# per https://kind.sigs.k8s.io/docs/user/quick-start/#loading-an-image-into-your-cluster
# so k8s doesn't try to pull images from external registries
#
# ensure volume paths are correct in deployment templates
```

Kind cluster setup
- Kind (K8s in Docker) runs the K8s node/host as a Docker container itself, so to mount local directories in the pods, we need to first mount it in the Kind node, from which it will be mounted into the pods
- Also for Kind, `extraPortMappings` allow the local host to make requests to an Ingress controller over ports 80/443; [Kind Ingress docs](https://kind.sigs.k8s.io/docs/user/ingress/)
- Create `kind_config.yaml` with below contents
```yaml
apiVersion: kind.x-k8s.io/v1alpha4
kind: Cluster
nodes:
  - role: control-plane
    extraMounts:
      - hostPath: /mnt/c/Users/JohnHupperts/Documents/Programming_Projects/Thesaurus_Rex/docker_k8s/letsencrypt/
        containerPath: /mnt/c/Users/JohnHupperts/Documents/Programming_Projects/Thesaurus_Rex/docker_k8s/letsencrypt/
    extraPortMappings:
    - containerPort: 80
      hostPort: 80
      protocol: TCP
    - containerPort: 443
      hostPort: 443
      protocol: TCP
#  - role: worker
#    extraMounts:
#      - hostPath: /mnt/c/Users/JohnHupperts/Documents/Programming_Projects/Thesaurus_Rex/docker_k8s/letsencrypt/
#        containerPath: /mnt/c/Users/JohnHupperts/Documents/Programming_Projects/Thesaurus_Rex/docker_k8s/letsencrypt/
```

```bash
kind create cluster --name local-dev --config kind_config.yaml

kind get clusters
kubectl get nodes --name local-dev
kubectl cluster-info
kubectl get all
# kubectl proxy  # to expose cluster to localhost
# kind delete cluster --name local-dev
```

Allow kubectl binary to port-forward K8s to localhost low ports
```bash
sudo setcap CAP_NET_BIND_SERVICE=+eip /usr/bin/kubectl
```

Docker build images
```bash
docker images

cd ~/Thesaurus_Rex/docker_k8s/go_live/services/
docker build -t nginx-reverse-proxy:latest ./nginx-reverse-proxy/
docker build -t certbot:latest ./certbot/
docker build -t waitress-flask-wsgi:latest ./waitress-flask-wsgi/

docker images
```

Kind load images into cluster local registry
```bash
kind load docker-image nginx-reverse-proxy:latest --name local-dev
kind load docker-image certbot:latest --name local-dev
kind load docker-image waitress-flask-wsgi:latest --name local-dev
```

Helm install charts
```bash
cd ~/Thesaurus_Rex/docker_k8s/
helm upgrade --install thesr ./helm/thesr/ --dry-run
kubectl get all
kubectl exec --stdin --tty nginx-reverse-proxy-56877cb6cb-4df7x -- /bin/bash
# curl -k https://localhost
```
