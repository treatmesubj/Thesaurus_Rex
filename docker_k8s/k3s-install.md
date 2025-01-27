```bash
# https://loganmarchione.com/2022/03/k3s-single-node-cluster-for-noobs/
curl -sfL https://get.k3s.io |  sh -s - --disable traefik --write-kubeconfig-mode 644
sudo systemctl status k3s.service
cp /etc/rancher/k3s/k3s.yaml ~/.kube/config
k cluster-info

# mount volumes to node

# nginx ingress controller
# https://medium.com/@alesson.viana/installing-the-nginx-ingress-controller-on-k3s-df2c68cae3c8
```
