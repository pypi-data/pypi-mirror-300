import pathlib
from ..args import subparsers
from ..upload import upload
# secret = subparsers.add_parser('secret', help='Secret help')
# secret.add_argument('--mode', nargs="?", type=str)

upload_arguments = subparsers.add_parser("upload", help="Sends a file to someone")
upload_arguments.add_argument(
	"--path",
	required=True,
	type=pathlib.Path,
	help="Which folder/file to send",
)
upload_arguments.add_argument(
	"--id",
	required=True,
	type=int,
	help="The session ID you will send to",
)
upload_arguments.add_argument("--verbose", action='store_true', help="Enables debug messages")
upload_arguments.set_defaults(func=upload)
