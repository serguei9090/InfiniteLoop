import { useState, useEffect, useRef } from "react";
import { Zap } from "lucide-react";

// Atomic Components
import { MainLayout } from "./components/templates/MainLayout";
import { DashboardHeader } from "./components/organisms/DashboardHeader";
import { MissionControl } from "./components/organisms/MissionControl";
import { LogicStream } from "./components/organisms/LogicStream";
import { ActionLedger } from "./components/organisms/ActionLedger";
import { StatusVisualizer } from "./components/molecules/StatusVisualizer";
import { Button } from "./components/atoms/Button";

interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
}

export default function App() {
  const [status, setStatus] = useState({ state: "Idle", retry: 0 });
  const [metrics, setMetrics] = useState({
    tps: 0,
    input_tokens: 0,
    output_tokens: 0,
    total_tokens: 0,
  });
  const [thoughts, setThoughts] = useState<string[]>([]);
  const [actions, setActions] = useState<any[]>([]);
  const [task, setTask] = useState("");
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content: "Immutable Core initialized. Awaiting mission parameters.",
    },
  ]);

  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const host =
      window.location.host === "localhost:5173"
        ? "localhost:8000"
        : window.location.host;
    ws.current = new WebSocket(`${protocol}//${host}/ws`);

    ws.current.onmessage = event => {
      const msg = JSON.parse(event.data);
      switch (msg.type) {
        case "status":
          setStatus(msg.data);
          if (msg.data.state === "Idle") setMetrics({ tps: 0 });
          break;
        case "metrics":
          setMetrics(msg.data);
          break;
        case "thought":
          setThoughts(prev => [...prev, msg.data]);
          break;
        case "action":
          setActions(prev => [msg.data, ...prev]);
          break;
      }
    };

    return () => ws.current?.close();
  }, []);

  const handleRunTask = async (missionTask: string) => {
    if (!missionTask) return;
    const hostAddress =
      window.location.host === "localhost:5173" ? "http://localhost:8000" : "";

    await fetch(`${hostAddress}/task/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task: missionTask }),
    });
    setTask("");
  };

  const handleSendMessage = (content: string) => {
    setChatMessages(prev => [...prev, { role: "user", content }]);
    if (
      content.toUpperCase().startsWith("RUN:") ||
      content.toUpperCase().startsWith("DEPLOY:")
    ) {
      handleRunTask(content.split(":")[1].trim());
    }
  };

  return (
    <MainLayout
      header={
        <DashboardHeader
          tps={metrics.tps}
          retry={status.retry}
          inputTokens={metrics.input_tokens}
          outputTokens={metrics.output_tokens}
        />
      }
      sidebar={
        <MissionControl
          messages={chatMessages}
          isThinking={status.state !== "Idle"}
          onSendMessage={handleSendMessage}
        />
      }
      content={
        <div className="flex flex-col gap-6 h-full">
          <StatusVisualizer state={status.state} />
          <div className="flex-1 flex gap-6 min-h-0">
            <LogicStream thoughts={thoughts} />
            <ActionLedger actions={actions} />
          </div>
        </div>
      }
      footer={
        <footer className="glass-panel rounded-3xl p-3 flex gap-4 border-2 border-white/5 shadow-2xl">
          <div className="flex-1 relative group">
            <div className="absolute left-6 top-1/2 -translate-y-1/2 text-neutral-500 group-focus-within:text-violet-500 transition-colors">
              <Zap className="w-5 h-5" />
            </div>
            <input
              value={task}
              onChange={e => setTask(e.target.value)}
              onKeyDown={e => e.key === "Enter" && handleRunTask(task)}
              className="w-full bg-black/40 border-2 border-white/5 rounded-2xl pl-16 pr-6 py-5 text-sm font-bold tracking-tight focus:border-violet-500/40 outline-none transition-all placeholder:text-neutral-700 text-white"
              placeholder="DEFINE STRATEGIC MISSION OBJECTIVE..."
            />
          </div>
          <Button
            onClick={() => handleRunTask(task)}
            disabled={status.state !== "Idle" || !task}
            variant="primary"
            size="lg"
            className="px-16 rounded-2xl text-[12px]"
          >
            Deploy Mission
          </Button>
        </footer>
      }
    />
  );
}
