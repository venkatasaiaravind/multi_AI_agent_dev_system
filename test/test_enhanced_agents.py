# test_enhanced_agents.py
from core.agent_factory import AgentFactory

print("🚀 Testing Enhanced Agent Factory with Reasoning Models\n")

# Test agent factory with your new reasoning configuration
factory = AgentFactory()

# Test different project types
test_projects = [
    {
        "type": "web_application",
        "description": "A modern e-commerce platform with user authentication, product catalog, shopping cart, and payment processing"
    },
    {
        "type": "api_service", 
        "description": "A RESTful API for a social media platform with posts, comments, likes, and user management"
    }
]

for project in test_projects:
    print(f"=" * 60)
    print(f"Testing: {project['type']}")
    print(f"=" * 60)
    
    agents = factory.create_agent_team(
        project["type"], 
        project["description"]
    )
    
    print(f"📊 Summary:")
    print(f"   • Created {len(agents)} specialized agents")
    print(f"   • Each agent has reasoning-optimized models")
    print(f"   • Ready for {project['type']} development")
    print()
