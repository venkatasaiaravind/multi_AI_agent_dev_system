from crewai import Agent
from typing import List, Dict, Any, Set
from config.model_config import ModelConfig
from tools.file_operations import FileWriteTool, ReadFileTool, ListDirectoryTool

class ComprehensiveAgentFactory:
    def __init__(self):
        self.model_config = ModelConfig()
        self.file_tools = [FileWriteTool(), ReadFileTool(), ListDirectoryTool()]
        
        # COMPREHENSIVE PROJECT TEMPLATES
        self.project_templates = {
            # Traditional Applications
            "web_application": ["system_architect", "backend_developer", "frontend_developer", "qa_engineer"],
            "api_service": ["system_architect", "backend_developer", "api_specialist", "qa_engineer"],
            "mobile_app": ["system_architect", "mobile_architect", "ios_developer", "android_developer", "qa_engineer"],
            "cli_tool": ["system_architect", "backend_developer", "qa_engineer"],
            
            # Enterprise & Business Systems
            "erp_system": ["enterprise_architect", "backend_developer", "database_specialist", "integration_specialist", "business_analyst", "qa_engineer"],
            "crm_platform": ["system_architect", "backend_developer", "frontend_developer", "database_specialist", "business_analyst", "qa_engineer"],
            "ecommerce_platform": ["ecommerce_architect", "backend_developer", "frontend_developer", "payment_specialist", "security_developer", "qa_engineer"],
            "supply_chain_system": ["system_architect", "backend_developer", "iot_specialist", "data_engineer", "business_analyst", "qa_engineer"],
            "business_intelligence": ["data_architect", "data_scientist", "backend_developer", "visualization_specialist", "data_engineer", "qa_engineer"],
            
            # AI/ML & Emerging Technologies  
            "ai_ml_application": ["ai_architect", "data_scientist", "ml_engineer", "data_engineer", "mlops_specialist", "ai_researcher"],
            "deep_learning_project": ["ai_architect", "deep_learning_specialist", "data_scientist", "gpu_optimization_specialist", "mlops_specialist"],
            "nlp_system": ["nlp_specialist", "data_scientist", "backend_developer", "ml_engineer", "linguistics_expert"],
            "computer_vision": ["cv_specialist", "data_scientist", "gpu_optimization_specialist", "ml_engineer", "image_processing_specialist"],
            
            # Blockchain & Web3
            "blockchain_project": ["blockchain_architect", "smart_contract_developer", "blockchain_core_developer", "security_auditor", "tokenomics_specialist"],
            "defi_platform": ["defi_architect", "smart_contract_developer", "frontend_developer", "security_auditor", "financial_analyst"],
            "nft_platform": ["blockchain_architect", "smart_contract_developer", "frontend_developer", "metadata_specialist", "community_manager"],
            "dapp_development": ["dapp_architect", "smart_contract_developer", "web3_frontend_developer", "ipfs_specialist", "qa_engineer"],
            
            # IoT & Edge Computing
            "iot_solution": ["iot_architect", "embedded_developer", "hardware_engineer", "wireless_specialist", "cloud_integration_specialist", "qa_engineer"],
            "edge_computing": ["edge_architect", "embedded_developer", "network_specialist", "optimization_specialist", "security_developer"],
            "smart_home_system": ["iot_architect", "embedded_developer", "mobile_developer", "cloud_integration_specialist", "security_developer"],
            
            # AR/VR & Gaming
            "ar_application": ["ar_architect", "unity_developer", "3d_specialist", "ux_designer", "mobile_developer"],
            "vr_application": ["vr_architect", "unity_developer", "3d_specialist", "audio_engineer", "performance_specialist"],
            "game_development": ["game_architect", "game_designer", "unity_developer", "graphics_engineer", "audio_engineer", "monetization_specialist"],
            "metaverse_platform": ["metaverse_architect", "blockchain_developer", "unity_developer", "3d_specialist", "networking_specialist"],
            
            # FinTech & Financial Systems
            "fintech_application": ["fintech_architect", "backend_developer", "payment_specialist", "compliance_officer", "risk_analyst", "security_developer"],
            "trading_platform": ["trading_architect", "quantitative_analyst", "backend_developer", "real_time_specialist", "risk_manager"],
            "payment_gateway": ["payment_architect", "backend_developer", "security_developer", "compliance_officer", "integration_specialist"],
            "robo_advisor": ["fintech_architect", "quantitative_analyst", "ml_engineer", "risk_analyst", "compliance_officer"],
            
            # HealthTech & Medical
            "healthtech_application": ["healthcare_architect", "backend_developer", "frontend_developer", "hipaa_compliance_specialist", "medical_data_specialist"],
            "telemedicine_platform": ["healthcare_architect", "backend_developer", "video_streaming_specialist", "security_developer", "medical_workflow_specialist"],
            "medical_device_software": ["medical_architect", "embedded_developer", "regulatory_specialist", "qa_engineer", "clinical_data_specialist"],
            
            # EdTech & Learning
            "edtech_platform": ["edtech_architect", "backend_developer", "frontend_developer", "learning_specialist", "content_management_specialist"],
            "lms_system": ["education_architect", "backend_developer", "frontend_developer", "assessment_specialist", "analytics_specialist"],
            "adaptive_learning": ["ai_architect", "data_scientist", "education_specialist", "backend_developer", "learning_analytics_specialist"],
            
            # Security & Infrastructure  
            "cybersecurity_software": ["security_architect", "security_developer", "penetration_tester", "threat_analyst", "compliance_officer"],
            "devsecops_platform": ["devsecops_architect", "security_developer", "devops_engineer", "automation_specialist", "vulnerability_specialist"],
            "cloud_infrastructure": ["cloud_architect", "devops_engineer", "network_specialist", "security_developer", "cost_optimization_specialist"],
            "network_management": ["network_architect", "network_engineer", "monitoring_specialist", "security_developer", "automation_specialist"],
            
            # Industry-Specific
            "agritech_solution": ["agritech_architect", "iot_specialist", "data_scientist", "backend_developer", "agricultural_specialist"],
            "proptech_platform": ["proptech_architect", "backend_developer", "frontend_developer", "gis_specialist", "legal_tech_specialist"],
            "logistics_system": ["logistics_architect", "backend_developer", "iot_specialist", "optimization_specialist", "integration_specialist"],
            
            # Media & Entertainment
            "streaming_platform": ["streaming_architect", "backend_developer", "video_specialist", "cdn_specialist", "analytics_specialist"],
            "social_media_platform": ["social_architect", "backend_developer", "frontend_developer", "algorithm_specialist", "content_moderation_specialist"],
            "content_management": ["cms_architect", "backend_developer", "frontend_developer", "search_specialist", "workflow_specialist"]
        }
        
        # COMPREHENSIVE AGENT ROLE DEFINITIONS
        self.agent_roles = self._initialize_agent_roles()
    
    def _initialize_agent_roles(self) -> Dict[str, Dict[str, Any]]:
        """Initialize comprehensive agent role definitions"""
        return {
            # STRATEGIC & ARCHITECTURE ROLES
            "system_architect": {
                "title": "Senior System Architect",
                "expertise": ["system_design", "scalability", "performance", "security"],
                "model_preference": "reasoning_heavy",
                "description": "Designs comprehensive system architectures with focus on scalability and maintainability"
            },
            "enterprise_architect": {
                "title": "Enterprise Solutions Architect", 
                "expertise": ["enterprise_systems", "integration", "governance", "compliance"],
                "model_preference": "reasoning_heavy",
                "description": "Specializes in large-scale enterprise system design and integration patterns"
            },
            "cloud_architect": {
                "title": "Cloud Solutions Architect",
                "expertise": ["aws", "azure", "gcp", "kubernetes", "microservices"],
                "model_preference": "reasoning_heavy", 
                "description": "Designs scalable cloud-native architectures and migration strategies"
            },
            
            # AI/ML SPECIALISTS
            "ai_architect": {
                "title": "AI/ML Solutions Architect",
                "expertise": ["machine_learning", "deep_learning", "model_architecture", "mlops"],
                "model_preference": "reasoning_heavy",
                "description": "Designs AI/ML system architectures and model deployment strategies"
            },
            "data_scientist": {
                "title": "Senior Data Scientist", 
                "expertise": ["statistics", "machine_learning", "data_analysis", "python", "r"],
                "model_preference": "coding_heavy",
                "description": "Develops ML models, performs statistical analysis, and extracts insights from data"
            },
            "ml_engineer": {
                "title": "Machine Learning Engineer",
                "expertise": ["mlops", "model_deployment", "tensorflow", "pytorch", "kubernetes"],
                "model_preference": "coding_heavy",
                "description": "Deploys and maintains ML models in production environments"
            },
            "data_engineer": {
                "title": "Senior Data Engineer",
                "expertise": ["data_pipelines", "spark", "kafka", "airflow", "sql"],
                "model_preference": "coding_heavy", 
                "description": "Builds and maintains data pipelines and infrastructure for ML workflows"
            },
            "ai_researcher": {
                "title": "AI Research Scientist",
                "expertise": ["research", "algorithms", "papers", "innovation", "mathematics"],
                "model_preference": "reasoning_heavy",
                "description": "Develops novel AI algorithms and conducts cutting-edge research"
            },
            "nlp_specialist": {
                "title": "NLP Engineering Specialist",
                "expertise": ["nlp", "transformers", "bert", "gpt", "linguistics"],
                "model_preference": "reasoning_heavy",
                "description": "Specializes in natural language processing and language model development"
            },
            "cv_specialist": {
                "title": "Computer Vision Specialist", 
                "expertise": ["computer_vision", "cnn", "opencv", "image_processing", "detection"],
                "model_preference": "coding_heavy",
                "description": "Develops computer vision systems and image processing algorithms"
            },
            
            # BLOCKCHAIN & WEB3
            "blockchain_architect": {
                "title": "Blockchain Solutions Architect",
                "expertise": ["blockchain", "consensus", "cryptography", "distributed_systems"],
                "model_preference": "reasoning_heavy",
                "description": "Designs blockchain architectures and decentralized system protocols"
            },
            "smart_contract_developer": {
                "title": "Smart Contract Developer",
                "expertise": ["solidity", "ethereum", "defi", "security_auditing", "gas_optimization"],
                "model_preference": "coding_heavy",
                "description": "Develops and audits smart contracts for various blockchain platforms"
            },
            "defi_architect": {
                "title": "DeFi Protocol Architect", 
                "expertise": ["defi", "liquidity", "yield_farming", "tokenomics", "amm"],
                "model_preference": "reasoning_heavy",
                "description": "Designs decentralized finance protocols and tokenomics models"
            },
            "web3_frontend_developer": {
                "title": "Web3 Frontend Developer",
                "expertise": ["react", "web3js", "ethers", "metamask", "ipfs"],
                "model_preference": "coding_heavy",
                "description": "Builds decentralized application frontends with Web3 integration"
            },
            
            # IOT & EMBEDDED
            "iot_architect": {
                "title": "IoT Solutions Architect",
                "expertise": ["iot", "sensors", "edge_computing", "protocols", "connectivity"],
                "model_preference": "reasoning_heavy",
                "description": "Designs end-to-end IoT solutions and device ecosystems"
            },
            "embedded_developer": {
                "title": "Embedded Systems Developer",
                "expertise": ["c", "cpp", "arduino", "raspberry_pi", "rtos", "firmware"],
                "model_preference": "coding_heavy",
                "description": "Develops firmware and embedded software for IoT devices"
            },
            "hardware_engineer": {
                "title": "Hardware Design Engineer",
                "expertise": ["circuit_design", "pcb", "sensors", "microcontrollers", "power_management"],
                "model_preference": "reasoning_heavy", 
                "description": "Designs hardware components and electronic systems for IoT devices"
            },
            
            # FINTECH & FINANCE
            "fintech_architect": {
                "title": "FinTech Solutions Architect",
                "expertise": ["finance", "payments", "regulations", "risk_management", "compliance"],
                "model_preference": "reasoning_heavy",
                "description": "Designs financial technology solutions with regulatory compliance"
            },
            "payment_specialist": {
                "title": "Payment Integration Specialist", 
                "expertise": ["payment_gateways", "pci_compliance", "fraud_detection", "apis"],
                "model_preference": "coding_heavy",
                "description": "Integrates payment systems and ensures secure transaction processing"
            },
            "quantitative_analyst": {
                "title": "Quantitative Financial Analyst",
                "expertise": ["quantitative_finance", "risk_modeling", "algorithms", "mathematics"],
                "model_preference": "reasoning_heavy",
                "description": "Develops quantitative models for trading and risk management"
            },
            "compliance_officer": {
                "title": "Financial Compliance Specialist",
                "expertise": ["regulations", "kyc", "aml", "gdpr", "sox", "auditing"],
                "model_preference": "reasoning_heavy",
                "description": "Ensures regulatory compliance and implements governance frameworks"
            },
            
            # SECURITY SPECIALISTS  
            "security_architect": {
                "title": "Cybersecurity Solutions Architect",
                "expertise": ["security", "threat_modeling", "zero_trust", "encryption", "compliance"],
                "model_preference": "reasoning_heavy",
                "description": "Designs comprehensive security architectures and threat mitigation strategies"
            },
            "security_developer": {
                "title": "Security Software Developer",
                "expertise": ["secure_coding", "penetration_testing", "vulnerability_assessment", "owasp"],
                "model_preference": "coding_heavy",
                "description": "Develops secure software and implements security controls"
            },
            "penetration_tester": {
                "title": "Senior Penetration Tester",
                "expertise": ["pen_testing", "vulnerability_assessment", "red_teaming", "social_engineering"],
                "model_preference": "reasoning_heavy",
                "description": "Conducts security assessments and ethical hacking exercises"
            },
            
            # GAME DEVELOPMENT
            "game_architect": {
                "title": "Game Systems Architect", 
                "expertise": ["game_engines", "unity", "unreal", "networking", "performance"],
                "model_preference": "reasoning_heavy",
                "description": "Designs game architectures and technical systems for optimal performance"
            },
            "game_designer": {
                "title": "Senior Game Designer",
                "expertise": ["game_mechanics", "user_experience", "monetization", "analytics"],
                "model_preference": "reasoning_heavy", 
                "description": "Creates engaging game mechanics and user experience flows"
            },
            "unity_developer": {
                "title": "Unity Game Developer",
                "expertise": ["unity", "csharp", "game_programming", "3d_graphics", "shaders"],
                "model_preference": "coding_heavy",
                "description": "Develops games and interactive applications using Unity engine"
            },
            "graphics_engineer": {
                "title": "Graphics Programming Engineer",
                "expertise": ["graphics_programming", "shaders", "rendering", "optimization", "gpu"],
                "model_preference": "coding_heavy",
                "description": "Develops advanced graphics systems and rendering pipelines"
            },
            
            # HEALTHCARE & MEDICAL
            "healthcare_architect": {
                "title": "Healthcare Solutions Architect",
                "expertise": ["healthcare", "hipaa", "hl7", "interoperability", "medical_workflows"],
                "model_preference": "reasoning_heavy",
                "description": "Designs healthcare systems with regulatory compliance and interoperability"
            },
            "medical_data_specialist": {
                "title": "Medical Data Systems Specialist", 
                "expertise": ["medical_data", "hl7", "fhir", "interoperability", "privacy"],
                "model_preference": "coding_heavy",
                "description": "Manages medical data systems and healthcare interoperability standards"
            },
            
            # TRADITIONAL DEVELOPMENT ROLES (Enhanced)
            "backend_developer": {
                "title": "Senior Backend Developer",
                "expertise": ["apis", "databases", "microservices", "performance", "security"],
                "model_preference": "coding_heavy",
                "description": "Develops robust backend systems and APIs with focus on performance and security"
            },
            "frontend_developer": {
                "title": "Senior Frontend Developer", 
                "expertise": ["react", "vue", "angular", "typescript", "performance", "accessibility"],
                "model_preference": "coding_heavy",
                "description": "Creates modern, responsive user interfaces with excellent user experience"
            },
            "mobile_architect": {
                "title": "Mobile Solutions Architect",
                "expertise": ["mobile_architecture", "cross_platform", "performance", "native_development"],
                "model_preference": "reasoning_heavy",
                "description": "Designs mobile application architectures for optimal performance and user experience"
            },
            "ios_developer": {
                "title": "Senior iOS Developer",
                "expertise": ["swift", "ios", "xcode", "app_store", "mobile_ui"],
                "model_preference": "coding_heavy",
                "description": "Develops native iOS applications with modern Swift and iOS frameworks"
            },
            "android_developer": {
                "title": "Senior Android Developer",
                "expertise": ["kotlin", "android", "jetpack_compose", "google_play", "mobile_ui"],
                "model_preference": "coding_heavy",
                "description": "Develops native Android applications using modern Android technologies"
            }
        }
    
    def create_agent_team(self, project_type: str, project_description: str, 
                         custom_requirements: List[str] = None) -> List[Agent]:
        """Create comprehensive agent team for any project type"""
        
        print(f"🎯 Creating specialized agent team for: {project_type.upper()}")
        print(f"📋 Project: {project_description}")
        if custom_requirements:
            print(f"🔧 Custom Requirements: {', '.join(custom_requirements)}")
        print()
        
        # Get base agent roles for project type
        base_roles = self.project_templates.get(project_type, ["system_architect", "backend_developer", "qa_engineer"])
        
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
                print(f"   🧠 Model: {agent.llm.model}")
                print(f"   🔧 Expertise: {', '.join(role_info['expertise'][:3])}...")
                print()
            else:
                print(f"⚠️ Unknown role: {role}, skipping...")
        
        print(f"🎉 Elite agent team assembled! {len(agents)} specialists ready for {project_type}")
        return agents
    
    def _analyze_custom_requirements(self, requirements: List[str]) -> List[str]:
        """Analyze custom requirements and suggest additional agent roles"""
        additional_roles = []
        
        requirement_mapping = {
            "blockchain": ["blockchain_architect", "smart_contract_developer"],
            "ai": ["ai_architect", "data_scientist", "ml_engineer"],
            "machine learning": ["data_scientist", "ml_engineer", "data_engineer"],
            "iot": ["iot_architect", "embedded_developer", "hardware_engineer"],
            "security": ["security_architect", "security_developer"],
            "fintech": ["fintech_architect", "payment_specialist", "compliance_officer"],
            "healthcare": ["healthcare_architect", "medical_data_specialist"],
            "gaming": ["game_architect", "game_designer", "unity_developer"],
            "mobile": ["mobile_architect", "ios_developer", "android_developer"],
            "cloud": ["cloud_architect", "devops_engineer"],
            "data": ["data_engineer", "data_scientist"]
        }
        
        for requirement in requirements:
            req_lower = requirement.lower()
            for keyword, roles in requirement_mapping.items():
                if keyword in req_lower:
                    additional_roles.extend(roles)
        
        return list(set(additional_roles))  # Remove duplicates
    
    def _create_specialized_agent(self, role: str, project_description: str, project_type: str) -> Agent:
        """Create a specialized agent with comprehensive configuration"""
        
        # Get role information
        role_info = self.agent_roles.get(role, {
            "title": role.replace("_", " ").title(),
            "expertise": ["general"],
            "model_preference": "balanced",
            "description": f"Specialist in {role.replace('_', ' ')}"
        })
        
        # Select optimal model based on role preference
        llm = self._select_optimal_model(role, role_info["model_preference"])
        
        # Create comprehensive goal and backstory
        goal = self._generate_role_goal(role, project_description, role_info)
        backstory = self._generate_role_backstory(role, role_info)
        
        return Agent(
            role=role_info["title"],
            goal=goal,
            backstory=backstory, 
            llm=llm,
            tools=self.file_tools,
            verbose=True,
            memory=True,
            allow_delegation=False,
            max_iter=5,  # Prevent infinite loops
            max_execution_time=300  # 5 minute timeout per agent
        )
    
    def _select_optimal_model(self, role: str, preference: str) -> Any:
        """Select the optimal model based on role and preference"""
        if preference == "reasoning_heavy":
            # Use high-reasoning models for architecture and strategy
            return self.model_config.get_model_for_role("system_architect")
        elif preference == "coding_heavy": 
            # Use coding-optimized models for development
            return self.model_config.get_model_for_role("backend_developer")
        else:
            # Balanced approach
            return self.model_config.get_model_for_role(role)
    
    def _generate_role_goal(self, role: str, project_description: str, role_info: Dict) -> str:
        """Generate comprehensive goal for the role"""
        base_goal = f"""As a {role_info['title']}, deliver expert solutions for: {project_description}

Your core responsibilities:
- Apply deep expertise in: {', '.join(role_info['expertise'])}
- Ensure best practices and industry standards compliance
- Collaborate effectively with other specialists
- Deliver production-ready, maintainable solutions
- Document your decisions and provide clear rationale

Focus Areas: {role_info['description']}
"""
        return base_goal
    
    def _generate_role_backstory(self, role: str, role_info: Dict) -> str:
        """Generate comprehensive backstory for the role"""
        return f"""You are a highly experienced {role_info['title']} with deep expertise in {', '.join(role_info['expertise'][:5])}.

You have successfully delivered complex projects across various industries and are known for:
- Technical excellence and innovative problem-solving
- Strong collaboration with cross-functional teams  
- Commitment to quality, security, and best practices
- Ability to mentor junior team members
- Staying current with latest industry trends and technologies

{role_info['description']}

You approach every project with professionalism, technical rigor, and a focus on delivering exceptional results that exceed client expectations."""

    def list_available_project_types(self) -> Dict[str, List[str]]:
        """List all available project types organized by category"""
        categories = {
            "Traditional Applications": [
                "web_application", "api_service", "mobile_app", "cli_tool"
            ],
            "Enterprise & Business": [
                "erp_system", "crm_platform", "ecommerce_platform", "supply_chain_system", "business_intelligence"
            ],
            "AI/ML & Data Science": [
                "ai_ml_application", "deep_learning_project", "nlp_system", "computer_vision"
            ],
            "Blockchain & Web3": [
                "blockchain_project", "defi_platform", "nft_platform", "dapp_development"
            ],
            "IoT & Edge Computing": [
                "iot_solution", "edge_computing", "smart_home_system"
            ],
            "AR/VR & Gaming": [
                "ar_application", "vr_application", "game_development", "metaverse_platform"
            ],
            "FinTech": [
                "fintech_application", "trading_platform", "payment_gateway", "robo_advisor"
            ],
            "HealthTech": [
                "healthtech_application", "telemedicine_platform", "medical_device_software"
            ],
            "EdTech": [
                "edtech_platform", "lms_system", "adaptive_learning"
            ],
            "Security & Infrastructure": [
                "cybersecurity_software", "devsecops_platform", "cloud_infrastructure", "network_management"
            ],
            "Industry Solutions": [
                "agritech_solution", "proptech_platform", "logistics_system"
            ],
            "Media & Entertainment": [
                "streaming_platform", "social_media_platform", "content_management"
            ]
        }
        return categories

    def get_role_expertise_map(self) -> Dict[str, List[str]]:
        """Get mapping of roles to their expertise areas"""
        return {role: info["expertise"] for role, info in self.agent_roles.items()}
