# 05. Latency and Token Cost Check

## Description
Measures runtime latency and token consumption to ensure the model remains operationally viable while maintaining quality targets.

## Code Sample
```python
import os
import time
from statistics import mean

from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-10-21",
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
    t0 = time.perf_counter()
    resp = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    latencies.append(time.perf_counter() - t0)
    tokens.append(resp.usage.total_tokens)

print({
    "latency_avg_s": round(mean(latencies), 3),
    "tokens_avg": round(mean(tokens), 1),
})

if mean(latencies) > 3.0:
    raise SystemExit("Performance gate failed: latency too high")
```
