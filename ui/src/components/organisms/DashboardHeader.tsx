import { Activity, Zap, Cpu, Hash } from "lucide-react";

export function DashboardHeader({
  tps,
  retry,
  inputTokens,
  outputTokens,
}: {
  tps: number;
  retry: number;
  inputTokens: number;
  outputTokens: number;
}) {
  return (
    <div className="grid grid-cols-4 gap-4 mb-2">
      <div className="glass-panel p-4 flex flex-col gap-2 relative overflow-hidden group">
        <div className="absolute -right-4 -bottom-4 opacity-[0.03] group-hover:opacity-[0.06] transition-opacity">
          <Activity size={80} />
        </div>
        <div className="flex items-center gap-2 text-slate-500 font-bold text-xs uppercase tracking-widest">
          <Activity size={14} className="text-accent" />
          Speed
        </div>
        <div className="text-2xl font-black text-slate-800 tracking-tighter">
          {tps.toFixed(1)} <span className="text-sm font-bold text-slate-400">t/s</span>
        </div>
      </div>

      <div className="glass-panel p-4 flex flex-col gap-2 relative overflow-hidden group">
        <div className="absolute -right-4 -bottom-4 opacity-[0.03] group-hover:opacity-[0.06] transition-opacity">
          <Zap size={80} />
        </div>
        <div className="flex items-center gap-2 text-slate-500 font-bold text-xs uppercase tracking-widest">
          <Zap size={14} className={retry > 0 ? "text-amber-500" : "text-emerald-500"} />
          Reflexion
        </div>
        <div className="text-2xl font-black text-slate-800 tracking-tighter">
          {retry} <span className="text-sm font-bold text-slate-400">retries</span>
        </div>
      </div>

      <div className="glass-panel p-4 flex flex-col gap-2 relative overflow-hidden group">
        <div className="absolute -right-4 -bottom-4 opacity-[0.03] group-hover:opacity-[0.06] transition-opacity">
          <Hash size={80} />
        </div>
        <div className="flex items-center gap-2 text-slate-500 font-bold text-xs uppercase tracking-widest">
          <Hash size={14} className="text-blue-400" />
          Input
        </div>
        <div className="text-2xl font-black text-slate-800 tracking-tighter">
          {inputTokens.toLocaleString()} <span className="text-sm font-bold text-slate-400">tok</span>
        </div>
      </div>

      <div className="glass-panel p-4 flex flex-col gap-2 relative overflow-hidden group">
        <div className="absolute -right-4 -bottom-4 opacity-[0.03] group-hover:opacity-[0.06] transition-opacity">
          <Cpu size={80} />
        </div>
        <div className="flex items-center gap-2 text-slate-500 font-bold text-xs uppercase tracking-widest">
          <Cpu size={14} className="text-purple-500" />
          Output
        </div>
        <div className="text-2xl font-black text-slate-800 tracking-tighter">
          {outputTokens.toLocaleString()} <span className="text-sm font-bold text-slate-400">tok</span>
        </div>
      </div>
    </div>
  );
}
