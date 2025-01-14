import sys
from typing import Literal, cast

from fastapi import APIRouter, HTTPException, Request
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import AsyncApiClient, AsyncMessagingApi, Configuration
from linebot.v3.webhook import WebhookParser
from linebot.v3.webhooks.models.message_event import MessageEvent
from linebot.v3.webhooks.models.source import Source

from kb_2315 import notify
from kb_2315.config import conf


channel_access_token: str = conf.line_channel_access_token
channel_secret: str = conf.line_channel_secret


if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

configuration = Configuration(access_token=channel_access_token)


async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser(channel_secret)
router = APIRouter()


@router.post("/callback")
async def handle_callback(request: Request) -> Literal["OK"]:
    signature: str = request.headers["X-Line-Signature"]

    byte_body: bytes = await request.body()
    body: str = byte_body.decode()

    try:
        events: list[MessageEvent] = parser.parse(body, signature)  # type: ignore
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        print(type(event))

        print(cast(Source, event.source).type)
        print(event.source)

        notify.line.send_message(message="sample message")

    return "OK"
