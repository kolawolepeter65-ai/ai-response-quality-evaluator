"""AI Response Quality Evaluator: deterministic checks and optional Gemini judge."""
import streamlit as st
from evaluator import evaluate_response
from ai_judge import judge_responses, CRITERIA

st.set_page_config(page_title="AI Response Quality Evaluator", page_icon="🧪", layout="wide")
st.title("🧪 AI Response Quality Evaluator")
st.caption("Compare two candidate AI responses. Choose auditable rules or an AI-assisted qualitative review.")

mode = st.radio("Evaluation mode", ["Rule-based checks (no key needed)", "AI Judge (Gemini API key required)"], horizontal=True)
prompt = st.text_area("Original prompt", "Explain RLHF in 20 words or fewer. Include the word feedback.")
left, right = st.columns(2)
with left:
    response_a = st.text_area("Response A", "RLHF uses human feedback to train models toward preferred behaviors.", height=170)
with right:
    response_b = st.text_area("Response B", "Reinforcement learning from human preferences trains artificial intelligence systems by incorporating collected preferences from human evaluators.", height=170)

if mode.startswith("Rule-based"):
    st.subheader("Evaluation rules")
    c1, c2 = st.columns(2)
    with c1:
        required = st.text_input("Required word or phrase", "feedback")
        max_words = st.number_input("Maximum words (0 = disabled)", min_value=0, value=20, step=1)
    with c2:
        prohibited = st.text_input("Prohibited word or phrase (optional)", "")
        prefix = st.text_input("Must start with (optional)", "")
    if st.button("Evaluate responses", type="primary"):
        rules = []
        if required.strip(): rules.append({"type": "must_include", "value": required.strip()})
        if max_words: rules.append({"type": "max_words", "value": int(max_words)})
        if prohibited.strip(): rules.append({"type": "must_not_include", "value": prohibited.strip()})
        if prefix.strip(): rules.append({"type": "starts_with", "value": prefix.strip()})
        if not rules:
            st.warning("Select at least one evaluation rule.")
        else:
            a, b = evaluate_response(response_a, rules), evaluate_response(response_b, rules)
            x, y = st.columns(2)
            x.metric("Response A", f'{a["score"]:.1f}/100')
            y.metric("Response B", f'{b["score"]:.1f}/100')
            if a["score"] == b["score"]: st.info("Result: Tie")
            else: st.success(f'Response {"A" if a["score"] > b["score"] else "B"} follows more selected rules.')
            st.dataframe([{"Rule": ai["rule"], "A": "Pass" if ai["passed"] else "Fail", "B": "Pass" if bi["passed"] else "Fail"} for ai, bi in zip(a["checks"], b["checks"])], use_container_width=True, hide_index=True)
            st.caption("Rule compliance is not the same as factual accuracy.")
else:
    st.subheader("AI-assisted evaluation")
    st.info("An LLM provides subjective rubric scores. It does not independently verify sources or guarantee accurate judgments.")
    api_key = st.text_input("Your Gemini API key", type="password", help="Do not paste API keys into GitHub, README files, or screenshots.")
    st.caption("The key is used for this evaluation request and is not intentionally saved by this app. API provider terms and billing apply. Never submit confidential project data.")
    if st.button("Ask AI to evaluate", type="primary"):
        if not api_key.strip():
            st.warning("Enter your Gemini API key to use the AI Judge.")
        else:
            try:
                with st.spinner("Evaluating responses..."):
                    result = judge_responses(prompt, response_a, response_b, api_key.strip())
                st.subheader(f'Preferred response: {result["winner"]}')
                st.write(result["reason"])
                st.dataframe([{"Criterion": k.replace("_", " ").title(), "A": result["scores"]["A"][k], "B": result["scores"]["B"][k]} for k in CRITERIA], hide_index=True, use_container_width=True)
                st.caption("Scores are 1–5; this is an AI opinion, not independently confirmed ground truth.")
            except Exception:
                st.error("The AI evaluation could not be completed. Check your API key, model access, quota, and network connection.")
