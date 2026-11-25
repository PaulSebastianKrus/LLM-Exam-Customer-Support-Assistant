from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from src.config import Settings
from src.ollama_client import OllamaClient, OllamaError
from src.prompts import SYSTEM_PROMPT, build_revision_prompt, build_user_prompt
from src.quality import review_draft
from src.rag import RagIndex, SearchResult, select_relevant_results


st.set_page_config(page_title="AcmeFlow Support Assistant", page_icon="💬", layout="wide")


@st.cache_resource
def load_index(path: str) -> tuple[RagIndex, str]:
    return RagIndex.load(Path(path))


def retrieve(
    client: OllamaClient,
    index: RagIndex,
    embed_model: str,
    query: str,
    top_k: int,
    min_score: float,
    max_score_gap: float,
) -> tuple[list[SearchResult], list[SearchResult]]:
    query_embedding = client.embed(embed_model, [query])[0]
    all_results = index.search(query_embedding, top_k=top_k)
    accepted = select_relevant_results(all_results, min_score, max_score_gap)
    return accepted, all_results


def generate_reviewed_draft(
    client: OllamaClient,
    model: str,
    ticket_text: str,
    user_prompt: str,
) -> tuple[str, list[str], bool]:
    """Generate once, then make one correction pass if deterministic checks fail."""
    draft = client.chat(model, SYSTEM_PROMPT, user_prompt)
    warnings = review_draft(ticket_text, draft)
    if not warnings:
        return draft, [], False

    revised = client.chat(
        model,
        SYSTEM_PROMPT,
        build_revision_prompt(user_prompt, draft, warnings),
    )
    return revised, review_draft(ticket_text, revised), True


settings = Settings()
client = OllamaClient(settings.ollama_base_url)

st.title("AcmeFlow Customer Support Assistant")
st.caption("A local LLM drafts customer replies from retrieved product documentation and policies.")

with st.sidebar:
    st.header("RAG settings")
    top_k = st.slider("Retrieved chunks", min_value=1, max_value=8, value=settings.top_k)
    min_score = st.slider(
        "Minimum similarity",
        min_value=0.0,
        max_value=1.0,
        value=settings.min_score,
        step=0.01,
    )
    max_score_gap = st.slider(
        "Maximum score gap from best match",
        min_value=0.01,
        max_value=0.30,
        value=settings.max_score_gap,
        step=0.01,
        help="Removes weak chunks even when they pass the absolute similarity threshold.",
    )
    comparison_mode = st.checkbox(
        "Also generate a no-RAG comparison",
        value=False,
        help="Makes a second local LLM call without project documentation for the exam demonstration.",
    )
    st.divider()
    st.write(f"Chat model: `{settings.chat_model}`")
    st.write(f"Embedding model: `{settings.embed_model}`")

try:
    index, indexed_model = load_index(str(settings.index_path))
except FileNotFoundError:
    st.error(
        "The RAG index has not been built. Start Ollama, install the configured embedding model, "
        "then run `python scripts/build_index.py`."
    )
    st.stop()

if indexed_model != settings.embed_model:
    st.error(
        f"The index uses `{indexed_model}`, but the app is configured for `{settings.embed_model}`. "
        "Rebuild the index or update the configuration."
    )
    st.stop()

with st.form("ticket_form"):
    subject = st.text_input("Ticket subject", placeholder="Charged after cancelling my annual plan")
    message = st.text_area(
        "Customer message",
        height=180,
        placeholder=(
            "Hi, my Team plan renewed yesterday for €144. I meant to cancel it. "
            "Can I receive a refund?"
        ),
    )
    submitted = st.form_submit_button("Draft support reply", type="primary")

if submitted:
    if not message.strip():
        st.warning("Enter a customer message first.")
        st.stop()

    query = f"{subject}\n{message}"
    try:
        accepted_results, raw_results = retrieve(
            client,
            index,
            settings.embed_model,
            query,
            top_k,
            min_score,
            max_score_gap,
        )
    except (OllamaError, ValueError) as exc:
        st.error(str(exc))
        st.stop()

    st.subheader("Retrieved evidence")
    if accepted_results:
        for result in accepted_results:
            with st.expander(
                f"{result.chunk.source} — {result.chunk.heading} · score {result.score:.3f}"
            ):
                st.write(result.chunk.text)
    else:
        best_score = raw_results[0].score if raw_results else 0.0
        st.warning(
            f"No evidence passed the similarity threshold. Best score: {best_score:.3f}. "
            "The ticket should be escalated instead of receiving a policy answer."
        )

    if accepted_results:
        current_date = datetime.now(ZoneInfo(settings.app_timezone)).date().isoformat()
        try:
            with st.spinner("The local model is drafting a grounded reply..."):
                grounded_prompt = build_user_prompt(
                        subject,
                        message,
                        accepted_results,
                        current_date,
                        settings.app_timezone,
                    )
                grounded, draft_warnings, was_revised = generate_reviewed_draft(
                    client,
                    settings.chat_model,
                    query,
                    grounded_prompt,
                )
            st.subheader("RAG-grounded draft")
            st.markdown(grounded)

            if was_revised:
                st.caption("The first draft triggered a quality check and was automatically revised once.")
            if draft_warnings:
                st.warning("Human review flags:\n\n- " + "\n- ".join(draft_warnings))

            if comparison_mode:
                with st.spinner("Generating the no-RAG comparison..."):
                    baseline_prompt = build_user_prompt(
                        subject,
                        message,
                        [],
                        current_date,
                        settings.app_timezone,
                    )
                    baseline, baseline_warnings, baseline_revised = generate_reviewed_draft(
                        client,
                        settings.chat_model,
                        query,
                        baseline_prompt,
                    )
                st.subheader("No-RAG comparison")
                st.markdown(baseline)
                if baseline_revised:
                    st.caption(
                        "The first no-RAG draft triggered the same quality check and was revised once."
                    )
                if baseline_warnings:
                    st.warning(
                        "No-RAG human review flags:\n\n- " + "\n- ".join(baseline_warnings)
                    )
                st.caption(
                    "Compare exact policy details, unsupported promises, uncertainty, and citations."
                )
        except OllamaError as exc:
            st.error(str(exc))
