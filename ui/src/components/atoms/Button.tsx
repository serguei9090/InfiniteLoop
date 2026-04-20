import { ButtonHTMLAttributes, ReactNode } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  children: ReactNode;
  variant?: "primary" | "secondary" | "glass" | "ghost";
  size?: "sm" | "md" | "lg";
}

export const Button = ({
  children,
  variant = "primary",
  size = "md",
  className = "",
  ...props
}: ButtonProps) => {
  const baseStyles =
    "glass-button flex items-center justify-center gap-2 font-black uppercase tracking-widest text-[10px] rounded-xl transition-all";

  const variants = {
    primary: "bg-white text-black hover:bg-neutral-200 shadow-xl",
    secondary:
      "bg-violet-600 text-white hover:bg-violet-500 shadow-lg shadow-violet-500/20",
    glass: "bg-white/5 border border-white/10 text-white hover:bg-white/10",
    ghost: "bg-transparent text-neutral-400 hover:text-white hover:bg-white/5",
  };

  const sizes = {
    sm: "px-4 py-2",
    md: "px-6 py-3",
    lg: "px-10 py-4",
  };

  return (
    <button
      className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};
