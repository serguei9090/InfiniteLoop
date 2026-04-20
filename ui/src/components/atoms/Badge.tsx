import { ReactNode } from "react";

interface BadgeProps {
  children: ReactNode;
  variant?: "success" | "danger" | "warning" | "info" | "neutral";
  className?: string;
}

export const Badge = ({
  children,
  variant = "neutral",
  className = "",
}: BadgeProps) => {
  const styles = {
    success: "bg-emerald-500/10 text-emerald-500 border-emerald-500/20",
    danger: "bg-red-500/10 text-red-500 border-red-500/20",
    warning: "bg-amber-500/10 text-amber-500 border-amber-500/20",
    info: "bg-blue-500/10 text-blue-500 border-blue-500/20",
    neutral: "bg-white/5 text-neutral-400 border-white/5",
  };

  return (
    <span
      className={`text-[9px] font-black px-2 py-0.5 rounded-md border backdrop-blur-sm ${styles[variant]} ${className}`}
    >
      {children}
    </span>
  );
};
