import logging
import websocket
import urllib.request
import json

from .output import log

class ShySDK:
	def __init__(self, cli_args, recieve_hook):
		self.socket = None
		self.arguments = cli_args
		self.recieve_hook = recieve_hook

	def sign_payload(self, struct):
		struct['signature'] = self.arguments.config.credentials._x509.sign(
			json.dumps(
				struct,
				separators=(',', ':'),
				sort_keys=True,
				ensure_ascii=False,
				allow_nan=False
			).encode()
		)

	def validate_identity(self):
		log(f"Validating fingerprint: {self.arguments.config.general.protocol}://{self.arguments.config.general.host}:{self.arguments.config.general.port}/v1/session/{self.arguments.config.credentials.fingerprint}/id", fg="gray", level=logging.DEBUG)
		
		struct = {
			"pubkey": self.arguments.config.credentials.pubkey
		}
		self.sign_payload(struct)

		url = f"{self.arguments.config.general.protocol}://{self.arguments.config.general.host}:{self.arguments.config.general.port}/v1/session/{self.arguments.config.credentials.fingerprint}/id"

		# Encode the JSON string to bytes
		payload = json.dumps(struct).encode('utf-8')

		# Create a request object
		req = urllib.request.Request(url, data=payload)

		# Add headers to the request
		req.add_header('Content-Type', 'application/json')
		req.add_header('Content-Length', str(len(payload)))

		# Send the request and receive the response
		try:
			with urllib.request.urlopen(req) as response:
				# Read and decode the response
				result = response.read().decode('utf-8')
		except urllib.error.HTTPError as e:
			log(f'Validation message: {e.read()}', fg="gray", level=logging.DEBUG)
			return False
		except urllib.error.URLError as e:
			log(f'HTTP Error {e.code} - {e.reason}: {e.read()}', fg="red", level=logging.ERROR)
			return False
		
		session_data = json.loads(result)

		if session_data.get('status', None) == 'valid':
			if session_data['session'] != self.arguments.config.credentials.identity:
				self.arguments.config.credentials.identity = session_data['session']
				self.arguments.config.save()

			log(f"Your session ID is: {self.arguments.config.credentials.identity}", fg="green", level=logging.INFO)

			return True

		return False

	def flush_session(self):
		self.arguments.config.credentials.identity = None
		self.arguments.config.save()

	def new_session(self) -> bool:
		log(f"Requesting a new session identity at \"{self.arguments.config.general.protocol}://{self.arguments.config.general.host}:{self.arguments.config.general.port}/v1/register\"", fg="gray", level=logging.DEBUG)
		struct = {
			"pubkey": self.arguments.config.credentials.pubkey
		}
		self.sign_payload(struct)

		url = f"{self.arguments.config.general.protocol}://{self.arguments.config.general.host}:{self.arguments.config.general.port}/v1/register"

		# Encode the JSON string to bytes
		payload = json.dumps(struct).encode('utf-8')

		# Create a request object
		req = urllib.request.Request(url, data=payload)

		# Add headers to the request
		req.add_header('Content-Type', 'application/json')
		req.add_header('Content-Length', str(len(payload)))

		# Send the request and receive the response
		try:
			with urllib.request.urlopen(req) as response:
				# Read and decode the response
				result = response.read().decode('utf-8')
		except urllib.error.HTTPError as e:
			log(f'HTTP Error {e.code} - {e.reason}: {e.read()}', fg="red", level=logging.ERROR)
			return False
		except urllib.error.URLError as e:
			log(f'HTTP Error: {e}', fg="red", level=logging.ERROR)
			return False
		
		session_data = json.loads(result)

		self.arguments.config.credentials.identity = session_data['new-id']
		self.arguments.config.credentials.fingerprint = session_data['fingerprint']

		self.arguments.config.save()

		log(f"Your session ID is: {self.arguments.config.credentials.identity}", fg="green", level=logging.INFO)

		return True

	def connect(self):
		log(f"Establishing connection to \"ws://{self.arguments.config.general.host}:{self.arguments.config.general.port}/v1/broker/connect\"", fg="gray", level=logging.DEBUG)
		self.socket = websocket.WebSocketApp(
			f"wss://{self.arguments.config.general.host}:{self.arguments.config.general.port}/v1/broker/connect",
			on_open=self.on_open,
			on_message=self.recieve_hook,
			on_error=self.on_error,
			on_close=self.on_close
		)

		return True

	def close(self):
		self.socket.close()

	def on_error(self, websocket, error):
		log(f"Socket Error: {error}", fg="red", level=logging.ERROR)

	def on_close(self, websocket, close_status_code, close_msg):
		log("Socket closed", fg="gray", level=logging.DEBUG)

	def on_open(self, websocket):
		log(f"Socket connected successfully", fg="gray", level=logging.DEBUG)
		struct = {
			"sender": self.arguments.config.credentials.identity
		}
		self.sign_payload(struct)
		websocket.send(json.dumps(struct))

	def serve(self):
		log(f"Blocking any other code from executing while WebSocket is active", fg="gray", level=logging.DEBUG)
		self.socket.run_forever()
		log(f"Code unblocked due to socket closure", fg="gray", level=logging.DEBUG)

	def send(self, data :str):
		self.socket.send(data)