import { GitBranch, GitCommit, GitMerge, Lock } from "lucide-react";

const mockSkills = [
	{ id: "core", label: "Immutable Core", status: "active", icon: GitCommit },
	{
		id: "fs",
		label: "File System Ops",
		status: "active",
		icon: GitBranch,
		parent: "core",
	},
	{
		id: "read",
		label: "Read/List",
		status: "active",
		icon: GitCommit,
		parent: "fs",
	},
	{
		id: "write",
		label: "Edit/Create",
		status: "active",
		icon: GitCommit,
		parent: "fs",
	},
	{
		id: "exec",
		label: "Bash Execution",
		status: "active",
		icon: GitBranch,
		parent: "core",
	},
	{
		id: "web",
		label: "Web Browsing",
		status: "learning",
		icon: GitMerge,
		parent: "core",
		progress: 65,
	},
	{
		id: "vision",
		label: "Computer Vision",
		status: "locked",
		icon: Lock,
		parent: "core",
	},
];

export function SkillTree() {
	return (
		<div className="h-full w-full bg-slate-50 rounded-2xl border border-slate-200 p-6 flex flex-col items-center justify-center relative overflow-hidden">
			{/* Background Grid */}
			<div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>

			<div className="relative z-10 flex flex-col gap-8 w-full max-w-md">
				{/* Very simplified tree visualization for UI purposes */}
				<div className="flex justify-center">
					<SkillNode skill={mockSkills[0]} />
				</div>

				<div className="flex justify-center gap-16 relative">
					{/* connecting lines */}
					<div className="absolute top-[-32px] left-1/2 w-px h-8 bg-slate-300" />
					<div className="absolute top-[-16px] left-[25%] right-[25%] h-px bg-slate-300" />
					<div className="absolute top-[-16px] left-[25%] w-px h-4 bg-slate-300" />
					<div className="absolute top-[-16px] right-[25%] w-px h-4 bg-slate-300" />

					<SkillNode skill={mockSkills[1]} />
					<SkillNode skill={mockSkills[4]} />
				</div>

				<div className="flex justify-center gap-8 relative">
					<SkillNode skill={mockSkills[5]} />
					<SkillNode skill={mockSkills[6]} />
				</div>
			</div>
		</div>
	);
}

function SkillNode({ skill }: { skill: any }) {
	const Icon = skill.icon;

	const getStatusStyle = () => {
		switch (skill.status) {
			case "active":
				return "bg-white border-emerald-500 text-emerald-600 shadow-[0_0_15px_rgba(16,185,129,0.2)]";
			case "learning":
				return "bg-white border-amber-500 text-amber-600 shadow-[0_0_15px_rgba(245,158,11,0.2)]";
			case "locked":
				return "bg-slate-100 border-slate-300 text-slate-400 border-dashed";
			default:
				return "bg-white border-slate-300 text-slate-600";
		}
	};

	return (
		<div className="flex flex-col items-center gap-2">
			<div
				className={`w-12 h-12 rounded-xl border-2 flex items-center justify-center relative transition-all hover:scale-105 cursor-pointer ${getStatusStyle()}`}
			>
				<Icon size={20} />
				{skill.status === "learning" && (
					<div className="absolute -bottom-1 -right-1 bg-amber-500 text-white text-[8px] font-bold px-1 rounded-sm">
						{skill.progress}%
					</div>
				)}
			</div>
			<span className="text-xs font-bold text-slate-700">{skill.label}</span>
		</div>
	);
}
