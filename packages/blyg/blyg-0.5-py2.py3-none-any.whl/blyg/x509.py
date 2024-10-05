import pydantic
import datetime
import cryptography
import logging
import base64
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
try:
	import PyKCS11
except ModuleNotFoundError:
	PyKCS11 = None

from .output import log


class RSAEncryptionError(BaseException):
	pass

class RSADecryptionError(BaseException):
	pass

class RSAInvalidSignature(BaseException):
	pass

class RSAInvalidCertificate(BaseException):
	pass

class NotYetImplemented(BaseException):
	pass


class X509(pydantic.BaseModel):
	pubkey :str
	privkey :str|None = None
	pem_certificate :str|None = None
	ca :str|None = None

	_hsm_session :None = None
	_privkey :None = None
	_pubkey :None = None
	_certificate :None = None
	_ca :None = None

	@pydantic.model_validator(mode='before')
	def pre_validation(cls, data):
		if data['pubkey'] and not any([data.get('privkey'), data.get('pem_certificate')]):
			# We allow loading only a pubkey for encryption and validation reasons
			pass
		elif not any([data.get('privkey'), data.get('pubkey'), data.get('pem_certificate')]):
			if data.get('ca'):
				csr = X509.generate_csr()
				log(f"Please get the CA to sign the generated CSR: {csr}")
				exit(0)
			else:
				data['privkey'], data['pubkey'], data['pem_certificate'] = X509.generate_certificate()

		return data

	@pydantic.model_validator(mode='after')
	def post_validation(self):
		if self.ca:
			self.validate_certificate()

		if self.ca:
			self._ca = cryptography.x509.load_pem_x509_certificate(
				self.ca.encode(),
				cryptography.hazmat.backends.default_backend()
			)

		self._pubkey = serialization.load_pem_public_key(
			self.pubkey.encode()
		)

		if self.privkey:
			self._privkey = serialization.load_pem_private_key(
				self.privkey.encode(),
				password=None, # If the private key is encrypted, provide the password here as bytes: password=b"your_password"
			)

		if self.pem_certificate:
			self._certificate = cryptography.x509.load_pem_x509_certificate(
				self.pem_certificate.encode(),
				cryptography.hazmat.backends.default_backend()
			)

		return self

	@property
	def certificate_authority(self):
		if not self._certificate_authority:
			self._certificate_authority = cryptography.x509.load_pem_x509_certificate(
				self.ca.encode(),
				cryptography.hazmat.backends.default_backend()
			)

		return self._certificate_authority

	@property
	def private_key(self) -> cryptography.hazmat.bindings._rust.openssl.rsa.RSAPrivateKey:
		if not self._privkey:
			self._privkey = cryptography.hazmat.primitives.serialization.load_pem_private_key(
				self.privkey.encode(),
				password=None, # If the private key is encrypted, provide the password here as bytes: password=b"your_password"
			)

		return self._privkey

	@property
	def public_key(self) -> cryptography.hazmat.bindings._rust.openssl.rsa.RSAPublicKey:
		if not self._pubkey:
			self._pubkey = cryptography.hazmat.primitives.serialization.load_pem_public_key(
			self.pubkey.encode()
		)

		return self._pubkey

	@property
	def certificate(self) -> cryptography.hazmat.bindings._rust.x509.Certificate:
		if not self._certificate:
			self._certificate = cryptography.x509.load_pem_x509_certificate(
				self.certificate_data.encode(),
				cryptography.hazmat.backends.default_backend()
			)

		return self._certificate

	def validate_certificate(self):
		ca_public_key = self.certificate_authority.public_key()
		signature = certificate.signature
		tbs_certificate_bytes = self.certificate.tbs_certificate_bytes
		hash_algorithm = self.certificate.signature_hash_algorithm

		try:
			if isinstance(ca_public_key, cryptography.hazmat.bindings._rust.openssl.rsa.RSAPublicKey):
				# Check if the signature algorithm uses PSS
				if certificate.signature_algorithm_oid._name == "RSASSA-PSS":
					padding_scheme = cryptography.hazmat.primitives.asymmetric.padding.PSS(
						mgf=cryptography.hazmat.primitives.asymmetric.padding.MGF1(hash_algorithm),
						salt_length=cryptography.hazmat.primitives.asymmetric.padding.PSS.MAX_LENGTH,
					)
				else:
					padding_scheme = cryptography.hazmat.primitives.asymmetric.padding.PKCS1v15()

				# Verify the signature using RSA public key
				ca_public_key.verify(
					signature,
					tbs_certificate_bytes,
					padding_scheme,
					hash_algorithm,
				)

			elif isinstance(ca_public_key, cryptography.hazmat.bindings._rust.openssl.ec.EllipticCurvePublicKey):
				# ECDSA signatures do not use padding
				ca_public_key.verify(
					signature,
					tbs_certificate_bytes,
					cryptography.hazmat.bindings._rust.openssl.ec.ECDSA(hash_algorithm),
				)

			else:
				raise NotYetImplemented("Unsupported public key type.")

			return True

		except Exception as e:
			raise RSAInvalidCertificate(str(e))

	@staticmethod
	def generate_private_key(keysize=4096):
		return cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key(
			public_exponent=65537, # https://stackoverflow.com/a/45293558/929999
			key_size=keysize,
		)

	@staticmethod
	def generate_certificate(*args, **kwargs):
		log(f"Generating new unique identity for this device", fg="gray", level=logging.DEBUG)
		private_key = X509.generate_private_key(4096)

		# Step 2: Get the public key from the private key
		public_key = private_key.public_key()

		# Optional Step 3: Create a self-signed certificate using x509
		# Define subject and issuer details
		subject = issuer = cryptography.x509.Name([
			cryptography.x509.NameAttribute(cryptography.x509.oid.NameOID.COUNTRY_NAME, kwargs.get('COUNTRY', 'SE')),
			cryptography.x509.NameAttribute(cryptography.x509.oid.NameOID.STATE_OR_PROVINCE_NAME, kwargs.get('STATE', 'Stockholm')),
			cryptography.x509.NameAttribute(cryptography.x509.oid.NameOID.LOCALITY_NAME, kwargs.get('CITY', 'Stockholm')),
			cryptography.x509.NameAttribute(cryptography.x509.oid.NameOID.ORGANIZATION_NAME, kwargs.get('ORGANIZATION', 'ShyShare')),
			cryptography.x509.NameAttribute(cryptography.x509.oid.NameOID.COMMON_NAME, kwargs.get('COMMON_NAME', 'share.blyg.se')),
		])

		# Build the certificate
		certificate = (
			cryptography.x509.CertificateBuilder()
			.subject_name(subject)
			.issuer_name(issuer)
			.public_key(public_key)
			.serial_number(cryptography.x509.random_serial_number())
			.not_valid_before(datetime.datetime.utcnow())
			.not_valid_after(
				# Certificate valid for one year
				datetime.datetime.utcnow() + datetime.timedelta(days=365)
			)
			.sign(private_key, cryptography.hazmat.primitives.hashes.SHA256())
		)

		privkey = private_key.private_bytes(
			encoding=cryptography.hazmat.primitives.serialization.Encoding.PEM,
			format=cryptography.hazmat.primitives.serialization.PrivateFormat.TraditionalOpenSSL,  # or PKCS8
			encryption_algorithm=cryptography.hazmat.primitives.serialization.NoEncryption(),      # or use BestAvailableEncryption(b"your_password")
		).decode()

		pubkey = public_key.public_bytes(
			encoding=cryptography.hazmat.primitives.serialization.Encoding.PEM,
			format=cryptography.hazmat.primitives.serialization.PublicFormat.SubjectPublicKeyInfo,
		).decode()

		certificate_data = certificate.public_bytes(
			cryptography.hazmat.primitives.serialization.Encoding.PEM
		).decode()

		log(f"A new device ID has been generated", fg="green")

		return privkey, pubkey, certificate_data

	@staticmethod
	def generate_csr(*args, **kwargs):
		csr_subject = cryptography.x509.Name([
			cryptography.x509.NameAttribute(cryptography.x509.oid.NameOID.COUNTRY_NAME, kwargs.get('COUNTRY', 'SE')),
			cryptography.x509.NameAttribute(cryptography.x509.oid.NameOID.STATE_OR_PROVINCE_NAME, kwargs.get('STATE', 'Stockholm')),
			cryptography.x509.NameAttribute(cryptography.x509.oid.NameOID.LOCALITY_NAME, kwargs.get('CITY', 'Stockholm')),
			cryptography.x509.NameAttribute(cryptography.x509.oid.NameOID.ORGANIZATION_NAME, kwargs.get('ORGANIZATION', 'ShyShare')),
			cryptography.x509.NameAttribute(cryptography.x509.oid.NameOID.COMMON_NAME, kwargs.get('COMMON_NAME', 'share.blyg.se')),
		])

		csr_builder = cryptography.x509.CertificateSigningRequestBuilder()
		csr_builder = csr_builder.subject_name(csr_subject)

		# Optional Step 3: Add extensions (e.g., Subject Alternative Names)
		if 'subjectAltNames' in kwargs:
			csr_builder = csr_builder.add_extension(
				cryptography.x509.SubjectAlternativeName([
					cryptography.x509.DNSName(altname)
					for altname in kwargs['subjectAltNames']
					# TODO: Support IP addresses
				]),
				critical=False  # Set to True if you want the extension to be marked as critical
			)

		# Optional: Add more extensions as needed
		# For example, Key Usage extension
		csr_builder = csr_builder.add_extension(
			cryptography.x509.KeyUsage(
				digital_signature=True,
				content_commitment=False,
				key_encipherment=True,
				data_encipherment=False,
				key_agreement=False,
				key_cert_sign=False,
				crl_sign=False,
				encipher_only=False,
				decipher_only=False,
			),
			critical=True
		)

		# Step 4: Sign the CSR with the private key
		csr = csr_builder.sign(
			private_key,
			cryptography.hazmat.primitives.hashes.SHA256(),
		)

		return csr.public_bytes(cryptography.hazmat.primitives.serialization.Encoding.PEM)

	def sign(self, data :bytes, base64_encode=True, urlsafe=False):
		if PyKCS11 is not None and self._hsm_session and isinstance(self.private_key, PyKCS11.CK_OBJECT_HANDLE):
			result = bytes(
				self._hsm_session.sign(
					self.private_key,
					data,
					PyKCS11.RSA_PSS_Mechanism(PyKCS11.CKM_SHA256_RSA_PKCS_PSS, PyKCS11.CKM_SHA256, PyKCS11.CKG_MGF1_SHA256, PyKCS11.LowLevel.CK_RSA_PKCS_PSS_PARAMS_LENGTH)
				)
			)
		else:
			result = self.private_key.sign(
				data,
				cryptography.hazmat.primitives.asymmetric.padding.PSS(
					mgf=cryptography.hazmat.primitives.asymmetric.padding.MGF1(cryptography.hazmat.primitives.hashes.SHA256()),
					salt_length=cryptography.hazmat.primitives.asymmetric.padding.PSS.MAX_LENGTH
				),
				cryptography.hazmat.primitives.hashes.SHA256()
			)

		if base64_encode:
			if urlsafe:
				return base64.urlsafe_b64encode(result).decode()
			else:
				return base64.b64encode(result).decode()
		else:
			return result

	def encrypt(self, data :bytes, base64_encode=True, urlsafe=False):
		if encrypted_data := self.public_key.encrypt(
			data,
			cryptography.hazmat.primitives.asymmetric.padding.OAEP(
				mgf=cryptography.hazmat.primitives.asymmetric.padding.MGF1(
					algorithm=cryptography.hazmat.primitives.hashes.SHA256()
				),
				algorithm=cryptography.hazmat.primitives.hashes.SHA256(),
				label=None
			)
		):
			if base64_encode:
				if urlsafe:
					return base64.urlsafe_b64encode(encrypted_data).decode()
				else:
					return base64.b64encode(encrypted_data).decode()
			else:
				return encrypted_data

		raise RSAEncryptionError("Could not encrypt data")

	def decrypt(self, data :bytes|str, base64_decode=True, urlsafe=False):
		if isinstance(data, str):
			if base64_decode:
				if urlsafe:
					data = base64.urlsafe_b64decode(data)
				else:
					data = base64.b64decode(data)
			else:
				data = data.encode()

		try:
			if plaintext := self.private_key.decrypt(
				data,
				cryptography.hazmat.primitives.asymmetric.padding.OAEP(
					mgf=cryptography.hazmat.primitives.asymmetric.padding.MGF1(
						algorithm=cryptography.hazmat.primitives.hashes.SHA256()
					),
					algorithm=cryptography.hazmat.primitives.hashes.SHA256(),
					label=None
				)
			):
				return plaintext
		except ValueError:
			raise RSADecryptionError(f"Could not decrypt RSA data")

	def verify_signature(self, data :str|bytes, signature :str|bytes, base64_decode=True, urlsafe=False):
		if isinstance(data, str):
			if base64_decode:
				if urlsafe:
					data = base64.urlsafe_b64decode(data)
				else:
					data = base64.b64decode(data)
			else:
				data = data.encode()

		if isinstance(signature, str):
			if base64_decode:
				if urlsafe:
					signature = base64.urlsafe_b64decode(signature)
				else:
					signature = base64.b64decode(signature)
			else:
				signature = signature.encode()

		try:
			if self.public_key.verify(
				signature,
				data,
				cryptography.hazmat.primitives.asymmetric.padding.PSS(
					mgf=cryptography.hazmat.primitives.asymmetric.padding.MGF1(cryptography.hazmat.primitives.hashes.SHA256()),
					salt_length=cryptography.hazmat.primitives.asymmetric.padding.PSS.MAX_LENGTH
				),
				cryptography.hazmat.primitives.hashes.SHA256()
			) is None:
				return True
		except cryptography.exceptions.InvalidSignature:
			raise RSAInvalidSignature("Invalid signature, data was not signed by this public key")