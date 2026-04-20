import { Cpu, Activity, Zap, MoveUpRight, MoveDownLeft } from "lucide-react";
import { Typography } from "../atoms/Typography";
import { MetricCard } from "../molecules/MetricCard";
import { Badge } from "../atoms/Badge";

interface DashboardHeaderProps {
  tps: number;
  retry: number;
  inputTokens?: number;
  outputTokens?: number;
}

export const DashboardHeader = ({
  tps,
  retry,
  inputTokens = 0,
  outputTokens = 0,
}: DashboardHeaderProps) => {
  return (
    <div className="glass-panel rounded-3xl p-8 flex flex-col gap-6">
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-6">
          <div className="p-4 bg-violet-600 rounded-2xl shadow-2xl shadow-violet-600/30">
            <Cpu className="w-8 h-8 text-white" />
          </div>
          <div>
            <Typography
              variant="h1"
              weight="black"
              className="flex items-center gap-3"
            >
              IMMUTABLE CORE
              <Badge variant="info" className="text-[10px] py-1 px-3">
                v0.1.0
              </Badge>
            </Typography>
            <Typography
              variant="body"
              className="mt-1 text-neutral-400 font-medium"
            >
              Autonomous Systems Management Dashboard
            </Typography>
          </div>
        </div>

        <div className="flex items-center gap-6">
          <div className="flex items-center bg-black/40 p-2 rounded-2xl border border-white/10">
            <MetricCard
              label="INPUT"
              value={inputTokens}
              unit="T"
              icon={MoveUpRight}
              color="text-neutral-500"
            />
            <div className="w-px h-10 bg-white/10 mx-2" />
            <MetricCard
              label="OUTPUT"
              value={outputTokens}
              unit="T"
              icon={MoveDownLeft}
              color="text-neutral-500"
            />
          </div>

          <div className="flex items-center bg-black/40 p-2 rounded-2xl border border-white/10">
            <MetricCard
              label="THROUGHPUT"
              value={tps}
              unit="TPS"
              icon={Activity}
              color="text-emerald-400"
            />
            <div className="w-px h-10 bg-white/10 mx-2" />
            <MetricCard
              label="RETRY POOL"
              value={retry}
              unit="/ 3"
              icon={Zap}
              color="text-violet-400"
            />
          </div>
        </div>
      </div>
    </div>
  );
};
