"""
Web search tool — DuckDuckGo search with fallback.

Merges the search client (formerly web_search_ddgs.py) with the tool wrapper.
Supports: ddgs (preferred), duckduckgo-search (compat), HTML fallback.
"""
import asyncio
import re
from typing import List, Tuple
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

from utils.logger import logger


def _normalize_result(r: dict) -> dict:
    return {
        "title": r.get("title", ""),
        "url": r.get("href", r.get("link", r.get("url", ""))),
        "snippet": r.get("body", r.get("snippet", "")),
    }


def _search_ddgs_sync(query: str, max_results: int) -> List[dict]:
    from ddgs import DDGS
    return [_normalize_result(r) for r in DDGS().text(query, max_results=max_results)]


def _search_duckduckgo_search_sync(query: str, max_results: int) -> List[dict]:
    from duckduckgo_search import DDGS
    with DDGS() as ddgs:
        return [_normalize_result(r) for r in ddgs.text(query, max_results=max_results)]


def _search_html_sync(query: str, max_results: int) -> List[dict]:
    url = f"https://lite.duckduckgo.com/lite/?q={quote_plus(query)}"
    req = Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (compatible; Vibeski/1.0)")
    with urlopen(req, timeout=15) as resp:
        html = resp.read().decode(errors="ignore")
    results = []
    links = re.findall(r'<a[^>]+rel="nofollow"[^>]+href="([^"]+)"[^>]*>(.+?)</a>', html, re.DOTALL)
    snippets = re.findall(r'<td[^>]*class="result-snippet"[^>]*>(.+?)</td>', html, re.DOTALL)
    for i, (link_url, title) in enumerate(links[:max_results]):
        if link_url.startswith("http"):
            results.append({
                "title": re.sub(r"<[^>]+>", "", title).strip(),
                "url": link_url,
                "snippet": re.sub(r"<[^>]+>", "", snippets[i]).strip() if i < len(snippets) else "",
            })
    return results


async def search(query: str, max_results: int = 5) -> Tuple[List[dict], str]:
    """
    Search DuckDuckGo. Returns (results, engine).
    results: [{title, url, snippet}, ...]
    engine: "ddgs" | "duckduckgo_search" | "duckduckgo_lite"
    """
    loop = asyncio.get_event_loop()
    for fn, engine in [
        (_search_ddgs_sync, "ddgs"),
        (_search_duckduckgo_search_sync, "duckduckgo_search"),
    ]:
        try:
            raw = await loop.run_in_executor(None, fn, query, max_results)
            if raw:
                return raw, engine
        except ImportError:
            pass
        except Exception as e:
            logger.warning(f"Web search [{engine}] failed: {e}")
    raw = await loop.run_in_executor(None, _search_html_sync, query, max_results)
    return raw, "duckduckgo_lite"


TOOLS = []  # Register with registry if desired
