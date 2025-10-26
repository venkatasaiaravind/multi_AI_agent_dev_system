from crewai import Agent
from typing import List, Dict, Any, Set
from config.model_config import ModelConfig
from tools.enhanced_file_operations import file_tools


class ComprehensiveAgentFactory:
    """Factory for creating specialized AI agents with file operation capabilities"""
    
    def __init__(self):
        # Initialize file tools - AGENTS CAN NOW WRITE FILES!
        self.file_tools = file_tools
        
        # Model configuration
        self.model_config = ModelConfig()
        
        # COMPREHENSIVE PROJECT TEMPLATES
        self.project_templates = {
            # Traditional Applications
            "web_application": ["system_architect", "backend_developer", "frontend_developer", "qa_engineer", "devops_engineer"],
            "api_service": ["system_architect", "backend_developer", "api_specialist", "qa_engineer"],
            "mobile_app": ["system_architect", "mobile_architect", "ios_developer", "android_developer", "qa_engineer"],
            "cli_tool": ["system_architect", "backend_developer", "qa_engineer"],
            
            # Enterprise & Business Systems
            "erp_system": ["enterprise_architect", "backend_developer", "database_specialist", "integration_specialist", "business_analyst", "qa_engineer"],
            "crm_platform": ["system_architect", "backend_developer", "frontend_developer", "database_specialist", "business_analyst", "qa_engineer"],
            "ecommerce_platform": ["ecommerce_architect", "backend_developer", "frontend_developer", "payment_specialist", "security_developer", "qa_engineer"],
            
            # AI/ML & Emerging Technologies
            "ai_ml_application": ["ai_architect", "data_scientist", "ml_engineer", "data_engineer", "mlops_specialist"],
            "deep_learning_project": ["ai_architect", "deep_learning_specialist", "data_scientist", "mlops_specialist"],
            "nlp_system": ["nlp_specialist", "data_scientist", "backend_developer", "ml_engineer"],
            "computer_vision": ["cv_specialist", "data_scientist", "ml_engineer"],
            
            # Blockchain & Web3
            "blockchain_project": ["blockchain_architect", "smart_contract_developer", "security_auditor"],
            "defi_platform": ["defi_architect", "smart_contract_developer", "frontend_developer", "security_auditor"],
            "nft_platform": ["blockchain_architect", "smart_contract_developer", "frontend_developer"],
            
            # IoT & Edge Computing
            "iot_solution": ["iot_architect", "embedded_developer", "hardware_engineer", "cloud_integration_specialist"],
            "edge_computing": ["edge_architect", "embedded_developer", "network_specialist"],
            "smart_home_system": ["iot_architect", "embedded_developer", "mobile_developer"],
            
            # AR/VR & Gaming
            "ar_application": ["ar_architect", "unity_developer", "3d_specialist"],
            "vr_application": ["vr_architect", "unity_developer", "3d_specialist"],
            "game_development": ["game_architect", "game_designer", "unity_developer", "graphics_engineer"],
            
            # FinTech & Financial Systems
            "fintech_application": ["fintech_architect", "backend_developer", "payment_specialist", "compliance_officer"],
            "trading_platform": ["trading_architect", "quantitative_analyst", "backend_developer"],
            "payment_gateway": ["payment_architect", "backend_developer", "security_developer"],
            
            # HealthTech & Medical
            "healthtech_application": ["healthcare_architect", "backend_developer", "hipaa_compliance_specialist"],
            "telemedicine_platform": ["healthcare_architect", "backend_developer", "video_streaming_specialist"],
            
            # EdTech & Learning
            "edtech_platform": ["edtech_architect", "backend_developer", "frontend_developer", "learning_specialist"],
            "lms_system": ["education_architect", "backend_developer", "frontend_developer"],
            
            # Security & Infrastructure
            "cybersecurity_software": ["security_architect", "security_developer", "penetration_tester"],
            "devsecops_platform": ["devsecops_architect", "security_developer", "devops_engineer"],
            "cloud_infrastructure": ["cloud_architect", "devops_engineer", "network_specialist"],
        }
        
        # COMPREHENSIVE AGENT ROLE DEFINITIONS
        self.agent_roles = self._initialize_agent_roles()
    
    def _initialize_agent_roles(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive agent role definitions with expertise areas"""
        return {
            # STRATEGIC & ARCHITECTURE ROLES
            "system_architect": {
                "title": "Senior System Architect",
                "expertise": ["system_design", "scalability", "performance", "security", "microservices"],
                "model_preference": "reasoning_heavy",
                "description": "Designs comprehensive system architectures with focus on scalability and maintainability"
            },
            "enterprise_architect": {
                "title": "Enterprise Solutions Architect",
                "expertise": ["enterprise_systems", "integration", "governance", "compliance"],
                "model_preference": "reasoning_heavy",
                "description": "Specializes in large-scale enterprise system design"
            },
            
            # DEVELOPMENT ROLES
            "backend_developer": {
                "title": "Senior Backend Developer",
                "expertise": ["apis", "databases", "microservices", "performance", "security"],
                "model_preference": "coding_heavy",
                "description": "Develops robust backend systems and APIs"
            },
            "frontend_developer": {
                "title": "Senior Frontend Developer",
                "expertise": ["react", "vue", "angular", "typescript", "performance"],
                "model_preference": "coding_heavy",
                "description": "Creates modern, responsive user interfaces"
            },
            "api_specialist": {
                "title": "API Design Specialist",
                "expertise": ["rest_api", "graphql", "openapi", "versioning"],
                "model_preference": "reasoning_heavy",
                "description": "Specializes in designing scalable APIs"
            },
            
            # MOBILE DEVELOPMENT
            "mobile_architect": {
                "title": "Mobile Solutions Architect",
                "expertise": ["mobile_architecture", "cross_platform", "performance"],
                "model_preference": "reasoning_heavy",
                "description": "Designs mobile app architectures"
            },
            "ios_developer": {
                "title": "Senior iOS Developer",
                "expertise": ["swift", "ios", "xcode", "app_store"],
                "model_preference": "coding_heavy",
                "description": "Develops native iOS applications"
            },
            "android_developer": {
                "title": "Senior Android Developer",
                "expertise": ["kotlin", "android", "jetpack_compose"],
                "model_preference": "coding_heavy",
                "description": "Develops native Android applications"
            },
            
            # AI/ML SPECIALISTS
            "ai_architect": {
                "title": "AI/ML Solutions Architect",
                "expertise": ["machine_learning", "deep_learning", "mlops"],
                "model_preference": "reasoning_heavy",
                "description": "Designs AI/ML system architectures"
            },
            "data_scientist": {
                "title": "Senior Data Scientist",
                "expertise": ["statistics", "machine_learning", "python", "r"],
                "model_preference": "coding_heavy",
                "description": "Develops ML models and statistical analysis"
            },
            "ml_engineer": {
                "title": "Machine Learning Engineer",
                "expertise": ["mlops", "model_deployment", "tensorflow", "pytorch"],
                "model_preference": "coding_heavy",
                "description": "Deploys and maintains ML models in production"
            },
            "data_engineer": {
                "title": "Senior Data Engineer",
                "expertise": ["data_pipelines", "spark", "kafka", "sql"],
                "model_preference": "coding_heavy",
                "description": "Builds and maintains data pipelines"
            },
            "deep_learning_specialist": {
                "title": "Deep Learning Specialist",
                "expertise": ["neural_networks", "cnn", "rnn", "transformers"],
                "model_preference": "reasoning_heavy",
                "description": "Specializes in deep learning models"
            },
            "nlp_specialist": {
                "title": "NLP Engineering Specialist",
                "expertise": ["nlp", "transformers", "bert", "gpt"],
                "model_preference": "reasoning_heavy",
                "description": "Specializes in natural language processing"
            },
            "cv_specialist": {
                "title": "Computer Vision Specialist",
                "expertise": ["computer_vision", "cnn", "detection", "segmentation"],
                "model_preference": "coding_heavy",
                "description": "Develops computer vision systems"
            },
            "mlops_specialist": {
                "title": "MLOps Engineering Specialist",
                "expertise": ["mlops", "kubernetes", "monitoring", "ci_cd"],
                "model_preference": "coding_heavy",
                "description": "Deploys and maintains ML models in production"
            },
            
            # BLOCKCHAIN & WEB3
            "blockchain_architect": {
                "title": "Blockchain Solutions Architect",
                "expertise": ["blockchain", "consensus", "cryptography", "distributed_systems"],
                "model_preference": "reasoning_heavy",
                "description": "Designs blockchain architectures"
            },
            "smart_contract_developer": {
                "title": "Smart Contract Developer",
                "expertise": ["solidity", "ethereum", "defi", "security_auditing"],
                "model_preference": "coding_heavy",
                "description": "Develops and audits smart contracts"
            },
            "defi_architect": {
                "title": "DeFi Protocol Architect",
                "expertise": ["defi", "liquidity", "yield_farming", "tokenomics"],
                "model_preference": "reasoning_heavy",
                "description": "Designs decentralized finance protocols"
            },
            
            # IOT & EMBEDDED
            "iot_architect": {
                "title": "IoT Solutions Architect",
                "expertise": ["iot", "sensors", "edge_computing", "protocols"],
                "model_preference": "reasoning_heavy",
                "description": "Designs end-to-end IoT solutions"
            },
            "embedded_developer": {
                "title": "Embedded Systems Developer",
                "expertise": ["c", "cpp", "arduino", "rtos", "firmware"],
                "model_preference": "coding_heavy",
                "description": "Develops firmware and embedded software"
            },
            "hardware_engineer": {
                "title": "Hardware Design Engineer",
                "expertise": ["circuit_design", "pcb", "sensors", "microcontrollers"],
                "model_preference": "reasoning_heavy",
                "description": "Designs hardware components"
            },
            
            # FINTECH & FINANCE
            "fintech_architect": {
                "title": "FinTech Solutions Architect",
                "expertise": ["finance", "payments", "regulations", "compliance"],
                "model_preference": "reasoning_heavy",
                "description": "Designs financial technology solutions"
            },
            "payment_specialist": {
                "title": "Payment Integration Specialist",
                "expertise": ["payment_gateways", "pci_compliance", "fraud_detection"],
                "model_preference": "coding_heavy",
                "description": "Integrates payment systems"
            },
            "quantitative_analyst": {
                "title": "Quantitative Financial Analyst",
                "expertise": ["quantitative_finance", "risk_modeling", "algorithms"],
                "model_preference": "reasoning_heavy",
                "description": "Develops quantitative models"
            },
            "compliance_officer": {
                "title": "Financial Compliance Specialist",
                "expertise": ["regulations", "kyc", "aml", "gdpr"],
                "model_preference": "reasoning_heavy",
                "description": "Ensures regulatory compliance"
            },
            
            # SECURITY SPECIALISTS
            "security_architect": {
                "title": "Cybersecurity Solutions Architect",
                "expertise": ["security", "threat_modeling", "encryption", "compliance"],
                "model_preference": "reasoning_heavy",
                "description": "Designs comprehensive security architectures"
            },
            "security_developer": {
                "title": "Security Software Developer",
                "expertise": ["secure_coding", "penetration_testing", "owasp"],
                "model_preference": "coding_heavy",
                "description": "Develops secure software"
            },
            "penetration_tester": {
                "title": "Senior Penetration Tester",
                "expertise": ["pen_testing", "vulnerability_assessment", "red_teaming"],
                "model_preference": "reasoning_heavy",
                "description": "Conducts security assessments"
            },
            "security_auditor": {
                "title": "Security Auditor",
                "expertise": ["auditing", "compliance", "risk_assessment"],
                "model_preference": "reasoning_heavy",
                "description": "Performs security audits"
            },
            
            # GAME DEVELOPMENT
            "game_architect": {
                "title": "Game Systems Architect",
                "expertise": ["game_engines", "unity", "performance", "networking"],
                "model_preference": "reasoning_heavy",
                "description": "Designs game architectures"
            },
            "game_designer": {
                "title": "Senior Game Designer",
                "expertise": ["game_mechanics", "user_experience", "monetization"],
                "model_preference": "reasoning_heavy",
                "description": "Creates engaging game mechanics"
            },
            "unity_developer": {
                "title": "Unity Game Developer",
                "expertise": ["unity", "csharp", "game_programming", "3d_graphics"],
                "model_preference": "coding_heavy",
                "description": "Develops games using Unity"
            },
            "graphics_engineer": {
                "title": "Graphics Programming Engineer",
                "expertise": ["graphics_programming", "shaders", "rendering", "gpu"],
                "model_preference": "coding_heavy",
                "description": "Develops advanced graphics systems"
            },
            
            # HEALTHCARE & MEDICAL
            "healthcare_architect": {
                "title": "Healthcare Solutions Architect",
                "expertise": ["healthcare", "hipaa", "hl7", "interoperability"],
                "model_preference": "reasoning_heavy",
                "description": "Designs healthcare systems"
            },
            "hipaa_compliance_specialist": {
                "title": "HIPAA Compliance Specialist",
                "expertise": ["hipaa", "privacy", "security", "compliance"],
                "model_preference": "reasoning_heavy",
                "description": "Ensures HIPAA compliance"
            },
            
            # SUPPORT & QUALITY ROLES
            "qa_engineer": {
                "title": "Senior QA Engineer",
                "expertise": ["testing", "automation", "bug_detection", "validation"],
                "model_preference": "reasoning_heavy",
                "description": "Ensures comprehensive quality"
            },
            "devops_engineer": {
                "title": "DevOps Engineering Specialist",
                "expertise": ["devops", "ci_cd", "kubernetes", "monitoring"],
                "model_preference": "coding_heavy",
                "description": "Handles deployment and operations"
            },
            "database_specialist": {
                "title": "Database Design Specialist",
                "expertise": ["database_design", "sql", "optimization", "scaling"],
                "model_preference": "coding_heavy",
                "description": "Designs and optimizes databases"
            },
            "business_analyst": {
                "title": "Senior Business Analyst",
                "expertise": ["requirements", "analysis", "documentation", "stakeholder_management"],
                "model_preference": "reasoning_heavy",
                "description": "Analyzes business requirements"
            },
        }
    
    def create_agent_team(self, project_type: str, project_description: str,
                         custom_requirements: List[str] = None) -> List[Agent]:
        """Create specialized agent team for any project type"""
        
        print(f"🎯 Creating specialized agent team for: {project_type.upper()}")
        print(f"📋 Project: {project_description}")
        
        if custom_requirements:
            print(f"🔧 Custom Requirements: {', '.join(custom_requirements[:3])}...")
        
        print()
        
        # Get base agent roles for project type
        base_roles = self.project_templates.get(
            project_type, 
            ["system_architect", "backend_developer", "qa_engineer", "devops_engineer"]
        )
        
        # Add custom roles based on requirements
        if custom_requirements:
            additional_roles = self._analyze_custom_requirements(custom_requirements)
            base_roles.extend(additional_roles)
        
        # Remove duplicates while preserving order
        agent_roles = list(dict.fromkeys(base_roles))
        
        # Create agents
        agents = []
        for i, role in enumerate(agent_roles, 1):
            if role in self.agent_roles:
                print(f"🤖 Creating agent {i}/{len(agent_roles)}: {role}")
                agent = self._create_specialized_agent(role, project_description, project_type)
                agents.append(agent)
                
                role_info = self.agent_roles[role]
                print(f"   ✅ {role_info['title']}")
                print(f"   🔧 Expertise: {', '.join(role_info['expertise'][:2])}...")
            else:
                print(f"   ⚠️ Unknown role: {role}, skipping...")
        
        print(f"\n🎉 Agent team ready! {len(agents)} specialists for {project_type}\n")
        
        return agents
    
    def _analyze_custom_requirements(self, requirements: List[str]) -> List[str]:
        """Analyze custom requirements and suggest additional agent roles"""
        
        additional_roles = []
        requirement_mapping = {
            "blockchain": ["blockchain_architect", "smart_contract_developer", "security_auditor"],
            "ai": ["ai_architect", "data_scientist", "ml_engineer", "data_engineer"],
            "machine learning": ["data_scientist", "ml_engineer", "data_engineer", "mlops_specialist"],
            "iot": ["iot_architect", "embedded_developer", "hardware_engineer"],
            "security": ["security_architect", "security_developer", "penetration_tester"],
            "fintech": ["fintech_architect", "payment_specialist", "compliance_officer"],
            "healthcare": ["healthcare_architect", "hipaa_compliance_specialist"],
            "gaming": ["game_architect", "game_designer", "unity_developer"],
            "mobile": ["mobile_architect", "ios_developer", "android_developer"],
            "cloud": ["cloud_architect", "devops_engineer"],
            "data": ["data_engineer", "data_scientist", "database_specialist"],
            "api": ["api_specialist", "backend_developer"],
            "frontend": ["frontend_developer"],
        }
        
        for requirement in requirements:
            req_lower = requirement.lower()
            for keyword, roles in requirement_mapping.items():
                if keyword in req_lower:
                    additional_roles.extend(roles)
        
        return list(set(additional_roles))  # Remove duplicates
    
    def _create_specialized_agent(self, role: str, project_description: str, project_type: str):
        """Create a specialized agent with working file tools"""
        
        # Get role information
        role_info = self.agent_roles.get(role, {
            "title": role.replace("_", " ").title(),
            "expertise": ["general"],
            "model_preference": "balanced",
            "description": f"Specialist in {role.replace('_', ' ')}"
        })
        
        # Select optimal model
        llm = self.model_config.get_model_for_role(role)
        
        # Create goal and backstory
        goal = self._generate_role_goal(role, project_description, role_info)
        backstory = self._generate_role_backstory(role, role_info)
        
        # Create agent WITH FILE TOOLS
        return Agent(
            role=role_info["title"],
            goal=goal,
            backstory=backstory,
            llm=llm,
            tools=self.file_tools,  # ← CRITICAL: Agents can now write files!
            verbose=True,
            memory=False,
            allow_delegation=False,
            max_iter=5,
            max_execution_time=900
        )
    
    def _generate_role_goal(self, role: str, project_description: str, role_info: Dict) -> str:
        """Generate goal for the role"""
        
        return f"""As a {role_info['title']}, deliver expert solutions for: {project_description}

Your core responsibilities:
- Apply deep expertise in: {', '.join(role_info['expertise'][:3])}
- Ensure best practices and standards compliance
- Collaborate effectively with other specialists
- Deliver production-ready solutions
- Use WriteFileTool to save your work

Focus: {role_info['description']}"""
    
    def _generate_role_backstory(self, role: str, role_info: Dict) -> str:
        """Generate backstory for the role"""
        
        return f"""You are a highly experienced {role_info['title']} with deep expertise in {', '.join(role_info['expertise'][:3])}.

You have successfully delivered complex projects and are known for:
- Technical excellence and innovative problem-solving
- Strong collaboration with cross-functional teams
- Commitment to quality and best practices
- Ability to mentor junior team members
- Staying current with latest industry trends

{role_info['description']}

You approach every task with professionalism, technical rigor, and focus on delivering exceptional results."""
    
    def list_available_project_types(self) -> Dict[str, List[str]]:
        """List all available project types"""
        
        categories = {
            "Traditional": ["web_application", "api_service", "mobile_app", "cli_tool"],
            "Enterprise": ["erp_system", "crm_platform", "ecommerce_platform"],
            "AI/ML": ["ai_ml_application", "nlp_system", "computer_vision"],
            "Blockchain": ["blockchain_project", "defi_platform", "nft_platform"],
            "IoT": ["iot_solution", "edge_computing", "smart_home_system"],
            "Gaming": ["ar_application", "vr_application", "game_development"],
            "FinTech": ["fintech_application", "trading_platform", "payment_gateway"],
            "HealthTech": ["healthtech_application", "telemedicine_platform"],
            "EdTech": ["edtech_platform", "lms_system"],
            "Security": ["cybersecurity_software", "devsecops_platform", "cloud_infrastructure"],
        }
        
        return categories