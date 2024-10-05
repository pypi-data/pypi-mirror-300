# IBM Confidential
# PID 5900-BAF
# Copyright StreamSets Inc., an IBM Company 2024

import argparse
import json
import logging
import os
import sys
from urllib.parse import urlparse

from tabulate import tabulate

from streamsets.sdk import ControlHub
from streamsets.testframework.arguments import add_run_profiles_arguments_to_parser
from streamsets.testframework.cli.run_profile_manager import create_run_profile_manager
from streamsets.testframework import logger as streamsets_logger
from streamsets.testframework.constants import DEFAULT_DOCKER_NETWORK, STF_TESTCONFIG_DIR
from streamsets.testframework.sdc import get_data_collector_info
from streamsets.testframework.st import get_transformer_info
from streamsets.testframework.utils import product_version_is_valid

# Get rid of handlers on the root logger to avoid duplicate output (see STF-959).
logging.getLogger().handlers.clear()

logger = logging.getLogger('streamsets.testframework.cli.info')

INFO_SYSTEM_RUN_PROFILES = 'run_profiles'
INFO_SYSTEM_SDC = 'sdc'
INFO_SYSTEM_TRANSFORMER = 'transformer'
# Note: names sensitive to other systems using it (e.g. STE)
INFO_FILE_NAME_SUFFIX = 'system_info.json'
SDC_SYSTEM_INFO_FILE_NAME = f'datacollector_{INFO_FILE_NAME_SUFFIX}'
SDC_SYSTEM_INFO_FILE_PATH = os.path.join(STF_TESTCONFIG_DIR, SDC_SYSTEM_INFO_FILE_NAME)
TRANSFORMER_SYSTEM_INFO_FILE_NAME = f'transformer_{INFO_FILE_NAME_SUFFIX}'
TRANSFORMER_SYSTEM_INFO_FILE_PATH = os.path.join(STF_TESTCONFIG_DIR, TRANSFORMER_SYSTEM_INFO_FILE_NAME)


def _main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     epilog="Run 'stf info <command> -h' for more information.")
    parser.add_argument('-a', '--always-pull', action='store_true',
                        help='Always pull new Docker images for StreamSets product')
    parser.add_argument('--docker-network', metavar='network', default=DEFAULT_DOCKER_NETWORK,
                        help='Docker network to use for StreamSets product')
    parser.add_argument('-v', '--verbose', action='store_true', help='Be noisier')
    subparsers = parser.add_subparsers(help='StreamSets product to use for info', dest='subcommand')

    sdc_parser = subparsers.add_parser(INFO_SYSTEM_SDC, help='StreamSets DataCollector info')
    sdc_ver_url_group = sdc_parser.add_mutually_exclusive_group(required=True)
    sdc_ver_url_group.add_argument('--server-url',
                                   help=('URL of existing StreamSets Data Collector server to get info from. '
                                         'Arg is mutually exclusive with --version'),
                                   metavar='url')
    sdc_ver_url_group.add_argument('--version',
                                   help=('StreamSets Data Collector version to use to get info from. This can be a '
                                         '<version> or Git hash as in git:<hash> format'),
                                   metavar='ver')

    transformer_parser = subparsers.add_parser(INFO_SYSTEM_TRANSFORMER, help='Transformer info')
    transformer_ver_url_group = transformer_parser.add_argument_group()
    transformer_ver_url_group.add_argument('--server-url',
                                           help=('URL of existing StreamSets Transformer server to get info from. '
                                                 'Arg is mutually exclusive with --version'),
                                           metavar='url')
    transformer_ver_url_group.add_argument('--version',
                                           help=('StreamSets Transformer version to use to get info from. '
                                                 'This can be a <version> or Git hash as in git:<hash> format'),
                                           metavar='ver')
    transformer_ver_url_group.add_argument('--scala-version',
                                           help='Scala version used in Transformer')
    run_profiles_parser = subparsers.add_parser(INFO_SYSTEM_RUN_PROFILES, help='Run Profiles info')
    run_profiles_group = run_profiles_parser.add_mutually_exclusive_group(required=True)
    run_profiles_group.add_argument('--list-run-elements',
                                    action='store_true',
                                    help=('List all run elements available for use and exit. Can be filtered with the '
                                          '`--run-element` argument.'))
    run_profiles_group.add_argument('--list-run-profiles',
                                    action='store_true',
                                    help=('List all run profiles available for use and exit.'))
    run_profiles_parser = add_run_profiles_arguments_to_parser(run_profiles_parser)

    sch_group = subparsers.add_parser('SCH options')
    sch_group.add_argument('--sch-credential-id', help='StreamSets Control Hub credential ID')
    sch_group.add_argument('--sch-token', help='StreamSets Control Hub token')
    sch_group.add_argument('--sch-dont-use-websocket-tunneling', action='store_true',
                           help='Do not use WebSocket tunneling for communication with execution engines')

    args = parser.parse_args()

    # Handle the case of `stf info` or `stf info -v` kind being run
    if len(sys.argv) == 1 or not args.subcommand:
        parser.print_help(sys.stderr)
        parser.exit(status=1)

    streamsets_logger.setLevel(logging.DEBUG if args.verbose else logging.INFO)

    if hasattr(args, 'version') and args.version:
        if not product_version_is_valid(args.version):
            raise ValueError('--version arg needs to be a <version> or Git hash in git:<hash> format')

    if args.subcommand == INFO_SYSTEM_SDC:
        logger.info('Getting info for StreamSets Data Collector ...')
        sdc_info = _get_product_info(args, get_data_collector_info)
        logger.info("SDC information:%s%s", os.linesep, json.dumps(sdc_info, indent=4, sort_keys=True))
    elif args.subcommand == INFO_SYSTEM_TRANSFORMER:
        logger.info('Getting info for StreamSets Transformer ...')
        transformer_info = _get_product_info(args, get_transformer_info)
        logger.info("Transformer information:%s%s", os.linesep, json.dumps(transformer_info, indent=4, sort_keys=True))
    elif args.subcommand == INFO_SYSTEM_RUN_PROFILES:

        psuedo_url = urlparse(args.testframework_vault)
        secret_engine, profiles_root = psuedo_url.path[1:].split('/', 1)

        manager = None
        try:
            manager = create_run_profile_manager('{}://{}'.format(psuedo_url.scheme, psuedo_url.netloc),
                                                 secret_engine,
                                                 profiles_root)

            if args.list_run_profiles:
                profile_list = manager.list_profiles()
                print(tabulate([(key, value.description, ', '.join(value.elements))
                                for key, value in profile_list.items()],
                               headers=['Run Profile', 'Description', 'Run Elements'], tablefmt='simple'))

            if args.list_run_elements:
                element_list = manager.list_elements(args.run_element)
                print(tabulate(element_list, headers=['Run Element', 'Description'], tablefmt='simple'))

        except Exception as exception:
            logger.error('Caught exception while trying to create run profile manager: %s', exception)

def _get_product_info(args, info_func):
    control_hub = ControlHub(credential_id=args.sch_credential_id,
                             token=args.sch_token,
                             use_websocket_tunneling=not args.sch_dont_use_websocket_tunneling,
                             aster_url=args.aster_server_url)
    product_args = {'control_hub': control_hub, 'always_pull': args.always_pull,
                    'server_url': args.server_url, 'write_info_file': True}

    if hasattr(args, 'scala_version'):
        product_args.update({'scala_version': args.scala_version})

    if args.version and args.version.startswith('git:'):
        product_args['git_hash'] = args.version[4:]
    else:
        product_args['version'] = args.version
    return info_func(**product_args)


if __name__ == '__main__':
    _main()
