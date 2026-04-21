import { Activity, AlertTriangle, ShieldCheck, Terminal } from "lucide-react";
import { useState } from "react";

export function LogsPage() {
	const [logLevel, setLogLevel] = useState("INFO");
	const [traceEnabled, setTraceEnabled] = useState(false);

	// Mock logs for demonstration
	const [logs] = useState([
		{
			time: "10:23:45",
			level: "INFO",
			message: "JIT Context Engine initialized. Parsed 45 files.",
		},
		{
			time: "10:23:48",
			level: "DEBUG",
			message: "Connecting to LM Studio at http://127.0.0.1:1234/v1",
		},
		{
			time: "10:23:50",
			level: "SUCCESS",
			message: "Model gemma-4-e4b loaded successfully. VRAM usage: 8.2GB.",
		},
		{
			time: "10:24:12",
			level: "WARN",
			message: "Tool execution took longer than expected (4.2s).",
		},
		{
			time: "10:25:01",
			level: "INFO",
			message: "Awaiting next mission parameters.",
		},
	]);

	const getLogColor = (level: string) => {
		switch (level) {
			case "INFO":
				return "text-blue-500";
			case "DEBUG":
				return "text-slate-400";
			case "SUCCESS":
				return "text-emerald-500";
			case "WARN":
				return "text-amber-500";
			case "ERROR":
				return "text-red-500";
			default:
				return "text-slate-600";
		}
	};

	const getLogIcon = (level: string) => {
		switch (level) {
			case "INFO":
				return <Activity size={14} />;
			case "SUCCESS":
				return <ShieldCheck size={14} />;
			case "WARN":
				return <AlertTriangle size={14} />;
			default:
				return <Terminal size={14} />;
		}
	};

	return (
		<div className="h-full w-full p-8 pb-24 flex flex-col gap-6 bg-surface-50 overflow-hidden">
			<header className="flex justify-between items-end shrink-0">
				<div>
					<h1 className="text-3xl font-bold text-slate-800 tracking-tight">
						System Logs
					</h1>
					<p className="text-slate-500 mt-2">
						Monitor core execution and agent traces in real-time.
					</p>
				</div>

				<div className="flex items-center gap-4 bg-white p-2 rounded-xl border border-slate-200 shadow-sm">
					<div className="flex items-center gap-2 px-3 border-r border-slate-100">
						<span className="text-sm font-medium text-slate-600">
							Trace Mode
						</span>
						<button
							onClick={() => setTraceEnabled(!traceEnabled)}
							className={`w-10 h-5 rounded-full relative transition-colors ${traceEnabled ? "bg-accent" : "bg-slate-300"}`}
						>
							<span
								className={`absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full transition-transform ${traceEnabled ? "translate-x-5" : "translate-x-0"}`}
							/>
						</button>
					</div>

					<div className="flex items-center gap-2 px-3">
						<span className="text-sm font-medium text-slate-600">Level</span>
						<select
							value={logLevel}
							onChange={(e) => setLogLevel(e.target.value)}
							className="bg-transparent text-sm font-bold text-slate-800 outline-none"
						>
							<option value="DEBUG">DEBUG</option>
							<option value="INFO">INFO</option>
							<option value="WARN">WARN</option>
							<option value="ERROR">ERROR</option>
						</select>
					</div>
				</div>
			</header>

			<div className="flex-1 glass-panel flex flex-col overflow-hidden">
				<div className="bg-slate-800 text-slate-300 px-4 py-2 text-xs font-mono font-bold uppercase tracking-wider flex border-b border-slate-700 rounded-t-2xl">
					<div className="w-24">Time</div>
					<div className="w-24">Level</div>
					<div className="flex-1">Message</div>
				</div>

				<div className="flex-1 bg-slate-900 p-4 overflow-y-auto custom-scrollbar font-mono text-sm rounded-b-2xl">
					{logs.map((log, i) => (
						<div
							key={i}
							className="flex hover:bg-slate-800/50 py-1.5 px-2 rounded transition-colors group"
						>
							<div className="w-24 text-slate-500">{log.time}</div>
							<div
								className={`w-24 flex items-center gap-1.5 font-bold ${getLogColor(log.level)}`}
							>
								{getLogIcon(log.level)}
								{log.level}
							</div>
							<div className="flex-1 text-slate-300 group-hover:text-white transition-colors">
								{log.message}
							</div>
						</div>
					))}
					{/* Faux typing cursor */}
					<div className="flex py-1.5 px-2 mt-2">
						<div className="w-4 h-4 bg-slate-500 animate-pulse" />
					</div>
				</div>
			</div>
		</div>
	);
}
