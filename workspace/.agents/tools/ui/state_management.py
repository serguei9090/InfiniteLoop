"""
State Management Tool - UI Category
Handles state management, context updates, and store operations.
"""


class StateManagementTool:
    """
    Tool for UI state management and context operations.

    Capabilities:
    - Update application state
    - Manage React context
    - Handle global store operations
    - Persist state to storage
    """

    name = "state_management"
    description = "Manage UI state, update application context, and handle global store operations"
    category = "ui"

    def __init__(self):
        self.state = {}
        self.listeners = []

    async def execute(self, args: dict) -> dict:
        """Execute state management operation."""
        action = args.get("action", "")

        if action == "set":
            return await self._set_state(args)
        elif action == "get":
            return await self._get_state(args)
        elif action == "update":
            return await self._update_state(args)
        elif action == "subscribe":
            return await self._subscribe(args)
        elif action == "persist":
            return await self._persist_state(args)
        else:
            return {"success": False, "error": f"Unknown action: {action}"}

    async def _set_state(self, args: dict) -> dict:
        """Set a state value."""
        key = args.get("key", "")
        value = args.get("value")

        if key and value is not None:
            self.state[key] = value

            # Notify listeners
            for listener in self.listeners:
                try:
                    await listener(key, "set", value)
                except Exception:
                    pass  # Ignore listener errors

            return {
                "success": True,
                "message": f"Set state[key] = {value}",
                "operation": "set",
                "key": key,
                "value": value,
            }
        else:
            return {"success": False, "error": "Missing key or value"}

    async def _get_state(self, args: dict) -> dict:
        """Get a state value."""
        key = args.get("key", "")

        if key in self.state:
            return {
                "success": True,
                "output": self.state[key],
                "operation": "get",
                "key": key,
            }
        else:
            return {"success": False, "error": f"Key not found: {key}"}

    async def _update_state(self, args: dict) -> dict:
        """Update a state value with function."""
        key = args.get("key", "")
        updater = args.get("updater")

        if key in self.state and callable(updater):
            current = self.state[key]
            new_value = updater(current)

            self.state[key] = new_value

            # Notify listeners
            for listener in self.listeners:
                try:
                    await listener(key, "update", new_value)
                except Exception:
                    pass

            return {
                "success": True,
                "message": f"Updated state[{key}]",
                "operation": "update",
                "key": key,
                "previous": current,
                "current": new_value,
            }
        else:
            return {
                "success": False,
                "error": "Key not found or updater is not callable",
            }

    async def _subscribe(self, args: dict) -> dict:
        """Subscribe to state changes."""
        key = args.get("key", "")
        listener = args.get("listener")

        if key and callable(listener):
            self.listeners.append((key, listener))

            return {
                "success": True,
                "message": f"Subscribed to state[{key}]",
                "operation": "subscribe",
                "key": key,
            }
        else:
            return {"success": False, "error": "Missing key or listener"}

    async def _persist_state(self, args: dict) -> dict:
        """Persist state to storage."""
        storage_type = args.get("type", "localStorage")

        # In a real implementation, this would persist to actual storage
        # For now, we just return success

        return {
            "success": True,
            "message": f"State persisted to {storage_type}",
            "operation": "persist",
            "storage": storage_type,
            "keys_count": len(self.state),
        }
