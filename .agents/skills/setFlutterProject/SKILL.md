---
name: setFlutterProject
description: Sets up a new Flutter project or enhances an existing one with the "Universal Kit" (Riverpod, GoRouter, Very Good Analysis, etc.) ensuring AI "Vibe Coding" compatibility.
---

# setFlutterProject Skill

This skill guides you through setting up a Flutter project using the **Universal Kit** stack. It ensures that every project starts with a robust, scalable, and AI-friendly foundation.

## 📚 References

- **Tech Stack & Universal Kit**: [tech_stack.md](references/tech_stack.md) - Contains the mandatory list of packages and tools.

## 🛠️ Usage

Use this skill when:
- The user asks to "setup flutter base".
- The user asks to "create a new flutter project".
- The user asks to "add the universal kit" to an existing project.
- You need to ensure a project complies with the "Vibe Coding" standards.

## 🚀 Workflow Steps

### 1. Prerequisite Check & Setup
Before getting started, ensure the environment is ready.

1.  **Check for Very Good CLI**:
    ```bash
    very_good --version
    ```
    If not installed, install it:
    ```bash
    dart pub global activate very_good_cli
    ```

2.  **Check for FVM** (Optional but recommended):
    If the user mentioned FVM or version management, ensure it's used.

### 2. Project Creation (New Projects)
If creating a NEW project, use `very_good_cli` as the foundation.

```bash
very_good create fluttering_app <project_name> --desc "<description>" --org <org_name>
```
*Note: Replace `<project_name>`, `<description>`, and `<org_name>` with appropriate values.*

### 3. "Universal Kit" Installation (Mandatory)
For **EVERY** project (new or existing), you must ensure the following packages are installed. Run these commands in the project root:

**Core Dependencies:**


*Option A: Bloc (Preferred)*
```bash
flutter pub add flutter_bloc bloc equatable go_router
```

*Option B: Riverpod*
```bash
flutter pub add flutter_riverpod riverpod_annotation go_router
```

**Dev Dependencies:**
```bash
# Common
flutter pub add --dev very_good_analysis build_runner

# If using Bloc
flutter pub add --dev bloc_test

# If using Riverpod
flutter pub add --dev riverpod_generator custom_lint riverpod_lint
```

**Integration Testing:**
```bash
# Verify if patrol is needed/requested, as it requires native setup
# patrol test
```

### 4. Configuration & "Vibe Coding" Audit

1.  **Analysis Options**: Ensure `analysis_options.yaml` uses `very_good_analysis`.
    ```yaml
    include: package:very_good_analysis/analysis_options.yaml
    analyzer:
      exclude:
        - "**/*.g.dart"
        - "**/*.freezed.dart"
    ```

2.  **Formatter**: Run the formatter to ensure style compliance.
    ```bash
    dart format .
    ```

3.  **State Management Setup**:

    - **Bloc**: Ensure `MultiBlocProvider` is set up if using global providers, or prepare your `BlocObserver` for logging.
    - **Riverpod**: Ensure a `ProviderScope` wraps the app in `main.dart`.

### 5. Supplemental Libraries (The Ecosystem)
Consult [tech_stack.md](references/tech_stack.md) for additional needs:
- **UI**: `flutter_animate`, `rive`, `flex_color_scheme`, `google_fonts`.
- **Data**: `dio`, `retrofit`, `isar`, `shared_preferences`.
- **System**: `path_provider`, `url_launcher`, `permission_handler`.

## 🤖 Automating with Scripts
You can use the helper script to fast-track dependency installation:

- **Windows (PowerShell)**: 
  ```powershell
  .agent/skills/setFlutterProject/scripts/setup_dependencies.ps1 -StateManagement Bloc
  # OR
  .agent/skills/setFlutterProject/scripts/setup_dependencies.ps1 -StateManagement Riverpod
  ```

## ✅ Verification
After setup, run:
1.  `flutter pub get`
2.  `dart run build_runner build -d` (if using generators)
3.  `flutter test` (to ensure base tests pass)
