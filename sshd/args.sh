#!/bin/sh

sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config 
sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config 
mkdir -p /var/run/sshd 
cat /root/tmp/authorized_keys >> /root/.ssh/authorized_keys 
cat /root/tmp/id_rsa > /root/.ssh/id_rsa 
cat /root/tmp/gitconfig > /root/.gitconfig
chmod 600 /root/.ssh/id_rsa 
cat /root/tmp/id_rsa.pub > /root/.ssh/id_rsa.pub