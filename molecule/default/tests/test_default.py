import os
import pytest
import yaml

import testinfra.utils.ansible_runner


testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.fixture()
def ansible_defaults():
    with open('playbook-vars.yml', 'r') as stream:
        return yaml.load(stream)


@pytest.mark.parametrize('package', ansible_defaults()['ssh_client_packages'])
def test_ssh_client_packages(host, package):
    assert host.package(package).is_installed


@pytest.mark.parametrize('package', ansible_defaults()['ssh_server_packages'])
def test_ssh_server_packages(host, package):
    assert host.package(package).is_installed


def test_ssh_moduli(host):
    f = host.file('/etc/ssh/moduli')

    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644

    assert not host.file('/etc/ssh/moduli.all').exists
    assert not host.file('/etc/ssh/moduli.safe').exists


@pytest.mark.parametrize('ssh_host_key',
                         ansible_defaults()['ssh_host_keys_bits'].keys())
def test_ssh_host_keys(host, ssh_host_key):
    priv = host.file('/etc/ssh/ssh_host_%s_key' % ssh_host_key)

    assert priv.exists
    assert priv.is_file
    assert priv.user == 'root'
    assert priv.group == 'root'
    assert priv.mode == 0o600

    pub = host.file('/etc/ssh/ssh_host_%s_key.pub' % ssh_host_key)

    assert pub.exists
    assert pub.is_file
    assert pub.user == 'root'
    assert pub.group == 'root'
    assert pub.mode == 0o644

    conf = host.file('/etc/ssh/sshd_config')

    assert conf.contains('HostKey /etc/ssh/ssh_host_%s_key' % ssh_host_key)


def test_ssh_host_key_algorithms(host, ansible_defaults):
    conf = host.file('/etc/ssh/sshd_config')

    host_key_algorithms = ansible_defaults['ssh_host_keys_bits'].keys()

    assert conf.contains('HostKeyAlgorithms %s' %
                         ','.join("ssh-" + s for s in host_key_algorithms))


def test_ssh_local_facts(host, ansible_defaults):
    local_facts_file = host.file('/etc/ansible/facts.d/ssh.fact')

    assert local_facts_file.exists
    assert local_facts_file.is_file
    assert local_facts_file.user == 'root'
    assert local_facts_file.group == 'root'
    assert local_facts_file.mode == 0o644

    local_facts_ssh = \
        host.ansible("setup")["ansible_facts"]["ansible_local"]["ssh"]

    if ansible_defaults['ssh_rebuild_moduli']:
        assert local_facts_ssh['ssh_moduli_rebuilt']
    else:
        assert not local_facts_ssh['ssh_moduli_rebuilt']

    if ansible_defaults['ssh_rebuild_host_keys']:
        assert local_facts_ssh['ssh_host_keys_rebuilt']
    else:
        assert not local_facts_ssh['ssh_host_keys_rebuilt']


@pytest.mark.parametrize('opt,value',
                         ansible_defaults()['ssh_client_config'].items())
def test_ssh_client_config(host, opt, value):
    f = host.file('/etc/ssh/ssh_config')

    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644

    assert f.contains('%s %s' % (opt, value))


@pytest.mark.parametrize('opt,value',
                         ansible_defaults()['ssh_server_config'].items())
def test_ssh_server_config(host, opt, value):
    f = host.file('/etc/ssh/sshd_config')

    assert f.exists
    assert f.is_file
    assert f.user == 'root'
    assert f.group == 'root'
    assert f.mode == 0o644

    assert f.contains('%s %s' % (opt, value))


def test_ssh_service(host):
    assert host.service('ssh').is_enabled
    assert host.service('ssh').is_running
