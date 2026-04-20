import { Terminal } from "lucide-react";
import { Typography } from "../atoms/Typography";
import { Badge } from "../atoms/Badge";

interface Action {
  success: boolean;
  output?: string;
  error?: string;
}

interface ActionLedgerProps {
  actions: Action[];
}

export const ActionLedger = ({ actions }: ActionLedgerProps) => {
  return (
    <div className="glass-panel rounded-3xl flex-1 flex flex-col overflow-hidden group">
      <header className="p-6 flex justify-between items-center border-b border-white/10 bg-white/[0.02]">
        <div className="flex items-center gap-3">
          <Terminal className="w-5 h-5 text-blue-400" />
          <Typography variant="h1" className="text-sm">
            Action Ledger
          </Typography>
        </div>
        <Badge variant="info" className="font-mono px-3 py-1">
          TOTAL OPS: {actions.length}
        </Badge>
      </header>

      <div className="p-6 flex-1 overflow-y-auto flex flex-col gap-4 custom-scrollbar scroll-smooth">
        {actions.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center gap-4 opacity-20">
            <Terminal className="w-10 h-10" />
            <Typography variant="caption" className="text-sm font-bold">
              Systems Ready for Operations
            </Typography>
          </div>
        ) : (
          actions.map((act, i) => (
            <div
              key={i}
              className="bg-black/40 border border-white/10 rounded-2xl p-6 animate-in fade-in slide-in-from-right-3 duration-500 hover:border-white/20 transition-all shadow-xl"
            >
              <div className="flex justify-between items-center mb-4">
                <Badge
                  variant={act.success ? "success" : "danger"}
                  className="px-3 py-1"
                >
                  {act.success ? "SUCCESS" : "FAILURE"}
                </Badge>
                <Typography
                  variant="code"
                  className="text-neutral-500 font-bold"
                >
                  OP_{actions.length - i}
                </Typography>
              </div>
              <Typography
                variant="code"
                className="text-neutral-300 text-[13px] leading-relaxed break-all line-clamp-4 hover:line-clamp-none transition-all cursor-help bg-black/20 p-4 rounded-xl border border-white/5"
              >
                {act.output || act.error}
              </Typography>
            </div>
          ))
        )}
      </div>

      <footer className="p-3 border-t border-white/5 bg-black/20">
        <div className="flex justify-between items-center opacity-40 hover:opacity-100 transition-opacity">
          <Typography variant="code" className="text-[8px]">
            LOG_BUFFER_STATUS: STABLE
          </Typography>
          <Typography variant="code" className="text-[8px]">
            0.00kb/s
          </Typography>
        </div>
      </footer>
    </div>
  );
};
