# Technology Stack & Universal Kit

## **1. 💎 The Universal Kit (Mandatory for ALL Projects)**

These are the non-negotiable tools. You must install/configure these in **every single Flutter project** (Game, App, or Tool) to ensure code quality and AI "Vibe Coding" compatibility.

| Category                | The Tool                     | Why?                                                                                         | Installation                                           |
| :---------------------- | :--------------------------- | :------------------------------------------------------------------------------------------- | :----------------------------------------------------- |
| **Linting**             | **very_good_analysis**     | Stricter than standard lints. Forces you (and AI agents) to write clean, bug-free code.      | `flutter pub add --dev very_good_analysis`            |
| **State Management**    | **Bloc** (Preferred) or **Riverpod** | Industry standards. **Bloc**: strict, testable (use `flutter_bloc`). **Riverpod**: flexible (use `riverpod_generator`). | `flutter pub add flutter_bloc` OR `flutter pub add flutter_riverpod` |
| **Navigation**          | **GoRouter**                 | Handles URL-based routing and Deep Links (e.g., myapp://quiz/123) on Android & Desktop.      | `flutter pub add go_router`                             |
| **Unit Testing**        | **flutter_test**            | Built-in test runner. Runs instantly on the Dart VM (no emulator needed).                    | *(Included in SDK)*                                    |
| **Integration Testing** | **Patrol**                   | The *only* tool that can click "Native" dialogs (Permissions, Notifications) on Android/iOS. | `patrol test`                                            |
| **Code Formatter**      | **Dart Format**              | Auto-formats code on save. Prevents "bike-shedding" about style.                             | `dart format .`                                          |

## **2. 📦 The Flutter Ecosystem Library**

Reference this list when looking for specific capabilities.

### **UI & Animation**

* **flutter_animate**: The easiest way to add effects (fade, slide, shake) to widgets.
* **rive**: For high-quality interactive vector animations (like Duolingo characters).
* **flex_color_scheme**: Generates beautiful color themes based on a single primary color.
* **google_fonts**: Hot-load fonts directly from Google Fonts.

### **Data & Networking**

* **dio**: The powerful HTTP client (replaces http). Supports interceptors and global config.
* **retrofit**: Generates type-safe API clients from your Dio interfaces (Agent friendly).
* **isar**: Super fast NoSQL local database. Great for storing quiz history offline.
* **shared_preferences**: Simple storage for small flags (e.g., "Dark Mode: On").

### **System Integration**

* **path_provider**: Find where to save files on Android vs. Windows.
* **url_launcher**: Open web links in the browser.
* **permission_handler**: Request Camera/Mic permissions cleanly.


## **3. 🐍 Backend Partners (Non-Dart)**

Only use these when the project requires Python libraries (like your Log Analysis app).

| Tool | Role | Official URL |
| :---- | :---- | :---- |
| **FastAPI** | High-performance Python API framework. | [fastapi.tiangolo.com](https://fastapi.tiangolo.com/) |
| **Uvicorn** | The server runner for FastAPI. | [uvicorn.org](https://www.uvicorn.org/) |
| **Drain3** | The Log Template Miner (Reason for using Python). | [github.com/logpai/drain3](https://github.com/logpai/drain3) |

## **4. 🕵️ Quality Control & DevOps**

Tools to ensure your app doesn't break.

| Tool              | Command / Usage          | Purpose                                                                                      |
| :---------------- | :----------------------- | :------------------------------------------------------------------------------------------- |
| **SonarQube**     | sonar-scanner            | Static analysis server. Tracks code smells and tech debt over time.                          |
| **LCOV**          | `flutter test --coverage` | Generates the code coverage report that SonarQube reads.                                     |
| **Very Good CLI** | `very_good create ...`    | Scaffolds new projects with all best practices pre-configured.                               |
| **FVM**           | `fvm use 3.27.0`           | **Flutter Version Manager**. Lets you use different Flutter versions for different projects. |
