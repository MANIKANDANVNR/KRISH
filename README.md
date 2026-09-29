\# KRISH



\### Personal AI Assistant — Local-First, Secure, and Modular



KRISH is a personal AI assistant project built by \*\*Manikandan\*\* as a learning and engineering project.



The project explores how a modern personal AI assistant can be designed with a modular architecture covering AI reasoning, memory, automation, security, multimodal interaction, voice, observability, and a desktop user interface.



KRISH is designed primarily for \*\*local and personal use\*\*, with an emphasis on privacy, controlled access, modular development, and maintainability.



\---



\## Project Goals



KRISH is being developed to explore:



\* Personal AI assistant architecture

\* Local AI model integration

\* Conversational intelligence

\* Persistent memory

\* Secure tool execution

\* Voice interaction

\* Multimodal capabilities

\* Automation

\* Desktop UI development

\* Testing and observability

\* Modular and maintainable Python architecture



The project is continuously evolving as part of Manikandan's software engineering and AI learning journey.



\---



\## Architecture



KRISH follows a modular Python architecture.



```text

KRISH

│

├── agent/            # Agent planning and execution

├── automation/       # Automation-related components

├── brain/             # AI reasoning and model providers

├── core/              # Core application components

├── evolution/        # Experimental evolution-related components

├── external\_data/    # External data interfaces

├── memory/            # Memory and context management

├── multimodal/       # Multimodal capabilities

├── observability/     # Logging and system observability

├── security/          # Security and access-control components

├── storage/           # Database and persistence layer

├── testing/           # Testing utilities

├── tests/             # Automated tests

├── tools/             # Assistant tools

├── ui/                # Desktop user interface

├── voice/             # Voice-related components

│

├── launcher.py        # Application launcher

├── main.py            # Main application entry point

├── pytest.ini         # Pytest configuration

├── requirements.txt   # Python dependencies

└── .env.example       # Environment configuration template

```



\---



\## Core Technologies



\* \*\*Python\*\*

\* \*\*PySide6\*\*

\* \*\*Ollama\*\*

\* \*\*Pytest\*\*

\* \*\*SQLite\*\*

\* \*\*Requests\*\*

\* \*\*python-dotenv\*\*



The exact capabilities of KRISH may change as individual components are developed and tested.



\---



\## AI Integration



KRISH is designed to work with locally available AI models through an AI provider layer.



The current project uses \*\*Ollama\*\* for local model integration.



This approach allows the assistant architecture to remain separated from the underlying model provider, making the system easier to develop and extend.



\---



\## Memory and Storage



KRISH contains dedicated components for memory and persistent storage.



The project uses a local database for runtime data and persistence.



Private runtime data such as local databases and environment files are intentionally excluded from version control.



\---



\## Security



Security is treated as an important part of the KRISH architecture.



The project contains dedicated security components intended to control access to assistant capabilities and tools.



The goal is to avoid treating every assistant capability as automatically trusted.



Security-related functionality will continue to be tested and improved as the project develops.



\---



\## Voice and Multimodal Development



KRISH contains dedicated modules for:



\* Voice interaction

\* Multimodal functionality

\* User interface integration



These components are part of the broader goal of creating a more natural personal assistant experience.



\---



\## Testing



Testing is an important part of the development process.



KRISH uses \*\*Pytest\*\* and maintains dedicated test directories and testing utilities.



The project is developed incrementally, with functionality being tested as individual components are implemented.



\---



\## Privacy and Local Development



KRISH is intended as a personal project with a local-first approach.



The repository does \*\*not\*\* intentionally include:



\* Environment secrets

\* Local databases

\* Virtual environments

\* IDE configuration

\* Python cache files

\* Runtime logs

\* Temporary files



These files are excluded through `.gitignore`.



\---



\## Development Philosophy



KRISH is being developed incrementally rather than as a single large system.



The development approach focuses on:



1\. Building individual components

2\. Testing them independently

3\. Integrating components carefully

4\. Fixing errors before expanding functionality

5\. Keeping the architecture modular

6\. Improving specific components deliberately



The project is primarily a practical learning and engineering project rather than a commercial product.



\---



\## Project Status



\*\*Version:\*\* `1.0.0`



\*\*Status:\*\* Active Development



KRISH is an evolving project. Some modules are experimental or under active development, and the implementation may change as the architecture matures.



\---



\## Future Direction



Potential future development areas include:



\* Improved conversational memory

\* More robust tool execution

\* Expanded voice interaction

\* Improved multimodal capabilities

\* Better desktop UI

\* Stronger security controls

\* More comprehensive testing

\* Improved automation

\* Additional local AI model support

\* Cross-device memory and conversation synchronization



Future features will be implemented only when they are deliberately developed and tested.



\---



\## Author



\*\*Manikandan\*\*



B.E. Computer Science and Engineering



GitHub: \[@MANIKANDANVNR](https://github.com/MANIKANDANVNR)



\---



\## Disclaimer



KRISH is an independent personal software project created for learning, experimentation, and practical software engineering experience.



It is not affiliated with or endorsed by OpenAI, Google, Microsoft, Meta, Anthropic, Ollama, or any other AI company or organization.



