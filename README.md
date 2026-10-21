# AI Response Quality Evaluator

A small, reproducible **AI evaluation portfolio project** that compares two sample AI responses against explicit prompt instructions and ranks them by compliance.

**Skills:** LLM evaluation · response ranking · rubric-based assessment · instruction following · data quality · Python

## Features

- Evaluates required or prohibited phrases, word limits, response prefixes, and exact line counts
- Scores each response from **0–100** based on proportion of constraints passed
- Compares response A and B, including ties
- Produces auditable per-rule results in JSON
- Includes six synthetic example pairs and four unit tests
- No API key, paid service, or third-party package required

## Run

Requires Python 3.9+.

```bash
python evaluator.py
python -m unittest discover -s tests -v
```

The first command creates `results.json` with scores and per-rule results. For custom datasets:

```bash
python evaluator.py --data data/sample_cases.json --output results.json
```

## Evaluation format

Each case in `data/sample_cases.json` has an ID, prompt, rules, and two candidate responses. Supported rules: `must_include`, `must_not_include`, `max_words`, `starts_with`, and `exact_lines`.

Each rule is equally weighted. The highest-scoring candidate wins; equal scores yield a tie.

## Scope and limitations

**This is a deterministic instruction-following benchmark, not an LLM-powered judge.** The illustrative responses are synthetic, not collected from real models. It does *not* verify factual correctness, helpfulness, or safety; and it does not constitute full RLHF evaluation. Simple substring matching and whitespace word counting have known edge cases. Further work could add human labels, fact-checking, inter-annotator agreement, and a genuine LLM-as-judge component.

Never publish confidential evaluation-platform tasks, private client data, or proprietary AI model outputs.

## Author

**Kolawole Peter Olusola** — AI Evaluation & Data Quality Portfolio

[Portfolio](https://techbykhay.site/) · [LinkedIn](https://www.linkedin.com/in/kolawole-peter-olusola/) · [Behance](https://www.behance.net/kolawolepeter2/)
