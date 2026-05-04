Author: Dmitry Porotov

---

# Nginx in a container with config script
This project contains a `Dockerfile` to build an Nginx container and `docker-compose.yaml` file to run the container.

The script `script.py` generates a config file for Nginx. Provided a domain it generates sub-domains for it.