import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class BeadsTracker:
    def __init__(self, workspace_root: str = "."):
        self.beads_dir = Path(workspace_root) / ".beads"
        self.issues_file = self.beads_dir / "issues.jsonl"
        self._ensure_setup()

    def _ensure_setup(self):
        if not self.beads_dir.exists():
            self.beads_dir.mkdir(parents=True, exist_ok=True)
        if not self.issues_file.exists():
            self.issues_file.touch()

    def _generate_id(self) -> str:
        # Beads uses a short ID format, let's use a short uuid
        return f"ai-{uuid.uuid4().hex[:6]}"

    def _read_all(self) -> List[Dict[str, Any]]:
        lines = []
        if not self.issues_file.exists():
            return lines

        with open(self.issues_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        lines.append(json.loads(line))
                    except json.JSONDecodeError:
                        logger.warning(f"Failed to parse line in issues.jsonl: {line}")
        return lines

    def _write_all(self, items: List[Dict[str, Any]]):
        with open(self.issues_file, "w", encoding="utf-8") as f:
            for item in items:
                f.write(json.dumps(item) + "\n")

    def get_open_issues(self) -> List[Dict[str, Any]]:
        items = self._read_all()
        return [
            item
            for item in items
            if item.get("_type") == "issue"
            and item.get("status") in ["open", "in_progress"]
        ]

    def add_issue(self, title: str, description: str = "") -> str:
        items = self._read_all()
        issue_id = self._generate_id()
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        new_issue = {
            "_type": "issue",
            "id": issue_id,
            "title": title,
            "description": description,
            "status": "open",
            "priority": 2,
            "issue_type": "task",
            "assignee": "ai-agent",
            "owner": "ai-agent",
            "created_at": now,
            "created_by": "ai-agent",
            "updated_at": now,
            "dependency_count": 0,
            "dependent_count": 0,
            "comment_count": 0,
        }

        items.append(new_issue)
        self._write_all(items)
        logger.info(f"Added new Beads issue: {issue_id} - {title}")
        return issue_id

    def update_status(
        self, issue_id: str, status: str, close_reason: Optional[str] = None
    ):
        items = self._read_all()
        updated = False
        now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        for item in items:
            if item.get("_type") == "issue" and item.get("id") == issue_id:
                item["status"] = status
                item["updated_at"] = now
                if status in ["closed", "done", "failed"]:
                    item["closed_at"] = now
                    if close_reason:
                        item["close_reason"] = close_reason
                    elif status == "failed":
                        item["close_reason"] = "Task failed"
                    else:
                        item["close_reason"] = "Completed"
                updated = True
                break

        if updated:
            self._write_all(items)
            logger.info(f"Updated Beads issue {issue_id} to status: {status}")
        else:
            logger.warning(f"Beads issue {issue_id} not found for status update")
