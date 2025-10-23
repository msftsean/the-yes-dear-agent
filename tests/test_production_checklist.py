from week4_features import ProductionChecklist


def test_run_all_checks():
    checklist = ProductionChecklist()

    # Run all checks
    results = checklist.run_all_checks()

    # Validate results structure
    assert "score" in results
    assert "results" in results
    assert isinstance(results["score"], int)
    assert isinstance(results["results"], dict)

    # Validate individual checks
    for check_name, check_result in results["results"].items():
        assert "ok" in check_result
        assert "message" in check_result


def test_check_tests_placeholder():
    checklist = ProductionChecklist()

    # Validate the placeholder behavior of check_tests
    ok, message = checklist.check_tests()
    assert not ok
    assert message == "No test results available"
