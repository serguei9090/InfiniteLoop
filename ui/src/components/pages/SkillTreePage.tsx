import { Book, Cpu, GitBranch, HelpCircle, Lock } from "lucide-react";

// Mock data representing nodes in each quadrant
const skillsNodes = [
	{ id: "s1", label: "File System", x: 150, y: 150, status: "active" },
	{
		id: "s2",
		label: "Read/Write",
		x: 250,
		y: 100,
		status: "active",
		parent: "s1",
	},
	{
		id: "s3",
		label: "Delete/Move",
		x: 250,
		y: 200,
		status: "active",
		parent: "s1",
	},
	{
		id: "s4",
		label: "Advanced I/O",
		x: 380,
		y: 150,
		status: "learning",
		parent: "s2",
	},
];

const knowledgeNodes = [
	{ id: "k1", label: "TypeScript", x: 150, y: 150, status: "active" },
	{ id: "k2", label: "React", x: 280, y: 100, status: "active", parent: "k1" },
	{
		id: "k3",
		label: "Tailwind",
		x: 280,
		y: 200,
		status: "active",
		parent: "k1",
	},
	{ id: "k4", label: "NextJS", x: 400, y: 100, status: "locked", parent: "k2" },
];

const modulesNodes = [
	{ id: "m1", label: "Context Engine", x: 150, y: 150, status: "active" },
	{
		id: "m2",
		label: "Tree-sitter",
		x: 250,
		y: 100,
		status: "active",
		parent: "m1",
	},
	{
		id: "m3",
		label: "Auto-Evolver",
		x: 250,
		y: 200,
		status: "learning",
		parent: "m1",
	},
];

const emptyNodes = [
	{ id: "e1", label: "Undiscovered", x: 200, y: 150, status: "locked" },
];

export function SkillTreePage() {
	return (
		<div className="h-full w-full bg-surface-50 p-8 pb-24 flex flex-col relative overflow-hidden font-sans">
			<header className="mb-8 shrink-0 relative z-10 text-center">
				<h1 className="text-4xl font-black text-slate-800 tracking-tight uppercase">
					Evolution Matrix
				</h1>
				<p className="text-slate-500 mt-2 font-mono text-sm tracking-widest">
					AGENT CAPABILITY TOPOLOGY
				</p>
			</header>

			{/* Main Canvas Area */}
			<div className="flex-1 relative bg-white rounded-3xl border border-slate-200 shadow-lg overflow-hidden">
				{/* Center Node (Core) */}
				<div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-20 w-24 h-24 bg-accent rounded-full border-4 border-white flex items-center justify-center shadow-xl">
					<Cpu size={40} className="text-white" />
				</div>

				{/* Crosshairs divider */}
				<div className="absolute top-0 bottom-0 left-1/2 w-px bg-slate-100 z-0" />
				<div className="absolute left-0 right-0 top-1/2 h-px bg-slate-100 z-0" />

				{/* Quadrant 1: Top Left - SKILLS */}
				<div className="absolute top-0 left-0 w-1/2 h-1/2 p-8 relative">
					<QuadrantLabel
						title="SKILLS"
						icon={<GitBranch />}
						color="text-emerald-500"
						bgColor="bg-emerald-50"
						align="left"
					/>
					<NodeCanvas
						nodes={skillsNodes}
						colorClass="emerald"
						direction="bottom-right"
					/>
				</div>

				{/* Quadrant 2: Top Right - KNOWLEDGE */}
				<div className="absolute top-0 right-0 w-1/2 h-1/2 p-8 relative">
					<QuadrantLabel
						title="KNOWLEDGE"
						icon={<Book />}
						color="text-blue-500"
						bgColor="bg-blue-50"
						align="right"
					/>
					<NodeCanvas
						nodes={knowledgeNodes}
						colorClass="blue"
						direction="bottom-left"
					/>
				</div>

				{/* Quadrant 3: Bottom Left - MODULES */}
				<div className="absolute bottom-0 left-0 w-1/2 h-1/2 p-8 relative">
					<QuadrantLabel
						title="MODULES"
						icon={<Cpu />}
						color="text-purple-500"
						bgColor="bg-purple-50"
						align="left"
						bottom
					/>
					<NodeCanvas
						nodes={modulesNodes}
						colorClass="purple"
						direction="top-right"
					/>
				</div>

				{/* Quadrant 4: Bottom Right - UNKNOWN */}
				<div className="absolute bottom-0 right-0 w-1/2 h-1/2 p-8 relative">
					<QuadrantLabel
						title="AWAITING DATA"
						icon={<HelpCircle />}
						color="text-slate-400"
						bgColor="bg-slate-50"
						align="right"
						bottom
					/>
					<NodeCanvas
						nodes={emptyNodes}
						colorClass="slate"
						direction="top-left"
					/>
				</div>
			</div>
		</div>
	);
}

// Subcomponents

function QuadrantLabel({ title, icon, color, bgColor, align, bottom }: any) {
	return (
		<div
			className={`absolute ${bottom ? "bottom-8" : "top-8"} ${align === "left" ? "left-8" : "right-8"} flex items-center gap-3 opacity-60`}
		>
			{align === "right" && (
				<h2 className={`text-2xl font-black tracking-widest ${color}`}>
					{title}
				</h2>
			)}
			<div
				className={`p-3 rounded-xl border border-slate-100 ${bgColor} ${color}`}
			>
				{icon}
			</div>
			{align === "left" && (
				<h2 className={`text-2xl font-black tracking-widest ${color}`}>
					{title}
				</h2>
			)}
		</div>
	);
}

function NodeCanvas({
	nodes,
	colorClass,
	direction,
}: {
	nodes: any[];
	colorClass: string;
	direction: string;
}) {
	const adjust = (val: number, isX: boolean) => {
		if (direction.includes("left") && isX) return `calc(100% - ${val}px)`;
		if (direction.includes("right") && isX) return `${val}px`;
		if (direction.includes("top") && !isX) return `calc(100% - ${val}px)`;
		if (direction.includes("bottom") && !isX) return `${val}px`;
		return `${val}px`;
	};

	const getColorHex = () => {
		switch (colorClass) {
			case "emerald":
				return "#10b981";
			case "blue":
				return "#3b82f6";
			case "purple":
				return "#a855f7";
			default:
				return "#94a3b8";
		}
	};

	const hexColor = getColorHex();

	return (
		<div className="absolute inset-0">
			<svg className="absolute inset-0 w-full h-full pointer-events-none">
				{nodes.map((node) => {
					if (!node.parent) return null;
					const parent = nodes.find((n) => n.id === node.parent);
					if (!parent) return null;

					return (
						<line
							key={`${node.id}-${parent.id}`}
							x1={adjust(node.x, true)}
							y1={adjust(node.y, false)}
							x2={adjust(parent.x, true)}
							y2={adjust(parent.y, false)}
							stroke={node.status === "locked" ? "#cbd5e1" : hexColor}
							strokeWidth="3"
							strokeDasharray={
								node.status === "learning" || node.status === "locked"
									? "6,6"
									: "none"
							}
							opacity={node.status === "locked" ? 0.5 : 0.8}
						/>
					);
				})}
			</svg>

			{nodes.map((node) => (
				<div
					key={node.id}
					className="absolute transform -translate-x-1/2 -translate-y-1/2 flex flex-col items-center gap-2 group cursor-pointer"
					style={{
						left: adjust(node.x, true),
						top: adjust(node.y, false),
					}}
				>
					<div
						className={`w-12 h-12 rounded-xl border-2 flex items-center justify-center transition-all bg-white z-10 shadow-sm
            ${node.status === "active" ? `border-${colorClass}-500 text-${colorClass}-500 shadow-[0_0_15px_${hexColor}40]` : ""}
            ${node.status === "learning" ? `border-${colorClass}-400 text-${colorClass}-400 border-dashed animate-pulse` : ""}
            ${node.status === "locked" ? "border-slate-200 text-slate-400 bg-slate-50" : ""}
            group-hover:scale-110
          `}
					>
						{node.status === "locked" ? (
							<Lock size={20} />
						) : (
							<div className="w-4 h-4 rounded-full bg-current" />
						)}
					</div>
					<span
						className={`text-[10px] font-bold uppercase tracking-wider px-2 py-1 rounded-md border whitespace-nowrap shadow-sm
             ${node.status === "active" ? "bg-slate-800 text-white border-slate-700" : "bg-white text-slate-500 border-slate-200"}
          `}
					>
						{node.label}
					</span>
				</div>
			))}
		</div>
	);
}
