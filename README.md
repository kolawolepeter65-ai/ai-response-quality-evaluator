# AI Response Quality Evaluator

[![Python Tests](https://github.com/kolawolepeter65-ai/ai-response-quality-evaluator/actions/workflows/tests.yml/badge.svg)](https://github.com/kolawolepeter65-ai/ai-response-quality-evaluator/actions/workflows/tests.yml)

[**Launch interactive demo**](https://ai-response-quality-evaluator-uteuquyrrjmtj6jjbw5h8z.streamlit.app/)

A reproducible portfolio tool for assessing candidate LLM responses. Two modes:

1. **Rule-based evaluation**: deterministic checks for required phrases, forbidden phrases, word limits, prefixes, and line counts. No API key.
2. **AI Judge**: optional Gemini 2.5 Flash-powered comparative evaluation of **accuracy, relevance, clarity, completeness, and instruction following**, with 1–5 rubric scores and a rationale. Bring your own Gemini API key.

AI-judged results are **subjective model assessments**, not verified facts or human ground truth. The judge may make mistakes, be inconsistent, or exhibit biases. This project does not implement RLHF training, and its example responses are synthetic.

## Run locally

Requires Python 3.9+.

```bash
pip install -r requirements.txt
streamlit run app.py
```

Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey). In AI Judge mode, paste it into the password field (never commit it to GitHub). API pricing, quotas, and provider data handling policies apply.

## CLI benchmark and tests

```bash
python evaluator.py
python -m unittest discover -s tests -v
```

Example comparison pairs live in `data/sample_cases.json`. The CLI writes detailed per-rule scores to `results.json`. Supported checks are `must_include`, `must_not_include`, `max_words`, `starts_with`, `exact_lines`. Each receives equal weight in the deterministic mode.

## Responsible use

- Never upload client secrets, private data, or confidential evaluation-platform tasks.
- Avoid using LLM judge scores as factual verification or as definitive human preference labels.
- An API key entered in the deployed app is sent to Google's Gemini API for the requested inference. This app does not intentionally persist the key. Consider Streamlit host access, Google provider terms, and fees.
- No hidden retrieval or independent external fact-checking is provided.

## Portfolio skills

LLM-as-a-judge · rubric design · response ranking · instruction-following evaluation · validation · Python · Streamlit · API integration · quality assurance

## Author

**Kolawole Peter Olusola**

[Portfolio](https://techbykhay.site/) · [LinkedIn](https://www.linkedin.com/in/kolawole-peter-olusola/) · [Behance](https://www.behance.net/kolawolepeter2/)
