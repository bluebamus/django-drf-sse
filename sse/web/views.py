import asyncio
import random

from django.http import StreamingHttpResponse
from django.shortcuts import render
from web.tasks import multitasking_update_state
from celery.result import AsyncResult
from asgiref.sync import sync_to_async


async def sse_stream(request):
    """
    Sends server-sent events to the client.
    """

    async def event_stream():
        emojis = ["🚀", "🐎", "🌅", "🦾", "🍇"]
        i = 0
        state = "FALSE"
        while state == "FALSE":
            try:
                yield f"data: {random.choice(emojis)} {i}\n\n"
                i += 1
                if i == 10:
                    state = "SUCCESS"
                    break
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                print("Client disconnected")
                break
            except Exception as e:
                # 다른 예외 처리
                print(f"An error occurred: {e}")
                break

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    return response


async def sse_stream_update_state(request):
    """
    Sends server-sent events to the client.
    """

    async def event_stream():
        emojis = ["🚀", "🐎", "🌅", "🦾", "🍇"]
        result = multitasking_update_state.delay(1, 2)
        task_result = await sync_to_async(AsyncResult)(result.task_id)

        while True:
            try:
                state = await sync_to_async(lambda: task_result.state)()
                print("state : ", state)
                if state in ["SUCCESS", "FAILURE"]:
                    print("get SUCCESS")
                    break
                if state == "IN_PROGRESS":
                    info = await sync_to_async(lambda: task_result.info)()
                    data = {
                        "state": state,
                        "current": info.get("current", 0),
                        "result": info.get("result", 0),
                    }
                    print("data : ", data)
                    print(".get('result' : ", data.get("result"))
                    yield f"data: {random.choice(emojis)} {data.get('result', '')}\n\n"
                else:
                    data = {"state": state}
                    yield f"data: {random.choice(emojis)} {state}\n\n"
                await asyncio.sleep(1)
            except asyncio.CancelledError:
                print("Client disconnected")
                break
            except Exception as e:
                # 다른 예외 처리
                print(f"An error occurred: {e}")
                break

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    return response


def index(request):
    return render(request, "index.html")


def index_update_state(request):
    return render(request, "index_update_state.html")
