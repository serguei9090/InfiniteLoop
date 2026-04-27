import os
import logging
from typing import Dict, List, Optional
from config import settings
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class AIProvider(BaseModel):
    name: str
    url: str
    api_key: str
    categories: List[str]  # coding, chat, handoff


class MultiAIManager:
    def __init__(self):
        self.providers: Dict[str, AIProvider] = {
            "gemini": AIProvider(
                name="gemini",
                url=os.environ.get(
                    "GOOGLE_API", "https://generativelanguage.googleapis.com/v1beta"
                ),
                api_key=os.environ.get("GEMINI_API_KEY", ""),
                categories=["coding", "chat"],
            ),
            "codex": AIProvider(
                name="codex",
                url="http://localhost:8001/v1",
                api_key="codex",
                categories=["coding"],
            ),
            "qwen": AIProvider(
                name="qwen",
                url="http://localhost:8002/v1",
                api_key="qwen",
                categories=["chat", "handoff"],
            ),
            "jules": AIProvider(
                name="jules",
                url="http://localhost:8003/v1",
                api_key="jules",
                categories=["coding", "chat"],
            ),
            "local": AIProvider(
                name="local",
                url=settings.llm_base_url,
                api_key="lm-studio",
                categories=["coding", "chat", "handoff"],
            ),
            "mock": AIProvider(
                name="mock",
                url="http://localhost:8000/api/mock-ai",
                api_key="mock",
                categories=["coding", "chat", "handoff"],
            ),
        }
        self.primary_provider = "local"
        self.backup_provider = "gemini"

    def get_provider_for_category(self, category: str) -> Optional[AIProvider]:
        for name, provider in self.providers.items():
            if category in provider.categories:
                return provider
        return None

    def get_failover_provider(self) -> AIProvider:
        return self.providers.get(self.backup_provider, self.providers["local"])

    def route_task(self, task: str, category: str = "coding") -> AIProvider:
        provider = self.get_provider_for_category(category)
        if provider:
            logger.info(f"Routing task to {provider.name} for category {category}")
            return provider

        logger.warning(
            f"No provider found for category {category}, falling back to {self.primary_provider}"
        )
        return self.providers[self.primary_provider]
