"""Verify example tools load from the registry."""


def test_web_search_tool_importable():
    """web_search_tool.py must exist and export a search function."""
    from tools.web_search_tool import search
    import asyncio
    import inspect
    assert inspect.iscoroutinefunction(search)


def test_system_tool_importable():
    """system_tool.py must be importable."""
    import tools.system_tool as st
    assert st is not None


def test_page_extract_tool_importable():
    """web_research/page_extract_tool.py must be importable."""
    import tools.web_research.page_extract_tool as pet
    assert pet is not None
