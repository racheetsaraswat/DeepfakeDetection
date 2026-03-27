from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

from ..db.mongodb import connect_to_mongo
from ..db.models import get_job


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("/{job_id}")
async def get_job_status(job_id: str):
	await connect_to_mongo()
	try:
		oid = ObjectId(job_id)
	except Exception:
		raise HTTPException(status_code=400, detail="Invalid job id")
	job = await get_job(oid)
	if not job:
		raise HTTPException(status_code=404, detail="Job not found")
	job["id"] = str(job["_id"])
	job["_id"] = str(job["_id"])
	# Use FastAPI's encoder so datetime and ObjectId are JSON serializable
	return JSONResponse(jsonable_encoder(job))


@router.get("/results/{job_id}")
async def get_job_results(job_id: str):
	# Alias per requirements: /results/{id} returns detection score, label, frame analysis
	await connect_to_mongo()
	try:
		oid = ObjectId(job_id)
	except Exception:
		raise HTTPException(status_code=400, detail="Invalid job id")
	job = await get_job(oid)
	if not job:
		raise HTTPException(status_code=404, detail="Job not found")
	result = {
		"job_id": str(job["_id"]),
		"status": job.get("status"),
		"score": job.get("score"),
		"label": job.get("label"),
		"frames": job.get("frames", []),
	}
	return JSONResponse(jsonable_encoder(result))














