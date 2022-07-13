# Test using docker-compose

## Preparation

### Run docker-compose

```shell
tests/test_compose.sh
```

### Run local tunnel

Run following command in new terminal window to create tunnel

```shell
ssh -R 80:localhost:8080 nokey@localhost.run
```

And copy generated link (the link must end with `lhrtunnel.link`)

NOTE:
if you see `no ssh tunnel here :(` you need to find new link in terminal

## Test events

For testing, an nginx container with a test page is used. Test page sends two custom events before (`before_img`) and 
after (`after_img`) displaying the image. Event name and other parameters can be passed to query_string


Links to create a preview:
- before displaying the image `https://<lhrtunnel.link>/preview.png?event=before_img&width=1200&height=630`
- after `https://<lhrtunnel.link>/preview.png?event=after_img&width=1200&height=630`

## Test WebGL support 

To test WebGL support use the link `https://<lhrtunnel.link>/webgl.png`
