"""Deterministic AI response instruction-compliance evaluator."""
import argparse
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent

def evaluate_response(response, rules):
    checks = []
    for rule in rules:
        kind, value = rule["type"], rule["value"]
        if kind == "must_include":
            passed = str(value).casefold() in response.casefold()
        elif kind == "must_not_include":
            passed = str(value).casefold() not in response.casefold()
        elif kind == "max_words":
            passed = len(response.split()) <= int(value)
        elif kind == "starts_with":
            passed = response.lstrip().casefold().startswith(str(value).casefold())
        elif kind == "exact_lines":
            passed = len(response.strip().splitlines()) == int(value)
        else:
            raise ValueError(f"Unknown rule type: {kind}")
        checks.append({"rule": f"{kind}: {value}", "passed": passed})
    score = round(100 * sum(c["passed"] for c in checks) / len(checks), 1) if checks else 0
    return {"score": score, "checks": checks}

def run(cases):
    results = []
    for case in cases:
        evaluations = {label: evaluate_response(case["responses"][label], case["rules"]) for label in ("A", "B")}
        a, b = evaluations["A"]["score"], evaluations["B"]["score"]
        winner = "tie" if a == b else ("A" if a > b else "B")
        results.append({"id": case["id"], "prompt": case["prompt"], "winner": winner, **evaluations})
    return results

def main():
    parser = argparse.ArgumentParser(description="Benchmark instruction-following in AI responses")
    parser.add_argument("--data", type=Path, default=BASE / "data" / "sample_cases.json")
    parser.add_argument("--output", type=Path, default=BASE / "results.json")
    args = parser.parse_args()
    cases = json.loads(args.data.read_text(encoding="utf-8"))
    results = run(cases)
    args.output.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    for item in results:
        print(f'{item["id"]}: A={item["A"]["score"]} B={item["B"]["score"]} winner={item["winner"]}')
    print(f"Saved {len(results)} evaluations to {args.output}")

if __name__ == "__main__":
    main()
