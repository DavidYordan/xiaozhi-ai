# config.yaml

```
llm:
  provider: deepseek
  base_url: https://api.deepseek.com
  api_key: "YOUR_DEEPSEEK_API_KEY"
  chat_model: deepseek-chat
  embed_model: deepseek-embedding
  client_backend: httpx
  endpoint_overrides: {}

server:
  resources_dir: "./data/resources"
  retrieve_method: "rag"
  top_k: 5
```

```
python -m uvicorn app:app --host 0.0.0.0 --port 8003 --reload
```