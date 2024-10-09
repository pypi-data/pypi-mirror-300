from typing import Optional
from pydantic import BaseModel, ConfigDict
from fastapi import APIRouter, Request

PREFIX = "/model"

class BasicModel(BaseModel):
    model_name: str
    model_type: str
    model_path: Optional[str] = None
    model_foundation: Optional[str] = None # for Peft Model

    model_config = ConfigDict(protected_namespaces=())

class GenerationConfig(BaseModel):
    do_sample: Optional[bool] = None
    temperature: Optional[float] = float('nan')
    top_k: Optional[int] = None
    top_p: Optional[float] = float('nan')
    repetition_penalty: Optional[float] = float('nan')

class GenerationRequest(BaseModel):
    input_text: str
    max_new_tokens: Optional[int] = None
    return_logits: Optional[bool] = None
    logits_top_k: Optional[int] = None
    stop_strings: Optional[list[str]] = None
    config: Optional[GenerationConfig] = None

    model_config=ConfigDict(protected_namespaces=())

class EncodeRequest(BaseModel):
    input_text: str

class DecodeRequest(BaseModel):
    input_ids: list[int]
    skip_special_tokens: Optional[bool] = None

def add_model_info(request: Request, item: BasicModel):
    server = request.app.state.server
    if item.model_name in server.module["model"].available_models:
        server.logger.info(item.model_name+" is already listed in [available_models].")
        if server.module["model"].available_models[item.model_name]["model_type"] != item.model_type:
            server.logger.info("Updating model type: "+server.module["model"].available_models[item.model_name]["model_type"]+" -> "+item.model_type+".")
            server.module["model"].available_models[item.model_name]["model_type"] = item.model_type
        if server.module["model"].available_models[item.model_name]["model_path"] != item.model_path:
            server.logger.info("Updating model path: "+server.module["model"].available_models[item.model_name]["model_path"]+" -> "+item.model_path+".")
            server.module["model"].available_models[item.model_name]["model_path"] = item.model_path
    else:
        server.module["model"].available_models[item.model_name] = {
            "model_type": item.model_type,
            "model_path": item.model_path
            }
    if item.model_foundation is not None:
        server.module["model"].available_models[item.model_name]["model_foundation"] = item.model_foundation
    return True

def load_model(request: Request, model_name: str):
    server = request.app.state.server
    try:
        server.module["model"].load_model_from_path(model_name)
        return True
    except Exception as e:
        return "【Error】: "+str(e)

def unload_model(request: Request, model_name: str):
    server = request.app.state.server
    if model_name in server.module["model"].loaded_models:
        del server.module["model"].loaded_models[model_name]
        return f"{model_name} is released successfully."
    else:
        return f"{model_name} is not loaded right now."

def simple_generate(request: Request, model_name: str, item: GenerationRequest):
    server = request.app.state.server
    output_text = server.module["model"].loaded_models[model_name](**item.model_dump(exclude_none=True))
    return output_text

def generate(request: Request, model_name: str, item: GenerationRequest):
    server = request.app.state.server
    try:
        assert model_name in server.module["model"].loaded_models
    except AssertionError:
        return f"【Error】: {model_name} is not loaded."

    # input = item.model_dump(exclude_none=True)
    # if item.config:
    #     config = item.config.model_dump(exclude_none=True)
    #     input["config"] = config
    outputs = server.module["model"].loaded_models[model_name].generate(**item.model_dump(exclude_none=True))
    return outputs

def tokenize(request: Request, model_name: str, item: EncodeRequest):
    server = request.app.state.server
    return server.module["model"].loaded_models[model_name].tokenize(**item.model_dump(exclude_none=True))

def detokenize(request: Request, model_name: str, item: DecodeRequest):
    server = request.app.state.server
    return server.module["model"].loaded_models[model_name].detokenize(**item.model_dump(exclude_none=True))

def get_model_router():
    router = APIRouter(prefix=PREFIX)

    router.add_api_route("/add_info", add_model_info, methods=["POST"])
    router.add_api_route("/load/{model_name}", load_model, methods=["GET"])
    router.add_api_route("/unload/{model_name}", unload_model, methods=["GET"])
    router.add_api_route("/call/{model_name}", simple_generate, methods=["POST"])
    router.add_api_route("/generate/{model_name}", generate, methods=["POST"])
    router.add_api_route("/tokenize/{model_name}", tokenize, methods=["POST"])
    router.add_api_route("/detokenize/{model_name}", detokenize, methods=["POST"])
    return router