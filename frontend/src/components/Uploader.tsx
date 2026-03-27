import { useState } from "react"
import { uploadFile } from "../services/api"

export default function Uploader({ onUploaded }: { onUploaded: (id: string) => void }) {
	const [busy, setBusy] = useState(false)
	const [error, setError] = useState<string | null>(null)

	async function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
		if (!e.target.files || e.target.files.length === 0) return
		const file = e.target.files[0]
		setBusy(true)
		setError(null)
		try {
			const res = await uploadFile(file)
			onUploaded(res.job_id)
		} catch (err: any) {
			setError(err?.message ?? "Upload failed")
		} finally {
			setBusy(false)
			e.target.value = ""
		}
	}

	return (
		<div className="space-y-4 glass-card p-5">
			<div className="space-y-1">
				<h1 className="text-xl font-semibold text-slate-50">Upload an image or video</h1>
				<p className="upload-hint">Smart deepfake detection powered by your local backend.</p>
			</div>

			<label className="upload-box cursor-pointer">
				<div className="space-y-1">
					<p className="text-sm font-medium text-slate-100">Click to choose a file</p>
					<p className="upload-hint">We never send your data to any external server.</p>
				</div>
				<input
					type="file"
					onChange={handleChange}
					disabled={busy}
					className="hidden"
				/>
			</label>

			<div className="flex items-center justify-between">
				<p className="upload-hint">Supported: <strong>image/*, video/*</strong></p>
				{busy && <p className="upload-status">Uploading...</p>}
			</div>

			{error && <p className="upload-error">{error}</p>}
		</div>
	)
}







