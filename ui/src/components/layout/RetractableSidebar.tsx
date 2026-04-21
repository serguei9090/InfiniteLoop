import { ChevronLeft, ChevronRight } from "lucide-react";
import { useUIStore } from "../../store/uiStore";

interface RetractableSidebarProps {
	children: React.ReactNode;
}

export function RetractableSidebar({ children }: RetractableSidebarProps) {
	const { isSidebarOpen, toggleSidebar } = useUIStore();

	return (
		<div
			className={`relative transition-all duration-300 ease-in-out h-full border-r border-slate-200 bg-white ${
				isSidebarOpen ? "w-[400px]" : "w-0"
			}`}
		>
			{/* Content wrapper with fixed width so it doesn't squish during transition */}
			<div
				className={`w-[400px] h-full overflow-hidden transition-opacity duration-300 ${
					isSidebarOpen ? "opacity-100" : "opacity-0"
				}`}
			>
				{children}
			</div>

			{/* Toggle Button */}
			<button
				onClick={toggleSidebar}
				className="absolute -right-4 top-1/2 -translate-y-1/2 w-8 h-16 bg-white border border-slate-200 rounded-r-xl shadow-md flex items-center justify-center text-slate-500 hover:text-accent z-10 transition-colors"
			>
				{isSidebarOpen ? <ChevronLeft size={20} /> : <ChevronRight size={20} />}
			</button>
		</div>
	);
}
