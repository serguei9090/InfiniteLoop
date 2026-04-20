import { ReactNode } from "react";

interface MainLayoutProps {
  header: ReactNode;
  content: ReactNode;
  sidebar: ReactNode;
  footer: ReactNode;
}

export const MainLayout = ({
  header,
  content,
  sidebar,
  footer,
}: MainLayoutProps) => {
  return (
    <div className="flex h-screen bg-neutral-950 text-neutral-100 font-sans selection:bg-violet-500/30 overflow-hidden">
      <div className="flex-1 flex flex-col p-[clamp(1rem,3vw,3rem)] gap-[clamp(1rem,2vw,2rem)] overflow-hidden">
        {header}
        <div className="flex-1 min-h-0">{content}</div>
        {footer}
      </div>
      {sidebar}
    </div>
  );
};
