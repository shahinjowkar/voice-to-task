#!/usr/bin/env python3
"""
Test script for construction and real estate voice commands
Demonstrates task parsing with industry-specific categories
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.task_parser import TaskParser

def test_construction_commands():
    """Test construction and real estate specific voice commands"""
    
    print("🏗️ Construction & Real Estate Voice Commands Test")
    print("=" * 60)
    
    parser = TaskParser()
    
    # Construction and real estate specific test commands
    test_commands = [
        # Construction Tasks
        "Task pour concrete foundation user John category Construction deadline next Friday",
        "Task install electrical wiring user Mike category Construction deadline this week",
        "Task frame second floor user Sarah category Construction deadline Monday",
        "Task build retaining wall user Bob category Construction deadline today",
        "Task install windows user Alice category Construction deadline Wednesday",
        
        # Inspection Tasks
        "Task inspect foundation work user Mike category Inspection deadline tomorrow",
        "Task check electrical compliance user Sarah category Inspection deadline today",
        "Task review plumbing installation user John category Inspection deadline Monday",
        "Task verify building code user Bob category Inspection deadline this week",
        "Task test fire alarm system user Alice category Inspection deadline Friday",
        
        # Maintenance Tasks
        "Task repair leaking roof user Sarah category Maintenance deadline today",
        "Task service HVAC units user Mike category Maintenance deadline this week",
        "Task fix electrical issues user John category Maintenance deadline tomorrow",
        "Task replace broken window user Bob category Maintenance deadline Monday",
        "Task troubleshoot heating system user Alice category Maintenance deadline Friday",
    ]
    
    print(f"Available Categories: {parser.predefined_categories}")
    print(f"Available Users: {parser.predefined_users}")
    print()
    
    for i, command in enumerate(test_commands, 1):
        print(f"Test {i:2d}: '{command}'")
        result = parser.parse_task_command(command)
        
        print(f"  → Title: '{result.get('title', 'None')}'")
        print(f"  → Assignee: '{result.get('assignee', 'None')}'")
        print(f"  → Category: '{result.get('category', 'None')}'")
        print(f"  → Deadline: '{result.get('deadline', 'None')}'")
        
        if 'assignee_similarity' in result:
            print(f"  → Assignee Similarity:")
            for user, score in result['assignee_similarity'][:2]:  # Show top 2
                print(f"    - {user}: {score:.3f}")
        
        if 'category_similarity' in result:
            print(f"  → Category Similarity:")
            for category, score in result['category_similarity'][:2]:  # Show top 2
                print(f"    - {category}: {score:.3f}")
        
        print(f"  → Success: {result.get('success', False)}")
        if result.get('errors'):
            print(f"  → Errors: {result['errors']}")
        print("-" * 60)

def show_voice_command_format():
    """Show the voice command format and tips"""
    
    print("🎤 Voice Command Format Guide")
    print("=" * 60)
    
    print("""
📋 STANDARD FORMAT:
"Task [task description] user [assignee name] category [category] deadline [deadline]"

📝 EXAMPLES:
• "Task pour concrete foundation user John category Construction deadline next Friday"
• "Task inspect electrical systems user Mike category Inspection deadline tomorrow"
• "Task repair leaking roof user Sarah category Maintenance deadline today"
• "Task create property listing user Lisa category Marketing deadline next week"

🎯 KEYWORDS TO REMEMBER:
• Start with: "Task"
• Assignee: "user [name]"
• Category: "category [category]"
• Deadline: "deadline [date]"

🗣️ RECORDING TIPS:
• Speak clearly and at moderate pace
• Pause briefly between sections
• Use natural language for deadlines
• Be specific with task descriptions
• Use full names for better matching

📅 COMMON DEADLINES:
• "today", "tomorrow", "this week", "next week"
• "Monday", "Tuesday", "Wednesday", etc.
• "next Friday", "end of month"
• Specific dates: "January 15th", "March 3rd 2025"
""")

if __name__ == "__main__":
    show_voice_command_format()
    print("\n" + "="*60 + "\n")
    test_construction_commands() 