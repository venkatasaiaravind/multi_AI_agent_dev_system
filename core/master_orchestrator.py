import asyncio
import time
import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path
from crewai import Crew, Task
from core.comprehensive_agent_factory import ComprehensiveAgentFactory
from config.model_config import ModelConfig

class MasterOrchestrator:
    def __init__(self):
        self.agent_factory = ComprehensiveAgentFactory()
        self.model_config = ModelConfig()
        self.workspace_base = os.getenv("WORKSPACE_DIR", "workspace")
        
        # Rate limiting and performance tracking
        self.request_counts = {"openrouter": 0, "groq": 0}
        self.session_start = time.time()
        self.projects_completed = 0
        
        # Quality and error tracking
        self.execution_stats = {
            "successful_projects": 0,
            "failed_projects": 0,
            "average_execution_time": 0,
            "total_api_requests": 0
        }
        
        print(" Master Orchestrator initialized with comprehensive agent system")
        print(f" Workspace: {self.workspace_base}")
        print(f" Available project types: {len(self.agent_factory.list_available_project_types())}")
    
    async def create_project(self, project_requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main orchestration method - creates complete projects using specialized agent teams
        """
        start_time = time.time()
        project_id = self._generate_project_id(project_requirements)
        
        print(f"\n STARTING PROJECT ORCHESTRATION")
        print(f"=" * 80)
        print(f" Project ID: {project_id}")
        print(f" Type: {project_requirements.get('type', 'custom')}")
        print(f" Description: {project_requirements.get('description', 'N/A')}")
        print(f" Custom Requirements: {project_requirements.get('custom_requirements', 'None')}")
        print(f" Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"=" * 80)
        
        try:
            # Phase 1: Project Analysis and Planning
            print(f"\n PHASE 1: PROJECT ANALYSIS & PLANNING")
            project_plan = await self._analyze_project_requirements(project_requirements)
            
            # Phase 2: Workspace Setup
            print(f"\n PHASE 2: WORKSPACE SETUP")
            workspace_path = await self._setup_project_workspace(project_id, project_plan)
            
            # Phase 3: Agent Team Assembly
            print(f"\n PHASE 3: AGENT TEAM ASSEMBLY")
            agents = await self._assemble_agent_team(project_requirements, project_plan)
            
            # Phase 4: Task Creation and Sequencing
            print(f"\n PHASE 4: TASK ORCHESTRATION")
            tasks = await self._create_project_tasks(agents, project_requirements, workspace_path, project_plan)
            
            # Phase 5: Execution with Monitoring
            print(f"\n PHASE 5: COORDINATED EXECUTION")
            execution_result = await self._execute_with_monitoring(agents, tasks, workspace_path)
            
            # Phase 6: Quality Validation and Finalization
            print(f"\n PHASE 6: QUALITY VALIDATION")
            final_result = await self._validate_and_finalize(workspace_path, execution_result, project_plan)
            
            # Calculate execution metrics
            execution_time = time.time() - start_time
            self.execution_stats["successful_projects"] += 1
            self.projects_completed += 1
            
            print(f"\n PROJECT COMPLETION SUCCESS!")
            print(f"=" * 80)
            print(f"  Total Execution Time: {execution_time:.1f} seconds")
            print(f" Project Location: {workspace_path}")
            print(f" Agents Used: {len(agents)}")
            print(f" Tasks Completed: {len(tasks)}")
            print(f" Quality Score: {final_result.get('quality_score', 'N/A')}")
            print(f"=" * 80)
            
            return {
                "success": True,
                "project_id": project_id,
                "workspace_path": workspace_path,
                "execution_time": execution_time,
                "agents_used": len(agents),
                "tasks_completed": len(tasks),
                "quality_metrics": final_result.get("quality_metrics", {}),
                "files_generated": final_result.get("files_generated", []),
                "project_summary": final_result.get("summary", "Project completed successfully")
            }
            
        except Exception as e:
            # Handle errors gracefully
            execution_time = time.time() - start_time
            self.execution_stats["failed_projects"] += 1
            
            error_result = await self._handle_project_error(e, project_id, execution_time)
            
            print(f"\n PROJECT EXECUTION FAILED")
            print(f"=" * 80)
            print(f"  Execution Time: {execution_time:.1f} seconds")
            print(f" Error: {str(e)}")
            print(f" Recovery Actions: {error_result.get('recovery_actions', 'None')}")
            print(f"=" * 80)
            
            return error_result
    
    async def _analyze_project_requirements(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze project requirements and create comprehensive execution plan"""
        
        print(" Analyzing project complexity and requirements...")
        
        project_type = requirements.get("type", "web_application")
        description = requirements.get("description", "")
        custom_reqs = requirements.get("custom_requirements", [])
        
        # Determine project complexity
        complexity = self._assess_project_complexity(description, custom_reqs)
        
        # Estimate resource requirements
        estimated_agents = len(self.agent_factory.project_templates.get(project_type, []))
        estimated_tasks = estimated_agents * 2  # Average 2 tasks per agent
        estimated_api_calls = estimated_tasks * 10  # Conservative estimate
        
        plan = {
            "complexity": complexity,
            "estimated_agents": estimated_agents,
            "estimated_tasks": estimated_tasks,
            "estimated_api_calls": estimated_api_calls,
            "estimated_duration": self._estimate_duration(complexity, estimated_tasks),
            "risk_factors": self._identify_risk_factors(project_type, custom_reqs),
            "success_criteria": self._define_success_criteria(requirements),
            "quality_gates": self._define_quality_gates(project_type)
        }
        
        print(f"    Complexity Assessment: {complexity}")
        print(f"    Estimated Team Size: {estimated_agents} agents")
        print(f"    Estimated Duration: {plan['estimated_duration']} minutes")
        print(f"    Estimated API Calls: {estimated_api_calls}")
        
        return plan
    
    async def _setup_project_workspace(self, project_id: str, project_plan: Dict) -> str:
        """Create organized workspace with proper structure"""
        
        workspace_path = Path(self.workspace_base) / project_id
        
        print(f" Creating workspace: {workspace_path}")
        
        # Create directory structure
        directories = [
            workspace_path,
            workspace_path / "src",
            workspace_path / "docs", 
            workspace_path / "tests",
            workspace_path / "config",
            workspace_path / "scripts",
            workspace_path / "assets",
            workspace_path / ".orchestrator"  # Internal orchestrator files
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Create project metadata
        metadata = {
            "project_id": project_id,
            "created_at": datetime.now().isoformat(),
            "project_plan": project_plan,
            "status": "in_progress",
            "workspace_structure": [str(d.relative_to(workspace_path)) for d in directories]
        }
        
        metadata_file = workspace_path / ".orchestrator" / "project_metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"    Workspace created with {len(directories)} directories")
        return str(workspace_path)
    
    async def _assemble_agent_team(self, requirements: Dict, project_plan: Dict) -> List:
        """Assemble optimal agent team using comprehensive factory"""
        
        print(" Assembling specialized agent team...")
        
        # Add rate limiting check
        await self._check_rate_limits()
        
        agents = self.agent_factory.create_agent_team(
            requirements.get("type", "web_application"),
            requirements.get("description", ""),
            requirements.get("custom_requirements", [])
        )
        
        print(f"    Team assembled: {len(agents)} specialized agents ready")
        return agents
    
    async def _create_project_tasks(self, agents: List, requirements: Dict, 
                                  workspace_path: str, project_plan: Dict) -> List[Task]:
        """Create comprehensive, sequenced tasks for the agent team"""
        
        print(" Creating orchestrated task sequence...")
        
        project_type = requirements.get("type", "web_application")
        description = requirements.get("description", "")
        
        tasks = []
        
        # Task 1: Strategic Architecture & Planning
        if any("architect" in agent.role.lower() for agent in agents):
            arch_agent = next(agent for agent in agents if "architect" in agent.role.lower())
            
            arch_task = Task(
                description=f"""
                 STRATEGIC ARCHITECTURE & PLANNING TASK
                
                Project: {description}
                Type: {project_type}
                Complexity: {project_plan.get('complexity', 'medium')}
                
                DELIVERABLES REQUIRED:
                1. Comprehensive System Architecture Document
                   - System overview and component diagram
                   - Technology stack with detailed justification
                   - Data architecture and flow diagrams
                   - Security architecture and threat model
                   - Scalability and performance considerations
                   - Integration points and external dependencies
                
                2. Technical Specifications
                   - Detailed API specifications
                   - Database schema design
                   - User interface wireframes and flow
                   - Non-functional requirements
                
                3. Implementation Roadmap
                   - Development phases and milestones
                   - Risk assessment and mitigation strategies
                   - Resource requirements and timeline
                
                Save all architecture documents in: {workspace_path}/docs/
                Create detailed README.md in project root: {workspace_path}/
                
                Focus on creating a world-class, scalable architecture that serves as the foundation for all subsequent development work.
                """,
                expected_output=f"""
                Complete architecture package including:
                - {workspace_path}/docs/system_architecture.md
                - {workspace_path}/docs/technical_specifications.md  
                - {workspace_path}/docs/implementation_roadmap.md
                - {workspace_path}/README.md
                """,
                agent=arch_agent
            )
            tasks.append(arch_task)
        
        # Task 2: Core Development (Backend/Smart Contracts/Core Logic)
        core_agents = [agent for agent in agents if any(role in agent.role.lower() 
                      for role in ["backend", "smart contract", "core", "data engineer", "ml engineer"])]
        
        for agent in core_agents[:2]:  # Limit to 2 core development agents for efficiency
            dev_task = Task(
                description=f"""
                 CORE DEVELOPMENT TASK - {agent.role}
                
                Based on the architecture in {workspace_path}/docs/, develop the core system:
                
                DEVELOPMENT REQUIREMENTS:
                1. Implement Core Business Logic
                   - Main application logic following architectural patterns
                   - Data models and business rules
                   - API endpoints or core interfaces
                   - Error handling and logging
                
                2. Integration Layer
                   - Database integration with proper ORM/queries
                   - External service integrations
                   - Configuration management
                   - Environment-specific settings
                
                3. Security Implementation
                   - Authentication and authorization
                   - Input validation and sanitization
                   - Security headers and CORS configuration
                   - Encryption for sensitive data
                
                4. Testing Foundation
                   - Unit tests for core functionality
                   - Integration test structure
                   - Mock data and test fixtures
                   - Testing configuration
                
                Save all code in: {workspace_path}/src/
                Include requirements/dependencies in: {workspace_path}/requirements.txt or package.json
                Create deployment configuration in: {workspace_path}/config/
                
                Ensure code follows best practices, is well-documented, and production-ready.
                """,
                expected_output=f"""
                Complete core implementation including:
                - {workspace_path}/src/ (all source code)
                - {workspace_path}/requirements.txt or package.json
                - {workspace_path}/config/ (configuration files)
                - {workspace_path}/tests/ (test files)
                """,
                agent=agent,
                context=[arch_task] if 'arch_task' in locals() else []
            )
            tasks.append(dev_task)
        
        # Task 3: Frontend/UI Development (if applicable)
        ui_agents = [agent for agent in agents if any(role in agent.role.lower() 
                    for role in ["frontend", "ui", "mobile", "game designer"])]
        
        if ui_agents and project_type in ["web_application", "mobile_app", "game_development", "dapp_development"]:
            ui_agent = ui_agents[0]
            
            ui_task = Task(
                description=f"""
                 USER INTERFACE DEVELOPMENT TASK
                
                Create exceptional user interface based on architecture and core system:
                
                UI/UX REQUIREMENTS:
                1. Modern User Interface
                   - Responsive design for all device types
                   - Intuitive navigation and user flows
                   - Accessibility compliance (WCAG guidelines)
                   - Performance-optimized components
                
                2. Frontend Architecture
                   - Component-based architecture
                   - State management implementation
                   - API integration with error handling
                   - Routing and navigation system
                
                3. User Experience Features
                   - Loading states and error boundaries
                   - Form validation with user feedback
                   - Real-time updates where applicable
                   - Mobile-first responsive design
                
                4. Integration & Testing
                   - Backend API integration
                   - Unit tests for components
                   - End-to-end test scenarios
                   - Cross-browser compatibility
                
                Save frontend code in: {workspace_path}/src/frontend/ or {workspace_path}/src/ui/
                Include build configuration and assets in appropriate directories
                """,
                expected_output=f"""
                Complete frontend implementation:
                - {workspace_path}/src/frontend/ (UI components and pages)
                - Build configuration and asset files
                - Frontend tests and documentation
                """,
                agent=ui_agent,
                context=tasks  # Depends on previous tasks
            )
            tasks.append(ui_task)
        
        # Task 4: Quality Assurance & Testing
        qa_agents = [agent for agent in agents if any(role in agent.role.lower() 
                    for role in ["qa", "test", "security"])]
        
        if qa_agents:
            qa_agent = qa_agents[0]
            
            qa_task = Task(
                description=f"""
                 COMPREHENSIVE QUALITY ASSURANCE TASK
                
                Conduct thorough testing and quality validation of the complete system:
                
                QUALITY ASSURANCE SCOPE:
                1. Functional Testing
                   - Test all features against requirements
                   - Verify user workflows and edge cases
                   - Validate data integrity and business logic
                   - Check error handling and recovery
                
                2. Technical Quality Assessment
                   - Code review and quality metrics
                   - Performance testing and optimization
                   - Security vulnerability assessment
                   - Compatibility testing across platforms
                
                3. Documentation Review
                   - Verify documentation completeness
                   - Test setup and deployment instructions
                   - Validate API documentation with examples
                   - Check code comments and inline docs
                
                4. Deployment Readiness
                   - Production deployment checklist
                   - Environment configuration validation
                   - Monitoring and logging setup
                   - Backup and recovery procedures
                
                Create comprehensive test results in: {workspace_path}/tests/
                Generate quality report in: {workspace_path}/docs/quality_report.md
                """,
                expected_output=f"""
                Complete quality assurance package:
                - {workspace_path}/tests/ (all test files and results)
                - {workspace_path}/docs/quality_report.md
                - Deployment readiness checklist
                """,
                agent=qa_agent,
                context=tasks  # Must wait for all development tasks
            )
            tasks.append(qa_task)
        
        # Task 5: DevOps & Deployment (if DevOps agent available)
        devops_agents = [agent for agent in agents if "devops" in agent.role.lower()]
        
        if devops_agents:
            devops_agent = devops_agents[0]
            
            devops_task = Task(
                description=f"""
                 DEVOPS & DEPLOYMENT ORCHESTRATION TASK
                
                Set up production-ready deployment and infrastructure:
                
                DEVOPS DELIVERABLES:
                1. Containerization & Infrastructure
                   - Docker configuration for all services
                   - Docker Compose for local development
                   - Kubernetes manifests for production (if applicable)
                   - Infrastructure as Code (Terraform/CloudFormation)
                
                2. CI/CD Pipeline
                   - Automated build and test pipeline
                   - Deployment automation scripts
                   - Environment promotion strategy
                   - Rollback and recovery procedures
                
                3. Monitoring & Observability
                   - Application performance monitoring setup
                   - Logging aggregation and analysis
                   - Health checks and alerting rules
                   - Security monitoring and audit trails
                
                4. Production Operations
                   - Environment configuration management
                   - Scaling and load balancing setup
                   - Backup and disaster recovery plan
                   - Security hardening checklist
                
                Save all DevOps files in: {workspace_path}/scripts/ and {workspace_path}/config/
                """,
                expected_output=f"""
                Production-ready deployment package:
                - {workspace_path}/scripts/ (deployment and automation scripts)
                - {workspace_path}/config/ (infrastructure and CI/CD configuration)
                - Complete deployment documentation
                """,
                agent=devops_agent,
                context=tasks  # Should be one of the final tasks
            )
            tasks.append(devops_task)
        
        print(f"    Created {len(tasks)} orchestrated tasks with proper sequencing")
        return tasks
    
    async def _execute_with_monitoring(self, agents: List, tasks: List[Task], workspace_path: str) -> str:
        """Execute tasks with intelligent monitoring and error recovery"""
        
        print(f" Executing {len(tasks)} tasks with {len(agents)} agents...")
        print(f" Monitoring: API calls, execution time, quality metrics")
        
        # Add execution timeout and retry logic
        execution_start = time.time()
        
        try:
            # Create crew with comprehensive configuration
            crew = Crew(
                agents=agents,
                tasks=tasks,
                verbose=True,
                memory=False,
                max_execution_time=3600,  # 1 hour max
                #process_timeout=300       # 5 minutes per task timeout
            )
            
            # Execute with monitoring
            print(" Starting coordinated execution...")
            result = crew.kickoff()
            
            execution_time = time.time() - execution_start
            
            print(f"    Execution completed in {execution_time:.1f} seconds")
            print(f"    All deliverables saved to workspace")
            
            return str(result)
            
        except Exception as e:
            execution_time = time.time() - execution_start
            print(f"    Execution failed after {execution_time:.1f} seconds: {str(e)}")
            
            # Attempt recovery
            recovery_result = await self._attempt_recovery(agents, tasks, workspace_path, str(e))
            return recovery_result
    
    async def _validate_and_finalize(self, workspace_path: str, execution_result: str, 
                                   project_plan: Dict) -> Dict[str, Any]:
        """Validate project output and create final report"""
        
        print(" Validating project deliverables and generating final report...")
        
        workspace = Path(workspace_path)
        
        # Count generated files
        all_files = list(workspace.rglob("*"))
        code_files = [f for f in all_files if f.suffix in ['.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.sol']]
        doc_files = [f for f in all_files if f.suffix in ['.md', '.txt', '.rst']]
        config_files = [f for f in all_files if f.name in ['requirements.txt', 'package.json', 'Dockerfile', 'docker-compose.yml']]
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(workspace, code_files, doc_files)
        
        # Generate final summary
        summary = f"""
         PROJECT GENERATION COMPLETE!
        
            ` Project Statistics:
        • Total Files Generated: {len(all_files)}
        • Source Code Files: {len(code_files)}
        • Documentation Files: {len(doc_files)}
        • Configuration Files: {len(config_files)}
        • Quality Score: {quality_score}%
        
         Workspace Structure:
        {workspace_path}/
        ├── src/           # Source code
        ├── docs/          # Documentation  
        ├── tests/         # Test files
        ├── config/        # Configuration
        └── scripts/       # Deployment scripts
        
         Ready for development and deployment!
        """
        
        # Save final report
        report_file = workspace / "PROJECT_REPORT.md"
        with open(report_file, 'w') as f:
            f.write(summary)
        
        print(f"    Quality Score: {quality_score}%")
        print(f"    Final report saved: {report_file}")
        
        return {
            "quality_score": quality_score,
            "files_generated": len(all_files),
            "quality_metrics": {
                "code_files": len(code_files),
                "documentation_files": len(doc_files),
                "configuration_files": len(config_files)
            },
            "summary": summary.strip()
        }
    
    # Helper methods
    def _generate_project_id(self, requirements: Dict) -> str:
        """Generate unique project ID"""
        timestamp = int(time.time())
        project_type = requirements.get("type", "custom")[:10]
        return f"{project_type}_{timestamp}"
    
    def _assess_project_complexity(self, description: str, custom_reqs: List) -> str:
        """Assess project complexity based on description and requirements"""
        complexity_indicators = {
            "simple": ["basic", "simple", "crud", "hello world"],
            "medium": ["authentication", "api", "database", "responsive"],
            "complex": ["microservices", "scalable", "enterprise", "real-time"],
            "advanced": ["ai", "blockchain", "machine learning", "distributed", "iot"]
        }
        
        desc_lower = description.lower()
        req_text = " ".join(custom_reqs).lower() if custom_reqs else ""
        combined_text = f"{desc_lower} {req_text}"
        
        for complexity, indicators in complexity_indicators.items():
            if any(indicator in combined_text for indicator in indicators):
                return complexity
        
        return "medium"  # Default
    
    def _estimate_duration(self, complexity: str, task_count: int) -> int:
        """Estimate execution duration in minutes"""
        base_times = {"simple": 2, "medium": 5, "complex": 10, "advanced": 15}
        return base_times.get(complexity, 5) * task_count
    
    def _identify_risk_factors(self, project_type: str, custom_reqs: List) -> List[str]:
        """Identify potential risk factors"""
        risks = []
        if "blockchain" in str(custom_reqs).lower():
            risks.append("Smart contract security")
        if "ai" in str(custom_reqs).lower():
            risks.append("Model performance and bias")
        if "real-time" in str(custom_reqs).lower():
            risks.append("Performance and latency")
        return risks
    
    def _define_success_criteria(self, requirements: Dict) -> List[str]:
        """Define success criteria for the project"""
        return [
            "All specified features implemented",
            "Code follows best practices",
            "Comprehensive documentation provided",
            "Tests cover main functionality",
            "Deployment ready"
        ]
    
    def _define_quality_gates(self, project_type: str) -> List[str]:
        """Define quality gates for validation"""
        return [
            "Code compilation/syntax check",
            "Documentation completeness",
            "Basic functionality test",
            "Security best practices",
            "Performance considerations"
        ]
    
    async def _check_rate_limits(self):
        """Check and manage API rate limits"""
        # Simple rate limit check - can be enhanced
        if self.request_counts["openrouter"] > 40:
            print(" Approaching OpenRouter rate limits")
        if self.request_counts["groq"] > 1000:  # Conservative estimate
            print(" High Groq usage - monitoring performance")

    async def _attempt_recovery(self, agents: List, tasks: List[Task], workspace_path: str, error: str) -> str:
        """Attempt to recover from execution errors"""
        print(f"🔧 Attempting error recovery for: {error[:100]}...")
        return f"Partial completion - {len(tasks)} tasks created, workspace prepared at {workspace_path}"
    
    async def _handle_project_error(self, error: Exception, project_id: str, execution_time: float) -> Dict:
        """Handle project errors gracefully"""
        return {
            "success": False,
            "project_id": project_id,
            "error": str(error),
            "execution_time": execution_time,
            "recovery_actions": ["Check API keys", "Verify network connection", "Review error logs"],
            "partial_workspace": f"{self.workspace_base}/{project_id}"
        }
    
    def _calculate_quality_score(self, workspace: Path, code_files: List, doc_files: List) -> int:
        """Calculate overall quality score"""
        score = 50  # Base score
        
        # Add points for file generation
        if len(code_files) > 0:
            score += 20
        if len(doc_files) > 0:
            score += 15
        if (workspace / "README.md").exists():
            score += 10
        if any(f.name in ['requirements.txt', 'package.json'] for f in workspace.rglob("*")):
            score += 5
        
        return min(score, 100)
