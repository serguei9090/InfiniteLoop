import { ReactNode } from "react";

interface TypographyProps {
  children: ReactNode;
  variant?: "h1" | "h2" | "h3" | "body" | "caption" | "code";
  className?: string;
  weight?: "normal" | "medium" | "semibold" | "bold" | "black";
}

export const Typography = ({
  children,
  variant = "body",
  weight = "normal",
  className = "",
}: TypographyProps) => {
  const baseStyles = "tracking-tight";

  const weights = {
    normal: "font-normal",
    medium: "font-medium",
    semibold: "font-semibold",
    bold: "font-bold",
    black: "font-black",
  };

  const variants = {
    h1: "text-3xl font-display tracking-tight text-white",
    h2: "text-base font-display uppercase tracking-widest text-neutral-300",
    h3: "text-xs font-bold uppercase tracking-widest text-neutral-400",
    body: "text-sm leading-relaxed text-neutral-300",
    caption: "text-[11px] uppercase tracking-widest font-bold text-neutral-500",
    code: "font-mono text-xs leading-normal text-neutral-400",
  };

  const Component =
    variant === "h1" || variant === "h2" || variant === "h3"
      ? variant
      : variant === "code"
        ? "code"
        : "p";

  return (
    <Component
      className={`${baseStyles} ${variants[variant]} ${weights[weight]} ${className}`}
    >
      {children}
    </Component>
  );
};
