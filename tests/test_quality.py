from src.quality import review_draft


def test_review_flags_verification_claim() -> None:
    warnings = review_draft(
        "My workspace was deleted.",
        "We have verified your email address and will continue.",
    )

    assert "The draft claims verification was completed." in warnings


def test_review_flags_expiry_claim_from_relative_date() -> None:
    warnings = review_draft(
        "I deleted it on Monday.",
        "The recovery period has expired.",
    )

    assert any("relative date" in warning for warning in warnings)


def test_review_flags_not_expired_claim_from_relative_date() -> None:
    warnings = review_draft(
        "I deleted it on Monday.",
        "The recovery period has not yet passed, but the date is unclear.",
    )

    assert any("relative date" in warning for warning in warnings)
