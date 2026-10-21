"""Interactive interface for the deterministic AI response evaluator."""
import streamlit as st
from evaluator import evaluate_response

st.set_page_config(page_title="AI Response Quality Evaluator", page_icon="🧪", layout="wide")
st.title("🧪 AI Response Quality Evaluator")
st.caption("Compare two AI-generated answers using explicit, auditable instruction checks. No API key required.")
st.info("This is a rule-based instruction-following evaluator, not an AI model that judges factual accuracy.")

prompt = st.text_area("Original prompt", "Explain RLHF in 20 words or fewer. Include the word feedback.")
left, right = st.columns(2)
with left:
    response_a = st.text_area("Response A", "RLHF uses human feedback to train models toward preferred behaviors.", height=170)
with right:
    response_b = st.text_area("Response B", "Reinforcement learning from human preferences trains artificial intelligence systems by incorporating collected preferences from human evaluators.", height=170)

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
    if required.strip():
        rules.append({"type": "must_include", "value": required.strip()})
    if max_words:
        rules.append({"type": "max_words", "value": int(max_words)})
    if prohibited.strip():
        rules.append({"type": "must_not_include", "value": prohibited.strip()})
    if prefix.strip():
        rules.append({"type": "starts_with", "value": prefix.strip()})
    if not rules:
        st.warning("Please enable at least one rule.")
    else:
        a = evaluate_response(response_a, rules)
        b = evaluate_response(response_b, rules)
        x, y = st.columns(2)
        x.metric("Response A", f'{a["score"]:.1f}/100')
        y.metric("Response B", f'{b["score"]:.1f}/100')
        if a["score"] == b["score"]:
            st.info("Result: Tie")
        else:
            st.success(f'Result: Response {"A" if a["score"] > b["score"] else "B"} follows more of the selected rules.')
        st.subheader("Rule-by-rule audit")
        st.dataframe([{
            "Rule": a_check["rule"],
            "Response A": "Pass" if a_check["passed"] else "Fail",
            "Response B": "Pass" if b_check["passed"] else "Fail",
        } for a_check, b_check in zip(a["checks"], b["checks"])], use_container_width=True, hide_index=True)
        st.caption("A passing rule does not guarantee factual accuracy, safety, or overall response quality.")
