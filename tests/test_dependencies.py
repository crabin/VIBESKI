"""Verify dependencies.py has no domain-specific imports."""


def test_no_domain_imports():
    """The module must import cleanly with no domain-specific symbols."""
    import router.dependencies as d
    # Must have these
    assert hasattr(d, "get_db_manager")
    assert hasattr(d, "get_prompt_manager")
    assert hasattr(d, "get_agent")
    assert hasattr(d, "get_session_id")
    # Must NOT have these
    assert not hasattr(d, "get_defense_manager")
    assert not hasattr(d, "get_main_controller")
    assert not hasattr(d, "get_os_controller")
    assert not hasattr(d, "get_os_detector")
    assert not hasattr(d, "get_agents")
