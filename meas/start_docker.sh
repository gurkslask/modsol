#!/bin/bash
app="docker.meas_rest"
docker build -t ${app} .
docker run -d -p 56733:5000 --name=${app} -v $PWD:/code ${app}
# docker run -p 56733:5000 --name=${app} -v $PWD:/code ${app}
