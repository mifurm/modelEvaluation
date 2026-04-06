"""05 - Latency and token cost check.

Runs live calls against Azure OpenAI / Foundry deployment and reports average
latency and token usage.
"""

import os
import time
from pathlib import Path
from statistics import mean

from openai import AzureOpenAI


def load_env_file(path: Path) -> None:
    """Load KEY=VALUE lines from .env without overriding existing env vars."""
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


ROOT = Path(__file__).resolve().parents[3]
load_env_file(ROOT / ".env")

required = ["AZURE_OPENAI_API_KEY", "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_DEPLOYMENT"]
missing = [key for key in required if not os.getenv(key)]
if missing:
    raise SystemExit(f"Missing required environment variables: {missing}")

# Guard against placeholder values from the template .env.
placeholders = {
    "AZURE_OPENAI_API_KEY": {"YOUR_AZURE_OPENAI_API_KEY"},
    "AZURE_OPENAI_ENDPOINT": {"https://YOUR-RESOURCE-NAME.openai.azure.com/"},
    "AZURE_OPENAI_DEPLOYMENT": {"YOUR_MODEL_DEPLOYMENT_NAME"},
}

bad_values = [
    key
    for key, blocked in placeholders.items()
    if os.getenv(key, "").strip() in blocked
]
if bad_values:
    raise SystemExit(
        f"Replace placeholder values in .env before running test 05: {bad_values}"
    )

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
)

deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]
prompts = [
    "Summarize KYC requirements for account closure.",
    "Explain transfer limits for international payments.",
]

latencies = []
tokens = []
for prompt in prompts:
    start = time.perf_counter()
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    latencies.append(time.perf_counter() - start)
    tokens.append(response.usage.total_tokens)

summary = {
    "latency_avg_s": round(mean(latencies), 3),
    "tokens_avg": round(mean(tokens), 1),
}
print(summary)

if summary["latency_avg_s"] > 3.0:
    raise SystemExit("Performance gate failed: latency too high")

print("Latency and token cost check passed")
