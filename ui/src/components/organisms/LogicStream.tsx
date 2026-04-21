import { BrainCircuit } from "lucide-react";
import { useEffect, useRef } from "react";

export function LogicStream({ thoughts }: { thoughts: string[] }) {
	const containerRef = useRef<HTMLDivElement>(null);

	useEffect(() => {
		if (containerRef.current) {
			containerRef.current.scrollTop = containerRef.current.scrollHeight;
		}
	}, [thoughts]);

	return (
		<div className="h-full glass-panel flex flex-col overflow-hidden border-slate-200">
			<div className="bg-slate-50 border-b border-slate-200 p-3 flex items-center gap-2 shrink-0">
				<BrainCircuit size={16} className="text-accent" />
				<span className="text-xs font-bold text-slate-700 tracking-wider uppercase">
					Logic Stream
				</span>
				<div className="ml-auto flex items-center gap-2">
					<span className="text-[10px] font-mono text-slate-400">
						{thoughts.length} cycles
					</span>
				</div>
			</div>
			<div
				ref={containerRef}
				className="flex-1 p-4 overflow-y-auto custom-scrollbar font-mono text-xs flex flex-col gap-2 bg-slate-900"
			>
				{thoughts.length === 0 ? (
					<div className="text-slate-500 italic flex items-center justify-center h-full">
						Awaiting thought process...
					</div>
				) : (
					thoughts.map((thought, i) => (
						<div
							key={i}
							className="text-slate-300 border-l-2 border-accent/50 pl-3 py-1 bg-slate-800/50 rounded-r shadow-sm"
						>
							<span className="text-accent/70 mr-2 text-[10px]">
								[{i.toString().padStart(4, "0")}]
							</span>
							{thought}
						</div>
					))
				)}
			</div>
		</div>
	);
}
