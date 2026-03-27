import { useNavigate } from "react-router-dom"
import Uploader from "../components/Uploader"

export default function Home() {
	const navigate = useNavigate()

	return (
		<div className="space-y-6">
			<h1 className="text-2xl font-semibold text-slate-50">Deepfake Detector</h1>
			<p className="text-slate-300">
				Upload an image or video to get a deepfake likelihood score from the demo model.
			</p>
			<Uploader onUploaded={(id) => navigate(`/results/${id}`)} />
		</div>
	)
}

