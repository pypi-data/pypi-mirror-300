from typing import Optional

from ... import logger
from ..utils.io import generation_logger
from ..utils.transform import convert_openai_logprobs
from ...utils.transform import clean_dict_null_value


class OpenAIChatModel:
    def __init__(self, 
                 client, 
                 model_name: str, 
                 system_prompt: Optional[str] = "You are a helpful assistant."):
        self.client = client
        self.system_prompt = system_prompt
        self.model_name = model_name
        self.backend = "OpenAI"

    @classmethod
    def from_client(cls, 
                    client, 
                    model_name: str):
        return cls(client, model_name)

    def __call__(self, input_text: str, 
                 max_new_tokens: Optional[int] = None):
        try:
            completion = self.client.chat.completions.create(
            model= self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": input_text}
            ],
            **clean_dict_null_value({"max_new_tokens": max_new_tokens})
            )
            return completion.choices[0].message.content
        except Exception as e:
            return "【Error】: " + str(e)

    @generation_logger
    def generate(self,
                 input_text: str,
                 max_new_tokens: Optional[int] = None,
                 return_logits: Optional[bool] = None,
                 logits_top_k: Optional[int] = 10,
                 stop_strings: Optional[list[str]] = None,
                 config: Optional[dict] = None):
        optional_kwargs = {
            "max_tokens": max_new_tokens,
            "logprobs": return_logits,
            "top_logprobs": logits_top_k if return_logits else None,
            "stop": stop_strings,
            "temperature": (config["temperature"] if "temperature" in config else None) if config else None,
            "top_p": (config["top_p"] if "top_p" in config else None) if config else None,
        }
        while True:
            try:
                completion = self.client.chat.completions.create(
                model= self.model_name,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": input_text}
                ],
                **clean_dict_null_value(optional_kwargs)
                )
                break
            except Exception as e:
                logger.info(f"【Error】: {e}")
        output_text = completion.choices[0].message.content
        logits_list = None
        if return_logits:
            logits_list = convert_openai_logprobs(completion.choices[0].logprobs)
        generation_output = {"output_text": output_text,
                            #  "input_id_list": input_id_list,
                            #  "input_token_list": input_token_list,
                             "input_text": input_text,
                            #  "full_id_list": full_id_list,
                            #  "full_token_list": full_token_list,
                            #  "full_text": full_text,
                             "logits": logits_list}
        return generation_output

    def chat(self, 
             messages: list[dict], 
             max_completion_tokens: Optional[int] = None, 
             logprobs: Optional[bool] = None, # Defaults to false
             top_logprobs: Optional[int] = 10, 
             stop: Optional[list[str]] = None):
        optional_kwargs = {"max_tokens": max_completion_tokens,
                           "logprobs": logprobs,
                           "top_logprobs": top_logprobs if logprobs else None,
                           "stop": stop}
        try:
            completion = self.client.chat.completions.create(
            model= self.model_name,
            messages=messages,
            **clean_dict_null_value(optional_kwargs)
            )
            return completion.model_dump()
        except Exception as e:
            return "【Error】: " + str(e)