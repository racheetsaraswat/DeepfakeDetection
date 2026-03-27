from datetime import datetime
from typing import List, Optional, Any
from pydantic import BaseModel, Field, ConfigDict
from bson import ObjectId


class PyObjectId(ObjectId):
	@classmethod
	def __get_validators__(cls):
		yield cls.validate

	@classmethod
	def validate(cls, v):
		if isinstance(v, ObjectId):
			return v
		if not ObjectId.is_valid(v):
			raise ValueError("Invalid ObjectId")
		return ObjectId(v)


class JobCreate(BaseModel):
	filename: str
	type: str  # "image" | "video"
	status: str = "queued"
	score: Optional[float] = None
	label: Optional[str] = None
	frames: Optional[List[str]] = None
	created_at: datetime = Field(default_factory=datetime.utcnow)


class JobDB(JobCreate):
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
	model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True, json_encoders={ObjectId: str})


class InferenceRequest(BaseModel):
	# For synchronous image predict; API accepts file in multipart
	threshold: float = 0.5


class InferenceResult(BaseModel):
	score: float
	label: str
	heatmap_path: Optional[str] = None
	frames: Optional[List[str]] = None
	extra: Optional[Any] = None
















