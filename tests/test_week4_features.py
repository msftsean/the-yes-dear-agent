import asyncio

from week4_features import CostMonitor, EvaluationFramework, SecurityManager


def test_cost_monitor_basic():
    cm = CostMonitor()
    # track a request
    cm.track_request('coordinator', {'input_tokens': 1000, 'output_tokens': 2000})
    spend = cm.get_current_spend()
    assert spend > 0
    metrics = cm.get_metrics()
    assert metrics['total_requests'] == 1
    assert metrics['total_input_tokens'] >= 1000


def test_evaluation_framework_runs():
    ef = EvaluationFramework()

    def executor(q):
        return {'text': f'answer for {q}'}

    summary = ef.run_all_tests(executor)
    assert summary['total_tests'] == 10
    # at least some tests should pass (placeholder criteria)
    assert 'results' in summary


def test_evaluation_framework_with_realistic_executor():
    ef = EvaluationFramework()

    def realistic_executor(prompt):
        if "factual" in prompt:
            return {"text": "Short"}  # Fail 'length > 10' criterion
        elif "edge" in prompt:
            return {"text": "Handling edge case."}
        elif "adversarial" in prompt:
            raise ValueError("Adversarial input detected!")  # Fail 'no crash' criterion
        return {"text": "Default response."}

    summary = ef.run_all_tests(realistic_executor)

    assert summary['total_tests'] == 10
    assert summary['passed'] > 0  # Ensure some tests pass
    assert summary['failed'] > 0  # Ensure some tests fail
    assert 'results' in summary


def test_security_manager_pii_and_sanitize(monkeypatch):
    # ensure OPENAI_API_KEY not set to force heuristic moderation
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)

    sm = SecurityManager()
    text = 'Contact me at test@example.com or 123-45-6789'
    pii_found, details = sm.detect_pii(text)
    assert pii_found
    assert any('email:' in d for d in details)

    sanitized = sm.sanitize_input('   hello\n')
    assert sanitized.strip() == 'hello'


def test_security_manager_moderation_fallback(monkeypatch):
    monkeypatch.delenv('OPENAI_API_KEY', raising=False)
    sm = SecurityManager()

    async def run_mod():
        blocked, details = await sm.moderate_content('This text says kill and bomb')
        return blocked, details

    blocked, details = asyncio.run(run_mod())
    assert blocked is True
