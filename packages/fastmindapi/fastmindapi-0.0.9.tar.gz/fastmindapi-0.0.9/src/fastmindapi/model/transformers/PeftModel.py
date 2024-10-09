from .CausalLM import TransformersCausalLM

class PeftCausalLM(TransformersCausalLM):
    def __init__(self, base_model: TransformersCausalLM, 
                 peft_model):
        self.raw_model = base_model.model
        self.tokenizer = base_model.tokenizer
        self.model = peft_model
        self.model_name = None

    @classmethod
    def from_path(cls, base_model: TransformersCausalLM, 
                  model_path: str):
        from peft import PeftModelForCausalLM
        return cls(base_model,
                            PeftModelForCausalLM.from_pretrained(base_model.model,model_path))
