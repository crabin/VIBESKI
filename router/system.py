"""
System router — system info, config, and status.
"""

import platform
from datetime import datetime
from typing import Optional

import psutil
from fastapi import APIRouter, HTTPException

from router.dependencies import get_db_manager, get_prompt_manager
from router.schemas import (
    SystemInfoResponse,
    SystemConfigResponse,
    SystemStatusResponse,
    CpuInfo,
    MemoryInfo,
    DiskInfo,
    LogLevelResponse,
    SetLogLevelRequest,
    SetApiKeyResponse,
)
from utils.logger import set_log_level, get_runtime_log_level, logger

router = APIRouter(prefix="/api/system", tags=["System"])


@router.get("/info", response_model=SystemInfoResponse, summary="System info")
async def system_info():
    """Get OS, architecture, Python version, etc."""
    try:
        return SystemInfoResponse(
            os_type=platform.system(),
            os_name=platform.system(),
            os_version=platform.version(),
            os_release=platform.release(),
            architecture=platform.machine(),
            processor=platform.processor() or "unknown",
            python_version=platform.python_version(),
            hostname=platform.node(),
            username=platform.os.getlogin() if hasattr(platform.os, 'getlogin') else "unknown",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get system info: {e}")


@router.get("/config", response_model=SystemConfigResponse, summary="LLM/model config")
async def system_config():
    """Return current LLM backend and model config."""
    try:
        from vibeski_config import settings
        return SystemConfigResponse(
            llm_provider=settings.llm_provider,
            ollama_model=settings.ollama_model,
            ollama_base_url=settings.ollama_base_url.rstrip("/") if settings.ollama_base_url else None,
            deepseek_model=getattr(settings, "deepseek_model", None),
            deepseek_base_url=getattr(settings, "deepseek_base_url", None),
            current_provider_model=None,
            current_provider_base_url=None,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get config: {e}")


@router.get("/status", response_model=SystemStatusResponse, summary="System status")
async def system_status():
    """Get CPU, memory, disk real-time status."""
    try:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=0.1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        cpu = CpuInfo(
            count=cpu_count,
            percent=cpu_percent,
            freq_current=cpu_freq.current if cpu_freq else None,
        )

        # Memory
        mem = psutil.virtual_memory()
        memory = MemoryInfo(
            total_gb=round(mem.total / (1024 ** 3), 2),
            used_gb=round(mem.used / (1024 ** 3), 2),
            available_gb=round(mem.available / (1024 ** 3), 2),
            percent=mem.percent,
        )

        # Disk
        disks = []
        for partition in psutil.disk_partitions()[:10]:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disks.append(
                    DiskInfo(
                        device=partition.device,
                        mountpoint=partition.mountpoint,
                        total_gb=round(usage.total / (1024 ** 3), 2),
                        used_gb=round(usage.used / (1024 ** 3), 2),
                        percent=usage.percent,
                    )
                )
            except Exception:
                pass

        return SystemStatusResponse(cpu=cpu, memory=memory, disks=disks)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get system status: {e}")


@router.get("/log-level", response_model=LogLevelResponse, summary="Get log level")
async def get_log_level_config():
    try:
        return LogLevelResponse(level=get_runtime_log_level())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get log level: {e}")


@router.post("/log-level", response_model=SetApiKeyResponse, summary="Set log level")
async def set_log_level_config(body: SetLogLevelRequest):
    try:
        target = (body.level or "").strip().upper()
        if target not in {"DEBUG", "INFO", "WARNING", "ERROR"}:
            return SetApiKeyResponse(success=False, message="Supported levels: DEBUG, INFO, WARNING, ERROR")

        applied = set_log_level(target, console_verbose=True)
        logger.bind(event="log_level").info(f"Log level changed to {applied}")
        return SetApiKeyResponse(success=True, message=f"Log level changed to {applied}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to set log level: {e}")
