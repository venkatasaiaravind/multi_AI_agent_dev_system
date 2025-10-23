# 🤖 Multi AI Agent Development System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.76.0+-orange.svg)](https://github.com/joaomdmoura/crewAI)

> **Transform your IDEAS into complete software projects** - From concept to production-ready code in minutes using 80+ specialized AI agents working collaboratively.

## 🌟 Overview

The **Multi AI Agent Development System** is an advanced, autonomous software development platform that leverages multiple AI agents to create complete, production-ready projects across 40+ technology domains. Built on CrewAI framework, it orchestrates specialized agents—each with unique expertise—to collaborate like a real development team.

### ✨ Key Features

- 🤖 **80+ Specialized AI Agents** - System architects, developers, QA engineers, security experts, and more
- 💰 **100% FREE Models** - Uses only free API models from OpenRouter and Groq (DeepSeek, Qwen, Nemotron)
- 🚀 **40+ Project Templates** - Web/Mobile apps, AI/ML systems, Blockchain, IoT, FinTech, Healthcare, Gaming
- 🎯 **End-to-End Automation** - From requirements to deployment-ready code
- 🔧 **Smart Orchestration** - Master orchestrator coordinates agent teams based on project needs
- 📊 **Quality Assurance** - Built-in testing, security auditing, and performance optimization
- 📁 **Organized Workspaces** - Automatic project structure generation with best practices

## 🏗️ Architecture

The system follows a hierarchical multi-agent architecture:

```
Master Orchestrator
    ├── Project Planning & Analysis
    ├── Agent Team Assembly (Dynamic based on project type)
    ├── Task Distribution & Coordination
    └── Quality Control & Delivery
```

### 🎭 Agent Categories

| Category | Agents | Expertise |
|----------|---------|-----------|
| **Strategic** | Master Orchestrator, Project Manager, System Architect | High-level planning, architecture design |
| **Development** | Backend/Frontend/Mobile Developers, DevOps Engineer | Code implementation across platforms |
| **Specialized** | AI/ML Engineers, Blockchain Developers, IoT Specialists | Domain-specific implementations |
| **Quality** | QA Engineers, Security Auditors, Performance Engineers | Testing, security, optimization |
| **Data** | Data Scientists, ML Engineers, Data Engineers | AI/ML, data pipelines, analytics |

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- OpenRouter API key (free tier)
- Groq API key (free tier)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/multi_AI_agent_dev_system.git
cd multi_AI_agent_dev_system
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the root directory:
```env
OPENROUTER_API_KEY=your_openrouter_api_key
GROQ_API_KEY=your_groq_api_key
WORKSPACE_DIR=workspace
```

To get free API keys:
- **OpenRouter**: Visit [openrouter.ai](https://openrouter.ai) and sign up
- **Groq**: Visit [console.groq.com](https://console.groq.com) and sign up

4. **Run the system**
```bash
python main.py
```

## 💻 Usage

### Interactive Mode

When you run `python main.py`, you'll see a menu of project categories:

```
🌐 Web & Mobile Applications
🤖 AI & Machine Learning
🔗 Blockchain & Web3
🏭 IoT & Industrial
💳 FinTech & Business
🏥 Healthcare & Education
🎮 Gaming & Entertainment
```

### Example: Creating a Web Application

```
1. Select category: Web & Mobile Applications
2. Choose project type: web_application
3. Describe your project: "Create a task management app with user authentication, 
   real-time updates, and a modern React frontend with Node.js backend"
4. Sit back and watch the agents work!
```

### Programmatic Usage

```python
from core.master_orchestrator import MasterOrchestrator
import asyncio

async def create_project():
    orchestrator = MasterOrchestrator()
    
    project_requirements = {
        "type": "web_application",
        "description": "Task management app with real-time collaboration",
        "custom_requirements": {
            "frontend": "React with TypeScript",
            "backend": "Node.js with Express",
            "database": "MongoDB",
            "features": ["authentication", "real-time updates", "file uploads"]
        }
    }
    
    result = await orchestrator.create_project(project_requirements)
    print(f"Project completed: {result['status']}")

asyncio.run(create_project())
```

## 📂 Project Structure

```
multi_AI_agent_dev_system/
├── config/
│   ├── __init__.py
│   └── model_config.py          # AI model configurations for different roles
├── core/
│   ├── __init__.py
│   ├── agent_factory.py         # Basic agent creation
│   ├── comprehensive_agent_factory.py  # 80+ specialized agents
│   └── master_orchestrator.py   # Main orchestration engine
├── tools/
│   ├── __init__.py
│   └── file_operations.py       # File I/O tools for agents
├── test/
│   ├── test_1.py
│   ├── test_api_calling.py
│   ├── test_comprehensive_agents.py
│   ├── test_enhanced_agents.py
│   └── test_master_orchestrator.py
├── logs/                        # System logs
├── workspace/                   # Generated projects
├── main.py                      # Entry point
├── requirements.txt
├── LICENSE
└── README.md
```

## 🎯 Supported Project Types

### Web & Mobile Applications
- Modern web applications (React/Vue + Node.js)
- Progressive Web Apps (PWA)
- Mobile apps (React Native, iOS, Android)
- E-commerce platforms

### AI & Machine Learning
- Computer vision systems
- Natural language processing
- Predictive analytics
- Recommendation engines
- Chatbots and conversational AI

### Blockchain & Web3
- DeFi platforms with smart contracts
- NFT marketplaces
- Cryptocurrency wallets
- DAOs (Decentralized Autonomous Organizations)

### IoT & Industrial
- Smart home automation
- Industrial monitoring systems
- Agricultural technology
- Supply chain tracking

### FinTech & Business
- Payment processing systems
- Algorithmic trading platforms
- Personal finance apps
- ERP systems

### Healthcare & Education
- Telemedicine platforms
- Electronic health records (EHR)
- Learning management systems (LMS)
- Educational assessment platforms

### Gaming & Entertainment
- Multiplayer video games
- Streaming platforms
- Social media applications
- AR/VR experiences

## 🔧 Configuration

### Model Configuration

The system uses different AI models optimized for specific roles:

| Role | Model | Provider | Configuration |
|------|-------|----------|---------------|
| Master Orchestrator | DeepSeek Chat v3.1 | OpenRouter | Reasoning: Medium effort |
| System Architect | DeepSeek Chat v3.1 | OpenRouter | Reasoning: High effort |
| Backend Developer | Qwen3 Coder | OpenRouter | Max tokens: 1000 |
| Frontend Developer | Qwen3 Coder | OpenRouter | Max tokens: 1000 |
| Senior Developer | Nemotron Nano 9B v2 | OpenRouter | Reasoning: Medium effort |

You can customize these in `config/model_config.py`.

### Workspace Configuration

Set your workspace directory in `.env`:
```env
WORKSPACE_DIR=workspace  # Default: workspace/
```

Generated projects are organized as:
```
workspace/
└── project_<id>_<timestamp>/
    ├── src/
    ├── tests/
    ├── docs/
    ├── config/
    └── README.md
```

## 🧪 Testing

Run the test suite:

```bash
# Test API connectivity
python test/test_api_calling.py

# Test agent creation
python test/test_comprehensive_agents.py

# Test orchestration
python test/test_master_orchestrator.py

# Run all tests
python -m pytest test/
```

## 📊 Performance & Limitations

### Performance Metrics
- Average project generation time: 3-10 minutes
- Supports concurrent agent execution
- Built-in rate limiting for API compliance

### Current Limitations
- Free tier API rate limits apply
- Complex enterprise projects may require manual refinement
- Generated code requires review before production deployment
- Some specialized domains may need additional expert input

## 🔒 Security & Best Practices

- All API keys are stored securely in `.env` (never committed to version control)
- Generated code includes security best practices
- Security auditor agent reviews critical components
- Regular dependency updates recommended

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Add tests for new features
- Update documentation as needed
- Ensure all tests pass before submitting PR

## 🐛 Troubleshooting

### Common Issues

**Issue: "API keys not found"**
```bash
# Solution: Check your .env file
cat .env  # Should show OPENROUTER_API_KEY and GROQ_API_KEY
```

**Issue: "Module not found"**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --upgrade
```

**Issue: "Rate limit exceeded"**
```bash
# Solution: Free tier limits apply. Wait a few minutes and try again.
# Consider spacing out complex projects.
```

**Issue: Windows encoding errors**
```bash
# Solution: The system auto-configures UTF-8 encoding on Windows.
# If issues persist, run: chcp 65001
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 venkatasaiaravind

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

## 🙏 Acknowledgments

- **CrewAI** - For the excellent multi-agent framework
- **OpenRouter** - For providing free access to powerful AI models
- **Groq** - For lightning-fast inference with free tier access
- **DeepSeek, Qwen, NVIDIA** - For open-source AI models

## 📞 Contact & Support

- **GitHub**: [venkatasaiaravind](https://github.com/venkatasaiaravind)
- **Issues**: [Report bugs or request features](https://github.com/yourusername/multi_AI_agent_dev_system/issues)

## 🗺️ Roadmap

- [ ] Add support for more AI model providers
- [ ] Implement real-time progress tracking dashboard
- [ ] Add code review and optimization agents
- [ ] Support for cloud deployment automation (AWS, GCP, Azure)
- [ ] Integration with version control systems (Git workflows)
- [ ] Multi-language support for generated documentation
- [ ] Agent learning from past project successes

## 📈 Stats

- **80+** Specialized AI agents
- **40+** Supported technologies
- **10+** Project categories
- **100%** Free to use

---

<div align="center">

**Made with ❤️ by developers, for developers**

⭐ Star this repo if you find it useful! ⭐

</div>
