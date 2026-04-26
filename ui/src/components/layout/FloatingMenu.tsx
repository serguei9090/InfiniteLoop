import { LayoutDashboard, Network, ScrollText, Settings } from "lucide-react";
import { NavLink } from "react-router-dom";

const MENU_ITEMS = [
	{ to: "/", icon: LayoutDashboard, label: "Dashboard" },
	{ to: "/skill-tree", icon: Network, label: "Skill Tree" },
	{ to: "/logs", icon: ScrollText, label: "Logs" },
	{ to: "/settings", icon: Settings, label: "Settings" },
];

export function FloatingMenu() {
	return (
		<div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50">
			<div className="glass-panel px-6 py-3 flex items-center gap-8 shadow-xl bg-white/90">
				{MENU_ITEMS.map(({ to, icon: Icon, label }) => (
					<NavLink
						key={to}
						to={to}
						className={({ isActive }) =>
							`flex flex-col items-center gap-1 transition-colors ${
								isActive
									? "text-accent"
									: "text-slate-500 hover:text-accent-dark"
							}`
						}
					>
						<Icon size={24} />
						<span className="text-[10px] font-bold uppercase tracking-wider">
							{label}
						</span>
					</NavLink>
				))}
			</div>
		</div>
	);
}
