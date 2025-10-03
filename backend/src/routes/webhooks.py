import json
import logging
import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.exc import IntegrityError
from svix.webhooks import Webhook

from ..database.db import create_challenge_quota
from ..database.models import get_db

load_dotenv()
router = APIRouter()


@router.post("/clerk")
async def handle_user_created(request: Request, db=Depends(get_db)):
    webhook_secret = os.getenv("CLERK_WEBHOOK_SECRET")
    if not webhook_secret:
        raise HTTPException(
            status_code=500, detail="CLERK_WEBHOOK_SECRET not set")

    body = await request.body()
    payload = body.decode("utf-8")
    headers = dict(request.headers)

    try:
        # Verify webhook
        wh = Webhook(webhook_secret)
        event = wh.verify(payload, headers)  # ✅ lowercase method

        # Process only `user.created`
        if event.get("type") != "user.created":
            return {"status": "ignored"}

        user_data = event.get("data", {})
        user_id = user_data.get("id")

        # Create challenge quota for new user
        create_challenge_quota(db, user_id)

        return {"status": "success"}

    except Exception as e:
        logging.exception("Webhook handling failed")
        raise HTTPException(
            status_code=400, detail=f"Webhook verification failed: {str(e)}")
