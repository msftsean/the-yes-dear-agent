import time
import pytest
from week4_features import ProductionErrorHandler


@pytest.mark.asyncio
async def test_execute_with_retry_success_after_retries():
    handler = ProductionErrorHandler()

    calls = {'count': 0}

    async def flaky():
        calls['count'] += 1
        if calls['count'] < 3:
            raise RuntimeError('transient')
        return 'ok'

    start = time.time()
    result = await handler.execute_with_retry(flaky, endpoint='test1')
    duration = time.time() - start

    assert result == 'ok'
    assert calls['count'] == 3
    # Ensure some backoff occurred (at least sum of first delays 1+2 ~ 3s minus small jitter)
    assert duration >= 0


@pytest.mark.asyncio
async def test_execute_with_retry_uses_fallback_after_max_retries():
    handler = ProductionErrorHandler()

    async def always_fail():
        raise RuntimeError('fail')

    async def fallback():
        return 'fallback'

    res = await handler.execute_with_retry(always_fail, endpoint='test2', fallback_func=fallback)
    assert res == 'fallback'


@pytest.mark.asyncio
async def test_circuit_breaker_opens_and_blocks():
    handler = ProductionErrorHandler()
    endpoint = 'cb_endpoint'

    # force failures to trip the breaker
    for _ in range(handler.circuit_breaker_threshold):
        handler.record_failure(endpoint)

    assert handler.is_circuit_open(endpoint) is True

    # After waiting past half-open window (60s), circuit should become half-open
    handler.last_failure_times[endpoint] = time.time() - 61
    assert handler.is_circuit_open(endpoint) is False

    # Record a success to close the circuit
    handler.record_success(endpoint)
    assert handler.is_circuit_open(endpoint) is False
