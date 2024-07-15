from fastapi import FastAPI, WebSocket, Form, Request, Response
from typing import List, Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from openai import OpenAI, AsyncOpenAI
from helper import post_http_request_skylora, post_http_request_v1, get_response
import os
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Use a list to store chat responses. Consider using a more scalable storage solution for production.
chat_responses: List[str] = []

# Initialize a chat log with a system message.
chat_log = [{
    'role': 'system',
    'content': ('You are a Helpful assistant, skilled in explaining complex concepts in simple terms. ')
}]


@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    """Serve the chat page."""
    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})


@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: Annotated[str, Form()]):
    """Handle user input from the chat form."""
    chat_responses.append(user_input)

    response = post_http_request_skylora('sky-lora', "http://172.31.0.1:8004/v1", user_input)

    bot_response = get_response(response)
    chat_log.append({'role': 'assistant', 'content': bot_response})
    chat_responses.append(bot_response)

    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Websocket endpoint for real-time AI responses."""
    await websocket.accept()
    while True:
        user_message = await websocket.receive_text()
        async for ai_response in post_http_request_v1('sky-lora', "http://172.31.0.1:8004/v1",user_message):
            await websocket.send_text(ai_response)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)
