# Examples

Examples can be run using docker-compose or minikube

## Docker-compose

Create env file

```shell
cp -f docker-compose/.env.example docker-compose/.env
```

Run

```shell
docker-compose -p epig --env-file docker-compose/.env -f docker-compose/docker-compose.yml up
```

## Minikube

Run Minikube

```shell
minikube start
minikube addons enable ingress
minikube addons enable ingress-dns
```

Copy configmap example and edit new file

```shell
cp -f k8s/configmap.yml.example k8s/configmap.yml
```

Generate password for redis

```shell
kubectl create secret generic redis-secret --from-literal=password=$(head -c 512 /dev/urandom | LC_CTYPE=C tr -cd 'a-zA-Z0-9' | head -c 64)
```

Build local images

```shell
minikube image build -t chromium-headless ../chromium-headless/
minikube image build -t preview-generator ../preview-generator/ 
```

Create nginx configmaps

```shell
kubectl create configmap nginx-html --from-file=nginx/html
kubectl create configmap nginx-template --from-file=nginx/templates/
```

Create persistant volumes

```shell
mkdir -p k8s/volume
minikube mount k8s/volume:/data/volume
```

Apply k8s config

```shell
kubectl apply -f ./k8s
```

Run minikube tunnel

```shell
minikube tunnel --cleanup=true
```

## Run local tunnel

Run following command in new terminal window to create tunnel

```shell
ssh -R 80:localhost:80 nokey@localhost.run
```

And copy generated link (the link must end with `lhrtunnel.link`)

### NOTE

if you see `no ssh tunnel here :(` you need to find new link in terminal.

## Test events

For testing, nginx container with a test page is used. The test page contains text and an image that appears after 2
seconds. The page sends two custom events before (`before_img`) and
after (`after_img`) the image is loaded. Event name and preview size can be passed to query_string.

Links to create a preview:

- before displaying the image `https://<lhrtunnel.link>/preview.png?event=before_img&width=1200&height=630`
- after `https://<lhrtunnel.link>/preview.png?event=after_img&width=1200&height=630`

## Test WebGL support

To test WebGL support use the link `https://<lhrtunnel.link>/webgl.png`.

## Test Opengraph protocol

You can test social media preview by sending the tunnel link (https://<lhrtunnel.link>) to https://www.opengraph.xyz.
Event name and preview size can be passed to query_string.