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

database:
  provider: "postgres"
  dsn: "postgresql://username:password@127.0.0.1:5432/postgres"
  embed_dim: 1536
```