from fastapi import FastAPI, Request, HTTPException, Header, status

import os
import uvicorn
from dotenv import load_dotenv

from linebot.exceptions import InvalidSignatureError
from linebot.v3 import (
    WebhookHandler,
)


from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
)

from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
)

load_dotenv()
app = FastAPI()

configuration = Configuration(access_token=os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("CHANNEL_SECRET"))



@app.post("/callback")
async def callback(request: Request, x_line_signature: str = Header(None)):
    body = await request.body()
    body_str = body.decode('utf-8')

    try:
        handler.handle(body_str, x_line_signature)
    except InvalidSignatureError:
        print("Invalid signature, Please check your channel access token/channel secret")
        raise HTTPException(status_code=400, detail="Invalid signature")


@handler.add(MessageEvent, message=TextMessageContent)
def handler_message(event: MessageEvent):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        reply_messsage = "Hello from dev Environment"

        line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[TextMessage(text=reply_messsage)]
            )
        )
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0")