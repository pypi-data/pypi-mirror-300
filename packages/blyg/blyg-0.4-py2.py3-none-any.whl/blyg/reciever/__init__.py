import threading
import time
import json
import logging
import hashlib
import base64
import pathlib
from Crypto import Random
from Crypto.Cipher import AES

from ..output import log, stylize_output
from ..shy import ShySDK
from ..x509 import X509

pubkey_database = {}
pending_messages = {}
transfer_keys = {}


class Transfer:
	def __init__(self, token, sdk, path):
		self.token = token
		self.sdk = sdk
		self.fh = None
		self.path = path

	def chunk(self, size=4092):
		if self.fh is None:
			self.fh = self.path.open('rb')

		return self.fh.read(size)

	def store(self, data, position=None):
		print(f"Storing {data} at position {position}")
		if self.fh is None:
			self.fh = self.path.open('wb')

		if position:
			self.fh.seek(position)
		else:
			self.fh.seek(self.path.stat().st_size)

		self.fh.write(data)

	def close(self):
		if self.fh:
			self.fh.close()

		self.fh = None


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


class DownloadWorker(threading.Thread):
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

					if download_path := self.sdk.arguments.path.expanduser().resolve().absolute():
						download_path = download_path / pathlib.Path(decrypted_message['offer']).name

					self.upload_handle = Transfer(token=decrypted_message['token'], sdk=self.sdk, path=download_path)
			elif decrypted_message.get('chunk') and isinstance(self.upload_handle, Transfer) and decrypted_message['token'] == self.upload_handle.token:
				log(f"{message['sender']} sent us a {len(base64.b64decode(decrypted_message['chunk']))} chunk", fg="gray", level=logging.DEBUG)
				self.upload_handle.store(base64.b64decode(decrypted_message['chunk']))
			elif decrypted_message.get('status') == 'complete':
				log(f"Transfer from {stylize_output(str(message['sender']), fg='green')} is now complete: {self.upload_handle.path}", fg="green")
				self.upload_handle.close()

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

				log(f"AES key successfully negotiated with {message['sender']}", fg="gray", level=logging.DEBUG)
		else:
			log(f"Encrypted message had an incorrect signature", fg="red", level=logging.ERROR)

	def recieve_hook(self, websocket, message):
		message = json.loads(message)
		log(f"Received: {message}", fg="gray", level=logging.DEBUG)

		if message.get('status') == 'waiting':
			log(f"Waiting for a file request with root {self.sdk.arguments.path}", fg="gray", level=logging.DEBUG)

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
				log(f"{message['sender']} is trying to transfer something to me", fg="gray", level=logging.DEBUG)
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

		elif message.get('status') == 'pubkey':
			if message['identity'] not in pubkey_database:
				log(f"Recieved public key for {message['identity']}", fg="gray", level=logging.DEBUG)
				pubkey_database[message['identity']] = X509(pubkey=message['pubkey'])

			if message['identity'] in pending_messages:
				log(f"Loading pending messages for {message['identity']}", fg="gray", level=logging.DEBUG)
				while len(pending_messages[message['identity']]):
					stored_message = pending_messages[message['identity']].pop(0)

					if stored_message.get('payload'):
						self.process_rsa_encrypted_message(stored_message)
					else:
						self.process_aes_encrypted_message(stored_message)


		# self.alive = False

	def run(self):
		while self.alive:
			time.sleep(0.025)

		self.sdk.close()

def recieve(args):
	# print(args.config.credentials._x509)
	downloader = DownloadWorker()

	downloader.sdk = ShySDK(
		args,
		downloader.recieve_hook
	)

	if args.config.credentials.identity:
		if not downloader.sdk.validate_identity():
			downloader.sdk.flush_session()

	if not args.config.credentials.identity and downloader.sdk.new_session() is False:
		raise PermissionError(f"Could not open a session against {args.config.general.protocol}://{args.config.general.host}:{args.config.general.port}")

	if not downloader.sdk.connect():
		raise PermissionError(f"Could not open websocket against wss://{args.config.general.host}:{args.config.general.port}")

	downloader.sdk.serve()