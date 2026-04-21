import { useEffect, useState } from "react";
import { Activity, Server, Database, Cpu, AlertTriangle, Clock } from "lucide-react";
import { Typography } from "../atoms/Typography";
import { Card } from "../molecules/Card";
import { MetricCard } from "../molecules/MetricCard";
import { Badge } from "../atoms/Badge";

interface DashboardMetrics {
  tps: number;
  activeConnections: number;
  memoryUsage: number;
  cpuUsage: number;
  uptime: number;
  latency: number;
}

interface ProcessInfo {
  id: string;
  name: string;
  status: "running" | "stopped" | "error";
  memory: number;
  cpu: number;
  startTime: string;
  restartCount: number;
}

const DashboardV2 = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [processes, setProcesses] = useState<ProcessInfo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchMetricsAndProcesses();
  }, []);

  const fetchMetricsAndProcesses = async () => {
    try {
      const hostAddress = window.location.host === "localhost:5173" 
        ? "http://localhost:8000" 
        : "";

      const metricsResponse = await fetch(`${hostAddress}/api/dashboard/metrics`);
      if (!metricsResponse.ok) throw new Error("Failed to fetch metrics");
      const metricsData = await metricsResponse.json();

      const processesResponse = await fetch(`${hostAddress}/api/dashboard/processes`);
      if (!processesResponse.ok) throw new Error("Failed to fetch processes");
      const processesData = await processesResponse.json();

      setMetrics(metricsData);
      setProcesses(processesData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error occurred");
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "running": return "success";
      case "error": return "danger";
      default: return "neutral";
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <Typography variant="h2" weight="bold">Loading Dashboard...</Typography>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-full">
        <Typography variant="body" color="danger">
          Error: {error}
        </Typography>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-[clamp(1rem,3vw,2rem)] p-[clamp(1rem,3vw,3rem)]">
      <div className="lg:col-span-1 space-y-[clamp(1rem,3vw,2rem)]">
        <Typography variant="h2" weight="black">System Metrics</Typography>
        
        <Card className="space-y-[clamp(0.5rem,1vw,1rem)]">
          {metrics && (
            <div className="grid grid-cols-2 gap-[clamp(0.5rem,1vw,1rem)]">
              <MetricCard
                label="THROUGHPUT"
                value={metrics.tps}
                unit="TPS"
                icon={Activity}
                color="text-emerald-400"
              />
              <MetricCard
                label="LATENCY"
                value={metrics.latency}
                unit="ms"
                icon={Clock}
                color="text-violet-400"
              />
              <MetricCard
                label="MEMORY"
                value={(metrics.memoryUsage / 1024).toFixed(2)}
                unit="GB"
                icon={Cpu}
                color="text-blue-400"
              />
              <MetricCard
                label="CONNECTIONS"
                value={metrics.activeConnections}
                unit="ACT"
                icon={Server}
                color="text-orange-400"
              />
            </div>
          )}
        </Card>

        <Card className="space-y-[clamp(0.5rem,1vw,1rem)]">
          <Typography variant="h3" weight="bold">Uptime</Typography>
          {metrics && (
            <div className="flex items-center gap-4 bg-black/40 p-4 rounded-2xl border border-white/10">
              <Clock className="w-8 h-8 text-violet-400" />
              <div>
                <Typography variant="body" className="font-bold text-white">
                  {Math.floor(metrics.uptime / 3600)}h {Math.floor((metrics.uptime % 3600) / 60)}m
                </Typography>
                <Typography variant="body" className="text-neutral-400">
                  Total system uptime
                </Typography>
              </div>
            </div>
          )}
        </Card>
      </div>

      <div className="lg:col-span-2 space-y-[clamp(1rem,3vw,2rem)]">
        <Typography variant="h2" weight="black">Active Processes</Typography>

        {processes.length === 0 ? (
          <Card>
            <Typography variant="body" color="neutral">
              No active processes detected.
            </Typography>
          </Card>
        ) : (
          processes.map((process) => (
            <Card key={process.id} className="space-y-[clamp(0.5rem,1vw,1rem)]">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className={`p-3 rounded-xl ${
                    process.status === "running" ? "bg-emerald-500/20" :
                    process.status === "error" ? "bg-red-500/20" : "bg-neutral-500/20"
                  }`}>
                    {process.status === "running" ? (
                      <Activity className="w-6 h-6 text-emerald-400" />
                    ) : process.status === "error" ? (
                      <AlertTriangle className="w-6 h-6 text-red-400" />
                    ) : (
                      <Server className="w-6 h-6 text-neutral-400" />
                    )}
                  </div>
                  <div>
                    <Typography variant="h3" weight="medium">{process.name}</Typography>
                    <Badge variant={getStatusColor(process.status)} className="text-[10px]">
                      {process.status.toUpperCase()}
                    </Badge>
                  </div>
                </div>
                
                <div className="flex items-center gap-6">
                  <MetricCard
                    label="CPU"
                    value={process.cpu}
                    unit="%"
                    icon={Cpu}
                    color="text-blue-400"
                  />
                  <MetricCard
                    label="MEM"
                    value={(process.memory / 1024).toFixed(2)}
                    unit="GB"
                    icon={Database}
                    color="text-purple-400"
                  />
                </div>
              </div>

              <div className="flex items-center justify-between bg-black/30 p-3 rounded-xl border border-white/5">
                <Typography variant="body" className="text-neutral-400">
                  Started: {new Date(process.startTime).toLocaleString()}
                </Typography>
                <Typography variant="body" className="text-neutral-400">
                  Restarts: {process.restartCount}
                </Typography>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};

export default DashboardV2;
