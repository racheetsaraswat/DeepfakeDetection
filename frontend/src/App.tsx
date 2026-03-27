import { Link, Outlet } from "react-router-dom"

export default function App() {
	return (
		<div className="app-shell">
			<header className="app-header">
				<div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
					<Link to="/" className="app-header-title">Deepfake Detector</Link>
					<nav className="space-x-4">
						<Link to="/" className="app-nav-link">Home</Link>
						<Link to="/about" className="app-nav-link">About</Link>
					</nav>
				</div>
			</header>
			<div className="bg-grid">
				<main className="max-w-6xl mx-auto px-4 py-10">
					<Outlet />
				</main>
			</div>
		</div>
	)
}













