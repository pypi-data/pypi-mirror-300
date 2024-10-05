import toml
import sysconfig
import os
import json
import pathlib
import pydantic
import typing
import cryptography.x509
import cryptography.hazmat.backends
import cryptography.hazmat.bindings
try:
	import PyKCS11
except ModuleNotFoundError:
	PyKCS11 = None

from .jsonify import JSON
from .x509 import X509

try:
	default_pkcs11_lib_path = next(pathlib.Path(sysconfig.get_config_var('LIBDIR')).glob('opensc-pkcs11.so*')) # r"/usr/lib/opensc-pkcs11.so"
except StopIteration:
	default_pkcs11_lib_path = r"/usr/lib/opensc-pkcs11.so"


class SessionCredentials(pydantic.BaseModel):
	identity :int|None = None
	fingerprint :str|None = None
	privkey :str|None = None
	pubkey :str|None = None
	pem_certificate :str|None = None
	_x509 :X509

	@pydantic.model_validator(mode='after')
	def pre_validation(self):
		self._x509 = X509(
			privkey=self.privkey,
			pubkey=self.pubkey,
			pem_certificate=self.pem_certificate
		)

		self.privkey = self._x509.privkey
		self.pubkey = self._x509.pubkey
		self.pem_certificate = self._x509.pem_certificate

		return self


class ShyConf(pydantic.BaseModel, arbitrary_types_allowed=True):
	"""
	The [notAnsible] part of the config.toml config
	"""
	protocol :str = "https"
	host :str = "share.blyg.se"
	port :int = 443
	pkcs11_lib :pathlib.Path = default_pkcs11_lib_path

	@pydantic.field_validator("pkcs11_lib")
	def validate_pkcs11_lib(cls, value):
		if PyKCS11 and not value is None:
			if (value := value.expanduser().resolve().absolute()).exists() is False:
				raise PermissionError(f"Could not locate opensc-pkcs11.lib: {value}")

		return value


class Configuration(pydantic.BaseModel):
	"""
	Defines the sections of config.toml, such as [general] and [credentials].
	These are the valid section headers, and they are define in :class:`ShyConf` and :class:`OPEntry`
	"""
	general :ShyConf
	credentials :SessionCredentials

	_path :pathlib.Path|None = None

	def save(self):
		with self._path.open('w') as fh:
			toml.dump(
				json.loads(
					self.model_dump_json()
				),
				fh
			)