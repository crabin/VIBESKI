"""
Tools router — list vibeski example tools.
"""

from fastapi import APIRouter

from tools.system_tool import TOOLS as SYSTEM_TOOLS
from tools.web_search_tool import TOOLS as WEB_SEARCH_TOOLS
from tools.web_research.page_extract_tool import TOOLS as PAGE_EXTRACT_TOOLS

router = APIRouter(prefix="/api/tools", tags=["Tools"])

_CATEGORIES = [
    ("system", "System Info", SYSTEM_TOOLS),
    ("web_search", "Web Search", WEB_SEARCH_TOOLS),
    ("web_research", "Web Research", PAGE_EXTRACT_TOOLS),
]


@router.get("", summary="List available tools")
async def list_tools():
    """Return all registered vibeski tools grouped by category."""
    categories_out = []
    tools_flat = []

    for cat_id, cat_name, tool_list in _CATEGORIES:
        items = [
            {"name": getattr(t, "name", str(t)), "description": getattr(t, "description", "")}
            for t in tool_list
        ]
        categories_out.append({
            "id": cat_id,
            "name": cat_name,
            "count": len(items),
            "tools": items,
        })
        tools_flat.extend([{**item, "category": cat_name} for item in items])

    return {
        "total": len(tools_flat),
        "categories": categories_out,
        "tools": tools_flat,
    }
