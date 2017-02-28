#!/usr/bin/env bash
sudo apt-get update
sudo apt-get install curl apt-transport-https ca-certificates
curl -fsSL https://yum.dockerproject.org/gpg | sudo apt-key add -
sudo add-apt-repository \
     "deb https://apt.dockerproject.org/repo/ \
       ubuntu-$(lsb_release -cs) \
       main"
sudo apt-get update
sudo apt-get install -y docker-engine python3-pip unrar
pip3 install docker rarfile pytest sh
sudo docker pull aatxe/pytest:latest
