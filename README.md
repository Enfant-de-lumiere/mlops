# mlops
## Partie 1 
4) J'utilise Nginx pour simplifier l'utilisation des requêtes API, cela permet de ne pas exposer les ports dans mes endpoints.
Il permet aussi de créer un seul endpoint sur plusieurs instances du même service ainsi les requêtes vont être distribué sur chacunes des instances. (exemple : 50 requêtes API en attente sur le même endpoint, Nginx va distribué équitablement ou pas sur toutes les instances du service_a pour effectuer les requêtes). 
5) Je n'utilise pas Kubernetes (Minikube) pour plusieurs raisons :
    -le projet n'est pas assez grand, j'ai uniquement 4 services.
    -je n'ai pas prévu de le déployer sur un cloud, cela aurait été pertinent d'utilise Minikube pour simuler Kubernetes
    en local puis Kurbenetes sur le cloud mais mon projet est uniquement en local.

