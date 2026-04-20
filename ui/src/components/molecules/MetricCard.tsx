import { ElementType } from "react";
import { IconWrapper } from "../atoms/IconWrapper";
import { Typography } from "../atoms/Typography";

interface MetricCardProps {
  label: string;
  value: string | number;
  unit?: string;
  icon: ElementType;
  color?: string;
}

export const MetricCard = ({
  label,
  value,
  unit,
  icon,
  color = "text-neutral-500",
}: MetricCardProps) => {
  return (
    <div className="flex flex-col gap-1.5 text-right px-4">
      <div className="flex items-center justify-end gap-2">
        <IconWrapper icon={icon} size="sm" color={color} />
        <Typography variant="h3" className="leading-none text-neutral-400">
          {label}
        </Typography>
      </div>
      <div className="flex items-baseline justify-end gap-1">
        <span
          className={`text-2xl font-black ${color.includes("neutral") ? "text-white" : color} tracking-tight`}
        >
          {value}
        </span>
        {unit && (
          <Typography
            variant="caption"
            className="text-neutral-600 font-medium"
          >
            {unit}
          </Typography>
        )}
      </div>
    </div>
  );
};
