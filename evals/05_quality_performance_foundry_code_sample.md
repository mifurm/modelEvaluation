# 5. Quality and Performance Evaluation - Foundry Code Sample

## Automation status
Automatable through Foundry evaluators.

```python
import os
from azure.ai.evaluation import (
    CoherenceEvaluator,
    FluencyEvaluator,
    GroundednessEvaluator,
    RelevanceEvaluator,
    evaluate,
)

model_config = {
    "azure_endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
    "api_key": os.environ["AZURE_OPENAI_API_KEY"],
    "deployment": os.environ["AZURE_OPENAI_DEPLOYMENT"],
}

result = evaluate(
    data="data/05_quality_eval.jsonl",
    evaluators={
        "coherence": CoherenceEvaluator(),
        "fluency": FluencyEvaluator(),
        "relevance": RelevanceEvaluator(),
        "groundedness": GroundednessEvaluator(),
    },
    model_config=model_config,
    output_path="outputs/05_quality_results.json",
)

metrics = result["metrics"]
print(metrics)

if metrics["relevance"] < 3.5 or metrics["groundedness"] < 3.0:
    raise SystemExit("Quality gate failed")
```

## Additional automatable approach
### Latency and cost quality correlation

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

