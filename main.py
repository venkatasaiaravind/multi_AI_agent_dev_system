import asyncio
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from core.master_orchestrator import MasterOrchestrator

# Fix Windows console encoding
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
        sys.stderr.reconfigure(encoding='utf-8', errors='ignore')
    except:
        pass

# Load environment variables
load_dotenv()

def display_banner():
    """Display system banner and capabilities"""
    print("=" * 80)
    print("🤖 ADVANCED MULTI-AGENT DEVELOPMENT SYSTEM")
    print("=" * 80)
    print("🚀 Transform your IDEAS into complete software projects")
    print("💡 From concept to production-ready code in minutes")
    print("🎯 Supports 40+ technologies: AI/ML, Blockchain, IoT, Web, Mobile & More")
    print("🤖 80+ Specialized AI agents working together")
    print("💰 Uses only FREE models - no API costs")
    print("=" * 80)

def show_project_categories():
    """Display available project categories with examples"""
    categories = {
        "🌐 Web & Mobile Applications": [
            "Modern web applications with React/Vue + Node.js backend",
            "Mobile apps with React Native or native iOS/Android",
            "Progressive web apps with offline capabilities",
            "E-commerce platforms with payment integration"
        ],
        
        "🤖 AI & Machine Learning": [
            "Computer vision systems for image/video analysis", 
            "Natural language processing applications",
            "Predictive analytics and recommendation engines",
            "Chatbots and conversational AI systems"
        ],
        
        "🔗 Blockchain & Web3": [
            "DeFi platforms with smart contracts and yield farming",
            "NFT marketplaces with minting and trading",
            "Cryptocurrency wallets and exchange platforms",
            "Decentralized autonomous organizations (DAOs)"
        ],
        
        "🏭 IoT & Industrial": [
            "Smart home automation systems",
            "Industrial monitoring with predictive maintenance",
            "Agricultural technology with sensor networks",
            "Supply chain tracking and logistics"
        ],
        
        "💳 FinTech & Business": [
            "Payment processing and digital wallets",
            "Algorithmic trading platforms",
            "Personal finance management apps",
            "Enterprise resource planning (ERP) systems"
        ],
        
        "🏥 Healthcare & Education": [
            "Telemedicine platforms with video consultation",
            "Electronic health records (EHR) systems",
            "Online learning management systems",
            "Educational content and assessment platforms"
        ],
        
        "🎮 Gaming & Entertainment": [
            "Video games with multiplayer capabilities",
            "Streaming platforms for content delivery",
            "Social media and community platforms",
            "AR/VR applications and experiences"
        ],
        
        "🔒 Security & Infrastructure": [
            "Cybersecurity monitoring and threat detection",
            "DevSecOps platforms and CI/CD pipelines",
            "Cloud infrastructure management tools",
            "Network monitoring and optimization systems"
        ]
    }
    
    print("\n📋 WHAT CAN WE BUILD FOR YOU?")
    print("=" * 60)
    
    for category, examples in categories.items():
        print(f"\n{category}")
        for i, example in enumerate(examples, 1):
            print(f"   {i}. {example}")
    
    print("\n💡 And many more! Describe any software idea and we'll build it.")

def get_user_idea():
    """Get user's project idea with guided prompting"""
    print("\n🎯 DESCRIBE YOUR PROJECT IDEA")
    print("=" * 50)
    print("💡 The more details you provide, the better the result!")
    print("🔥 Include: purpose, features, target users, technology preferences")
    print()
    
    # Main project description
    while True:
        description = input("📝 What do you want to build? (Be as detailed as possible)\n💬 Your idea: ").strip()
        if len(description) < 10:
            print("❌ Please provide more details (at least 10 characters)")
            continue
        break
    
    print(f"\n✅ Got it: {description}")
    
    # Project type selection
    print(f"\n🏷️ What type of project is this?")
    project_types = {
        "1": ("web_application", "Web Application (websites, web apps)"),
        "2": ("mobile_app", "Mobile Application (iOS, Android, cross-platform)"),
        "3": ("ai_ml_application", "AI/ML Application (machine learning, data science)"),
        "4": ("blockchain_project", "Blockchain/Web3 (DeFi, NFT, crypto)"), 
        "5": ("api_service", "API Service (REST APIs, microservices)"),
        "6": ("iot_solution", "IoT Solution (sensors, devices, automation)"),
        "7": ("fintech_application", "FinTech (payments, trading, finance)"),
        "8": ("game_development", "Game Development (video games, AR/VR)"),
        "9": ("healthtech_application", "HealthTech (medical, telemedicine)"),
        "10": ("ecommerce_platform", "E-commerce (online stores, marketplaces)"),
        "custom": ("custom", "Custom Type (I'll specify)")
    }
    
    for key, (_, desc) in project_types.items():
        print(f"   {key}. {desc}")
    
    while True:
        choice = input(f"\n🎯 Select project type (1-10 or 'custom'): ").strip().lower()
        if choice in project_types:
            if choice == "custom":
                project_type = input("📝 Enter your custom project type: ").strip()
                if not project_type:
                    project_type = "custom_application"
            else:
                project_type = project_types[choice][0]
            break
        print("❌ Invalid choice. Please try again.")
    
    # Technology preferences
    print(f"\n🔧 Any specific technologies you want to use?")
    print("💡 Examples: React, Python, Node.js, TensorFlow, Solidity, etc.")
    tech_input = input("🛠️  Technology preferences (comma-separated, or press Enter to skip): ").strip()
    tech_preferences = [tech.strip() for tech in tech_input.split(",") if tech.strip()] if tech_input else []
    
    # Target users
    target_users = input(f"\n👥 Who are the target users? (e.g., consumers, businesses, developers): ").strip()
    if not target_users:
        target_users = "general users"
    
    # Key features
    print(f"\n✨ What are the main features you want?")
    features_input = input("📋 Key features (comma-separated): ").strip()
    key_features = [feat.strip() for feat in features_input.split(",") if feat.strip()] if features_input else []
    
    # Additional requirements
    additional = input(f"\n🎨 Any additional requirements? (scalability, security, integrations, etc.): ").strip()
    
    # Compile complete requirements
    enhanced_description = f"{description}"
    
    if target_users != "general users":
        enhanced_description += f" The target users are {target_users}."
    
    if key_features:
        enhanced_description += f" Key features include: {', '.join(key_features)}."
    
    if additional:
        enhanced_description += f" Additional requirements: {additional}."
    
    # Build custom requirements list
    custom_requirements = []
    if tech_preferences:
        custom_requirements.extend(tech_preferences)
    if key_features:
        custom_requirements.extend(key_features)
    if additional:
        custom_requirements.extend([req.strip() for req in additional.replace(',', ' ').split() if len(req.strip()) > 2])
    
    return {
        "description": enhanced_description,
        "type": project_type,
        "custom_requirements": list(set(custom_requirements)),  # Remove duplicates
        "original_idea": description,
        "target_users": target_users,
        "tech_preferences": tech_preferences,
        "key_features": key_features
    }

def show_project_summary(requirements):
    """Display project summary for confirmation"""
    print(f"\n🎯 PROJECT SUMMARY")
    print("=" * 60)
    print(f"📝 Original Idea: {requirements['original_idea']}")
    print(f"🏷️  Project Type: {requirements['type'].replace('_', ' ').title()}")
    print(f"👥 Target Users: {requirements['target_users']}")
    
    if requirements['tech_preferences']:
        print(f"🔧 Technologies: {', '.join(requirements['tech_preferences'])}")
    
    if requirements['key_features']:
        print(f"✨ Key Features: {', '.join(requirements['key_features'])}")
    
    if requirements['custom_requirements']:
        print(f"🎨 Requirements: {', '.join(requirements['custom_requirements'][:5])}")
        if len(requirements['custom_requirements']) > 5:
            print(f"    ... and {len(requirements['custom_requirements']) - 5} more")
    
    print(f"\n📖 Enhanced Description:")
    print(f"💬 {requirements['description']}")
    print("=" * 60)

async def main():
    display_banner()
    
    # Verify API keys
    if not os.getenv("OPENROUTER_API_KEY") or not os.getenv("GROQ_API_KEY"):
        print("\n❌ ERROR: API Keys Not Found!")
        print("=" * 40)
        print("Please add your API keys to the .env file:")
        print("OPENROUTER_API_KEY=sk-or-v1-your-key-here")
        print("GROQ_API_KEY=gsk_your-key-here")
        print("\n🔗 Get free keys at:")
        print("• OpenRouter: https://openrouter.ai")
        print("• Groq: https://console.groq.com")
        return
    
    # Initialize orchestrator
    try:
        print(f"\n🔄 Initializing AI Agent System...")
        orchestrator = MasterOrchestrator()
        print("✅ System ready! 80+ specialized agents loaded.")
    except Exception as e:
        print(f"❌ Failed to initialize system: {e}")
        return
    
    # Main interaction loop
    while True:
        print(f"\n🎯 WHAT WOULD YOU LIKE TO DO?")
        print("=" * 40)
        print("1. 🚀 Build a new project from my idea")
        print("2. 📋 See examples of what we can build") 
        print("3. 📊 View system capabilities")
        print("4. 🚪 Exit")
        
        choice = input(f"\n💬 Your choice (1-4): ").strip()
        
        if choice == "1":
            # Build new project
            print(f"\n🎉 GREAT! Let's bring your idea to life!")
            
            try:
                # Get user's idea
                requirements = get_user_idea()
                
                # Show summary and confirm
                show_project_summary(requirements)
                
                confirm = input(f"\n✅ Ready to build this project? (y/n): ").strip().lower()
                if confirm != 'y':
                    print("💡 No problem! Feel free to refine your idea and try again.")
                    continue
                
                # Generate the project
                print(f"\n🚀 STARTING PROJECT GENERATION")
                print("=" * 80)
                print("⏳ This will take 5-20 minutes depending on complexity...")
                print("📊 You can monitor progress in real-time below:")
                print("🤖 Our AI agents are working on your project...")
                print("=" * 80)
                
                start_time = datetime.now()
                result = await orchestrator.create_project(requirements)
                end_time = datetime.now()
                
                if result["success"]:
                    print(f"\n🎉 PROJECT GENERATION COMPLETED!")
                    print("=" * 80)
                    print(f"✅ SUCCESS! Your project is ready!")
                    print(f"📁 Location: {result['workspace_path']}")
                    print(f"⏱️  Total Time: {(end_time - start_time).total_seconds():.1f} seconds")
                    print(f"🤖 AI Agents Used: {result['agents_used']}")
                    print(f"📋 Tasks Completed: {result['tasks_completed']}")
                    print(f"📄 Files Generated: {result.get('quality_metrics', {}).get('files_generated', 'Multiple')}")
                    print(f"🎯 Quality Score: {result.get('quality_metrics', {}).get('quality_score', 'High')}%")
                    print("=" * 80)
                    print(f"\n📖 NEXT STEPS:")
                    print(f"1. Open the project folder: {result['workspace_path']}")
                    print(f"2. Read the README.md for setup instructions")
                    print(f"3. Follow the architecture documentation in /docs/")
                    print(f"4. Run the project and start customizing!")
                    print(f"\n🚀 Your AI-generated project is ready for development!")
                
                else:
                    print(f"\n❌ PROJECT GENERATION FAILED")
                    print(f"Error: {result.get('error', 'Unknown error')}")
                    if result.get('partial_workspace'):
                        print(f"Partial work saved at: {result['partial_workspace']}")
                        print(f"You can check what was generated so far.")
                
            except KeyboardInterrupt:
                print(f"\n⚠️  Generation stopped by user")
                print("💡 No worries! You can try again anytime.")
            except Exception as e:
                print(f"\n💥 Unexpected error: {str(e)}")
                print("🔧 Please check your API keys and internet connection.")
        
        elif choice == "2":
            # Show examples
            show_project_categories()
            input(f"\nPress Enter to continue...")
        
        elif choice == "3":
            # Show capabilities
            print(f"\n🤖 SYSTEM CAPABILITIES")
            print("=" * 50)
            print("🎯 Project Types: 40+ (Web, Mobile, AI/ML, Blockchain, IoT, etc.)")
            print("🤖 AI Agents: 80+ specialized roles")
            print("🧠 AI Models: Free models from OpenRouter & Groq")
            print("💰 Cost: $0 - completely free to use")
            print("⚡ Speed: 5-20 minutes per project")
            print("🎨 Quality: Production-ready code with documentation")
            print("🔧 Output: Complete projects with setup instructions")
            print("📁 Storage: All files saved locally in organized structure")
            print("🚀 Technologies: Latest frameworks and best practices")
            
            categories = orchestrator.agent_factory.list_available_project_types()
            print(f"\n📋 Available Project Categories: {len(categories)}")
            for category in categories.keys():
                print(f"   • {category}")
            
            input(f"\nPress Enter to continue...")
        
        elif choice == "4":
            print(f"\n👋 Thanks for using the Multi-Agent Development System!")
            print("🚀 Happy coding with your AI-generated projects!")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n👋 Goodbye! Thanks for using the Multi-Agent Development System!")
