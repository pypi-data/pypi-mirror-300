from .transformers.CausalLM import TransformersCausalLM
from .transformers.PeftModel import PeftCausalLM
from .llama_cpp.LLM import LlamacppLLM
from .openai.ChatModel import OpenAIChatModel
from .vllm.LLM import vLLMLLM

class ModelModule:
    def __init__(self):
        self.available_models = {}
        self.loaded_models = {}
        self.client = {}

    # TODO rewrite load_model, also in server.core.main
    # def load_model(self, model_name: str, model):
    #     self.loaded_models[model_name] = model

    def load_model_from_path(self, model_name: str):
        '''
        Load the specific model.
        '''
        model_type = self.available_models[model_name]["model_type"]
        model_path = self.available_models[model_name]["model_path"]
        
        # 匹配模型类型
        match model_type:
            case "Transformers_CausalLM":
                self.loaded_models[model_name] = TransformersCausalLM.from_path(model_path)
                self.loaded_models[model_name].model_name = model_name
            case "Peft_CausalLM":
                model_foundation = self.available_models[model_name]["model_foundation"]
                if model_foundation not in self.loaded_models:
                    self.loaded_models[model_foundation] = TransformersCausalLM.from_path(self.available_models[model_foundation]["model_path"])
                base_model = self.loaded_models[model_foundation]
                assert isinstance(base_model, TransformersCausalLM)
                self.loaded_models[model_name] = PeftCausalLM.from_path(base_model, model_path)
                self.loaded_models[model_name].model_name = model_name
            case "Llamacpp_LLM":
                self.loaded_models[model_name] = LlamacppLLM.from_path(model_path)
                self.loaded_models[model_name].model_name = model_name 
            case "OpenAI_ChatModel":
                self.loaded_models[model_name] = OpenAIChatModel.from_client(self.client["OpenAI"], model_name)
                self.loaded_models[model_name].model_name = model_name
            case "vLLM_LLM":
                self.loaded_models[model_name] = vLLMLLM.from_path(model_path)
                self.loaded_models[model_name].model_name = model_name
