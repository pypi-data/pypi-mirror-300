# IBM Confidential
# PID 5900-BAF
# Copyright StreamSets Inc., an IBM Company 2024

import argparse
import configparser
import io
import json
import logging
import os
import socket
import subprocess
import sys
import tarfile
import time

import docker

from .. import logger as streamsets_logger
from ..__version__ import __version__

DEFAULT_TESTFRAMEWORK_DOCKER_REPO = 'streamsets/testframework-4.x'
DOCKER_IMAGE_3_X = 'streamsets/testframework:3.x'
DOCKER_IMAGE_4_X = '{}:latest'.format(DEFAULT_TESTFRAMEWORK_DOCKER_REPO)
DEFAULT_DOCKER_CONFIG_DIRECTORY = os.path.expanduser('~/.docker')
DEFAULT_DOCKER_IMAGE = DOCKER_IMAGE_4_X
DEFAULT_DOCKER_NETWORK = 'cluster'
DEFAULT_DOCKER_TIMEOUT = 120

SDK_USER_CONFIG_PATH = os.path.expanduser('~/.streamsets')
SDK_ACTIVATION_FILE_NAME = 'rsa-signed-activation-info.properties'

DEFAULT_TESTFRAMEWORK_CONFIG_DIRECTORY = os.path.expanduser('~/.streamsets/testframework')

DEFAULT_BUILD_NAME = 'latest'
DEFAULT_BUILD_S3_BUCKET = 'nightly.streamsets.com'
DEFAULT_BUILD_DOCKER_REPO = 'streamsets/datacollector-libs'

DEFAULT_TESTS_DOCKER_REPO = 'streamsets/tests'
DOCKER_LABEL_TESTS_NAME = 'com.streamsets.tests-name'

DOCKER_IMAGE_CLI_DIR = '/root/testframework/streamsets/testframework/cli'

ENV_VAR_FILENAME = 'testframework_env_vars.json'

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     epilog="Run 'stf <command> -h' for more information on a specific subcommand.")
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__))
    parser.add_argument('-v', '--verbose', action='store_true', help='Be noisier')
    parser.add_argument('--docker-image',
                        metavar='image',
                        help='Docker image to use for the STF container')
    parser.add_argument('--release',
                        help='Release version to use the appropriate STF image',
                        choices=['3.x', '4.x'])
    parser.add_argument('--docker-image-dont-pull',
                        action='store_true',
                        help="Don't pull STF Docker image")
    parser.add_argument('--docker-network',
                        metavar='network',
                        help='Docker network to which to attach the STF container',
                        default=DEFAULT_DOCKER_NETWORK)
    parser.add_argument('--sdc-resources-directory',
                        metavar='dir',
                        help=('A directory containing resources to mount into the SDC container'))
    parser.add_argument('--testframework-config-directory',
                        metavar='dir',
                        help=("A directory containing STF configuration files to mount into the "
                              "STF container"),
                        default=DEFAULT_TESTFRAMEWORK_CONFIG_DIRECTORY)
    parser.add_argument('--env-var', action='append', metavar='var',
                        help=('One or more environment variables to set. Retrieves host environment variable(s) as '
                              'given by this argument unless the value is passed with "=", in which case '
                              'it is used as environment variable value'))
    parser.add_argument('--tests-image',
                        metavar='image',
                        help=('Docker image to use for the tests container. '
                              'When passed, tests container is used for tests and not the current directory'))
    advanced_group = parser.add_argument_group('advanced arguments', 'Stuff for StreamSets devs, mostly')
    advanced_group.add_argument('-p', '--publish',
                                action='append',
                                metavar='<ports>',
                                help=("Publish a container’s port(s) to the host. Identical to using -p option in a "
                                      "docker run command"))
    advanced_group.add_argument('--streamsets-sdk-directory',
                                metavar='dir',
                                help=("Path to the an `sdk` folder containing source code of the "
                                      "StreamSets SDK for Python"))
    advanced_group.add_argument('--streamsets-sdk-key-path',
                                metavar='file',
                                help=("Path to the `sdk` key"),
                                default=os.path.join(SDK_USER_CONFIG_PATH, 'activation', SDK_ACTIVATION_FILE_NAME))
    advanced_group.add_argument('--testframework-directory',
                                metavar='dir',
                                help=("A testframework directory to mount into the STF container (for use "
                                      "when making STF changes that don't require a rebuild of the image)"))
    advanced_group.add_argument('--working-directory',
                                metavar='dir',
                                help=("Directory to be used as working directory during execution"),
                                default=os.getcwd())
    advanced_group.add_argument('--docker-config-directory',
                                metavar='dir',
                                help='A directory containing docker configuration to mount into the STF container',
                                default=DEFAULT_DOCKER_CONFIG_DIRECTORY)
    advanced_group.add_argument('--docker-extra-options',
                                metavar='<docker options>',
                                help='Options to be sent directly to the Docker command that will launch the STF',
                                default='')
    subparsers = parser.add_subparsers(help='Test Framework subcommands', dest='subcommand')

    benchmark_subparser = subparsers.add_parser('benchmark', help='Run performance metrics', add_help=False)
    benchmark_subparser.add_argument('benchmark_command', metavar='<test command>',
                                     help='Arguments to pass to benchmark framework',
                                     nargs=argparse.REMAINDER)

    build_subparser = subparsers.add_parser('build',
                                            help='Build STF Docker images',
                                            add_help=False)
    build_subparser.add_argument('build_command', metavar='<build command>',
                                 help='Arguments to pass to the image build script',
                                 nargs=argparse.REMAINDER)

    info_subparser = subparsers.add_parser('info', help='Sub-system info', add_help=False)
    info_subparser.add_argument('info_command', metavar='<info command>',
                                help='Arguments to pass to the info script',
                                nargs=argparse.REMAINDER)

    shell_subparser = subparsers.add_parser('shell', help='Open a shell within the STF container')
    shell_subparser.add_argument('shell_command', metavar='<shell command>',
                                 help='Shell command to execute',
                                 nargs=argparse.REMAINDER)

    start_parser = subparsers.add_parser('start', help='Start a sub-system')
    start_subparser = start_parser.add_subparsers(help='sub-system to start', dest='sub_system')
    start_subparser.required = True
    start_sdc_subparser = start_subparser.add_parser('sdc', help='Start SDC', add_help=False)
    start_st_subparser = start_subparser.add_parser('st', help='Start Transformer', add_help=False)

    stop_parser = subparsers.add_parser('stop', help='Stop a sub-system')
    stop_subparser = stop_parser.add_subparsers(help='sub-system to stop', dest='sub_system')
    stop_subparser.required = True
    stop_sdc_subparser = stop_subparser.add_parser('sdc', help='Stop SDC', add_help=False)
    stop_st_subparser = stop_subparser.add_parser('st', help='Stop Transformer', add_help=False)

    test_stub_parser = subparsers.add_parser('stub', help='Generate a Test Stub', add_help=False)
    test_stub_parser.add_argument('generate_teststub_command', metavar='<generate test stub command>',
                                  help='Arguments to pass to the generate test stub script',
                                  nargs=argparse.REMAINDER)

    test_subparser = subparsers.add_parser('test', help='Run STF tests', add_help=False)
    test_subparser.add_argument('test_command', metavar='<test command>',
                                help='Arguments to pass to our test execution framework',
                                nargs=argparse.REMAINDER)

    args, unknown = parser.parse_known_args()

    # Handle the case of `stf` or `stf -v` kind being run
    if len(sys.argv) == 1 or not args.subcommand:
        parser.print_help(sys.stderr)
        sys.exit(1)

    testframework_config_directory = os.path.realpath(os.path.expanduser(args.testframework_config_directory))
    streamsets_logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    client = docker.from_env()

    docker_image = _pick_docker_image(args.docker_image, args.release) or DEFAULT_DOCKER_IMAGE
    is_3_x = docker_image.split(':')[0].lower() == DOCKER_IMAGE_3_X.split(':')[0].lower()

    _get_or_pull_docker_image(client, docker_image, args.docker_image_dont_pull)
    logger.info('Docker image %s repo SHA is %s', docker_image,
                client.images.get(docker_image).labels.get('com.streamsets.testframework.repo-sha', 'Unknown'))

    ini_parser = configparser.ConfigParser()
    ini_parser.read_string(_read_ini_file(client, docker_image))

    _create_docker_network(client, args.docker_network)

    container_hostname = _get_stf_container_hostname(client)

    environment = {
        'HOST_HOSTNAME': socket.gethostname(),
        'PYTHONDONTWRITEBYTECODE': '1', # Disable creation of troublesome __pycache__ files.
        'TZ': os.readlink('/etc/localtime').split('zoneinfo/')[1], # sync host time zone to docker container
        'TESTFRAMEWORK_CONFIG_DIRECTORY': testframework_config_directory,
    }

    for variable in json.loads(ini_parser.get('DEFAULT', 'HostEnvironmentVariablesToImport')):
        if variable in os.environ:
            environment[variable] = os.getenv(variable)

    env_var_file_path = os.path.join(testframework_config_directory, ENV_VAR_FILENAME)
    os.remove(env_var_file_path) if os.path.exists(env_var_file_path) else None
    if args.env_var:
        env_vars = []
        for env_var in args.env_var:
            if '=' not in env_var and not env_var in os.environ:
                raise ValueError('"{}" passed for --env-var does not exist in environment variables'.format(env_var))

            if '=' in env_var:
                environment[env_var.split('=', 1)[0]] = env_var.split('=', 1)[1]
                env_vars.append(env_var.split('=', 1)[0])
            else:
                environment[env_var] = os.getenv(env_var)
                env_vars.append(env_var)

        with open(env_var_file_path, 'w') as env_file_handle:
            env_file_handle.write(json.dumps(env_vars))

    stf_container_activation_file_path = None
    if is_3_x:
        if not os.path.isfile(args.streamsets_sdk_key_path):
            raise ActivationError(('Could not find SDK activation file for 3.x at {}. Make sure it is present in the '
                                   'directory, or use --streamsets-sdk-key-path for a path '
                                   'to the SDK key').format(args.streamsets_sdk_key_path))
        else:
            stf_container_activation_file_path = os.path.join('/root/.streamsets/activation', SDK_ACTIVATION_FILE_NAME)

    container_configs = {
        'auto_remove': False,
        'detach': True,
        'environment': environment,
        'hostname': container_hostname,
        'network': args.docker_network,
        'volumes': {testframework_config_directory: dict(bind='/etc/testframework', mode='rw'),
                    '/var/run/docker.sock': dict(bind='/var/run/docker.sock', mode='rw'),
                    args.docker_config_directory: dict(bind='/root/.docker', mode='rw')},
        'volumes_from': [],
        'tty': True if sys.stdout.isatty() else False,
        'working_dir': '/root/tests',
    }

    if stf_container_activation_file_path:
        container_configs['volumes'][args.streamsets_sdk_key_path] = dict(bind=stf_container_activation_file_path,
                                                                          mode='ro')

    if args.tests_image:
        docker_tests_image = _get_or_pull_tests_image(client, args.tests_image, args.docker_image_dont_pull)
        container_configs['volumes_from'].append(client.containers.create(docker_tests_image, auto_remove=True).id)
    else:
        container_configs['volumes'][args.working_directory] = dict(bind='/root/tests', mode='rw')

    if args.sdc_resources_directory:
        environment['SDC_RESOURCES_DIRECTORY'] = os.path.realpath(os.path.expanduser(args.sdc_resources_directory))

    if args.testframework_directory:
        container_configs['volumes'][args.testframework_directory] = dict(bind='/root/testframework', mode='rw')

    if args.streamsets_sdk_directory:
        container_configs['volumes'][args.streamsets_sdk_directory] = dict(bind=('/usr/local/lib/python3.7/'
                                                                                 'site-packages/streamsets/sdk'),
                                                                           mode='rw')
        environment['STREAMSETS_SDK_DIRECTORY'] = True

    if args.publish:
        ports = dict()
        for pair in args.publish:
            ports.update({pair.split(':')[1]: pair.split(':')[0]})
        container_configs['ports'] = ports

    if args.subcommand == 'shell':
        shell_command = 'bash' if not args.shell_command else ' '.join('"{}"'.format(arg) for arg in args.shell_command)
        _run_interactive(docker_image, shell_command, container_configs, args.docker_extra_options)
    elif args.subcommand == 'test':
        test_index = sys.argv.index('test')
        shell_command = 'pytest {}'.format(' '.join('"{}"'.format(arg) for arg in sys.argv[test_index+1:]))
        shell_command = shell_command.replace('$', '\$')
        _run_interactive(docker_image, shell_command, container_configs, args.docker_extra_options)
    elif args.subcommand == 'benchmark':
        benchmark_index = sys.argv.index('benchmark')
        command = 'pytest {}'.format(' '.join('"{}"'.format(arg) for arg in sys.argv[benchmark_index+1:]))
        container = client.containers.run(docker_image, command, **container_configs)
        logger.debug('Running command (%s) in STF container (%s) ...', command, container.id)
        for line in container.attach(stream=True):
            sys.stdout.write(line.decode())
    elif args.subcommand == 'build':
        build_index = sys.argv.index('build')
        build_commands = (['-v'] if args.verbose else []) + sys.argv[build_index+1:]
        command = ('python3 {} {}'.format(os.path.join(DOCKER_IMAGE_CLI_DIR, 'build.py'),
                                          ' '.join('"{}"'.format(arg) for arg in build_commands)))
        container = client.containers.run(docker_image, command, **container_configs)
        logger.debug('Running command (%s) in STF container (%s) ...', command, container.id)
        for line in container.attach(stream=True):
            sys.stdout.write(line.decode())
    elif args.subcommand == 'stub':
        stub_index = sys.argv.index('stub')
        stub_commands = (['-v'] if args.verbose else []) + sys.argv[stub_index + 1:]
        command = ('python3 {} {}'.format(os.path.join(DOCKER_IMAGE_CLI_DIR, 'generate_test_stub.py'),
                                          ' '.join('"{}"'.format(arg) for arg in stub_commands)))
        container = client.containers.run(docker_image, command, **container_configs)
        logger.debug('Running command (%s) in STF container (%s) ...', command, container.id)
        for line in container.attach(stream=True):
            sys.stdout.write(line.decode())
    elif args.subcommand == 'start':
        start_commands = sys.argv[sys.argv.index('start')+1:]
        if args.sub_system in ['sdc', 'st']:
            sub_system_command = 'python3 {}'.format(
                os.path.join(DOCKER_IMAGE_CLI_DIR, ('start_sdc.py' if args.sub_system == 'sdc' else 'start_st.py'))
            )
            sub_system_args = ((['-v'] if args.verbose else []) + ['--docker-network', args.docker_network] +
                               start_commands[1:])
            command = ('{} {}'.format(sub_system_command, ' '.join('"{}"'.format(arg) for arg in sub_system_args)))
            container = client.containers.run(docker_image, command, **container_configs)
            logger.debug('Running command (%s) in STF container (%s) ...', command, container.id)
            for line in container.attach(stream=True):
                sys.stdout.write(line.decode())
    elif args.subcommand == 'stop':
        stop_commands = sys.argv[sys.argv.index('stop')+1:]
        if args.sub_system in ['sdc', 'st']:
            sub_system_command = 'python3 {}'.format(
                os.path.join(DOCKER_IMAGE_CLI_DIR, ('stop_sdc.py' if args.sub_system == 'sdc' else 'stop_st.py'))
            )
            sub_system_args = stop_commands[1:]
            command = ('{} {}'.format(sub_system_command, ' '.join('"{}"'.format(arg) for arg in sub_system_args)))
            container = client.containers.run(docker_image, command, **container_configs)
            logger.debug('Running command (%s) in STF container (%s) ...', command, container.id)
            for line in container.attach(stream=True):
                sys.stdout.write(line.decode())
    elif args.subcommand == 'info':
        info_index = sys.argv.index('info')
        info_commands = (['-v'] if args.verbose else []) + sys.argv[info_index+1:]
        shell_command = ('python3 {} {}'.format(os.path.join(DOCKER_IMAGE_CLI_DIR, 'info.py'),
                                                ' '.join('"{}"'.format(arg) for arg in info_commands)))
        _run_interactive(docker_image, shell_command, container_configs, args.docker_extra_options)
    # If a container instance was created, we return its status code.
    if 'container' in locals():
        sys.exit(container.wait()['StatusCode'])


def _run_interactive(docker_image, shell_command, container_configs, extra_options):
    # Helper method to run a docker image in an interactive fashion if possible
    volumes = ' '.join('-v "{}:{}"'.format(k, v['bind']) for k, v in container_configs['volumes'].items())
    volumes_from = ' '.join('--volumes-from {}'.format(id) for id in container_configs['volumes_from'])
    environments = ' '.join('-e {}="{}"'.format(k, (v or '')) for k, v in container_configs['environment'].items())
    interactive = '-i' if sys.stdout.isatty() else ''
    ports = (' '.join(f'-p {v}:{k}' for k, v in container_configs['ports'].items())
             if 'ports' in container_configs.keys()
             else '')
    command = 'docker run {} -t --rm -w {} --net {} -h {} {} {} {} {} {} {} {}'.format(interactive,
                                                                                       container_configs['working_dir'],
                                                                                       container_configs['network'],
                                                                                       container_configs['hostname'],
                                                                                       volumes,
                                                                                       volumes_from,
                                                                                       environments,
                                                                                       ports,
                                                                                       extra_options,
                                                                                       docker_image,
                                                                                       shell_command)
    with subprocess.Popen(command, shell=True) as child:
        child.communicate()
        sys.exit(child.returncode)


def _create_docker_network(client, name):
    # Create network only if they are not default Docker networks
    if name not in ('bridge', 'host', 'none'):
        try:
            client.networks.create(name=name, check_duplicate=True)
            logger.debug('Successfully created network (%s).', name)
        except docker.errors.APIError as api_error:
            if api_error.explanation == 'network with name {} already exists'.format(name):
                logger.debug('Network (%s) already exists. Continuing without creating ...', name)
            else:
                raise


def _get_stf_container_hostname(client):
    # We set the STF container's hostname to match the host's to make the experience of running
    # tests as seamless as if they were being run from the host itself.

    # We need special logic to check whether Docker for Mac is being used and then handling
    # how it exposes ports to 'localhost'.
    docker_hostname = client.info()['Name']
    logger.debug('Docker detected hostname: %s', docker_hostname)

    hostname = subprocess.check_output('hostname', shell=True, universal_newlines=True).strip()
    logger.debug('Shell detected hostname: %s', hostname)

    if docker_hostname == hostname:
        return subprocess.check_output('hostname -f', shell=True, universal_newlines=True).strip()
    elif docker_hostname.startswith('linuxkit') or docker_hostname == 'moby':
        return 'localhost'


def _add_help(parser):
    """Utility method that adds a help argument to whichever parser is passed to it. This is
    needed to correctly handle display of help messages through the various parsers we create
    dynamically at runtime.

    Args:
        parser (:py:obj:`argparse.ArgumentParser`): Parser instance.
    """
    parser.add_argument('-h', '--help',
                        action='help',
                        default=argparse.SUPPRESS,
                        help='show this help message and exit')


def _pick_docker_image(docker_image, release):
    """Utility method to pick docker image.

    Args:
        docker_image (:obj:`str`): Docker image name with tag from args.
        release (obj:`str`): Release option in {'3.x', '4.x'} from args.

    Returns:
        Docker image as an instance of obj:`str`.
    """
    if docker_image and release:
        raise Exception('Both --docker-image and --release cannot be specified at the same time.')

    if release == '4.x':
        return DOCKER_IMAGE_4_X
    elif release == '3.x':
        return DOCKER_IMAGE_3_X

    if docker_image and ':' not in docker_image:
        return '{}:{}'.format(DEFAULT_TESTFRAMEWORK_DOCKER_REPO, docker_image)

    return docker_image


def _read_ini_file(client, docker_image):
    # Utility function to read content of cli.ini file from STF docker image.
    docker_client = docker.APIClient(timeout=DEFAULT_DOCKER_TIMEOUT)
    container_id = docker_client.create_container(image=docker_image)['Id']
    try:
        bits, stat = docker_client.get_archive(container=container_id,
                                               path=os.path.join(DOCKER_IMAGE_CLI_DIR, 'cli.ini'))
        tarstream = io.BytesIO()
        for chunk in bits:
            tarstream.write(chunk)
        tarstream.seek(0)

        with tarfile.open(fileobj=tarstream) as tarfile_:
            for tarinfo in tarfile_.getmembers():
                ini_content = tarfile_.extractfile(tarinfo).read().decode()

        return ini_content
    finally:
        docker_client.remove_container(container=container_id, v=True, force=True)


def _docker_pull_with_retries(client, docker_image, attempts=4, wait=10):
    # Utility function to provide retries for Docker pull operations.
    try:
        return client.images.pull(docker_image)
    except Exception as exc:
        attempts = attempts - 1
        if attempts > 0:
            logger.debug('%s exception while pulling Docker image %s. %s retries left. Retrying in %s seconds ...',
                         type(exc).__name__, docker_image, attempts, wait)
            time.sleep(wait)
            return _docker_pull_with_retries(client, docker_image, attempts, wait*2)
        logger.debug('Retries exhausted. Giving up ...')
        raise exc


def _get_or_pull_docker_image(client, docker_image, docker_image_dont_pull):
    # Utility function to check if Docker image is required to be pulled or not.
    if docker_image_dont_pull:
        try:
            client.images.get(docker_image)
        except docker.errors.ImageNotFound:
            logger.warning('Docker image not found locally. Pulling Docker image %s ...', docker_image)
            _docker_pull_with_retries(client, docker_image)
    else:
        try:
            logger.info('Pulling Docker image %s ...', docker_image)
            _docker_pull_with_retries(client, docker_image)
        except Exception as pull_error:
            try:
                client.images.get(docker_image)
                logger.warning('Unable to pull latest Docker image for %s. Using cached image ...', docker_image)
            except docker.errors.ImageNotFound:
                raise pull_error from None


def _get_or_pull_tests_image(client, tests_image, docker_image_dont_pull):
    # Utility function to check if tests Docker image is required to be pulled or not.
    # Check if tests image is full name form or not. Image full name form is of org/repo:image name
    if ':' in tests_image:
        docker_tests_image_fullname = tests_image
    else:
        docker_tests_image_fullname = '{}:{}'.format(DEFAULT_TESTS_DOCKER_REPO, tests_image)
    _get_or_pull_docker_image(client, docker_tests_image_fullname, docker_image_dont_pull)
    tests_name_label = client.images.get(docker_tests_image_fullname).labels.get(DOCKER_LABEL_TESTS_NAME)
    if not tests_name_label:
        raise ValueError(('Cannot proceed due to missing "{}" label on '
                          'Docker image {}').format(DOCKER_LABEL_TESTS_NAME, docker_tests_image_fullname))
    logger.info('Docker image %s repo SHA is %s', docker_tests_image_fullname,
                client.images.get(docker_tests_image_fullname).labels.get(
                    'com.streamsets.{}.tests.repo-sha'.format(tests_name_label), 'Unknown'))
    return docker_tests_image_fullname


class ActivationError(Exception):
    """Activation error."""
    def __init__(self, reason=None):
        self.reason = reason

    def __str__(self):
        return ('Failed to activate StreamSets SDK'
                'for Python ({}).'.format('reason: {}'.format(self.reason)
                                          if self.reason else 'no reason provided'))
