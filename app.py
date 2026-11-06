import re
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Meeting-to-Action Assistant", page_icon="📝", layout="wide")

TASK_VERBS = r"(prepare|create|send|contact|book|arrange|review|complete|submit|share|organize|call|email|update|finish|design|test|deploy|discuss|schedule|confirm|finalize|assign|collect|present|write|check|build|develop|implement)"
OWNER_PATTERNS = [
    re.compile(r"\b([A-Z][a-z]+)\s+(?:will|to)\s+(.+)", re.IGNORECASE),
    re.compile(r"\b([A-Z][a-z]+)\s+(?:is responsible for)\s+(.+)", re.IGNORECASE),
]
DEADLINE_PATTERN = re.compile(
    r"\b(today|tomorrow|tonight|next\s+\w+|by\s+\w+(?:\s+\d{1,2})?|before\s+\w+(?:\s+\d{1,2})?|on\s+\w+(?:\s+\d{1,2})?)\b",
    re.IGNORECASE
)

def clean_sentence(s):
    return re.sub(r"\s+", " ", s).strip(" \t-•")

def split_sentences(text):
    return [clean_sentence(x) for x in re.split(r"(?<=[.!?])\s+|\n+", text) if clean_sentence(x)]

def extract_tasks(sentences):
    tasks = []
    for sentence in sentences:
        owner, action, deadline = "Not specified", sentence, "Not specified"
        owner_found = False
        for pattern in OWNER_PATTERNS:
            match = pattern.search(sentence)
            if match:
                owner = match.group(1).strip()
                action = match.group(2).strip().rstrip(".")
                owner_found = True
                break
        deadline_match = DEADLINE_PATTERN.search(sentence)
        if deadline_match:
            deadline = deadline_match.group(0)
            action = re.sub(re.escape(deadline), "", action, flags=re.IGNORECASE).strip(" ,.")
        action_match = re.search(TASK_VERBS + r"\b.*", action, re.IGNORECASE)
        has_task_verb = bool(action_match)
        has_assignment = owner_found or bool(re.search(r"\b(we will|must|should|need to|action item)\b", sentence, re.IGNORECASE))
        if has_task_verb and has_assignment:
            tasks.append({"Owner": owner, "Task": action, "Deadline": deadline,
                          "Status": "Needs clarification" if owner == "Not specified" or deadline == "Not specified" else "Pending"})
    return tasks

st.title("📝 AI-Powered Meeting-to-Action Assistant")
st.caption("M1-P2 | Rule-based intelligent prototype | No API key required")
st.info("This prototype uses text patterns to extract likely tasks. Review its output because rule-based extraction can miss context or misinterpret wording.")

example = """We will conduct an AI workshop next Friday.
Rahul will prepare the presentation by Thursday.
Priya will contact the participants tomorrow.
The venue is not finalized.
We need to confirm the projector and microphone."""
with st.expander("Load example meeting notes"):
    st.code(example)

transcript = st.text_area("Paste meeting transcript or notes", height=230, placeholder="Paste meeting notes here...")
if st.button("Analyze meeting", type="primary"):
    if not transcript.strip():
        st.error("Please enter meeting notes first.")
    else:
        sentences = split_sentences(transcript)
        lower = transcript.casefold()
        decisions = [s for s in sentences if re.search(r"\b(decided|agreed|approved|will conduct|will organize|confirmed|selected)\b", s, re.IGNORECASE)]
        unresolved = [s for s in sentences if re.search(r"\b(not finalized|not decided|unclear|tbd|to be decided|pending|not confirmed|unsure)\b", s, re.IGNORECASE)]
        tasks = extract_tasks(sentences)

        st.subheader("1. Meeting summary")
        summary_sentences = sentences[:4]
        st.write(" ".join(summary_sentences) if summary_sentences else "No readable sentences were found.")
        if len(sentences) > 4:
            st.caption(f"Showing the first 4 of {len(sentences)} sentences as a concise extractive summary.")

        st.subheader("2. Decisions identified")
        if decisions:
            for d in decisions:
                st.markdown(f"- {d}")
        else:
            st.write("No explicit decision phrases were detected.")

        st.subheader("3. Action items")
        if tasks:
            df = pd.DataFrame(tasks)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.download_button("Download action items (CSV)", df.to_csv(index=False).encode("utf-8"),
                               "meeting_action_items.csv", "text/csv")
        else:
            st.warning("No likely action items were detected. Try notes with clear task verbs and assigned owners.")

        st.subheader("4. Unclear or pending items")
        if unresolved:
            for item in unresolved:
                st.markdown(f"- {item}")
        else:
            st.write("No explicit unresolved phrases were detected.")

        st.subheader("5. Clarification questions")
        questions = []
        for t in tasks:
            if t["Owner"] == "Not specified":
                questions.append(f"Who is responsible for: {t['Task']}?")
            if t["Deadline"] == "Not specified":
                questions.append(f"What is the deadline for: {t['Task']}?")
        for item in unresolved:
            questions.append(f"Can you confirm the status and next action for: {item}?")
        questions = list(dict.fromkeys(questions))
        if questions:
            for q in questions:
                st.markdown(f"- {q}")
        else:
            st.write("No clarification questions were generated by the current rules.")

        st.caption("Limitations: the summary is extractive, task extraction is pattern-based, and date phrases are not converted to calendar dates. Verify all output against the original transcript.")
