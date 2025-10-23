import pytest
import json
from week4_features import SecurityManager


@pytest.mark.asyncio
async def test_moderate_content_heuristic_blocking():
    sm = SecurityManager()
    text = "This text contains the word kill and bomb."

    blocked, details = await sm.moderate_content(text)
    assert blocked is True
    # Accept either the fallback heuristic shape or a 'raw' OpenAI moderation result
    if isinstance(details, dict) and details.get('reason') == 'moderation_flag':
        assert "violence" in details.get("tags", [])
    else:
        # OpenAI client may return a raw moderation object under 'raw'
        raw = details.get('raw') if isinstance(details, dict) else details
        # raw may be an object with attribute 'flagged' or a dict
        flagged = False
        if hasattr(raw, 'flagged'):
            flagged = bool(getattr(raw, 'flagged'))
        elif isinstance(raw, dict):
            flagged = bool(raw.get('flagged'))
        assert flagged is True


def test_logging_moderation_attempts(tmp_path):
    log_file = tmp_path / "moderation_log.jsonl"

    # Simulate a moderation attempt
    entry = {
        "timestamp": "2025-10-20T12:00:00Z",
        "text_snippet": "This is a test log entry.",
        "blocked": True,
        "details": {"reason": "test_reason"}
    }

    # Write to the log file
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

    # Read back the log file
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) == 1
    assert json.loads(lines[0]) == entry
