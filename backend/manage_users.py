#!/usr/bin/env python3
"""
User management script for VoiceTaskAI
Allows viewing and updating the predefined users list
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config import settings
from app.utils.task_parser import TaskParser

def show_current_users():
    """Display current predefined users"""
    print("👥 Current Predefined Users")
    print("=" * 40)
    
    users = settings.predefined_users_list
    if users:
        for i, user in enumerate(users, 1):
            print(f"{i}. {user}")
    else:
        print("No users defined")
    print()

def test_user_mapping():
    """Test user name mapping with current users"""
    print("🎯 Testing User Name Mapping")
    print("=" * 40)
    
    parser = TaskParser()
    users = settings.predefined_users_list
    
    if not users:
        print("No users defined to test with")
        return
    
    # Test with variations of each user
    test_cases = []
    for user in users:
        test_cases.extend([
            user.lower(),
            user + " user",
            user + "e",  # Common transcription error
            user[:-1] if len(user) > 1 else user,  # Missing last letter
        ])
    
    # Add some common transcription errors
    test_cases.extend([
        "alice", "alise", "alicee",
        "bob", "bobb", "bob user",
        "charlie", "charley", "charli",
        "address", "adress",  # From your test case
        "unknown", "xyz"
    ])
    
    for test_name in test_cases:
        mapped_name = parser._map_user_name(test_name)
        similarity_matrix = parser._calculate_similarity_matrix(test_name)
        
        print(f"'{test_name}' → '{mapped_name}'")
        print(f"  Similarity scores:")
        for user, score in similarity_matrix[:3]:  # Show top 3
            print(f"    {user}: {score:.3f}")
        print()

def update_users(new_users):
    """Update the predefined users list"""
    print("🔄 Updating Predefined Users")
    print("=" * 40)
    
    # Convert list to comma-separated string
    users_str = ",".join(new_users)
    
    # Update environment variable
    os.environ["PREDEFINED_USERS"] = users_str
    
    print(f"Updated users: {new_users}")
    print("Note: This change will take effect when you restart the application")
    print("To make it permanent, add to your .env file:")
    print(f"PREDEFINED_USERS={users_str}")
    print()

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manage_users.py show          # Show current users")
        print("  python manage_users.py test          # Test user mapping")
        print("  python manage_users.py update user1,user2,user3  # Update users")
        return
    
    command = sys.argv[1].lower()
    
    if command == "show":
        show_current_users()
    elif command == "test":
        test_user_mapping()
    elif command == "update":
        if len(sys.argv) < 3:
            print("Error: Please provide users to update")
            print("Example: python manage_users.py update Alice,Bob,Charlie")
            return
        
        new_users = [user.strip() for user in sys.argv[2].split(",")]
        update_users(new_users)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main() 