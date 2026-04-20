/** @vitest-environment jsdom */
import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import App from "../App";

// Mock Lucide components
vi.mock("lucide-react", () => ({
  Terminal: () => <div data-testid="icon-terminal" />,
  Activity: () => <div data-testid="icon-activity" />,
  Zap: () => <div data-testid="icon-zap" />,
  Shield: () => <div data-testid="icon-shield" />,
  Brain: () => <div data-testid="icon-brain" />,
  Cpu: () => <div data-testid="icon-cpu" />,
  GitBranch: () => <div data-testid="icon-git-branch" />,
  Play: () => <div data-testid="icon-play" />,
  RotateCcw: () => <div data-testid="icon-rotate-ccw" />,
  Layout: () => <div data-testid="icon-layout" />,
  Layers: () => <div data-testid="icon-layers" />,
  MousePointer2: () => <div data-testid="icon-mouse" />,
  Settings: () => <div data-testid="icon-settings" />,
  List: () => <div data-testid="icon-list" />,
  CheckCircle: () => <div data-testid="icon-check" />,
  AlertCircle: () => <div data-testid="icon-alert" />,
  Send: () => <div data-testid="icon-send" />,
  Bot: () => <div data-testid="icon-bot" />,
  User: () => <div data-testid="icon-user" />,
  MessageSquare: () => <div data-testid="icon-msg" />,
}));

describe("App Component", () => {
  it("renders the core dashboard identity", () => {
    render(<App />);
    expect(
      screen.getByRole("heading", { level: 1, name: /IMMUTABLE CORE/i })
    ).toBeInTheDocument();
  });

  it("renders the custom mission control area", () => {
    render(<App />);
    expect(
      screen.getByRole("heading", { name: /Mission Control/i })
    ).toBeInTheDocument();
    expect(
      screen.getByPlaceholderText(/Inject commands or mission parameters/i)
    ).toBeInTheDocument();
  });

  it("renders action ledger and metrics", () => {
    render(<App />);
    expect(
      screen.getByRole("heading", { name: /Action Ledger/i })
    ).toBeInTheDocument();
    expect(screen.getByText(/Throughput/i)).toBeInTheDocument();
  });
});
