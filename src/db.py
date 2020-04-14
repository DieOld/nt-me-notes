from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from pymongo.results import UpdateResult, InsertOneResult, DeleteResult

MONGODB_URI = 'mongodb://root:toor@notes_db/'

DB = None
COLLECTION = None
CLIENT = None


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


async def find_user(username):
    return await db().users.find_one({"username": username.lower()})


async def create_user(user_data):
    await db().users.insert_one({
        'username': user_data['username'].lower(),
        'password': await user_data['password'],
        'friends': []
    })


async def insert_note(owner_id: str, note: str) -> InsertOneResult:
    """
    State % 2 === 0 - don't done
    State % 2 !== 0 - done
    """
    res = await db().notes.insert_one({
        'owner': owner_id,
        'note': note,
        'state': 0
    })
    return res


async def update_note_state(_id: str, owner_id: str) -> UpdateResult:
    return await db().notes.update_one({'owner': owner_id, '_id': ObjectId(_id)}, {'$inc': {
        'state': 1
    }})


async def get_user_notes(_id: str) -> list:
    notes = []
    async for note in db().notes.find({'owner': _id}):
        notes.append(note)
    return notes


async def delete_note(_id: str, owner_id: str) -> DeleteResult:
    return await db().notes.delete_one({'owner': owner_id, "_id": ObjectId(_id)})
