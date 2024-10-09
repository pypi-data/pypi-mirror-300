from typing import Optional

from pydantic import BaseModel, ConfigDict
from fastapi import APIRouter, Request

PREFIX = "/openai"

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: list[ChatMessage]
    max_completion_tokens: Optional[int] = None
    logprobs: Optional[bool] = None
    top_logprobs: Optional[int] = None
    stop: Optional[list[str]] = None

    model_config=ConfigDict(protected_namespaces=())


def chat_completions(request: Request, item: ChatRequest):
    server = request.app.state.server
    try:
        assert item.model in server.module["model"].loaded_models
    except AssertionError:
        return f"【Error】: {item.model} is not loaded."
    
    chat_params = item.model_dump(exclude_none=True)
    del chat_params["model"]
    outputs = server.module["model"].loaded_models[item.model].chat(**chat_params)
    return outputs

def get_openai_router():
    router = APIRouter(prefix=PREFIX)

    router.add_api_route("/chat/completions", chat_completions, methods=["POST"])
    return router