const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000"

export async function uploadFile(file: File): Promise<{ job_id: string }> {
	const form = new FormData()
	form.append("file", file)
	const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: form })
	if (!res.ok) {
		throw new Error(`Upload failed: ${res.status}`)
	}
	return await res.json()
}

export async function getJob(id: string) {
	const res = await fetch(`${API_BASE}/jobs/${id}`)
	if (!res.ok) throw new Error("Job not found")
	return await res.json()
}

export async function getResults(id: string) {
	const res = await fetch(`${API_BASE}/jobs/results/${id}`)
	if (!res.ok) throw new Error("Results not found")
	return await res.json()
}














