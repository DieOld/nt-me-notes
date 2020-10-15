from aiohttp import web
import api

routes = [
    web.get('/api/ping', api.ping, allow_head=False),
    web.post('/api/register', api.register),
    web.post('/api/login', api.login),
    web.post('/api/insert-note', api.insert_note),
    web.patch('/api/update-note-state', api.update_note_state),
    web.delete('/api/delete-note', api.delete_note),
    web.get('/api/get-user-notes', api.get_user_notes, allow_head=False)
]
