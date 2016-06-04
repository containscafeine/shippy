import docker
import pytest
from random import randint
from shipy.dpyexec import Shipy


@pytest.fixture
def shipy():
    return Shipy()


@pytest.fixture(scope='function')
def client(request):
    client = docker.Client(base_url='unix://var/run/docker.sock')

    def container_fin():
        for container in client.containers(all=True):
            name = str(container['Names'][0])[1:]
            if name.startswith('bruce') and \
                    name.endswith('wayne'):
                client.remove_container(name, force=True)

    request.addfinalizer(container_fin)
    return client


def cinput(cmd):
    return cmd.split()


def container_name():
    prefix = 'bruce'
    suffix = 'wayne'
    return '{}-{}-{}'.format(prefix, randint(1, 10000000), suffix)


def test_docker_run_template(client,
                             shipy,
                             farg=' ',
                             fval=' ',
                             fval2=' ',
                             cimage='busybox',
                             cargs='ping 127.0.0.1',
                             cn=None):

    if cn is None:
        cn = container_name()
    farg2 = ' ' if fval2 == ' ' else farg
    container = shipy.shipy(
        cinput('run {} {} {} {} --name {} {} {}'
               .format(farg, fval, farg2, fval2, cn, cimage, cargs)))
    return container
