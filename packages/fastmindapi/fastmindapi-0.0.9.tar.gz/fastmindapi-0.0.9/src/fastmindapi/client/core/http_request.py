import json
import requests
    
class HTTPRequest:
    def __init__(self, address: str):
        self.address = address

    def get(self, route: str, headers: dict={}):
        url = f"http://{self.address}{route}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是 200，将引发 HTTPError
        return response.json()  # 假设返回的是 JSON 数据


    def post(self, route: str, headers: dict={"Content-Type": "application/json"}, data: dict={}):
        url = f"http://{self.address}{route}"
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # 如果响应状态码不是 200，将引发 HTTPError
        return response.json()  # 假设返回的是 JSON 数据

