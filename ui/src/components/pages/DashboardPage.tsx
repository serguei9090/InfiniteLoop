import { RetractableSidebar } from "../layout/RetractableSidebar";
import { MissionControl } from "../organisms/MissionControl";
import { LogicStream } from "../organisms/LogicStream";
import { ActionLedger } from "../organisms/ActionLedger";
import { DashboardHeader } from "../organisms/DashboardHeader";
import { useState, useEffect, useRef } from "react";
import { Target, Clock, ArrowRight } from "lucide-react";

interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
}

export function DashboardPage() {
  const [status, setStatus] = useState({ state: "Idle", retry: 0 });
  const [metrics, setMetrics] = useState({
    tps: 0,
    input_tokens: 0,
    output_tokens: 0,
    total_tokens: 0,
  });
  const [thoughts, setThoughts] = useState<string[]>([]);
  const [actions, setActions] = useState<any[]>([]);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      role: "assistant",
      content: "Immutable Core initialized. Awaiting mission parameters.",
    },
  ]);

  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const host = window.location.host === "localhost:5173" ? "localhost:8000" : window.location.host;

    if (!ws.current || ws.current.readyState === WebSocket.CLOSED) {
      ws.current = new WebSocket(`${protocol}//${host}/ws`);

      ws.current.onmessage = (event) => {
        try {
          const msg = JSON.parse(event.data);
          switch (msg.type) {
            case "status":
              setStatus(msg.data);
              if (msg.data.state === "Idle") setMetrics({ tps: 0, input_tokens: 0, output_tokens: 0, total_tokens: 0 });
              break;
            case "metrics":
              setMetrics(msg.data);
              break;
            case "thought":
              setThoughts((prev) => [...prev, msg.data]);
              break;
            case "action":
              setActions((prev) => [msg.data, ...prev]);
              break;
          }
        } catch (e) {
          console.error("Error parsing websocket message", e);
        }
      };
    }

    return () => {
       if (ws.current && ws.current.readyState === WebSocket.OPEN) {
          ws.current.close();
       }
    };
  }, []);

  const handleRunTask = async (missionTask: string) => {
    if (!missionTask) return;
    const hostAddress = window.location.host === "localhost:5173" ? "http://localhost:8000" : "";

    await fetch(`${hostAddress}/task/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ task: missionTask }),
    });
  };

  const handleSendMessage = (content: string) => {
    setChatMessages((prev) => [...prev, { role: "user", content }]);
    if (content.toUpperCase().startsWith("RUN:") || content.toUpperCase().startsWith("DEPLOY:")) {
      handleRunTask((content.split(":")[1] || "").trim());
    }
  };

  return (
    <div className="flex h-full w-full pb-24">
      {/* Retractable Left Sidebar */}
      <RetractableSidebar>
        <div className="flex flex-col h-full overflow-y-auto custom-scrollbar p-4 gap-6 bg-surface-50">
           <MissionControl
              messages={chatMessages}
              isThinking={status.state !== "Idle"}
              onSendMessage={handleSendMessage}
           />
           <div className="h-64 shrink-0">
             <LogicStream thoughts={thoughts} />
           </div>
           <div className="h-64 shrink-0">
             <ActionLedger actions={actions} />
           </div>
        </div>
      </RetractableSidebar>

      {/* Main Content Area */}
      <div className="flex-1 p-8 flex flex-col gap-6 overflow-y-auto custom-scrollbar">
        <DashboardHeader
          tps={metrics.tps}
          retry={status.retry}
          inputTokens={metrics.input_tokens}
          outputTokens={metrics.output_tokens}
        />

        <div className="flex-1 bg-white rounded-3xl p-8 shadow-sm border border-slate-200 flex flex-col">
           <div className="mb-6 flex items-center justify-between">
             <div>
               <h2 className="text-2xl font-bold text-slate-800 tracking-tight">Active Missions</h2>
               <p className="text-slate-500 mt-1">Currently running or queued operational tasks.</p>
             </div>
             <div className="bg-blue-50 text-accent px-4 py-2 rounded-xl text-sm font-bold flex items-center gap-2 border border-blue-100">
                <Target size={18} />
                2 Concurrent
             </div>
           </div>

           <div className="grid grid-cols-2 gap-6">
              {/* Mission Card 1 */}
              <div className="border border-slate-200 rounded-2xl p-6 hover:shadow-md transition-shadow relative overflow-hidden group">
                 <div className="absolute top-0 left-0 w-1 h-full bg-accent" />
                 <div className="flex justify-between items-start mb-4">
                    <h3 className="font-bold text-slate-800 text-lg">UI Component Refactor</h3>
                    <span className="bg-amber-100 text-amber-700 text-xs font-bold px-2 py-1 rounded">IN PROGRESS</span>
                 </div>
                 <p className="text-slate-500 text-sm mb-6 line-clamp-2">
                   Analyzing react files to identify duplicate code patterns and extract them into shared atomic components.
                 </p>
                 <div className="flex items-center justify-between mt-auto pt-4 border-t border-slate-100">
                    <div className="flex items-center gap-2 text-slate-400 text-xs font-mono">
                      <Clock size={14} /> 45m elapsed
                    </div>
                    <button className="text-accent hover:text-accent-dark flex items-center gap-1 text-sm font-bold">
                      View Trace <ArrowRight size={16} />
                    </button>
                 </div>
              </div>

              {/* Mission Card 2 */}
              <div className="border border-slate-200 rounded-2xl p-6 hover:shadow-md transition-shadow relative overflow-hidden">
                 <div className="absolute top-0 left-0 w-1 h-full bg-slate-300" />
                 <div className="flex justify-between items-start mb-4">
                    <h3 className="font-bold text-slate-800 text-lg">System Update Prep</h3>
                    <span className="bg-slate-100 text-slate-600 text-xs font-bold px-2 py-1 rounded">QUEUED</span>
                 </div>
                 <p className="text-slate-500 text-sm mb-6 line-clamp-2">
                   Waiting for current operations to finish before initiating environment package updates and tests.
                 </p>
                 <div className="flex items-center justify-between mt-auto pt-4 border-t border-slate-100">
                    <div className="flex items-center gap-2 text-slate-400 text-xs font-mono">
                      <Clock size={14} /> Pending
                    </div>
                 </div>
              </div>

           </div>
        </div>
      </div>
    </div>
  );
}
