import { Brain, Activity, RotateCcw, Play, GitBranch } from "lucide-react";
import { Typography } from "../atoms/Typography";
import { IconWrapper } from "../atoms/IconWrapper";

interface LogicStreamProps {
  thoughts: string[];
}

export const LogicStream = ({ thoughts }: LogicStreamProps) => {
  return (
    <div className="glass-panel rounded-3xl p-8 flex-[1.5] flex flex-col gap-6 overflow-hidden relative group">
      <div className="absolute top-0 right-0 p-12 opacity-[0.02] pointer-events-none group-hover:opacity-[0.05] transition-opacity duration-1000">
        <Brain className="w-56 h-56 text-white" />
      </div>

      <header className="flex justify-between items-center">
        <div>
          <Typography variant="h2" weight="black" className="text-white">
            Workflow Matrix
          </Typography>
          <div className="h-1 w-16 bg-violet-600 mt-2 rounded-full"></div>
        </div>
        <div className="flex gap-3">
          <IconWrapper
            icon={RotateCcw}
            size="sm"
            color="text-violet-500"
            className="opacity-50"
          />
          <IconWrapper
            icon={Play}
            size="sm"
            color="text-neutral-500"
            className="opacity-30"
          />
          <IconWrapper
            icon={GitBranch}
            size="sm"
            color="text-neutral-500"
            className="opacity-30"
          />
        </div>
      </header>

      <div className="grid grid-cols-3 gap-6">
        {[
          {
            icon: RotateCcw,
            title: "RECURSIVE",
            sub: "TDD-GATED",
            active: true,
            color: "text-violet-400",
          },
          {
            icon: Play,
            title: "SEQUENTIAL",
            sub: "LINEAR",
            active: false,
            color: "text-blue-400",
          },
          {
            icon: GitBranch,
            title: "PARALLEL",
            sub: "CONCURRENT",
            active: false,
            color: "text-emerald-400",
          },
        ].map((mode, i) => (
          <button
            key={i}
            className={`flex flex-col gap-4 p-6 rounded-2xl transition-all duration-300 border-2 ${
              mode.active
                ? "bg-violet-600/10 border-violet-500/40 shadow-2xl shadow-violet-600/10"
                : "bg-white/[0.02] border-white/5 opacity-30 grayscale cursor-not-allowed"
            }`}
          >
            <IconWrapper
              icon={mode.icon}
              size="md"
              color={mode.color}
              className={mode.active ? "animate-pulse" : ""}
            />
            <div>
              <Typography
                variant="caption"
                weight="black"
                className="text-white text-[12px]"
              >
                {mode.title}
              </Typography>
              <Typography
                variant="code"
                className="text-[10px] text-neutral-500 tracking-wider mt-0.5"
              >
                {mode.sub}
              </Typography>
            </div>
          </button>
        ))}
      </div>

      <div className="flex-1 flex flex-col gap-4 min-h-0">
        <Typography
          variant="h3"
          className="flex items-center gap-3 text-neutral-400"
        >
          <Brain className="w-4 h-4 text-violet-500" /> Neural Stream (Logic
          Output)
        </Typography>
        <div className="flex-1 overflow-y-auto font-mono text-[13px] text-neutral-300 leading-relaxed bg-black/60 p-8 rounded-3xl border border-white/10 shadow-2xl custom-scrollbar selection:bg-violet-500/50">
          {thoughts.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full gap-6 opacity-30">
              <Activity className="w-12 h-12 animate-pulse text-violet-500" />
              <Typography variant="caption" className="text-sm font-bold">
                Awaiting Cognitive Transmission...
              </Typography>
            </div>
          ) : (
            thoughts.join("")
          )}
        </div>
      </div>
    </div>
  );
};
