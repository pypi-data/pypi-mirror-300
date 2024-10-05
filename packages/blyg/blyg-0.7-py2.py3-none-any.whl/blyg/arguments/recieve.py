import pathlib
from ..args import subparsers
from ..reciever import recieve

# secret = subparsers.add_parser('secret', help='Secret help')
# secret.add_argument('--mode', nargs="?", type=str)

recieve_arguments = subparsers.add_parser("recieve", help="Starts a reciever")
recieve_arguments.add_argument(
	"--path",
	required=True,
	type=pathlib.Path,
	help="Where to store the downloads",
)
recieve_arguments.add_argument("--verbose", action='store_true', help="Enables debug messages")
recieve_arguments.set_defaults(func=recieve)
