import { ElementType } from "react";

interface IconWrapperProps {
  icon: ElementType;
  color?: string;
  size?: "xs" | "sm" | "md" | "lg";
  className?: string;
  glow?: boolean;
}

export const IconWrapper = ({
  icon: Icon,
  color = "text-white",
  size = "sm",
  className = "",
  glow = false,
}: IconWrapperProps) => {
  const sizes = {
    xs: "w-3 h-3",
    sm: "w-4 h-4",
    md: "w-6 h-6",
    lg: "w-10 h-10",
  };

  return (
    <div className={`relative flex items-center justify-center ${className}`}>
      {glow && (
        <div
          className={`absolute inset-0 blur-lg opacity-40 animate-pulse ${color.replace("text-", "bg-")}`}
        ></div>
      )}
      <Icon className={`${sizes[size]} ${color} relative z-10`} />
    </div>
  );
};
