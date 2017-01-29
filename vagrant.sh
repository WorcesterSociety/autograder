#!/usr/bin/env bash
sudo apt-get update
sudo apt-get install curl apt-transport-https ca-certificates python-software-properties
curl -fsSL https://yum.dockerproject.org/gpg | sudo apt-key add -
sudo add-apt-repository \
     "deb https://apt.dockerproject.org/repo/ \
       ubuntu-$(lsb_release -cs) \
       main"
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install -y docker-engine oracle-java8-installer
