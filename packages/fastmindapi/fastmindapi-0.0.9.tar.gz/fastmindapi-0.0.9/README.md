# FastMindAPI

![PyPI - Version](https://img.shields.io/pypi/v/fastmindapi?style=flat-square&color=red) ![GitHub License](https://img.shields.io/github/license/fairyshine/FastMindAPI?style=flat-square&color=yellow) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/fairyshine/FastMindAPI?style=flat-square&color=green) ![PyPI - Downloads](https://img.shields.io/pypi/dm/fastmindapi?style=flat-square&color=blue)

An easy-to-use, high-performance(?) backend for serving LLMs and other AI models, built on FastAPI.

## ✨ 1 Features

### 1.1 Model: Support models with various backends

- ✅  [Transformers](https://github.com/huggingface/transformers)
  - `Transformers_CausalLM` ( `AutoModelForCausalLM`)
  - `Peft_CausalLM` ( `PeftModelForCausalLM` )
- ✅  [llama.cpp](https://github.com/abetlen/llama-cpp-python)
  - `Llamacpp_LLM` (`Llama`)
- ✅  [OpenAI](https://platform.openai.com/docs/api-reference/introduction)
  - `OpenAI_ChatModel` (`/chat/completions`)
- ✅  [vllm](https://github.com/vllm-project/vllm)
  - `vLLM_LLM`(`LLM`)

- [MLC LLM](https://llm.mlc.ai)
- ...

### 1.2 Modules: More than just chatting with models

- Function Calling (extra tools in Python)
- Retrieval
- Agent
- ...

### 1.3 Flexibility: Easy to Use & Highly Customizable

- Load the model when coding / runtime
- Add any APIs you want

## 🚀 2 Quick Start

### 2.1 Installation

```shell
pip install fastmindapi
```

### 2.2 Usage (*C/S*)

#### 2.2.1 Run the server (*S*)

##### in Terminal

```shell
fastmindapi-server --port 8000 --apikey sk-19992001
```

##### in Python
```Python
import fastmindapi as FM

# Run the server with authentication key, port 8000 for default
server = FM.Server(API_KEY="sk-19992001")
server.run()
```

#### 2.2.2 Access the service (*C*)

##### via client

```shell
# For concise documention
curl http://IP:PORT/docs#/

# Use Case
# 1. add model info
curl http://127.0.0.1:8000/model/add_info \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-19992001" \
  -d '{
  "model_name": "gemma2",
  "model_type": "Transformers_CausalLM",
  "model_path": ".../PTM/gemma-2-2b"
}'

# 2. load model
curl http://127.0.0.1:8000/model/load/gemma2 -H "Authorization: Bearer sk-19992001"

# 3. run model inference
# 3.1 Generation API
curl http://127.0.0.1:8000/model/generate/gemma2 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-19992001" \
  -d '{
  "input_text": "Do you know something about Dota2?",
  "max_new_tokens": 100,
  "return_logits": true,
  "logits_top_k": 10,
  "stop_strings": ["\n"]
}'

# 3.2 OpenAI like API
curl http://127.0.0.1:8000/openai/chat/completions 
	-H "Content-Type: application/json" \
	-H "Authorization: Bearer sk-19992001" \
	-d '{
  "model": "gemma2",
  "messages": [
    {
      "role": "system",
      "content": "You are a test assistant."
    },
    {
      "role": "user",
      "content": "Do you know something about Dota2?"
    }
  ],
  "max_completion_tokens": 100,
  "logprobs": true,
  "top_logprobs": 10,
  "stop": ["\n"]
}'
```

##### via HTTP requests
```python
import fastmindapi as FM

# 127.0.0.1:8000 for default address
client = FM.Client(IP="x.x.x.x", PORT=xxx, API_KEY="sk-19992001") 

# 1. add model info
model_info_list = [
  {
    "model_name": "gemma2",
    "model_type": "Transformers_CausalLM",
    "model_path": ".../PTM/gemma-2-2b"
  },
]
client.add_model_info_list(model_info_list)

# 2. load model
client.load_model("gemma2")

# 3. run model inference
generation_request={
  "input_text": "Do you know something about Dota2?",
  "max_new_tokens": 10,
  "return_logits": True,
  "logits_top_k": 10,
  "stop_strings": ["."]
}
client.generate("gemma2", generation_request)
```

> 🪧 **We primarily maintain the backend server; the client is provided for reference only.** The main usage is through sending HTTP requests. (We might release FM-GUI in the future.)

