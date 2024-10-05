import importlib
import sys
import pathlib

# Load .git version before the builtin version
if pathlib.Path('./blyg/__init__.py').absolute().exists():
	spec = importlib.util.spec_from_file_location("blyg", "./blyg/__init__.py")

	if spec is None or spec.loader is None:
		raise ValueError('Could not retrieve spec from file: blyg/__init__.py')

	blyg = importlib.util.module_from_spec(spec)
	sys.modules["blyg"] = blyg
	spec.loader.exec_module(blyg)
else:
	# Use the installed name
	import blyg

if __name__ == '__main__':
	blyg.run_as_a_module()