import requests

class Server:

	def __init__(self, server_url: str = "https://ppc.tecsci.com.br/api/v1.0") -> None:
		self.server_url = server_url
		self.token = None
		self.response = None

	def login(self) -> bool:
		try:
			response = requests.post(
				self.server_url + "/auth/login",
				headers={'Content-Type': 'application/json'},
				json={'username': 'gustavo.elias', 'password': '12345678'}
				)
			self.token = response.json().get("access_token")
			return True
		except Exception as e:
			print(e)
			return False

	def get_request(self, endpoint, params=None):
		return requests.get(
			self.server_url + "/" + endpoint,
			headers= {"Authorization": f"Bearer {self.token}"},
			params = params
			).json()

	def post_request(self, endpoint, data=None):
		response =  requests.post(
			self.server_url + "/" + endpoint,
			json=data,
			headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json", }
			)
		print(response.status_code)
		if (response.status_code != 201):
			print(response.json())

server = Server()
server.login()