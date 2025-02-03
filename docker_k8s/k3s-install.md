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

# install my helm chart
helm upgrade --install thesr ./helm/thesr/ --dry-run
k get node -o wide  # internal-ip
k get svc nginx-reverse-proxy  # ports
curl http://192.168.1.47:30112

# nginx ingress controller
# https://medium.com/@alesson.viana/installing-the-nginx-ingress-controller-on-k3s-df2c68cae3c8
# https://kubernetes.github.io/ingress-nginx/deploy/
helm upgrade --install ingress-nginx ingress-nginx \
  --repo https://kubernetes.github.io/ingress-nginx \
  --namespace ingress-nginx --create-namespace
kubectl get service --namespace ingress-nginx ingress-nginx-controller --output wide --watch


# stop everything
helm uninstall thesr
/usr/local/bin/k3s-killall.sh


# uninstall
# https://thriveread.com/uninstall-and-remove-k3s-completely/
```

