from aiohttp.web import get, put, patch, delete
import view

routes = [
    get("/ping", view.ping),
    put("/insert-note", view.insert_note),
    patch("/update-note-state", view.update_note_state),
    delete("/delete-note", view.delete_note),
    get("/get-user-notes", view.get_user_notes)
]