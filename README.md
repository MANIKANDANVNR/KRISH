<div align="center">

# 🧠 KRISH

### **Personal AI Assistant • Local-First • Modular • Secure**

*A personal AI engineering project built by Manikandan.*

<br>

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-Desktop_UI-41CD52?style=for-the-badge\&logo=qt\&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_AI-000000?style=for-the-badge)
![Pytest](https://img.shields.io/badge/Pytest-Testing-0A9EDC?style=for-the-badge\&logo=pytest\&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active_Development-orange?style=for-the-badge)

<br>

**Building a personal AI assistant from the ground up — one component at a time.**

</div>

---

## 🚀 What is KRISH?

**KRISH** is a personal AI assistant project created by **Manikandan** to explore the engineering behind modern AI assistants.

Rather than building one large application, KRISH is organized into independent modules for AI reasoning, memory, security, tools, automation, voice, multimodal functionality, storage, observability, testing, and desktop UI.

The project is primarily designed for **local and personal use** and serves as a practical software engineering and AI learning project.

> **KRISH is not intended to be a commercial product. It is a long-term personal engineering project.**

---

# ✨ What KRISH Explores

<table>
<tr>
<td width="50%">

### 🧠 AI Brain

* Local AI model integration
* Provider abstraction
* Context handling
* Response validation
* AI routing

</td>
<td width="50%">

### 🤖 Agent System

* Task planning
* Execution
* Verification
* Recovery
* Tool integration

</td>
</tr>

<tr>
<td>

### 🧠 Memory

* Conversation memory
* Working memory
* Episodic memory
* Long-term memory
* Retrieval

</td>
<td>

### 🔐 Security

* Authentication
* Authorization
* Permissions
* Risk evaluation
* Approval workflows
* Security policies

</td>
</tr>

<tr>
<td>

### 🛠️ Tools

* Calculator
* Python execution
* File operations
* System operations
* Web-related tools

</td>
<td>

### 🖥️ Desktop UI

* Chat interface
* Dashboard
* Agent panel
* Memory panel
* Security panel
* Settings

</td>
</tr>

<tr>
<td>

### 🎙️ Voice

* Voice pipeline
* Voice interaction architecture
* Assistant-oriented audio workflow

</td>
<td>

### 👁️ Multimodal

* Document handling
* Image-related components
* Multimodal architecture

</td>
</tr>
</table>

---

# 🏗️ Architecture

KRISH follows a modular architecture where major responsibilities are separated into dedicated components.

```text
                         ┌──────────────────────┐
                         │       KRISH UI       │
                         │      PySide6         │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Core Runtime    │
                         │ Lifecycle / State    │
                         │ Service Registry     │
                         └──────────┬───────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  │                 │                 │
                  ▼                 ▼                 ▼
           ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
           │    Brain    │  │    Agent    │  │   Memory    │
           │ AI / LLM    │  │ Planning    │  │ Context     │
           │ Providers   │  │ Execution   │  │ Retrieval   │
           └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
                  │                │                │
                  └────────────────┼────────────────┘
                                   │
                                   ▼
                         ┌──────────────────────┐
                         │        Tools         │
                         │ Calculator / Python  │
                         │ Files / System / Web │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Security        │
                         │ Auth / Permissions   │
                         │ Policy / Approval    │
                         └──────────────────────┘

              ┌────────────────┐       ┌────────────────┐
              │     Voice      │       │   Multimodal   │
              └────────────────┘       └────────────────┘

                         ┌──────────────────────┐
                         │       Storage        │
                         │      SQLite DB       │
                         └──────────────────────┘
```

---

# 📂 Project Structure

```text
KRISH/
│
├── agent/             # Agent planning and execution
├── automation/        # Automation components
├── brain/             # AI brain and model providers
├── core/              # Runtime and core services
├── evolution/         # Evolution-related experimental components
├── external_data/     # External data interfaces
├── memory/            # Memory and retrieval
├── multimodal/        # Document and image components
├── observability/     # Health and logging
├── security/          # Authentication and security controls
├── storage/           # Database and persistence
├── testing/           # Testing utilities
├── tests/             # Automated tests
├── tools/             # Assistant tools
├── ui/                # PySide6 desktop interface
├── voice/             # Voice pipeline
│
├── launcher.py        # Application launcher
├── main.py            # Main application entry point
├── pytest.ini         # Pytest configuration
├── requirements.txt   # Python dependencies
└── .env.example       # Environment configuration template
```

---

# 🧰 Technology Stack

| Technology           | Purpose                      |
| -------------------- | ---------------------------- |
| 🐍 **Python**        | Core application development |
| 🧠 **Ollama**        | Local AI model integration   |
| 🖥️ **PySide6**      | Desktop user interface       |
| 🗄️ **SQLite**       | Local persistence            |
| 🧪 **Pytest**        | Automated testing            |
| 🌐 **Requests**      | HTTP communication           |
| ⚙️ **python-dotenv** | Environment configuration    |

---

# 🔐 Security First

Security is a dedicated architectural layer in KRISH rather than an afterthought.

The project contains components for:

```text
Authentication
      ↓
Identity
      ↓
Authorization
      ↓
Permissions
      ↓
Risk Evaluation
      ↓
Approval
      ↓
Tool Execution
      ↓
Audit
```

This architecture is intended to provide controlled access to assistant capabilities and tools.

Security functionality is continuously developed and tested as the project evolves.

---

# 🧠 Memory Architecture

KRISH separates different types of memory rather than storing every piece of information in one place.

```text
                ┌─────────────────┐
                │   Conversation  │
                └────────┬────────┘
                         │
              ┌──────────┼──────────┐
              ▼          ▼          ▼
         Working      Episodic    Long-Term
         Memory       Memory       Memory
              │          │          │
              └──────────┼──────────┘
                         ▼
                    Retrieval
                         │
                         ▼
                     AI Context
```

The goal is to make future development of context-aware personal assistance easier while keeping memory responsibilities modular.

---

# 🤖 Agent Architecture

KRISH includes an agent-oriented execution architecture.

```text
User Request
     │
     ▼
   Intent
     │
     ▼
   Planner
     │
     ▼
Plan Validation
     │
     ▼
   Executor
     │
     ▼
    Tools
     │
     ▼
  Verifier
     │
     ├───────────────┐
     │               │
   Success         Failure
     │               │
     ▼               ▼
  Reporter        Recovery
```

This structure allows individual agent components to be developed and tested independently.

---

# 🎙️ Voice & Multimodal Development

KRISH includes dedicated modules for voice and multimodal functionality.

### Voice

```text
Microphone
    ↓
Voice Pipeline
    ↓
Speech Processing
    ↓
AI Interaction
    ↓
Assistant Response
```

### Multimodal

The project contains components for:

* Document processing
* Image-related functionality
* Multimodal interaction architecture

These areas are under active development.

---

# 🧪 Testing

Testing is a major part of the KRISH development process.

The repository contains dedicated tests for areas including:

* Agent functionality
* Brain functionality
* Core runtime
* Intelligence
* Memory
* Security
* Streaming
* Tools
* Tool integration
* Conversation functionality

Run the test suite with:

```bash
pytest
```

---

# 🛡️ Privacy & Local-First Design

KRISH is designed with personal/local usage in mind.

The repository intentionally excludes runtime and private files such as:

```text
.env
data/
*.db
__pycache__/
.pytest_cache/
.idea/
```

This helps prevent local secrets, databases, generated files, and development-specific configuration from being committed to Git.

---

# 🗺️ Development Roadmap

KRISH is being developed incrementally.

### Current Focus

```text
[████████████████░░░░]  Active Development
```

### Development Areas

* [x] Modular project architecture
* [x] Local AI provider integration
* [x] Memory architecture
* [x] Security architecture
* [x] Agent architecture
* [x] Desktop UI foundation
* [x] Tool architecture
* [x] Automated testing structure
* [x] Voice module foundation
* [x] Multimodal module foundation
* [ ] Further integration and refinement
* [ ] Expanded voice capabilities
* [ ] Expanded multimodal capabilities
* [ ] More advanced automation
* [ ] Cross-device capabilities
* [ ] Continuous architecture improvements

> The roadmap represents development direction, not a claim that every planned feature is currently implemented.

---

# 🎯 Development Philosophy

KRISH follows a simple principle:

> **Build → Test → Integrate → Verify → Improve**

Instead of adding large numbers of features at once, individual components are developed and tested before the architecture is expanded.

The project also avoids automatic uncontrolled self-modification. Improvements are intended to be deliberate and component-specific.

---

# 📊 Project Status

| Category          | Status          |
| ----------------- | --------------- |
| Core Architecture | 🟢 Active       |
| AI Brain          | 🟢 Active       |
| Agent System      | 🟢 Active       |
| Memory            | 🟢 Active       |
| Security          | 🟢 Active       |
| Tools             | 🟢 Active       |
| Desktop UI        | 🟢 Active       |
| Voice             | 🟡 Developing   |
| Multimodal        | 🟡 Developing   |
| Automation        | 🟡 Developing   |
| Evolution         | 🟡 Experimental |

**Version:** `1.0.0`

**Status:** `Active Development`

---

# 💡 Why I Built KRISH

KRISH is more than a personal assistant experiment.

It is a practical way for me to learn and demonstrate:

* Python software architecture
* AI application development
* Local LLM integration
* Agent design
* Memory systems
* Security engineering
* Desktop application development
* Testing
* Debugging
* Git and GitHub
* Modular software design

The project gives me a place to experiment with real engineering problems instead of only building isolated coding exercises.

---

# 👨‍💻 Author

<div align="center">

### **Manikandan**

**B.E. Computer Science and Engineering**

Personal AI • Python • Software Engineering • AI Systems

<br>

[![GitHub](https://img.shields.io/badge/GitHub-MANIKANDANVNR-181717?style=for-the-badge\&logo=github)](https://github.com/MANIKANDANVNR)

</div>

---

# 📜 Disclaimer

KRISH is an independent personal software project created for learning, experimentation, and practical software engineering experience.

It is not affiliated with or endorsed by OpenAI, Google, Microsoft, Meta, Anthropic, Ollama, or any other AI company or organization.

---

<div align="center">

### 🧠 KRISH

**A personal AI project. Built from code. Improved through engineering.**

⭐ If you're interested in the project, feel free to explore the repository.

</div>
