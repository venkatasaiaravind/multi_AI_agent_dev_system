# test_master_orchestrator.py
import asyncio
from core.master_orchestrator import MasterOrchestrator

async def test_master_orchestrator():
    print("🚀 TESTING MASTER ORCHESTRATOR SYSTEM")
    print("=" * 80)
    
    orchestrator = MasterOrchestrator()
    
    # Test cases with different complexity levels
    test_projects = [
        {
            "name": "Simple Web App Test",
            "requirements": {
                "type": "web_application",
                "description": "A simple todo list application with user authentication and task management",
                "custom_requirements": ["authentication", "database"]
            }
        },
        {
            "name": "AI/ML Project Test", 
            "requirements": {
                "type": "ai_ml_application",
                "description": "AI-powered sentiment analysis system for social media monitoring with real-time dashboard",
                "custom_requirements": ["nlp", "real-time", "dashboard", "sentiment_analysis"]
            }
        }
    ]
    
    for i, test_project in enumerate(test_projects, 1):
        print(f"\n🧪 TEST CASE {i}: {test_project['name']}")
        print("=" * 60)
        
        try:
            result = await orchestrator.create_project(test_project["requirements"])
            
            if result["success"]:
                print(f"\n✅ SUCCESS!")
                print(f"📁 Project Location: {result['workspace_path']}")
                print(f"⏱️ Execution Time: {result['execution_time']:.1f}s")
                print(f"🤖 Agents Used: {result['agents_used']}")
                print(f"📋 Tasks Completed: {result['tasks_completed']}")
                print(f"🎯 Quality Score: {result.get('quality_metrics', {}).get('quality_score', 'N/A')}")
            else:
                print(f"\n❌ FAILED: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"\n💥 EXCEPTION: {str(e)}")
        
        print(f"\n{'='*60}")
    
    print(f"\n🎉 Master Orchestrator testing complete!")
    print("Ready for full project generation!")

if __name__ == "__main__":
    asyncio.run(test_master_orchestrator())
