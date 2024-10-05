import pathlib
from ..args import subparsers
from ..receiver import receive

# secret = subparsers.add_parser('secret', help='Secret help')
# secret.add_argument('--mode', nargs="?", type=str)

receive_arguments = subparsers.add_parser("receive", help="Starts a receiver")
receive_arguments.add_argument(
	"--path",
	required=True,
	type=pathlib.Path,
	help="Where to store the downloads",
)
receive_arguments.add_argument("--verbose", action='store_true', help="Enables debug messages")
receive_arguments.set_defaults(func=receive)
