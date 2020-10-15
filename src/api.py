from aiohttp.web import json_response
from aiohttp_swagger import swagger_path
from decorators import login_required

import db
import utils


@swagger_path('/swagger/ping.yaml')
async def ping(request):
    return json_response({"message": "pong"}, status=200)


@swagger_path('/swagger/login.yaml')
async def login(request):
    msg, status = await utils.verify_user(await request.json())
    return json_response(msg, status=status)


@swagger_path('/swagger/register.yaml')
async def register(request):
    data = await request.json()
    if not await utils.validate_register_data(data):
        return json_response({"message": "Invalid register data"}, status=403)
    data['password'] = utils.hash_pass(data['password1'])
    await db.create_user(data)
    return json_response({"message": "success"}, status=200)


@swagger_path('/swagger/insert_note.yaml')
@login_required
async def insert_note(request):
    data = await request.json()
    note = data.get("text")
    if note:
        insert_result = await db.insert_note(request.user['_id'], note)
        if insert_result:
            note = await db.db().notes.find_one({'_id': insert_result.inserted_id})
            note['_id'] = str(note['_id'])
            return json_response({"message": note}, status=200)
        return json_response({"message": "Something went wrong"}, status=501)
    return json_response({"message": "You can't create empty note"}, status=403)


@swagger_path('/swagger/update_note_state.yaml')
@login_required
async def update_note_state(request):
    data = await request.json()
    if await db.update_note_state(_id=data['_id'], owner_id=request.user['_id']):
        return json_response({"message": "OK"}, status=200)
    return json_response({"message": "Something went wrong."}, status=501)


@swagger_path('/swagger/delete_note.yaml')
@login_required
async def delete_note(request):
    data = await request.json()
    if await db.delete_note(_id=data['_id'], owner_id=request.user['_id']):
        return json_response({"message": "OK"}, status=200)
    return json_response({"message": "Something went wrong"}, status=501)


@swagger_path('/swagger/get_user_notes.yaml')
@login_required
async def get_user_notes(request):
    notes = await db.get_user_notes(request.user['_id'])
    return json_response(await utils.iterable_objects_object_id_to_str(notes), status=200)
