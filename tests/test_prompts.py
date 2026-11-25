from src.prompts import build_user_prompt


def test_prompt_adds_mandatory_constraint_for_relative_date() -> None:
    prompt = build_user_prompt(
        "Restore workspace",
        "I deleted it on Monday.",
        [],
        "2026-11-25",
        "Europe/Copenhagen",
    )

    assert "MANDATORY TEMPORAL CONSTRAINT" in prompt
    assert "Ask the customer for the exact calendar date" in prompt
