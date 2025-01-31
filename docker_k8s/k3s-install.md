```bash
# https://loganmarchione.com/2022/03/k3s-single-node-cluster-for-noobs/
# no traefik
curl -sfL https://get.k3s.io | INSTALL_K3S_EXEC="server --disable=traefik" K3S_KUBECONFIG_MODE="644" sh -s -
sudo systemctl status k3s.service
cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
k cluster-info

# mount volumes to node
# create an sc, local pv, and pvc

# load local Docker images to k3s
docker save certbot > certbot.tar
sudo k3s ctr images import certbot.tar
docker save nginx-reverse-proxy | sudo k3s ctr images import -
docker save waitress-flask-wsgi | sudo k3s ctr images import -
sudo k3s ctr images ls

# nginx ingress controller
# https://medium.com/@alesson.viana/installing-the-nginx-ingress-controller-on-k3s-df2c68cae3c8

# uninstall
# https://thriveread.com/uninstall-and-remove-k3s-completely/
```

