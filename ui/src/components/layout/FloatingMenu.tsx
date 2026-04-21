import { LayoutDashboard, Network, ScrollText, Settings } from "lucide-react";
import { NavLink } from "react-router-dom";

export function FloatingMenu() {
	return (
		<div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50">
			<div className="glass-panel px-6 py-3 flex items-center gap-8 shadow-xl bg-white/90">
				<NavLink
					to="/"
					className={({ isActive }) =>
						`flex flex-col items-center gap-1 transition-colors ${
							isActive ? "text-accent" : "text-slate-500 hover:text-accent-dark"
						}`
					}
				>
					<LayoutDashboard size={24} />
					<span className="text-[10px] font-bold uppercase tracking-wider">
						Dashboard
					</span>
				</NavLink>

				<NavLink
					to="/skill-tree"
					className={({ isActive }) =>
						`flex flex-col items-center gap-1 transition-colors ${
							isActive ? "text-accent" : "text-slate-500 hover:text-accent-dark"
						}`
					}
				>
					<Network size={24} />
					<span className="text-[10px] font-bold uppercase tracking-wider">
						Skill Tree
					</span>
				</NavLink>

				<NavLink
					to="/logs"
					className={({ isActive }) =>
						`flex flex-col items-center gap-1 transition-colors ${
							isActive ? "text-accent" : "text-slate-500 hover:text-accent-dark"
						}`
					}
				>
					<ScrollText size={24} />
					<span className="text-[10px] font-bold uppercase tracking-wider">
						Logs
					</span>
				</NavLink>

				<NavLink
					to="/settings"
					className={({ isActive }) =>
						`flex flex-col items-center gap-1 transition-colors ${
							isActive ? "text-accent" : "text-slate-500 hover:text-accent-dark"
						}`
					}
				>
					<Settings size={24} />
					<span className="text-[10px] font-bold uppercase tracking-wider">
						Settings
					</span>
				</NavLink>
			</div>
		</div>
	);
}
