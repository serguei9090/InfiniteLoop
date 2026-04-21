import { Route, Routes } from "react-router-dom";
import { FloatingMenu } from "./components/layout/FloatingMenu";
import { DashboardPage } from "./components/pages/DashboardPage";
import { LogsPage } from "./components/pages/LogsPage";
import { SettingsPage } from "./components/pages/SettingsPage";
import { SkillTreePage } from "./components/pages/SkillTreePage";

export default function App() {
	return (
		<div className="h-screen w-full bg-surface-50 flex overflow-hidden relative">
			{/* Main Content Area */}
			<div className="flex-1 relative h-full">
				<Routes>
					<Route path="/" element={<DashboardPage />} />
					<Route path="/logs" element={<LogsPage />} />
					<Route path="/settings" element={<SettingsPage />} />
					<Route path="/skill-tree" element={<SkillTreePage />} />
				</Routes>
			</div>

			{/* Floating Navigation */}
			<FloatingMenu />
		</div>
	);
}
