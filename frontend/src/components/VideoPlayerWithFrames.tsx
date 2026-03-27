export default function VideoPlayerWithFrames({ frames }: { frames: string[] }) {
	// Frames are absolute/relative paths on backend filesystem in this scaffold.
	// For a production-ready app, serve frames via a static files endpoint.
	return (
		<div className="space-y-3 glass-card p-5">
			<p className="text-sm text-slate-300">
				Extracted frames <span className="text-sky-300">({frames.length})</span>
			</p>
			<div className="grid grid-cols-2 md:grid-cols-4 gap-3">
				{frames.slice(0, 12).map((f, i) => (
					<div key={i} className="frame-tile">
						<div className="frame-filename">{f}</div>
					</div>
				))}
			</div>
			<p className="text-xs text-slate-500">
				Note: frames are not served publicly in this scaffold.
			</p>
		</div>
	)
}













