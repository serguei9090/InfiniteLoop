import { RefreshCw, Save } from "lucide-react";
import { useState } from "react";

export function SettingsPage() {
	const [settings, setSettings] = useState({
		provider: "LM Studio",
		apiKey: "",
		model: "gemma-4-e4b",
		url: "http://127.0.0.1:1234/v1",
		autoFetch: true,
	});

	const handleChange = (
		e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>,
	) => {
		const { name, value, type } = e.target as HTMLInputElement;
		const checked = (e.target as HTMLInputElement).checked;

		setSettings((prev) => ({
			...prev,
			[name]: type === "checkbox" ? checked : value,
		}));
	};

	const handleSave = () => {
		// TODO: Connect to backend endpoint
	};

	return (
		<div className="h-full w-full p-8 pb-24 overflow-y-auto bg-surface-50">
			<div className="max-w-4xl mx-auto flex flex-col gap-8">
				<header>
					<h1 className="text-3xl font-bold text-slate-800 tracking-tight">
						Configuration Settings
					</h1>
					<p className="text-slate-500 mt-2">
						Manage LLM providers and core agent parameters.
					</p>
				</header>

				<div className="glass-panel p-8">
					<h2 className="text-xl font-semibold text-slate-800 mb-6 border-b border-slate-100 pb-2">
						LLM Provider
					</h2>

					<div className="grid gap-6 md:grid-cols-2">
						<div className="flex flex-col gap-2">
							<label className="text-sm font-medium text-slate-700">
								Provider
							</label>
							<select
								name="provider"
								value={settings.provider}
								onChange={handleChange}
								className="p-3 bg-white border border-slate-200 rounded-xl outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 transition-all text-slate-700"
							>
								<option value="LM Studio">LM Studio (Local)</option>
								<option value="Ollama">Ollama (Local)</option>
								<option value="OpenAI">OpenAI</option>
								<option value="Anthropic">Anthropic</option>
							</select>
						</div>

						<div className="flex flex-col gap-2">
							<label className="text-sm font-medium text-slate-700">
								API URL
							</label>
							<input
								name="url"
								type="text"
								value={settings.url}
								onChange={handleChange}
								placeholder="http://127.0.0.1:1234/v1"
								className="p-3 bg-white border border-slate-200 rounded-xl outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 transition-all text-slate-700"
							/>
						</div>

						<div className="flex flex-col gap-2 md:col-span-2">
							<label className="text-sm font-medium text-slate-700">
								API Key
							</label>
							<input
								name="apiKey"
								type="password"
								value={settings.apiKey}
								onChange={handleChange}
								placeholder="Leave blank for local providers"
								className="p-3 bg-white border border-slate-200 rounded-xl outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 transition-all text-slate-700"
							/>
						</div>

						<div className="flex flex-col gap-2">
							<label className="text-sm font-medium text-slate-700">
								Model Selector
							</label>
							<div className="relative">
								<input
									name="model"
									type="text"
									value={settings.model}
									onChange={handleChange}
									className="w-full p-3 pr-10 bg-white border border-slate-200 rounded-xl outline-none focus:border-accent focus:ring-2 focus:ring-accent/20 transition-all text-slate-700"
								/>
								<button className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-accent transition-colors">
									<RefreshCw size={16} />
								</button>
							</div>
						</div>

						<div className="flex items-center gap-3 mt-8">
							<input
								name="autoFetch"
								type="checkbox"
								id="autoFetch"
								checked={settings.autoFetch}
								onChange={handleChange}
								className="w-5 h-5 rounded border-slate-300 text-accent focus:ring-accent"
							/>
							<label
								htmlFor="autoFetch"
								className="text-sm font-medium text-slate-700"
							>
								Auto-fetch available models on startup
							</label>
						</div>
					</div>

					<div className="mt-8 flex justify-end">
						<button
							onClick={handleSave}
							className="flex items-center gap-2 bg-accent hover:bg-accent-dark text-white px-6 py-3 rounded-xl font-semibold transition-colors shadow-sm"
						>
							<Save size={18} />
							Save Configuration
						</button>
					</div>
				</div>
			</div>
		</div>
	);
}
