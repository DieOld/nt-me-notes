from aiohttp import web
import api

routes = [
    web.get("/ping", api.ping),
    web.post('/register', api.register),
    web.post('/login', api.login),
    web.post("/insert-note", api.insert_note),
    web.patch("/update-note-state", api.update_note_state),
    web.delete("/delete-note", api.delete_note),
    web.get("/get-user-notes", api.get_user_notes)
]
