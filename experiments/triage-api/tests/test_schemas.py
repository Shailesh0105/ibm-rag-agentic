import pytest
from pydantic import ValidationError

from app.schemas import TriageResult


def test_unknown_category_is_rejected():
    with pytest.raises(ValidationError):
        TriageResult(category="shipping", urgency="low", summary="s", reply_draft="r")
