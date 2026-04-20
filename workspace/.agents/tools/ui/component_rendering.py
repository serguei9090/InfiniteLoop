"""
Component Rendering Tool - UI Category
Handles UI component rendering and template generation.
"""


class ComponentRenderingTool:
    """
    Tool for UI component rendering and template operations.
    
    Capabilities:
    - Generate HTML templates
    - Render React components (as JSX)
    - Create UI layouts
    - Validate component structure
    """
    
    name = "component_rendering"
    description = "Render UI components, generate HTML templates, and create UI layouts"
    category = "ui"
    
    def __init__(self):
        self.render_count = 0
    
    async def execute(self, args: dict) -> dict:
        """Execute component rendering operation."""
        action = args.get("action", "")
        
        if action == "generate_html":
            return await self._generate_html(args)
        elif action == "render_component":
            return await self._render_component(args)
        elif action == "create_layout":
            return await self._create_layout(args)
        else:
            return {
                "success": False,
                "error": f"Unknown action: {action}"
            }
    
    async def _generate_html(self, args: dict) -> dict:
        """Generate HTML template."""
        template_type = args.get("type", "basic")
        
        templates = {
            "basic": self._get_basic_template(),
            "dashboard": self._get_dashboard_template(),
            "form": self._get_form_template()
        }
        
        if template_type in templates:
            self.render_count += 1
            
            return {
                "success": True,
                "output": templates[template_type],
                "operation": "generate_html",
                "type": template_type
            }
        else:
            return {
                "success": False,
                "error": f"Unknown template type: {template_type}"
            }
    
    async def _render_component(self, args: dict) -> dict:
        """Render a React component."""
        component_name = args.get("name", "")
        props = args.get("props", {})
        
        # Generate JSX representation
        jsx = f"""
<React.Fragment>
  <Component name="{component_name}" {...{props}} />
</React.Fragment>
"""
        
        self.render_count += 1
        
        return {
            "success": True,
            "output": jsx,
            "operation": "render_component",
            "name": component_name
        }
    
    async def _create_layout(self, args: dict) -> dict:
        """Create a UI layout."""
        layout_type = args.get("type", "default")
        
        layouts = {
            "default": self._get_default_layout(),
            "dashboard": self._get_dashboard_layout(),
            "sidebar": self._get_sidebar_layout()
        }
        
        if layout_type in layouts:
            self.render_count += 1
            
            return {
                "success": True,
                "output": layouts[layout_type],
                "operation": "create_layout",
                "type": layout_type
            }
        else:
            return {
                "success": False,
                "error": f"Unknown layout type: {layout_type}"
            }
    
    def _get_basic_template(self) -> str:
        """Get basic HTML template."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Basic Template</title>
</head>
<body>
    <div id="root"></div>
    <script src="/static/bundle.js"></script>
</body>
</html>"""
    
    def _get_dashboard_template(self) -> str:
        """Get dashboard HTML template."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <nav class="sidebar">...</nav>
    <main class="content">
        <header>...</header>
        <div class="dashboard-grid">...</div>
    </main>
    <script src="/static/bundle.js"></script>
</body>
</html>"""
    
    def _get_form_template(self) -> str:
        """Get form HTML template."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Form Template</title>
</head>
<body>
    <form class="form-container">
        <h2>Form Title</h2>
        <div class="form-group">
            <label for="field">Field Label</label>
            <input type="text" id="field" name="field">
        </div>
        <button type="submit">Submit</button>
    </form>
</body>
</html>"""
    
    def _get_default_layout(self) -> str:
        """Get default layout."""
        return """
<div class="layout-container">
    <header class="layout-header">...</header>
    <div class="layout-main">
        <aside class="layout-sidebar">...</aside>
        <main class="layout-content">...</main>
    </div>
    <footer class="layout-footer">...</footer>
</div>"""
    
    def _get_dashboard_layout(self) -> str:
        """Get dashboard layout."""
        return """
<div class="dashboard-layout">
    <nav class="sidebar-nav">
        <ul>
            <li><a href="/dashboard">Dashboard</a></li>
            <li><a href="/projects">Projects</a></li>
            <li><a href="/settings">Settings</a></li>
        </ul>
    </nav>
    <main class="dashboard-main">
        <div class="metrics-grid">...</div>
        <div class="content-area">...</div>
    </main>
</div>"""
    
    def _get_sidebar_layout(self) -> str:
        """Get sidebar layout."""
        return """
<div class="sidebar-layout">
    <aside class="sidebar">
        <div class="logo">...</div>
        <nav class="sidebar-nav">...</nav>
    </aside>
    <main class="main-content">...</main>
</div>"""
