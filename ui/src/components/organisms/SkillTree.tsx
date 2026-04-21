import { useEffect, useState, useRef } from "react";
import { Typography } from "../atoms/Typography";
import { Activity, Box, Cpu, Wrench } from "lucide-react";

interface TreeNode {
  name: string;
  type: "module" | "tool" | "skill" | "context";
  status: "active" | "inactive" | "error";
  children?: TreeNode[];
}

export const SkillTree = () => {
  const [nodes, setNodes] = useState<TreeNode[]>([
    {
      name: "Context Manager",
      type: "context",
      status: "active",
    },
    {
      name: "Modules",
      type: "module",
      status: "active",
      children: [
        { name: "ADK Orchestrator", type: "module", status: "active" },
        { name: "Evolution Engine", type: "module", status: "active" },
      ],
    },
    {
      name: "Tools",
      type: "tool",
      status: "active",
      children: [
        { name: "read_file", type: "tool", status: "active" },
        { name: "write_file", type: "tool", status: "active" },
      ],
    },
    {
      name: "Skills",
      type: "skill",
      status: "active",
      children: [
        { name: "Python Coding", type: "skill", status: "active" },
      ],
    },
  ]);

  const getIcon = (type: string) => {
    switch (type) {
      case "module":
        return <Box className="w-5 h-5 text-blue-400" />;
      case "tool":
        return <Wrench className="w-5 h-5 text-violet-400" />;
      case "skill":
        return <Activity className="w-5 h-5 text-emerald-400" />;
      case "context":
        return <Cpu className="w-5 h-5 text-amber-400" />;
      default:
        return <Box className="w-5 h-5 text-white" />;
    }
  };

  return (
    <div className="glass-panel rounded-3xl p-6 h-full flex flex-col relative border border-white/10">
      <div className="flex items-center gap-3 mb-6">
        <Typography variant="h3" weight="bold" className="text-white">
          System Capability Matrix
        </Typography>
      </div>

      <div className="flex-1 relative bg-black/20 rounded-2xl p-8 border border-white/5 overflow-hidden">
        {/* Core Node */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 flex flex-col items-center z-10">
          <div className="w-20 h-20 rounded-full bg-violet-600/20 border-2 border-violet-500/50 flex items-center justify-center shadow-[0_0_30px_rgba(139,92,246,0.3)] backdrop-blur-sm">
            <Cpu className="w-8 h-8 text-violet-400" />
          </div>
          <Typography variant="caption" className="mt-3 font-bold text-violet-300">
            IMMUTABLE CORE
          </Typography>
        </div>

        {/* North: Modules */}
        <div className="absolute top-8 left-1/2 -translate-x-1/2 flex flex-col items-center">
          <div className="p-3 bg-blue-500/10 rounded-xl border border-blue-500/30">
             {getIcon("module")}
          </div>
          <Typography variant="caption" className="mt-2 text-blue-300">Modules</Typography>
        </div>

        {/* South: Tools */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center">
           <Typography variant="caption" className="mb-2 text-violet-300">Tools</Typography>
           <div className="p-3 bg-violet-500/10 rounded-xl border border-violet-500/30">
             {getIcon("tool")}
          </div>
        </div>

        {/* East: Skills */}
        <div className="absolute top-1/2 right-8 -translate-y-1/2 flex items-center gap-3">
          <Typography variant="caption" className="text-emerald-300">Skills</Typography>
           <div className="p-3 bg-emerald-500/10 rounded-xl border border-emerald-500/30">
             {getIcon("skill")}
          </div>
        </div>

        {/* West: Context */}
        <div className="absolute top-1/2 left-8 -translate-y-1/2 flex items-center gap-3">
          <div className="p-3 bg-amber-500/10 rounded-xl border border-amber-500/30">
             {getIcon("context")}
          </div>
          <Typography variant="caption" className="text-amber-300">Context</Typography>
        </div>

        {/* Connection Lines (SVG) */}
        <svg className="absolute inset-0 w-full h-full pointer-events-none opacity-20">
            <line x1="50%" y1="50%" x2="50%" y2="20%" stroke="currentColor" strokeWidth="2" strokeDasharray="4 4" className="text-blue-400" />
            <line x1="50%" y1="50%" x2="50%" y2="80%" stroke="currentColor" strokeWidth="2" strokeDasharray="4 4" className="text-violet-400" />
            <line x1="50%" y1="50%" x2="80%" y2="50%" stroke="currentColor" strokeWidth="2" strokeDasharray="4 4" className="text-emerald-400" />
            <line x1="50%" y1="50%" x2="20%" y2="50%" stroke="currentColor" strokeWidth="2" strokeDasharray="4 4" className="text-amber-400" />
        </svg>

      </div>
    </div>
  );
};
