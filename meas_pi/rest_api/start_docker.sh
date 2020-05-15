#!/bin/bash
app="docker.pi_rest"
docker build -t ${app} .
docker run -d -p 56733:80 --name=${app} -v $PWD:/code ${app}
