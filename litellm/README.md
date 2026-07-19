# LiteLLM gateway — deployment

The [gateway](../docs/glossary.md#litellm) that routes the **non-Claude** models. Claude never passes through here (see [`config.yaml`](config.yaml) for why). This directory is everything the Docker server needs.

## What gets deployed where

| Thing | Where it comes from |
|---|---|
| The container image | **Pulled** from `ghcr.io/berriai/litellm:main-stable` — LiteLLM publishes it; nothing is built locally |
| The configuration | [`config.yaml`](config.yaml) in this repo, mounted read-only into the container |
| Hostnames and keys | An untracked `.env` at the repo root (copy [`.env.example`](../.env.example)); never committed |

## Deploy (on the Docker server)

Everything below is a one-time setup on the machine that runs Docker.

```bash
git clone https://github.com/<you>/aidsef.git
cd aidsef
cp .env.example .env
```

Edit `.env` and set three values:

- `AIDSEF_VLLM_BASE` — your inference host, e.g. `http://spark-hostname:8000/v1` (the `/v1` suffix matters)
- `LITELLM_MASTER_KEY` — generate a random secret, e.g. `openssl rand -hex 24`, prefixed `sk-`
- `AIDSEF_LITELLM_URL` — this server's own address, e.g. `http://docker-hostname:4000` (used by the agents, not by the gateway itself)

Then start it:

```bash
cd litellm
docker compose up -d
docker compose logs -f      # watch for "Uvicorn running on ..."
```

## Verify before trusting it

Config files describe intent; only the running service is fact. Check the service, not the file:

```bash
# 1. Is it alive?
curl http://localhost:4000/health/liveliness

# 2. Do the three aliases exist, and do they reach the Spark?
curl -H "Authorization: Bearer $LITELLM_MASTER_KEY" http://localhost:4000/v1/models
```

The second command must list `coder`, `testwriter`, and `docwriter`. If it errors, the gateway can't reach vLLM — check `AIDSEF_VLLM_BASE` and that the Spark is reachable over [Tailscale](../docs/glossary.md#tailscale) from *this* machine.

## Notes

- **Spend logging** is commented out in `config.yaml`. It needs a [Langfuse](https://langfuse.com) instance and its keys in `.env`; without them the callback fails at runtime. Enable it when you want per-role cost telemetry for retros.
- **Updating the config**: `config.yaml` is mounted read-only, so edit it in the repo and run `docker compose restart` — the container reads it at startup.
- **The master key is a real secret.** It grants access to every model behind the gateway. Keep it in `.env` (gitignored) and rotate it if it leaks.
