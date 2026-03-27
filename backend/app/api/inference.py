from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import tempfile
import shutil

from ..inference.run_inference import run_image_inference
from ..storage import save_upload


router = APIRouter(prefix="/inference", tags=["inference"])


@router.post("/predict")
async def predict_image(file: UploadFile = File(...)):
	content_type = file.content_type or ""
	is_image = content_type.startswith("image/")
	if not is_image:
		raise HTTPException(status_code=400, detail="Only image/* supported for synchronous inference.")

	with tempfile.NamedTemporaryFile(delete=False) as tmp:
		tmp_path = Path(tmp.name)
		shutil.copyfileobj(file.file, tmp)
	dest = save_upload(tmp_path, file.filename)
	result = run_image_inference(dest)
	return JSONResponse(result)
















