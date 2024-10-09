from .http_request import HTTPRequest


class Client:
    def __init__(self, IP: str="127.0.0.1", PORT: int=8000, API_KEY: str="sk-anything"):
        self.address = IP + ":" + str(PORT)
        self.request = HTTPRequest(self.address)
        self.api_key = API_KEY

    def add_model_info_list(self, model_info_list: list):
        for model_info in model_info_list:
            response = self.request.post("/model/add_info", data=model_info, headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"})

    def get_model_info(self, model_name: str):
        available_models = self.request.get("/available_models")
        loaded_models = self.request.get("/loaded_models")
        return {"available_models": available_models, "loaded_models": loaded_models}

    def load_model(self, model_name: str):
        response = self.request.get(f"/model/load/{model_name}", headers={"Authorization": f"Bearer {self.api_key}"})

    def unload_model(self, model_name: str):
        response = self.request.get(f"/model/unload/{model_name}", headers={"Authorization": f"Bearer {self.api_key}"})

    def generate(self, model_name: str, data: dict={}):
        response = self.request.post(f"/model/generate/{model_name}", data=data, headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"})
        return response
