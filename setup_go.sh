#!/bin/bash

# Download Go binary
wget https://go.dev/dl/go1.22.1.linux-amd64.tar.gz

# Remove existing Go installation and extract downloaded archive
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.22.1.linux-amd64.tar.gz

# Set up environment variables
echo 'export GOPATH=$HOME/' >> ~/.bashrc
echo 'export PATH=$PATH:/usr/local/go/bin:$GOPATH/bin' >> ~/.bashrc

# Source the .bashrc file to apply changes immediately
source ~/.bashrc

# Clean up downloaded archive
rm go1.22.1.linux-amd64.tar.gz
go version
echo "Go has been installed and environment variables have been configured."
