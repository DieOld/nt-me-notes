from motor.motor_asyncio import AsyncIOMotorClient
import os

password = os.environ["PASS"]
MONGODB_URI = f'mongodb+srv://notes:{password}@notes_db/'

DB = None
COLLECTION = None
CLIENT = None
ALGORITHM = environ['ALGORITHM']
SECRET = environ['SECRET']


def client():
    global CLIENT
    if CLIENT is None:
        CLIENT = AsyncIOMotorClient(MONGODB_URI)
    return CLIENT


def db():
    global DB
    if DB is None:
        DB = client()["notes_api"]
    return DB


def collection():
    global COLLECTION
    if COLLECTION is None:
        COLLECTION = db()["notes"]
    return COLLECTION


async def get_user_notes(username: str) -> list:
    """
    Function for getting user data(
    returns list of dicts that contains notes (
    id of single note, text of single note, and state of single note (is done or not)
        )
    )
    """
    user_data = await collection().find_one({"username": username})
    return user_data.get("notes")


async def generate_note_id(username: str) -> int:
    obj = await collection().find_one({"username": username})
    return len(obj["notes"]) + 1


async def insert_note(text: str, username: str) -> None:
    """Functions that insert text to the user notes
    with default is_done state: False.
    """
    _id = await generate_note_id(username)
    collection().update_one({"username": username},
                            {"$push": {"notes": {"_id": _id,
                                                 "text": text, "is_done": 1}}})


async def update_note_state(_id: int, username: str) -> None:
    """Function change state of note for specify user"""
    collection().update_one({"username": username,
                             "notes._id": _id
                             }, {"$inc": {"notes.$.is_done": 1}})


async def delete_note(_id: int, username: str) -> None:
    """Function delete specify note of specify user"""
    collection().update_one({"username": username},
                            {"$pull": {"notes": {"_id": _id}}})
