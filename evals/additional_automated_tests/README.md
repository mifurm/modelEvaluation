# Additional Automated Tests - Runbook

This folder contains standalone scripts for each test so you can run them directly.

## Prerequisites

1. Run from workspace root: `/Users/furman/Dev/evals`
2. Python 3.10+ available
3. Install required packages:

```bash
/usr/local/bin/python3 -m pip install pandas openai
```

Optional packages for other evaluation files in this repo:

```bash
/usr/local/bin/python3 -m pip install azure-ai-evaluation mlflow
```

For test 05 (live latency and token usage), define Foundry vars in `.env`:

- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_DEPLOYMENT`
- Optional: `AZURE_OPENAI_API_VERSION`

## Run Each Test

```bash
/usr/local/bin/python3 evals/additional_automated_tests/scripts/01_rule_based_risk_trigger_scan.py
/usr/local/bin/python3 evals/additional_automated_tests/scripts/02_control_to_metric_coverage_gate.py
/usr/local/bin/python3 evals/additional_automated_tests/scripts/03_representativeness_floor_checks.py
/usr/local/bin/python3 evals/additional_automated_tests/scripts/04_safety_severity_distribution_gate.py
/usr/local/bin/python3 evals/additional_automated_tests/scripts/05_latency_and_token_cost_check.py
/usr/local/bin/python3 evals/additional_automated_tests/scripts/06_canary_secret_leakage_probe.py
/usr/local/bin/python3 evals/additional_automated_tests/scripts/07_counterfactual_pair_disparity_test.py
/usr/local/bin/python3 evals/additional_automated_tests/scripts/08_artifact_integrity_hashing.py
/usr/local/bin/python3 evals/additional_automated_tests/scripts/09_reviewer_policy_consistency_audit.py
/usr/local/bin/python3 evals/additional_automated_tests/scripts/10_rolling_zscore_drift_alarm.py
/usr/local/bin/python3 evals/additional_automated_tests/scripts/11_documentation_completeness_checker.py
/usr/local/bin/python3 evals/additional_automated_tests/scripts/12_conformity_checklist_validator.py
```

## Notes

- Test 03 default minimum samples per group is `2` for seed data. Override with:

```bash
MIN_SAMPLES_PER_GROUP=50 /usr/local/bin/python3 evals/additional_automated_tests/scripts/03_representativeness_floor_checks.py
```

- Test 05 requires live access to your Foundry deployment and valid credentials.
