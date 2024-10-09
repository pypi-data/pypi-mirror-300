import math

def convert_openai_logprobs(logprobs):
    logprobs = logprobs.model_dump()
    logits_list = []
    for token_info in logprobs["content"]:
        logits = {
            "token": token_info["token"],
            "pred_token": [],
            # "logits": [],
            "probs": [],
            "logprobs": []
        }
        for predict_info in token_info["top_logprobs"]:
            logits["pred_token"].append(predict_info["token"])
            logits["logprobs"].append(round(predict_info["logprob"],4))
            logits["probs"].append(round(math.exp(predict_info["logprob"]),4))
        logits_list.append(logits)
    return logits_list