import pathlib
import argparse

parser = argparse.ArgumentParser(description="A set of common parameters for shy share cli", add_help=False)

parser.add_argument("--config", nargs="?", help="Which config to load, defaults to ~/.config/blyg/share.toml", default=pathlib.Path("~/.config/blyg/share.toml"), type=pathlib.Path)
parser.add_argument("--verbose", action='store_true', help="Enables debug messages")

subparsers = parser.add_subparsers(help='Modules')