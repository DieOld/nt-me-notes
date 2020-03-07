from aiohttp.web import json_response

import db


async def ping(request):
    return json_response({"message": "pong"}, status=200)


async def insert_note(request):
    text = await request.json()
    text = text.get("text")
    if text:
        username = request.user["username"]
        await db.insert_note(text, username)
        return json_response({"message": "OK"}, status=200)
    return json_response({"message": "invalid data"}, status=403)


async def update_note_state(request):
    req = await request.post()
    note_id = int(req["_id"])
    username = request.user["username"]
    await db.update_note_state(_id=note_id, username=username)
    return json_response({"message": "OK"}, status=200)


async def delete_note(request):
    req = await request.json()
    note_id = int(req["_id"])
    username = request.user["username"]
    await db.delete_note(_id=note_id, username=username)
    return json_response({"message": "OK"}, status=200)


async def get_user_notes(request):
    notes = await db.get_user_notes(request.user['username'])
    return json_response(notes, status=200)
