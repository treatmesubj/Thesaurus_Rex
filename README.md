# Thesaurus-Rex
CLI wrapper for [Merriam-Webster Collegiate Dictionary & Thesaurus APIs](https://dictionaryapi.com/products/index)

### Installation
- from [PyPI](https://pypi.org/project/thesr): `pip install thesr`
- from [GitHub](https://github.com/treatmesubj/Thesaurus_Rex): `pip install "git+https://github.com/treatmesubj/Thesaurus_Rex"`

### Usage

```
python thesr.py [-h] --word WORD [--antonyms] [--define] [--verbose]
```
Common English phrases & idioms such as `tongue-in-cheek` or `dime-a-dozen` sometimes work as well

```
john@spectre:~
$ python thesr.py -w purport -v

[purport!]

(noun) the idea that is conveyed or intended to be conveyed to the mind by language, symbol, or action
        synonyms: ['content', 'denotation', 'drift', 'import', 'intent', 'intention', 'meaning', 'sense',
'significance', 'signification']
        antonyms: []


(verb) to have in mind as a purpose or goal
        synonyms: ['aim', 'allow', 'aspire', 'calculate', 'contemplate', 'design', 'go', 'intend', 'look', 'mean']
        antonyms: []


(verb) to state as a fact usually forcefully
        synonyms: ['affirm', 'allege', 'assert', 'aver', 'avouch', 'avow', 'claim', 'contend', 'declare', 'insist']
        antonyms: ['deny', 'gainsay']


---Dictionary--------------------------------------------------------------------
(verb) to have the often specious appearance of being, intending, or claiming (something implied or inferred); also
: claim
        intend, purpose


(noun) meaning conveyed, professed, or implied : import; also : substance, gist
etymology:
        Middle English, from Anglo-French, content, tenor, from purporter to carry, mean, purport, from pur-
thoroughly + porter to carry {ma}{mat|purchase:1|}, {mat|port|}{/ma}
```

## [Thesaurus-Rex Web Server](./docker_k8s)
### [thesr.online](https://thesr.online)
Check out Thesaurus-Rex's ~~[Docker](https://www.docker.com/) (Compose)~~ [Kubernetes](https://kubernetes.io/) containerized web experience built with an [NGINX](https://www.nginx.com/) hardened reverse proxy & TLS/SSL encryption container in front of a containerized [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/) web server & [Flask](https://flask.palletsprojects.com/en/2.2.x/) framework Python application.\
It's running on a [ufw](https://wiki.debian.org/Uncomplicated%20Firewall%20%28ufw%29) firewalled Debian virtual machine in the cloud courtesy of [Linode](https://www.linode.com/).\
[fail2ban](https://github.com/fail2ban/fail2ban) protects the server from bruteforce attacks. Though, RSA asymetric cryptographic public-encrypt-key/private-decrypt-key pairs are used for administration of the host; OpenSSH server's password authentication is disabled.\
I bought the [thesr.online](https://thesr.online) domain from [Hover](https://www.hover.com/).\
The TLS/SSL cryptographic certificate for the [thesr.online](https://thesr.online) domain is validated & signed by the [Let's Encrypt](https://letsencrypt.org/) [open source](https://github.com/letsencrypt/boulder) certificate authority.

![](./images/thesr_web.png)

#### The Internet's Spooky
[https://thesr.online](https://thesr.online) has been on the internet for about 2 weeks now (5/12/23).\
Here's a geo-map of thousands of malicious IP addresses that tried to bruteforce guess my credentials to gain control of my server from just some of the logs.\
Also, here's a sample of the latest traffic to my server from the logs, showing probably botnets, trying to extract credentials, upload binary data, and exploit old software vulnerabilities.

![](./images/sshers.png)\
![](./images/nginx_tail.png)

### [Docker Compose](https://docs.docker.com/compose/) -> [Kubernetes](https://kubernetes.io/)
I first used [Kompose](https://github.com/kubernetes/kompose) to roughly translate my Docker Compose files to K8s resources.\
Then, I used [k3s](https://k3s.io/) to run a local cluster to develop and test my project.\
I learned, asked, and answered some StackOverflow questions about [Linux network
interfaces](https://stackoverflow.com/a/79406073/11255791) and more about
[Linux DNS resolution
configuration](https://stackoverflow.com/a/79407204/11255791).\
I used [Helm](https://helm.sh) to deploy the workload to my cluster.\
My Nginx reverse proxy remains in place as a `Deployment` mounting the
Letsencrypt certifcates via `PersistentVolumeClaim` and a `LoadBalancer` service routes
external traffic to Nginx.\
A `CronJob` attempts to renew my Letsencrypt certificates every 15 days.

See [docker\_k8s/README.md](./docker_k8s/README.md) for the detailed steps.

*Update (02/12/25):* Turns out k8s IPv6 needs some extra configuration, so I've removed the IPv6 DNS AAAA record for `thesr.online` for now.

![](./images/k3s-demo.gif)
