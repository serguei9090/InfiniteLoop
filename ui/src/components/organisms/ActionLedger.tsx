import { FileEdit, Play, Search, TerminalSquare, Trash2 } from "lucide-react";

export function ActionLedger({ actions }: { actions: any[] }) {
	const getIcon = (type: string) => {
		switch (type) {
			case "read_file":
			case "list_files":
				return <Search size={14} className="text-blue-500" />;
			case "edit_file":
			case "create_file":
				return <FileEdit size={14} className="text-emerald-500" />;
			case "delete_file":
				return <Trash2 size={14} className="text-red-500" />;
			case "run_command":
				return <Play size={14} className="text-amber-500" />;
			default:
				return <TerminalSquare size={14} className="text-slate-500" />;
		}
	};

	return (
		<div className="h-full glass-panel flex flex-col overflow-hidden border-slate-200">
			<div className="bg-slate-50 border-b border-slate-200 p-3 flex items-center gap-2 shrink-0">
				<TerminalSquare size={16} className="text-accent" />
				<span className="text-xs font-bold text-slate-700 tracking-wider uppercase">
					Action Ledger
				</span>
			</div>
			<div className="flex-1 overflow-y-auto p-2 custom-scrollbar flex flex-col gap-1 bg-white">
				{actions.length === 0 ? (
					<div className="text-slate-400 text-xs italic flex items-center justify-center h-full">
						No actions recorded
					</div>
				) : (
					actions.map((action, i) => (
						<div
							key={i}
							className="flex flex-col gap-1 p-2 bg-slate-50 hover:bg-slate-100 rounded-lg border border-slate-100 transition-colors"
						>
							<div className="flex items-center gap-2">
								{getIcon(action.tool)}
								<span className="text-xs font-bold text-slate-700 font-mono">
									{action.tool}
								</span>
								<span className="text-[10px] text-slate-400 ml-auto font-mono">
									#{actions.length - i}
								</span>
							</div>
							<div className="text-[10px] text-slate-500 font-mono truncate pl-6">
								{JSON.stringify(action.args)}
							</div>
							{action.result && (
								<div className="mt-1 pl-6">
									<div className="text-[10px] bg-slate-800 text-slate-300 p-1.5 rounded border border-slate-700 max-h-20 overflow-y-auto custom-scrollbar font-mono break-all">
										{action.result}
									</div>
								</div>
							)}
						</div>
					))
				)}
			</div>
		</div>
	);
}
