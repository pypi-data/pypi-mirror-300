import json
import logging
import threading
import time
import os
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

from ..output import log, stylize_output
from ..shy import ShySDK
from ..x509 import X509

pubkey_database = {}
pending_messages = {}
transfer_keys = {}


class Transfer:
	def __init__(self, token, sdk):
		self.token = token
		self.sdk = sdk
		self.fh = None

	def chunk(self, size=4092):
		if self.fh is None:
			self.fh = self.sdk.arguments.path.open('rb')

		return self.fh.read(size)

class AESCipher(object):
	@staticmethod
	def encrypt(data, key :bytes, on_encrypted=None):
		if isinstance(data, dict):
			data = json.dumps(data)

		#data = self._pad(data)
		iv = Random.new().read(AES.block_size)
		cipher = AES.new(key, AES.MODE_GCM, iv)

		encrypted_data, tag = cipher.encrypt_and_digest(data.encode('UTF-8'))

		struct = {
			'data' : base64.b64encode(encrypted_data + tag).decode('UTF-8'),
			'key': base64.b64encode(key).decode('UTF-8'),
			'iv': base64.b64encode(iv).decode('UTF-8')
		}

		if on_encrypted and (response := on_encrypted(struct)):
			struct = response

		return struct

	@staticmethod
	def decrypt(data, key, iv):
		cipher = AES.new(base64.b64decode(key), AES.MODE_GCM, nonce=base64.b64decode(iv))
		e_data = base64.b64decode(data)
		return cipher.decrypt_and_verify(e_data[:-16], e_data[-16:]).decode('UTF-8')

		# return AESCipher._unpad(cipher.decrypt(data[AES.block_size:])).decode('utf-8')

	@staticmethod
	def _pad(s):
		return s + (AES.block_size - len(s) % AES.block_size) * bytes(chr(AES.block_size - len(s) % AES.block_size), 'UTF-8')

	@staticmethod
	def _unpad(s):
		return s[:-ord(s[len(s)-1:])]


class UploadWorker(threading.Thread):
	def __init__(self):
		self._sdk = None
		threading.Thread.__init__(self)
		self.alive = True
		self.upload_handle = None
		self.start()

	@property
	def sdk(self):
		return self._sdk

	@sdk.setter
	def sdk(self, val):
		self._sdk = val

	def process_aes_encrypted_message(self, message):
		signature = message.pop('signature')

		verify_struct = json.dumps(
			message,
			separators=(',', ':'),
			sort_keys=True,
			ensure_ascii=False,
			allow_nan=False
		).encode()

		if pubkey_database[message['sender']].verify_signature(verify_struct, signature):
			log(f"Message was signed correctly by the sender themselves", fg="gray", level=logging.DEBUG)
			decrypted_message = json.loads(AESCipher.decrypt(
				message['transfer']['data'],
				transfer_keys[message['sender']],
				message['transfer']['iv']
			))
			log(f"(decrypted) {decrypted_message}", fg="blue", level=logging.DEBUG)

			if decrypted_message.get('offer'):
				log(f"{stylize_output(str(message['sender']), fg='green')} is offering: {stylize_output(decrypted_message['offer'], fg="green")} {stylize_output('('+str(decrypted_message['size'])+')', fg="gray")}")
				log(f"Do you accept this file transfer?")
				choice = input('Y/n: ').lower().strip()

				if choice == 'y':
					struct = {
						"sender": self.sdk.arguments.config.credentials.identity,
						"recipient": message['sender'],
						"transfer" : AESCipher.encrypt({
								"accept" : decrypted_message['token']
							}, base64.b64decode(transfer_keys[message['sender']])
						)
					}

					self.sdk.sign_payload(struct)
					self.sdk.send(json.dumps(struct))
			elif self.upload_handle and decrypted_message.get('accept') == self.upload_handle:
				log(f"{stylize_output(str(message['sender']), fg='green')} accepted: {stylize_output(self.sdk.arguments.path, fg="green")} {stylize_output('('+str(self.sdk.arguments.path.stat().st_size)+')', fg="gray")}")
				self.upload_handle = Transfer(token=self.upload_handle, sdk=self.sdk)

	def process_rsa_encrypted_message(self, message):
		signature = message.pop('signature')

		verify_struct = json.dumps(
			message,
			separators=(',', ':'),
			sort_keys=True,
			ensure_ascii=False,
			allow_nan=False
		).encode()

		if pubkey_database[message['sender']].verify_signature(verify_struct, signature):
			log(f"Message was signed correctly by the sender themselves", fg="gray", level=logging.DEBUG)
			decrypted_message = json.loads(self.sdk.arguments.config.credentials._x509.decrypt(message['payload']))
			log(f"(decrypted) {decrypted_message}", fg="teal", level=logging.DEBUG)

			if decrypted_message.get('new-aes-key'):
				log(f"Got new AES key from {message['sender']}", fg="gray", level=logging.DEBUG)
				transfer_keys[message['sender']] = decrypted_message['new-aes-key']

				struct = {
					"sender": self.sdk.arguments.config.credentials.identity,
					"recipient": message['sender'],
					"payload" : pubkey_database[message['sender']].encrypt(
						json.dumps({
							"accept-aes-key" : hashlib.sha256(decrypted_message['new-aes-key'].encode()).hexdigest()
						}).encode()
					)
				}

				self.sdk.sign_payload(struct)
				self.sdk.send(json.dumps(struct))
			elif decrypted_message.get('accept-aes-key'):
				log(f"Validating accepted transfer key hash from sender", fg="gray", level=logging.DEBUG)
				if not decrypted_message['accept-aes-key'] == hashlib.sha256(transfer_keys[message['sender']].encode()).hexdigest():
					del transfer_keys[message['sender']]
					raise PermissionError(f"Accepted AES key does not match hashsum of what we agreed on")
				log(f"AES key successfully negotiated with {message['sender']}", fg="gray", level=logging.DEBUG)

	def recieve_hook(self, websocket, message):
		message = json.loads(message)

		log(f"Received: {message}", fg="gray", level=logging.DEBUG)

		if message.get('status') == 'waiting':
			log(f"Requesting public key for {self.sdk.arguments.id}", fg="gray", level=logging.DEBUG)
			struct = {
				"sender": self.sdk.arguments.config.credentials.identity,
				"pubkey": self.sdk.arguments.id
			}
			self.sdk.sign_payload(struct)
			self.sdk.send(json.dumps(struct))

		elif message.get('status') == 'pubkey':
			log(f"Received public key for {message['identity']}", fg="gray", level=logging.DEBUG)
			pubkey_database[message['identity']] = X509(pubkey=message['pubkey'])

			log(f"Negotiating an AES key with {self.sdk.arguments.id}", fg="gray", level=logging.DEBUG)
			transfer_keys[message['identity']] = base64.b64encode(os.urandom(32)).decode()
			struct = {
				"sender": self.sdk.arguments.config.credentials.identity,
				"recipient": self.sdk.arguments.id,
				"payload" : pubkey_database[message['identity']].encrypt(
					json.dumps({
						"new-aes-key" : transfer_keys[message['identity']]
					}).encode()
				)
			}
			self.sdk.sign_payload(struct)
			self.sdk.send(json.dumps(struct))
		elif message.get('recipient') == self.sdk.arguments.config.credentials.identity:
			if message.get('payload'):
				log(f"{message['sender']} is attempting a key exchange with me", fg="gray", level=logging.DEBUG)

				if message['sender'] not in pubkey_database:
					log(f"Requesting public key for {message['sender']}", fg="gray", level=logging.DEBUG)
					struct = {
						"sender": self.sdk.arguments.config.credentials.identity,
						"pubkey": message['sender']
					}
					self.sdk.sign_payload(struct)
					self.sdk.send(json.dumps(struct))
					if message['sender'] not in pending_messages:
						pending_messages[message['sender']] = []

					log(f"Storing encrypted message in queue until we get the public key", fg="gray", level=logging.DEBUG)
					pending_messages[message['sender']].append(message)
				else:
					self.process_rsa_encrypted_message(message)
			elif message.get('transfer'):
				log(f"{message['sender']} has accepted a transfer", fg="gray", level=logging.DEBUG)
				if message['sender'] not in pubkey_database:
					log(f"Requesting public key for {message['sender']}", fg="gray", level=logging.DEBUG)
					struct = {
						"sender": self.sdk.arguments.config.credentials.identity,
						"pubkey": message['sender']
					}
					self.sdk.sign_payload(struct)
					self.sdk.send(json.dumps(struct))
					if message['sender'] not in pending_messages:
						pending_messages[message['sender']] = []

					log(f"Storing encrypted message in queue until we get the public key", fg="gray", level=logging.DEBUG)
					pending_messages[message['sender']].append(message)
				else:
					self.process_aes_encrypted_message(message)
		elif message.get('status') == 'success':
			pass
		else:
			self.alive = False

		if self.sdk.arguments.id in transfer_keys and self.upload_handle is None:
			log(f"Uploading file {self.sdk.arguments.path}", fg="gray", level=logging.DEBUG)
			transfer_token = hashlib.sha512(os.urandom(32)).hexdigest()
			struct = {
				"sender": self.sdk.arguments.config.credentials.identity,
				"recipient": self.sdk.arguments.id,
				"transfer" : AESCipher.encrypt({
						"offer" : self.sdk.arguments.path.name,
						"size" : self.sdk.arguments.path.stat().st_size,
						"token" : transfer_token
					}, base64.b64decode(transfer_keys[self.sdk.arguments.id])
				)
			}

			self.sdk.sign_payload(struct)
			self.sdk.send(json.dumps(struct))

			self.upload_handle = transfer_token

	def run(self):
		while self.alive:
			if isinstance(self.upload_handle, Transfer):
				if chunk := self.upload_handle.chunk():
					struct = {
						"sender": self.sdk.arguments.config.credentials.identity,
						"recipient": self.sdk.arguments.id,
						"transfer" : AESCipher.encrypt({
								"chunk" : base64.b64encode(chunk).decode(),
								"token" : self.upload_handle.token
							}, base64.b64decode(transfer_keys[self.sdk.arguments.id])
						)
					}

					self.sdk.sign_payload(struct)
					self.sdk.send(json.dumps(struct))
				else:
					struct = {
						"sender": self.sdk.arguments.config.credentials.identity,
						"recipient": self.sdk.arguments.id,
						"transfer" : AESCipher.encrypt({
								"status" : "complete",
								"token" : self.upload_handle.token
							}, base64.b64decode(transfer_keys[self.sdk.arguments.id])
						)
					}

					self.sdk.sign_payload(struct)
					self.sdk.send(json.dumps(struct))

					self.upload_handle = None
					del(transfer_keys[self.sdk.arguments.id])
					self.alive = False
			else:
				time.sleep(0.025)

		self.sdk.close()
		log(f"Transfer to {stylize_output(str(self.sdk.arguments.id), fg='green')} is now complete", fg="green")

def upload(args):
	if (absolute_path := args.config._path.expanduser().resolve().absolute()).exists() is False:
		raise FileNotFoundError(f"Could not upload file because it does not exist: {absolute_path}")
	# print(args.config.credentials._x509)
	uploader = UploadWorker()

	uploader.sdk = ShySDK(
		args,
		uploader.recieve_hook
	)

	if args.config.credentials.identity:
		if not uploader.sdk.validate_identity():
			uploader.sdk.flush_session()

	if not args.config.credentials.identity and uploader.sdk.new_session() is False:
		raise PermissionError(f"Could not open a session against {args.config.general.protocol}://{args.config.general.host}:{args.config.general.port}")

	if not uploader.sdk.connect():
		raise PermissionError(f"Could not open websocket against wss://{args.config.general.host}:{args.config.general.port}")

	uploader.sdk.serve()