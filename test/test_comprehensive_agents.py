# test_comprehensive_agents.py
from core.comprehensive_agent_factory import ComprehensiveAgentFactory
# At the top of test_master_orchestrator.py
import sys
import os

# Fix Windows console encoding
if sys.platform.startswith('win'):
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8', errors='ignore')
    sys.stderr.reconfigure(encoding='utf-8', errors='ignore')

def test_comprehensive_system():
    print("🚀 TESTING COMPREHENSIVE MULTI-AGENT SYSTEM")
    print("=" * 80)
    
    factory = ComprehensiveAgentFactory()
    
    # Display available project types
    print("\n📋 AVAILABLE PROJECT TYPES:")
    categories = factory.list_available_project_types()
    for category, types in categories.items():
        print(f"\n🏷️ {category}:")
        for project_type in types:
            print(f"   • {project_type}")
    
    print("\n" + "=" * 80)
    
    # Test advanced project types
    test_cases = [
        {
            "type": "ai_ml_application",
            "description": "AI-powered customer service chatbot with sentiment analysis, multilingual support, and integration with CRM systems",
            "custom_req": ["nlp", "sentiment_analysis", "cloud_deployment"]
        },
        {
            "type": "defi_platform", 
            "description": "Decentralized lending protocol with automated market making, yield farming, and governance token",
            "custom_req": ["smart_contracts", "tokenomics", "security_audit"]
        },
        {
            "type": "iot_solution",
            "description": "Smart factory monitoring system with predictive maintenance, real-time analytics, and edge computing",
            "custom_req": ["industrial_iot", "predictive_analytics", "edge_computing"]
        },
        {
            "type": "fintech_application",
            "description": "Algorithmic trading platform with risk management, regulatory compliance, and real-time market data",
            "custom_req": ["algorithmic_trading", "compliance", "real_time_data"]
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 TEST CASE {i}: {test_case['type'].upper()}")
        print("=" * 60)
        
        agents = factory.create_agent_team(
            test_case["type"],
            test_case["description"], 
            test_case["custom_req"]
        )
        
        print(f"\n TEAM SUMMARY:")
        print(f"   • Total Specialists: {len(agents)}")
        print(f"   • Project Complexity: Advanced")
        print(f"   • Technology Stack: Cutting-edge")
        
        # Show agent expertise distribution
        expertise_count = {}
        for agent in agents:
            role = next((role for role, info in factory.agent_roles.items() 
                        if info["title"] == agent.role), "unknown")
            if role != "unknown":
                for expertise in factory.agent_roles[role]["expertise"][:2]:
                    expertise_count[expertise] = expertise_count.get(expertise, 0) + 1
        
        print(f"   • Top Expertise Areas: {', '.join(list(expertise_count.keys())[:5])}")
        print(f"   • Ready for: {test_case['type'].replace('_', ' ').title()} Development")
        print()

if __name__ == "__main__":
    test_comprehensive_system()
