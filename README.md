Ansible Role: SSH
=========

[![Build Status](https://travis-ci.org/lnovara/ansible-ssh.svg?branch=master)](https://travis-ci.org/lnovara/ansible-ssh)
[![Ansible Galaxy](https://img.shields.io/badge/galaxy-lnovara.ssh-blue.svg)](https://galaxy.ansible.com/lnovara/ssh)

Install and configure SSH server and client.

Requirements
------------

An Ansible 2.2 or higher installation.

Role Variables
--------------

Available variables are listed below, along with default values (see
defaults/main.yml).

    ssh_client_packages:
      - openssh-client

Packages to install to provide SSH client functionalities.

    ssh_server_packages:
      - openssh-server

Packages to install to provide SSH server functionalities.

    ssh_client_config: {}

Dictionary holding SSH client configuration. The complete SSH client
configuration reference can be found
[here](https://linux.die.net/man/5/ssh_config).<br/>
**NOTE**: the provided SSH client configuration will be merged with the default
one defined in `vars/main.yml`.

    ssh_server_config: {}

Dictionary holding SSH server configuration. The complete SSH server
configuration reference can be found
[here](https://linux.die.net/man/5/sshd_config).<br/>
**NOTE**: the provided SSH server configuration will be merged with the default
one defined in `vars/main.yml`.

    ssh_rebuild_moduli: yes

Rebulild `/etc/ssh/moduli` file that contain primes for Diffie-Hellman Group
Exchange (DH-GEX).  
**NOTE**: the role records a ``ssh.ssh_moduli_rebuilt`` local fact  in order not
to rebuild ``/etc/ssh/moduli`` at every run.

    ssh_moduli_bits: 4096

Number of bits for DH-GEX primes.

    ssh_rebuild_host_keys: yes

Rebuild SSH host keys.  
**NOTE**: the role records a ``ssh.ssh_host_keys_rebuilt`` local fact in order
not to rebuild SSH host keys at every run.

    ssh_host_keys_bits:
      ed25519: 512  # Ed25519 keys have fixed length, number of bits is ignored
      rsa: 4096

Dictionary holding key type and length of SSH public keys to be created.

Dependencies
------------

[config_encoder_filters](https://github.com/jtyr/ansible-config_encoder_filters)

Example Playbook
----------------

    - name: Install and configure SSH on all hosts.
      hosts: all
      roles:
         - config_encoder_filters
         - lnovara.ssh

Testing
-------

This role uses [molecule](https://molecule.readthedocs.io/en/latest/) to
implement automatic testing of its functionalities.

To execute the tests

```bash
pip install tox

git clone https://github.com/lnovara/ansible-ssh.git

cd ansible-ssh

# test all the scenarios
tox
```

License
-------

MIT

Author Information
------------------

Luca Novara
