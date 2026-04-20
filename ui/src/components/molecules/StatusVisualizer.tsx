import { Cpu, Layers } from "lucide-react";
import { IconWrapper } from "../atoms/IconWrapper";
import { Typography } from "../atoms/Typography";

interface StatusVisualizerProps {
  state: string;
}

export const StatusVisualizer = ({ state }: StatusVisualizerProps) => {
  const getStatusColor = (s: string) => {
    switch (s) {
      case "Thinking":
        return "text-violet-400";
      case "Executing Tool":
        return "text-blue-400";
      case "Validating":
        return "text-emerald-400";
      case "Failed":
        return "text-red-400";
      default:
        return "text-neutral-400";
    }
  };

  const isIdle = state === "Idle";

  return (
    <div className="h-40 rounded-xl bg-black/40 border border-white/5 flex flex-col items-center justify-center text-center relative overflow-hidden transition-all duration-500">
      <div className="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-violet-500 to-transparent opacity-30"></div>

      {isIdle ? (
        <div className="animate-in fade-in duration-700">
          <div className="p-3 bg-neutral-800/30 rounded-full mb-3 inline-block">
            <IconWrapper icon={Layers} size="md" color="text-neutral-500" />
          </div>
          <Typography variant="h2" weight="bold">
            CORE SLEEPING
          </Typography>
          <Typography variant="caption" className="text-neutral-600 mt-1">
            Awaiting mission parameters from Command
          </Typography>
        </div>
      ) : (
        <div className="flex flex-col items-center animate-in fade-in zoom-in duration-500">
          <IconWrapper
            icon={Cpu}
            size="lg"
            color={getStatusColor(state)}
            glow
            className="animate-bounce"
          />
          <Typography
            variant="h1"
            weight="black"
            className={`mt-4 ${getStatusColor(state).replace("text-", "text-glow-")}`}
          >
            {state}
          </Typography>
          <Typography
            variant="code"
            className="mt-1 px-3 py-0.5 bg-white/5 rounded-full border border-white/5"
          >
            ORD_EXEC_LOOP_01
          </Typography>
        </div>
      )}
    </div>
  );
};
