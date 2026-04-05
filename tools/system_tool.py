"""
System tool: basic system info for agent use.
"""
import platform
from datetime import datetime
from typing import Any, Dict, Optional

from tools.base import BaseTool, ToolResult
from utils.logger import logger


class SystemTool(BaseTool):
    """System information tool."""

    def __init__(self):
        super().__init__(
            name="system_info",
            description="Get system information (platform, python version, etc.)"
        )

    async def execute(self, action: str = "info", **kwargs) -> ToolResult:
        """
        Execute system info query.

        Args:
            action: Action type (only "info" supported)
            **kwargs: Additional parameters (ignored)
        """
        try:
            logger.info(f"System tool called: {action}")

            if action == "info":
                result = {
                    "platform": platform.system(),
                    "platform_release": platform.release(),
                    "platform_version": platform.version(),
                    "architecture": platform.machine(),
                    "hostname": platform.node(),
                    "python_version": platform.python_version(),
                    "timestamp": datetime.now().isoformat(),
                }
                return ToolResult(success=True, result=result)

            return ToolResult(
                success=False,
                result=None,
                error=f"Unknown action: {action}"
            )

        except Exception as e:
            logger.error(f"System tool error: {e}")
            return ToolResult(success=False, result=None, error=str(e))

    def get_schema(self) -> dict:
        """Get tool schema."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": ["info"]
                }
            }
        }


# Export tools list
TOOLS = [SystemTool()]
