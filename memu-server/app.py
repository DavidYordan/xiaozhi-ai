import sys
import logging
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
try:
    import yaml
except Exception as e:
    raise RuntimeError("pyyaml_required") from e

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MEMU_SRC = PROJECT_ROOT / "memU" / "src"
if MEMU_SRC.exists():
    sys.path.insert(0, str(MEMU_SRC))
    for k in list(sys.modules.keys()):
        if k.startswith("memu"):
            m = sys.modules.get(k)
            f = getattr(m, "__file__", "") if m else ""
            if f and str(MEMU_SRC) not in f:
                del sys.modules[k]

from memu.app import MemoryService


class MemorizeReq(BaseModel):
    resource_url: str
    modality: str
    summary_prompt: str | None = None


class RetrieveReq(BaseModel):
    queries: list[dict]


def build_service() -> MemoryService:
    cfg_path = Path(__file__).parent / "config.yaml"
    if not cfg_path.exists():
        raise RuntimeError("config_yaml_missing")
    raw = cfg_path.read_text(encoding="utf-8")
    cfg = yaml.safe_load(raw) or {}

    llm = dict(cfg.get("llm", {}))
    api_key = str(llm.get("api_key", "")).strip()
    if not api_key:
        raise RuntimeError("api_key_missing")
    base_url = str(llm.get("base_url", "https://api.deepseek.com")).strip()
    provider = str(llm.get("provider", "deepseek")).strip()
    chat_model = str(llm.get("chat_model", "deepseek-chat")).strip()
    embed_model = str(llm.get("embed_model", "deepseek-embedding")).strip()
    client_backend = str(llm.get("client_backend", "httpx")).strip()
    endpoint_overrides = dict(llm.get("endpoint_overrides", {}))

    server = dict(cfg.get("server", {}))
    resources_dir = str(server.get("resources_dir", str(PROJECT_ROOT / "data" / "resources")))
    retrieve_method = str(server.get("retrieve_method", "rag"))
    top_k = int(server.get("top_k", 5))

    llm_cfg: dict[str, Any] = {
        "api_key": api_key,
        "client_backend": client_backend,
        "base_url": base_url,
        "provider": provider,
        "chat_model": chat_model,
        "embed_model": embed_model,
        "endpoint_overrides": endpoint_overrides,
    }

    blob_cfg = {"resources_dir": resources_dir}
    db_cfg = {"provider": "memory"}
    retrieve_cfg = {"method": retrieve_method, "top_k": top_k}

    return MemoryService(
        llm_config=llm_cfg,
        blob_config=blob_cfg,
        database_config=db_cfg,
        retrieve_config=retrieve_cfg,
    )


app = FastAPI()
service = build_service()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/memorize")
async def memorize(req: MemorizeReq):
    try:
        return await service.memorize(
            resource_url=req.resource_url,
            modality=req.modality,
            summary_prompt=req.summary_prompt,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    try:
        import uvicorn
    except Exception as e:
        raise RuntimeError("uvicorn_required") from e
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")
    uvicorn.run(app, host="localhost", port=8765, log_level="info")


@app.post("/retrieve")
async def retrieve(req: RetrieveReq):
    try:
        return await service.retrieve(queries=req.queries)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
