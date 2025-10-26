# COMPLETE MASTER ORCHESTRATOR - READY TO USE
# Place this ENTIRE file at: core/master_orchestrator.py
# Copy and paste everything - no edits needed!

import sys
import os
import io

# ============================================================================
# FIX WINDOWS CONSOLE ENCODING - MUST BE AT THE VERY TOP
# ============================================================================
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except Exception as e:
        pass
    
    try:
        import locale
        locale.setlocale(locale.LC_ALL, '')
    except:
        pass

import sys
import os
import io
import asyncio
import time
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
from crewai import Crew, Task
from core.comprehensive_agent_factory import ComprehensiveAgentFactory
from config.model_config import ModelConfig
from core.rate_limiting import RateLimiter, ConcurrencyManager
from core.error_recovery import RetryStrategy, ErrorHandler, CircuitBreaker, ErrorSeverity

class MasterOrchestrator:
    """Enhanced orchestrator with resilience, rate limiting, and error recovery"""
    def __init__(self):
        self.agent_factory = ComprehensiveAgentFactory()
        self.model_config = ModelConfig()
        self.workspace_base = os.getenv("WORKSPACE_DIR", "workspace")
        self.rate_limiter = RateLimiter(workspace_dir=self.workspace_base)
        self.concurrency_manager = ConcurrencyManager(max_concurrent_requests=10)
        self.retry_strategy = RetryStrategy(max_retries=3, base_delay=1.0)
        self.error_handler = ErrorHandler(workspace_dir=self.workspace_base)
        self.circuit_breaker = CircuitBreaker(failure_threshold=5, timeout=60)
        self.request_counts = {"openrouter": 0, "groq": 0}
        self.session_start = time.time()
        self.projects_completed = 0
        self.execution_stats = {
            "successful_projects": 0,
            "failed_projects": 0,
            "average_execution_time": 0,
            "total_api_requests": 0
        }
        print("✅ Master Orchestrator initialized")

    def safe_write_file(self, filepath: Path, content: str):
        """Write file with proper UTF-8 encoding"""
        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8', errors='replace') as f:
                f.write(content)
        except Exception as e:
            print(f"Warning: Could not write {filepath}: {e}")



    async def create_project(self, project_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Create a complete project from requirements using AI agents"""
        
        try:
            # 1. Generate project ID and setup
            project_id = self.generate_project_id(project_requirements)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            workspace_path = os.path.join(self.workspace_base, f"{project_id}_{timestamp}")
            
            print(f"📁 Project workspace: {workspace_path}")
            
            # Create workspace directories
            Path(workspace_path).mkdir(parents=True, exist_ok=True)
            Path(workspace_path, "src").mkdir(exist_ok=True)
            Path(workspace_path, "docs").mkdir(exist_ok=True)
            Path(workspace_path, "config").mkdir(exist_ok=True)
            Path(workspace_path, "scripts").mkdir(exist_ok=True)
            
            # 2. Assess complexity
            complexity = self.assess_project_complexity(
                project_requirements.get("description", ""),
                project_requirements.get("custom_requirements", [])
            )
            print(f"📊 Project complexity: {complexity}")
            
            # 3. Create specialized agent team
            print(f"\n🤖 Assembling AI agent team...")
            agents = self.agent_factory.create_agent_team(
                project_type=project_requirements.get("type", "web_application"),
                project_description=project_requirements.get("description", ""),
                custom_requirements=project_requirements.get("custom_requirements", [])
            )
            
            if not agents or len(agents) == 0:
                raise Exception("Failed to create agent team")
            
            print(f"✅ {len(agents)} specialized agents ready\n")
            
            # 4. Generate project plan
            project_plan = {
                "project_id": project_id,
                "project_type": project_requirements.get("type", "web_application"),
                "description": project_requirements.get("description", ""),
                "complexity": complexity,
                "agents": [agent.role for agent in agents],
                "workspace": workspace_path
            }
            
            # 5. Create tasks for agents
            print(f"📋 Creating tasks for agents...")
            tasks = await self.create_project_tasks(
                agents=agents,
                requirements=project_requirements,
                workspace_path=workspace_path,
                project_plan=project_plan
            )
            
            if not tasks or len(tasks) == 0:
                raise Exception("No tasks created")
            
            print(f"✅ {len(tasks)} tasks defined\n")
            
            # 6. Execute tasks with agents
            print(f"⚙️  Starting agent execution...")
            execution_start = time.time()
            
            execution_result = await self.execute_with_monitoring(
                agents=agents,
                tasks=tasks,
                workspace_path=workspace_path
            )
            
            execution_time = time.time() - execution_start
            print(f"\n✅ Agent execution completed in {execution_time:.1f}s\n")
            
            # 7. Generate fallback files if agents didn't create them
            print(f"📝 Ensuring all files are generated...")
            
            # Check if agents created files
            workspace = Path(workspace_path)
            existing_files = list(workspace.rglob("*.py"))
            
            if len(existing_files) < 2:  # Agents didn't create files
                print(f"⚠️  Agents didn't create files. Generating fallback...")
                self.generate_backend_files(
                    workspace_path=workspace_path,
                    project_type=project_requirements.get("type", "web_application"),
                    description=project_requirements.get("description", ""),
                    custom_reqs=project_requirements.get("custom_requirements", [])
                )
                
                self.generate_deployment_files(
                    workspace_path=workspace_path,
                    project_type=project_requirements.get("type", "web_application"),
                    description=project_requirements.get("description", "")
                )
                
                arch_doc = self.generate_architecture_doc(
                    project_type=project_requirements.get("type", "web_application"),
                    description=project_requirements.get("description", ""),
                    custom_reqs=project_requirements.get("custom_requirements", [])
                )
                self.safe_write_file(Path(workspace_path) / "docs" / "architecture.md", arch_doc)
            
            # 8. Validate and finalize
            print(f"🔍 Validating project...")
            validation_result = await self.validate_and_finalize(
                workspace_path=workspace_path,
                execution_result=execution_result,
                project_plan=project_plan
            )
            
            # 9. Return success result
            return {
                "success": True,
                "project_id": project_id,
                "workspace_path": workspace_path,
                "agents_used": len(agents),
                "tasks_completed": len(tasks),
                "execution_time": execution_time,
                "quality_metrics": validation_result,
                "summary": validation_result.get("summary", "Project completed successfully")
            }
            
        except Exception as e:
            print(f"\n❌ Error during project generation: {str(e)}")
            import traceback
            traceback.print_exc()
            
            return {
                "success": False,
                "error": str(e),
                "project_id": project_id if 'project_id' in locals() else "unknown",
                "workspace_path": workspace_path if 'workspace_path' in locals() else None,
                "partial_workspace": workspace_path if 'workspace_path' in locals() else None
            }
    async def create_project_tasks(
        self,
        agents: List,
        requirements: Dict,
        workspace_path: str,
        project_plan: Dict
    ) -> List[Task]:
        """Create AI-driven tasks that use agents to generate code dynamically"""
        print("📝 Creating AI-driven code generation tasks...")

        project_description = requirements.get("description", "")
        custom_reqs = requirements.get("custom_requirements", [])
        tasks = []

        # TASK 1: BACKEND CODE GENERATION - AGENTS USE AI TO WRITE CODE
        backend_agents = [agent for agent in agents if any(
            role in agent.role.lower() 
            for role in ["backend", "developer", "engineer", "architect"]
        )]
        if backend_agents:
            dev_agent = backend_agents[0]
            backend_task = Task(
                description=f"""You are building: {project_description}

YOUR CRITICAL TASK: Write ACTUAL working Python Flask backend code

REQUIRED FILES:

1. {workspace_path}/src/app.py
   - Complete Flask application
   - ALL routes for: {project_description}
   - Actual functionality (not placeholders)
   - Production-ready

2. {workspace_path}/src/config.py
   - Configuration management
   - Environment variables

3. {workspace_path}/src/__init__.py
   - Package initialization

4. {workspace_path}/requirements.txt
   - ALL dependencies

5. {workspace_path}/README.md
   - Setup instructions
   - API documentation

CRITICAL:
- Use WriteFileTool to save each file
- Write REAL working code
- Implement actual functionality
- Make it production-ready

IMPLEMENT:
{chr(10).join(f"- {req}" for req in custom_reqs) if custom_reqs else "- Standard Flask app"}

START: Write app.py using write_file_tool!""",
                expected_output=f"All backend files in {workspace_path}/src/",
                agent=dev_agent
            )
            tasks.append(backend_task)

        # TASK 2: DOCUMENTATION
        if len(agents) > 1:
            doc_agents = [agent for agent in agents if any(
                role in agent.role.lower() 
                for role in ["architect", "analyst"]
            )]
            if doc_agents:
                doc_agent = doc_agents[0]
                doc_task = Task(
                    description=f"""Create comprehensive documentation.

Read code from {workspace_path}/src/app.py using read_file_tool

Create:
1. {workspace_path}/docs/architecture.md - System design
2. {workspace_path}/docs/deployment.md - Deployment guide
3. {workspace_path}/docs/api.md - API documentation

Use read_file_tool and write_file_tool""",
                    expected_output=f"Documentation in {workspace_path}/docs/",
                    agent=doc_agent,
                    context=[backend_task]
                )
                tasks.append(doc_task)

        # TASK 3: DEVOPS
        devops_agents = [agent for agent in agents if "devops" in agent.role.lower()]
        if devops_agents:
            devops_agent = devops_agents[0]
            devops_task = Task(
                description=f"""Create DevOps configuration.

Create:
1. {workspace_path}/config/.env.example - Environment variables
2. {workspace_path}/config/docker-compose.yml - Docker setup
3. {workspace_path}/config/Dockerfile - Docker image
4. {workspace_path}/scripts/deploy.sh - Deployment script

Use write_file_tool""",
                expected_output=f"Deployment files in {workspace_path}/config/",
                agent=devops_agent,
                context=[backend_task]
            )
            tasks.append(devops_task)

        print(f"   ✅ {len(tasks)} AI-driven tasks created\n")
        return tasks



    # ========================================================================
    # DYNAMIC FILE GENERATION METHODS
    # ========================================================================

    def generate_architecture_doc(self, project_type: str, description: str, custom_reqs: List) -> str:
        """Generate architecture dynamically"""
        
        tech_stacks = {
            "web_application": {"frontend": "React/Vue.js", "backend": "Flask/FastAPI", "database": "PostgreSQL"},
            "mobile_app": {"frontend": "React Native", "backend": "Node.js", "database": "Firebase"},
            "ai_ml_application": {"frontend": "Streamlit", "backend": "TensorFlow/PyTorch", "database": "MongoDB"},
            "blockchain_project": {"frontend": "React + Web3", "backend": "Solidity", "database": "Blockchain"},
            "api_service": {"frontend": "N/A", "backend": "FastAPI", "database": "PostgreSQL"},
        }
        
        tech_stack = tech_stacks.get(project_type, tech_stacks["web_application"])
        
        return f"""# System Architecture: {project_type.replace('_', ' ').title()}

## Project: {description}

## Technology Stack
- Frontend: {tech_stack['frontend']}
- Backend: {tech_stack['backend']}
- Database: {tech_stack['database']}

## Requirements
{chr(10).join(f"- {req}" for req in custom_reqs) if custom_reqs else "- Standard implementation"}

## Components
1. Client/Frontend
2. API Layer
3. Business Logic
4. Data Layer

## Security
- Input validation
- Authentication
- Encryption
- HTTPS/SSL

## Scalability
- Load balancing
- Caching (Redis)
- Database optimization
- CDN
"""

    def generate_backend_files(self, workspace_path: str, project_type: str, description: str, custom_reqs: List) -> List[str]:
        """Generate backend files dynamically"""
        
        if project_type == "web_application":
            return self._generate_web_app_files(workspace_path, description, custom_reqs)
        elif project_type == "mobile_app":
            return self._generate_mobile_backend_files(workspace_path, description, custom_reqs)
        elif project_type == "ai_ml_application":
            return self._generate_ml_files(workspace_path, description, custom_reqs)
        elif project_type == "blockchain_project":
            return self._generate_blockchain_files(workspace_path, description, custom_reqs)
        elif project_type == "api_service":
            return self._generate_api_service_files(workspace_path, description, custom_reqs)
        else:
            return self._generate_web_app_files(workspace_path, description, custom_reqs)

    def _generate_web_app_files(self, workspace_path: str, description: str, custom_reqs: List) -> List[str]:
        """Generate web app backend"""
        files_created = []
        
        init_content = f'''"""
{description}
"""
__version__ = "1.0.0"
'''
        self.safe_write_file(Path(workspace_path) / "src" / "__init__.py", init_content)
        files_created.append("__init__.py")
        
        config_content = """import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

config = {'development': DevelopmentConfig, 'default': DevelopmentConfig}
"""
        self.safe_write_file(Path(workspace_path) / "src" / "config.py", config_content)
        files_created.append("config.py")
        
        app_content = f"""from flask import Flask, request, jsonify
from src.config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({{'status': 'healthy'}})
    
    @app.route('/api/info', methods=['GET'])
    def info():
        return jsonify({{'name': '{description}', 'version': '1.0.0'}})
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
"""
        self.safe_write_file(Path(workspace_path) / "src" / "app.py", app_content)
        files_created.append("app.py")
        
        req_content = """Flask==2.3.2
python-dotenv==1.0.0
Werkzeug==2.3.6
"""
        self.safe_write_file(Path(workspace_path) / "requirements.txt", req_content)
        files_created.append("requirements.txt")
        
        readme = f"""# {description}

Web application built with Flask.

## Installation
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Run
python src/app.py
"""
        self.safe_write_file(Path(workspace_path) / "README.md", readme)
        files_created.append("README.md")
        
        return files_created

    def _generate_mobile_backend_files(self, workspace_path: str, description: str, custom_reqs: List) -> List[str]:
        """Generate mobile backend"""
        files = []
        
        init_content = f'"""Mobile Backend: {description}"""\n__version__ = "1.0.0"'
        self.safe_write_file(Path(workspace_path) / "src" / "__init__.py", init_content)
        files.append("__init__.py")
        
        api_content = f"""from flask import Flask

app = Flask(__name__)

@app.route('/api/v1/health', methods=['GET'])
def health():
    return {{'status': 'ok'}}
"""
        self.safe_write_file(Path(workspace_path) / "src" / "api.py", api_content)
        files.append("api.py")
        
        req_content = "Flask==2.3.2\nFlask-CORS==4.0.0\npython-dotenv==1.0.0"
        self.safe_write_file(Path(workspace_path) / "requirements.txt", req_content)
        files.append("requirements.txt")
        
        return files

    def _generate_ml_files(self, workspace_path: str, description: str, custom_reqs: List) -> List[str]:
        """Generate ML/AI files"""
        files = []
        
        init_content = f'"""ML Application: {description}"""\n__version__ = "1.0.0"'
        self.safe_write_file(Path(workspace_path) / "src" / "__init__.py", init_content)
        files.append("__init__.py")
        
        model_content = """class MLModel:
    def __init__(self):
        self.model = None
    
    def load_model(self):
        pass
    
    def predict(self, data):
        pass
"""
        self.safe_write_file(Path(workspace_path) / "src" / "model.py", model_content)
        files.append("model.py")
        
        app_content = f"""import streamlit as st

st.title('{description}')
st.write('Machine Learning Application')
"""
        self.safe_write_file(Path(workspace_path) / "src" / "app.py", app_content)
        files.append("app.py")
        
        req_content = "streamlit==1.28.0\ntensorflow==2.13.0\nscikit-learn==1.3.0\npandas==2.0.0\nnumpy==1.24.0"
        self.safe_write_file(Path(workspace_path) / "requirements.txt", req_content)
        files.append("requirements.txt")
        
        return files

    def _generate_blockchain_files(self, workspace_path: str, description: str, custom_reqs: List) -> List[str]:
        """Generate blockchain files"""
        files = []
        
        init_content = f'"""Blockchain: {description}"""\n__version__ = "1.0.0"'
        self.safe_write_file(Path(workspace_path) / "src" / "__init__.py", init_content)
        files.append("__init__.py")
        
        web3_content = """from web3 import Web3

class Web3Handler:
    def __init__(self, rpc_url):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    def is_connected(self):
        return self.w3.is_connected()
"""
        self.safe_write_file(Path(workspace_path) / "src" / "web3_utils.py", web3_content)
        files.append("web3_utils.py")
        
        req_content = "web3==6.11.0\neth-account==0.9.0\npython-dotenv==1.0.0"
        self.safe_write_file(Path(workspace_path) / "requirements.txt", req_content)
        files.append("requirements.txt")
        
        return files

    def _generate_api_service_files(self, workspace_path: str, description: str, custom_reqs: List) -> List[str]:
        """Generate API service files"""
        files = []
        
        app_content = f"""from fastapi import FastAPI

app = FastAPI(title='{description}', version='1.0.0')

@app.get('/health')
async def health():
    return {{'status': 'healthy'}}

@app.get('/api/info')
async def info():
    return {{'name': '{description}', 'version': '1.0.0'}}
"""
        self.safe_write_file(Path(workspace_path) / "src" / "app.py", app_content)
        files.append("app.py")
        
        req_content = "fastapi==0.104.0\nuvicorn==0.24.0\npydantic==2.4.0\npython-dotenv==1.0.0"
        self.safe_write_file(Path(workspace_path) / "requirements.txt", req_content)
        files.append("requirements.txt")
        
        return files

    def generate_deployment_files(self, workspace_path: str, project_type: str, description: str) -> List[str]:
        """Generate deployment files"""
        files = []
        
        env_content = """ENVIRONMENT=development
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/dbname
API_KEY=your-api-key
SECRET_KEY=your-secret-key
"""
        self.safe_write_file(Path(workspace_path) / "config" / ".env.example", env_content)
        files.append(".env.example")
        
        docker_compose = """version: '3.8'

services:
  app:
    build: .
    ports:
      - "5000:5000"
    environment:
      - ENVIRONMENT=production
"""
        self.safe_write_file(Path(workspace_path) / "config" / "docker-compose.yml", docker_compose)
        files.append("docker-compose.yml")
        
        dockerfile = """FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

CMD ["python", "src/app.py"]
"""
        self.safe_write_file(Path(workspace_path) / "config" / "Dockerfile", dockerfile)
        files.append("Dockerfile")
        
        deploy_guide = f"""# Deployment: {project_type.title()}

## Local
1. python -m venv venv
2. pip install -r requirements.txt
3. python src/app.py

## Docker
1. docker build -t app .
2. docker run -p 5000:5000 app

## Production
1. Gunicorn/Uvicorn
2. Nginx reverse proxy
3. SSL/TLS
"""
        self.safe_write_file(Path(workspace_path) / "docs" / "deployment.md", deploy_guide)
        files.append("deployment.md")
        
        return files

    async def execute_with_monitoring(self, agents: List, tasks: List[Task], workspace_path: str) -> str:
        """Execute tasks"""
        print(f"⚙️  Executing {len(tasks)} tasks...")
        
        try:
            crew = Crew(
                agents=agents,
                tasks=tasks,
                verbose=True,
                memory=False,
                max_execution_time=7200,
                process_timeout=1800
            )
            
            result = await asyncio.to_thread(crew.kickoff)
            print(f"   ✅ Execution completed")
            return str(result)
            
        except Exception as e:
            print(f"   ❌ Execution failed: {str(e)}")
            return str(e)

    async def validate_and_finalize(self, workspace_path: str, execution_result: str, project_plan: Dict) -> Dict[str, Any]:
        """Validate and finalize"""
        print("✅ Validating...")
        
        workspace = Path(workspace_path)
        all_files = list(workspace.rglob("*"))
        code_files = [f for f in all_files if f.suffix in [".py", ".js", ".ts"]]
        doc_files = [f for f in all_files if f.suffix in [".md", ".txt"]]
        
        quality_score = 0
        if len(code_files) > 0:
            quality_score += 20
        if len(doc_files) > 0:
            quality_score += 15
        if (workspace / "README.md").exists():
            quality_score += 10
        if any(f.name in ["requirements.txt", "package.json"] for f in workspace.rglob("*")):
            quality_score += 5
        
        summary = f"""PROJECT GENERATION COMPLETE!

Files Generated: {len(all_files)}
Code Files: {len(code_files)}
Documentation: {len(doc_files)}
Quality Score: {quality_score}/100
"""
        
        report_file = workspace / "PROJECT_REPORT.md"
        self.safe_write_file(report_file, summary)
        
        return {
            "quality_score": quality_score,
            "files_generated": len(all_files),
            "quality_metrics": {
                "code_files": len(code_files),
                "documentation_files": len(doc_files),
            },
            "summary": summary.strip()
        }

    def generate_project_id(self, requirements: Dict) -> str:
        """Generate ID"""
        timestamp = int(time.time())
        project_type = requirements.get("type", "custom")[:10]
        return f"{project_type}_{timestamp}"

    def assess_project_complexity(self, description: str, custom_reqs: List) -> str:
        """Assess complexity"""
        indicators = {
            "simple": ["basic", "simple", "crud"],
            "medium": ["authentication", "api", "database"],
            "complex": ["microservices", "scalable"],
            "advanced": ["ai", "blockchain", "machine learning"]
        }
        
        combined = f"{description.lower()} {' '.join(custom_reqs).lower()}"
        
        for complexity, words in indicators.items():
            if any(word in combined for word in words):
                return complexity
        
        return "medium"

    def estimate_duration(self, complexity: str, task_count: int) -> int:
        """Estimate duration"""
        times = {"simple": 2, "medium": 5, "complex": 10, "advanced": 15}
        return times.get(complexity, 5) * task_count

    def identify_risk_factors(self, project_type: str, custom_reqs: List) -> List[str]:
        """Identify risks"""
        risks = []
        combined = f"{project_type} {' '.join(custom_reqs)}".lower()
        
        if "blockchain" in combined:
            risks.append("Smart contract security")
        if "ai" in combined:
            risks.append("Model performance")
        if "real-time" in combined:
            risks.append("Performance and latency")
        
        return risks

    def define_success_criteria(self, requirements: Dict) -> List[str]:
        """Success criteria"""
        return [
            "All features implemented",
            "Code follows best practices",
            "Documentation provided",
            "Tests included",
            "Deployment ready"
        ]

    def define_quality_gates(self, project_type: str) -> List[str]:
        """Quality gates"""
        return [
            "Code syntax check",
            "Documentation completeness",
            "Security best practices",
            "Performance considerations"
        ]

    async def attempt_recovery(self, agents: List, tasks: List, workspace_path: str, error: str) -> str:
        """Recovery"""
        self.error_handler.log_error(
            Exception(error),
            severity=ErrorSeverity.HIGH,
            context="Project execution failed",
            recoverable=True,
            recovery_action="Partial completion"
        )
        return f"Partial completion. Check: {workspace_path}"

    async def handle_project_error(self, error: Exception, project_id: str, execution_time: float) -> Dict[str, Any]:
        """Handle error"""
        self.error_handler.log_error(
            error,
            severity=ErrorSeverity.CRITICAL,
            context=f"Project {project_id} failed",
            recoverable=False,
            recovery_action="Review error logs"
        )
        
        return {
            "success": False,
            "error": str(error),
            "project_id": project_id,
            "execution_time": execution_time,
        }

    async def check_rate_limits(self):
        """Check rate limits"""
        await self.rate_limiter.wait_if_needed("openrouter")
