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

## Docker Compose -> K8s

```
$ # you need the letsencrypt dir with certs already created by Docker Compose init_TLS cerbot above
$ cd ~/Thesaurus_Rex/docker/
$ ls -1
go_live
init_TLS
letsencrypt
README.md
```

- [Install Kompose](https://github.com/kubernetes/kompose)

```bash
curl -L https://github.com/kubernetes/kompose/releases/download/v1.29.0/kompose-linux-amd64 -o kompose
./kompose convert -f ./go_live/docker-compose.yml --volumes hostPath -c
mkdir helm
mv ./go_live/docker_compose/ ./helm/thesr/
rm kompose
# add `imagePullPolicy: IfNotPresent` to each of ./helm/thesr/templates/*deployment.yaml
# per https://kind.sigs.k8s.io/docs/user/quick-start/#loading-an-image-into-your-cluster
# so k8s doesn't try to pull images from external registries
```

- [Install Docker](https://docs.docker.com/engine/install/debian/)
    - [Docker user group](https://docs.docker.com/engine/install/linux-postinstall/)
- [Install Kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation)
    - easiest to first [install Go](https://go.dev/doc/install)
        - put Go bins on `$PATH`; [my bashrc](https://github.com/treatmesubj/Tips-Tricks/blob/master/configs/Linux/Bash/.bashrc_john.sh)
    - then, `go install sigs.k8s.io/kind@v0.20.0`
- [Install Kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/)
- [Install Helm](https://helm.sh/docs/intro/install/)
- [Kind & Helm](https://faun.pub/local-kubernetes-with-kind-helm-and-a-sample-service-4755e3e6eff4)

```bash
kind create cluster --name local-dev
kind get clusters
kubectl cluster-info
# kubectl proxy  # to expose cluster to localhost

# run local registry, build images, push to local registry, so they can be pulled by K8s
#       https://docs.docker.com/registry/deploying/#run-a-local-registry
#       BONUS
#       build & push images up to docker registry
#            https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
#            docker login
#            kubectl create secret generic regcred \
#              --from-file=.dockerconfigjson=/home/john/.docker/config.json \
#              --type=kubernetes.io/dockerconfigjson
#            kubectl get secret regcred --output=yaml

# helm upgrade --install thesr ./helm/thesr/ --dry-run

```
