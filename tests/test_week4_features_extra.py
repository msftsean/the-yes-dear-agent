
from week4_features import CostOptimizer, ProductionErrorHandler, ProductionChecklist


def test_cost_optimizer_cache_and_clear():
    co = CostOptimizer()
    co.cache_response('q1', {'text': 'resp1'})
    cached = co.get_cached_response('q1')
    assert cached is not None
    co.clear_cache()
    assert co.get_cached_response('q1') is None


def test_error_handler_retry_success():
    peh = ProductionErrorHandler()
    state = {'attempts': 0}

    def flaky():
        state['attempts'] += 1
        if state['attempts'] < 3:
            raise Exception('fail')
        return 'ok'

    import asyncio

    result = asyncio.run(peh.execute_with_retry(flaky, endpoint='testretry'))
    assert result == 'ok'


def test_production_checklist_structure():
    pc = ProductionChecklist()
    res = pc.run_all_checks()
    assert 'score' in res
    assert 'results' in res
