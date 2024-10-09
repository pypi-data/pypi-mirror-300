from pydantic import BaseModel, ConfigDict

class GenerationRequest(BaseModel):
    input_text: str
    max_new_tokens: int = None
    return_logits: bool = False
    logits_top_k: int = 10
    stop_strings: list[str] = None

    model_config=ConfigDict(protected_namespaces=())
