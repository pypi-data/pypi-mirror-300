import os
import stat
import toml
import json
import logging

from .args import parser
from .arguments.receive import receive_arguments
from .arguments.upload import upload_arguments
from .config import Configuration, ShyConf, SessionCredentials
from .output import log

def run_as_a_module():
	args, unknowns = parser.parse_known_args()

	args.config = args.config.expanduser().resolve().absolute()

	log_adapter = logging.getLogger('share.blyg.se')
	if args.verbose:
		logging.basicConfig(level=logging.DEBUG, format='%(message)s')
		log_adapter.setLevel(logging.DEBUG)
	else:
		logging.basicConfig(level=logging.INFO, format='%(message)s')
		log_adapter.setLevel(logging.INFO)

	if args.config.parent.exists() is False:
		args.config.parent.mkdir(parents=True, exist_ok=True)

	os.chmod(
	    str(args.config.parent),
	    stat.S_IRUSR |
	    stat.S_IWUSR |
	    stat.S_IXUSR |
	    stat.S_IRGRP |
	    stat.S_IXGRP # |
	    # stat.S_IWGRP |
	    # stat.S_IROTH
	    # stat.S_IXOTH
	)

	if args.config.exists():
		os.chmod(
		    str(args.config),
		    stat.S_IRUSR |
		    stat.S_IWUSR |
		    stat.S_IRGRP # |
		    # stat.S_IWGRP |
		    # stat.S_IROTH
		)

		with args.config.open('r') as fh:
			new_config = Configuration(**toml.load(fh))
			new_config._path = args.config
			args.config = new_config
	else:
		new_config = Configuration(general=ShyConf(), credentials=SessionCredentials())

		with args.config.open('w') as fh:
			toml.dump(
				json.loads(
					new_config.model_dump_json()
				),
				fh
			)

		new_config._path = args.config
		args.config = new_config

	if 'func' in dir(args):
		args.func(args)