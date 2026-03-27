import { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { getJob, getResults } from "../services/api"
import ResultCard from "../components/ResultCard"
import VideoPlayerWithFrames from "../components/VideoPlayerWithFrames"

export default function Results() {
	const { id } = useParams()
	const [job, setJob] = useState<any>(null)
	const [results, setResults] = useState<any>(null)
	const [loading, setLoading] = useState(true)

	useEffect(() => {
		let mounted = true
		async function fetchData() {
			if (!id) return
			try {
				const [j, r] = await Promise.all([getJob(id), getResults(id)])
				if (!mounted) return
				setJob(j)
				setResults(r)
			} finally {
				if (mounted) setLoading(false)
			}
		}
		fetchData()
		const interval = setInterval(fetchData, 2000)
		return () => {
			mounted = false
			clearInterval(interval)
		}
	}, [id])

	if (loading) return <p className="text-slate-300">Loading...</p>
	if (!job) return <p className="text-rose-300">Job not found.</p>

	return (
		<div className="space-y-6">
			<h1 className="text-2xl font-semibold text-slate-50">Results</h1>
			<ResultCard result={results} />
			{job.type === "video" && job.frames && job.frames.length > 0 && (
				<VideoPlayerWithFrames frames={job.frames} />
			)}
		</div>
	)
}













