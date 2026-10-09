#!/bin/sh

# Enable root login over SSH
sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# Enable public key authentication
sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config

# Disable password authentication
sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# Create directory for sshd runtime
mkdir -p /var/run/sshd

# Idempotent key setup (mkdir guards images built without /root/.ssh)
mkdir -p /root/.ssh

# Copy authorized_keys file (overwrite, not append - restarts must not duplicate)
cat /root/tmp/authorized_keys > /root/.ssh/authorized_keys
chmod 600 /root/.ssh/authorized_keys

# Copy private key
cat /root/tmp/id_rsa > /root/.ssh/id_rsa

# Copy Git configuration
cat /root/tmp/gitconfig > /root/.gitconfig

# Set appropriate permissions for private key
chmod 600 /root/.ssh/id_rsa

# Copy public key
cat /root/tmp/id_rsa.pub > /root/.ssh/id_rsa.pub

# Start sshd in the foreground
/usr/sbin/sshd -D -o ListenAddress=0.0.0.0
