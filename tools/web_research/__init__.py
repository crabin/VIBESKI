"""
Web research tools.
"""
from tools.web_research.page_extract_tool import PageExtractTool

WEB_RESEARCH_TOOLS = [
    PageExtractTool(),
]

__all__ = [
    "PageExtractTool",
    "WEB_RESEARCH_TOOLS",
]
