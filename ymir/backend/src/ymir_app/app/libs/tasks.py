import aiohttp
import json
from typing import Dict

from fastapi.logger import logger
from fastapi import FastAPI

from app.config import settings


async def post_task_update(payload: Dict) -> Dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "http://127.0.0.1:8088/api/v1/tasks/status", json=payload, headers={"api-key": settings.APP_API_KEY}
        ) as resp:
            resp.raise_for_status()
            return await resp.json()


async def update_task_status(app: FastAPI, msg: str) -> None:
    payload = json.loads(msg)
    namespace = f"/{payload['user_id']}"

    logger.info("update task status via internal endpoint")
    try:
        payload_ = await post_task_update(payload)
    except (aiohttp.ClientError, aiohttp.http_exceptions.HttpProcessingError):
        logger.exception("Failed to post update status with payload %s", payload)
    except Exception:
        logger.exception("Non-aiohttp exception occurred with payload %s", payload)
    else:
        logger.info("send task status to frontend with payload: %s to namespace: %s", payload_, namespace)
        resp = await app.sio.emit(event="update_taskstate", data=payload_, namespace=namespace)  # type: ignore
