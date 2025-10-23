import time
from week4_features import CostOptimizer


def test_cache_response_and_retrieval():
    optimizer = CostOptimizer()
    query = "What is the capital of France?"
    context = "Geography"
    response = {"text": "Paris"}

    # Cache the response
    optimizer.cache_response(query, response, cost=0.1, context=context)

    # Retrieve the cached response
    cached = optimizer.get_cached_response(query, context)
    assert cached == response


def test_cache_ttl_expiry():
    optimizer = CostOptimizer()
    optimizer.cache_ttl_seconds = 1  # Set TTL to 1 second

    query = "What is the capital of France?"
    context = "Geography"
    response = {"text": "Paris"}

    # Cache the response
    optimizer.cache_response(query, response, cost=0.1, context=context)

    # Ensure the response is retrievable immediately
    cached = optimizer.get_cached_response(query, context)
    assert cached == response

    # Wait for TTL to expire
    time.sleep(1.5)

    # Ensure the cache is expired
    cached = optimizer.get_cached_response(query, context)
    assert cached is None


def test_clear_cache():
    optimizer = CostOptimizer()
    query = "What is the capital of France?"
    context = "Geography"
    response = {"text": "Paris"}

    # Cache the response
    optimizer.cache_response(query, response, cost=0.1, context=context)

    # Clear the cache
    optimizer.clear_cache()

    # Ensure the cache is empty
    cached = optimizer.get_cached_response(query, context)
    assert cached is None
