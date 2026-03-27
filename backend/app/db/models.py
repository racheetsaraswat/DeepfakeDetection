from datetime import datetime
from typing import Optional, List, Dict, Any
from bson import ObjectId
from . import mongodb


def _jobs():
	if mongodb.jobs_collection is None:
		raise RuntimeError("MongoDB has not been initialized. Call connect_to_mongo() first.")
	return mongodb.jobs_collection


async def create_job(filename: str, file_type: str, status: str = "queued") -> ObjectId:
	doc = {
		"filename": filename,
		"type": file_type,
		"status": status,
		"score": None,
		"label": None,
		"frames": [],
		"created_at": datetime.utcnow(),
	}
	result = await _jobs().insert_one(doc)
	return result.inserted_id


async def update_job(job_id: str | ObjectId, update: Dict[str, Any]) -> None:
	oid = ObjectId(job_id) if not isinstance(job_id, ObjectId) else job_id
	await _jobs().update_one({"_id": oid}, {"$set": update})


async def get_job(job_id: str | ObjectId) -> Optional[Dict[str, Any]]:
	oid = ObjectId(job_id) if not isinstance(job_id, ObjectId) else job_id
	return await _jobs().find_one({"_id": oid})




