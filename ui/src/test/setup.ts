import "@testing-library/jest-dom";
import { vi } from "vitest";

// Mock WebSocket
class MockWebSocket {
  onopen: any = null;
  onmessage: any = null;
  onclose: any = null;
  onerror: any = null;
  send = vi.fn();
  close = vi.fn();
}

(global as any).WebSocket = MockWebSocket;
