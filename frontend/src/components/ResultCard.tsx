export default function ResultCard({ result }: { result: any }) {
	if (!result) return null
	const { status, score, label } = result

	// Inline background color so it overrides the default card bg
	const bgStyle: React.CSSProperties =
		label === "FAKE"
			? { backgroundColor: "rgba(248, 113, 113, 0.20)" } // light red
			: label === "REAL"
				? { backgroundColor: "rgba(34, 197, 94, 0.20)" } // light green
				: {}

	const pillClass =
		label === "FAKE"
			? "pill-danger"
			: label === "REAL"
				? "pill-success"
				: label === "UNCERTAIN"
					? "pill-warning"
					: "pill-neutral"

	return (
		<div className="glass-card-strong p-5 space-y-4" style={bgStyle}>
			<div className="flex items-center justify-between gap-4">
				<div>
					<p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Status</p>
					<p className="text-lg font-semibold text-slate-50">{status}</p>
				</div>
				<div>
					<p className="text-xs font-semibold uppercase tracking-wide text-slate-400">Score</p>
					<p className="text-lg font-semibold text-sky-300">
						{score != null ? score.toFixed(3) : "-"}
					</p>
				</div>
				<div className="text-right">
					<p className="text-xs font-semibold uppercase tracking-wide text-slate-400 mb-1">Label</p>
					<span className={pillClass}>
						{label ?? "-"}
					</span>
				</div>
			</div>
			<p className="text-xs text-slate-400">
				Higher scores indicate a higher likelihood that the media is a deepfake.
				{label === "UNCERTAIN" && (
					<span className="block mt-1 text-amber-400/90">
						Score is in the uncertain range — the model is not confident.
					</span>
				)}
			</p>
		</div>
	)
}













