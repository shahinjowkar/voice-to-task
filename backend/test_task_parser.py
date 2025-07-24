#!/usr/bin/env python3
"""
Test script for Task Parser
"""
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_task_parser():
    """Test the task parser with various voice commands"""
    try:
        from app.utils.task_parser import TaskParser
        
        print("🧪 Testing Task Parser")
        print("=" * 50)
        
        # Initialize parser
        print("📦 Loading Task Parser...")
        parser = TaskParser()
        print("✅ Task Parser loaded successfully!")
        
        # Test cases using key words: assign, user, deadline
        test_cases = [
            # Perfect format
            'assign "review quarterly report" user "Alex" deadline "Friday"',
            
            # Without deadline
            'assign "create landing page" user "Sarah"',
            
            # Your actual voice command (adapted)
            'assign "task 1" user "individual 2" deadline "next week"',
            
            # Natural language deadline
            'assign "update website" user "John" deadline "next week"',
            
            # Today/tomorrow
            'assign "send email" user "Mike" deadline "tomorrow"',
            
            # Complex task name
            'assign "finalize the quarterly financial report" user "Alex Johnson" deadline "Friday"',
        ]
        
        print("\n📝 Testing Task Parsing:")
        print("=" * 50)
        
        for i, test_text in enumerate(test_cases, 1):
            print(f"\n🧪 Test {i}: '{test_text}'")
            print("-" * 40)
            
            result = parser.parse_task_command(test_text)
            
            if result['success']:
                print("✅ SUCCESS!")
                print(f"   📋 Task: {result['title']}")
                print(f"   👤 Assignee: {result['assignee']}")
                print(f"   📅 Deadline: {result['deadline']}")
                if result['errors']:
                    print(f"   ⚠️  Warnings: {result['errors']}")
            else:
                print("❌ FAILED!")
                print(f"   Errors: {result['errors']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing task parser: {e}")
        return False

def main():
    """Main function"""
    print("🎙️ VoiceTaskAI - Task Parser Test")
    print("=" * 50)
    
    success = test_task_parser()
    
    if success:
        print("\n🎉 Task parser test completed!")
        print("✅ Ready for Step 2.2: Enhanced parsing")
    else:
        print("\n❌ Task parser test failed!")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 