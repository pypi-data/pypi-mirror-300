from typing import Optional

from ..utils.io import generation_logger
from ...utils.transform import clean_dict_null_value

class vLLMLLM:
    def __init__(self, 
                 model):
        self.model = model
        self.tokenizer = self.model.get_tokenizer()
        self.model_name = None
        self.backend = "vLLM"

    @classmethod
    def from_path(cls, 
                  model_path: str):
        from vllm import LLM
        return cls(LLM(model=model_path, trust_remote_code=True))

    def __call__(self, 
                 input_text: str, 
                 max_new_tokens: Optional[int] = None):
        from vllm import SamplingParams
        outputs = self.model.generate([input_text], SamplingParams(**({ "max_tokens": max_new_tokens } if max_new_tokens else {})))
        output_text = outputs[0].outputs[0].text
        return output_text

    @generation_logger
    def generate(self,
                 input_text: str,
                 max_new_tokens: Optional[int] = None,
                 return_logits: Optional[bool] = None,
                 logits_top_k: Optional[int] = 10,
                 stop_strings: Optional[list[str]] = None,
                 config: Optional[dict] = None):
        from vllm import SamplingParams
        sampling_kwargs = {
            "max_tokens": max_new_tokens,
            "logprobs": logits_top_k if return_logits else None,
            "prompt_logprobs": logits_top_k if return_logits else None,
            "stop": stop_strings,
            "repetition_penalty": (config["repetition_penalty"] if "repetition_penalty" in config else None) if config else None,
            "temperature": (config["temperature"] if "temperature" in config else None) if config else None,
            "top_p": (config["top_p"] if "top_p" in config else None) if config else None,
            "top_k": (config["top_k"] if "top_k" in config else None) if config else None,
        }
        outputs = self.model.generate(prompts=[input_text], sampling_params=SamplingParams(**clean_dict_null_value(sampling_kwargs)))

        output_text = outputs[0].outputs[0].text
        full_text = input_text + output_text

        input_id_list = outputs[0].prompt_token_ids
        output_id_list = list(outputs[0].outputs[0].token_ids)
        full_id_list = input_id_list + output_id_list

        full_token_list = [self.tokenizer.decode([token_id]) for token_id in full_id_list]
        input_token_list = full_token_list[:len(input_id_list)]

        logits_list = None
        if return_logits:
            import math
            raw_input_logits_list = outputs[0].prompt_logprobs
            raw_output_logits_list = outputs[0].outputs[0].logprobs
            raw_logits_list = raw_input_logits_list + raw_output_logits_list
    
            logits_list = [{"id": full_id_list[0], "token": full_token_list[0]}]
            for i in range(1, len(full_id_list)):
                token_id = full_id_list[i]
                token = full_token_list[i]
                raw_info_dict = raw_logits_list[i]
                logits = {
                    "id": token_id,
                    "token": token,
                    "pred_id": [None]*logits_top_k,
                    "pred_token": [None]*logits_top_k,
                    # "logits": [],
                    "probs": [None]*logits_top_k,
                    "logprobs": [None]*logits_top_k
                }
                for chosen_token_id in raw_info_dict:
                    raw_info = raw_info_dict[chosen_token_id]
                    rank = raw_info.rank
                    if rank <= logits_top_k:
                        logprob = raw_info.logprob
                        decoded_token = raw_info.decoded_token

                        logits["pred_id"][rank-1] = chosen_token_id
                        logits["pred_token"][rank-1] = decoded_token
                        logits["probs"][rank-1] = round(math.exp(logprob),4)
                        logits["logprobs"][rank-1] = round(logprob,4) if logprob != float("-inf") else None
                logits_list.append(logits)

        generation_output = {"output_text": output_text,
                             "input_id_list": input_id_list,
                             "input_token_list": input_token_list,
                             "input_text": input_text,
                             "full_id_list": full_id_list,
                             "full_token_list": full_token_list,
                             "full_text": full_text,
                             "logits": logits_list
                             }
        return generation_output

    def chat(self, 
             messages: list[dict], 
             max_completion_tokens: Optional[int] = None, 
             logprobs: Optional[bool] = None, 
             top_logprobs: Optional[int] = 10, 
             stop: Optional[list[str]] = None):
        import time
        from vllm import SamplingParams
        sampling_kwargs = {
            "max_tokens": max_completion_tokens,
            "logprobs": top_logprobs if logprobs else None,
            "stop": stop,
        }
        outputs = self.model.chat(messages=messages, sampling_params=SamplingParams(**clean_dict_null_value(sampling_kwargs)))

        openai_logprobs = None
        if logprobs:
            openai_logprobs = []
            for token_prob in outputs[0].outputs[0].logprobs:
                probs = {
                    "token": token_prob[next(iter(token_prob))].decoded_token,
                    "logprob": token_prob[next(iter(token_prob))].logprob,
                    "top_logprobs": [None]*top_logprobs
                }
                for chosen_token_id in token_prob:
                    rank = token_prob[chosen_token_id].rank
                    if rank <= top_logprobs:
                        top_prob = {
                            "token": token_prob[chosen_token_id].decoded_token,
                            "logprob": token_prob[chosen_token_id].logprob
                        }
                        probs["top_logprobs"][rank-1] = top_prob
                openai_logprobs.append(probs)

        choices = []
        choices.append({
            "index": 0,
            "message": {
                "role": "assistant",
                "content": outputs[0].outputs[0].text
            },
            "logprobs": openai_logprobs,
            "finish_reason": outputs[0].outputs[0].finish_reason
        })

        prompt_token_length = len(outputs[0].prompt_token_ids)
        completion_token_length = len(list(outputs[0].outputs[0].token_ids))

        response = {
            "id": f"chatcmpl-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": self.model_name,
            "choices": choices,
            "usage": {
                "prompt_tokens": prompt_token_length,
                "completion_tokens": completion_token_length,
                "total_tokens": prompt_token_length + completion_token_length
            }
        }
        return response
    
    def tokenize(self, 
                 input_text: str) -> list[int]:
        return self.tokenizer.encode(input_text)
    
    def detokenize(self, 
                   input_ids: list[int],
                   skip_special_tokens: Optional[bool] = True) -> str:
        return self.tokenizer.decode(input_ids, 
                                     skip_special_tokens=skip_special_tokens,
                                     clean_up_tokenization_spaces=False)