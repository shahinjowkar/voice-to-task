#!/usr/bin/env python3
"""
Test script for user name mapping functionality
Demonstrates similarity matching between transcribed names and predefined users
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.task_parser import TaskParser

def test_user_mapping():
    """Test user name mapping with various transcribed names"""
    
    print("🎯 User Name Mapping Test")
    print("=" * 50)
    
    # Initialize parser
    parser = TaskParser()
    
    # Test cases with various transcribed names
    test_cases = [
        "Alice",
        "alice", 
        "alise",
        "alicee",
        "alice user",
        "Bob",
        "bob",
        "bobb",
        "bob user",
        "Charlie",
        "charlie",
        "charley",
        "charli",
        "charlie user",
        "address",  # From your test case
        "adress",
        "addres",
        "unknown_name",
        "xyz",
        ""
    ]
    
    print(f"Predefined users: {parser.predefined_users}")
    print()
    
    for test_name in test_cases:
        print(f"Testing: '{test_name}'")
        
        # Get mapped name
        mapped_name = parser._map_user_name(test_name)
        
        # Get similarity matrix
        similarity_matrix = parser._calculate_similarity_matrix(test_name)
        
        print(f"  → Mapped to: '{mapped_name}'")
        print(f"  → Similarity scores:")
        for user, score in similarity_matrix:
            print(f"    - {user}: {score:.3f}")
        print()

def test_task_parsing_with_mapping():
    """Test full task parsing with user name mapping"""
    
    print("🎯 Task Parsing with User Mapping Test")
    print("=" * 50)
    
    parser = TaskParser()
    
    # Test cases that might have transcription errors
    test_commands = [
        "Task inspecting the balcony, user address, deadline January 3rd 2025.",
        "Task review documents, user alice, deadline tomorrow.",
        "Task call client, user bobb, deadline Friday.",
        "Task send email, user charley, deadline next week.",
        "Task update website, user adress, deadline today.",
    ]
    
    for command in test_commands:
        print(f"Command: '{command}'")
        result = parser.parse_task_command(command)
        
        print(f"  → Title: '{result.get('title', 'None')}'")
        print(f"  → Assignee: '{result.get('assignee', 'None')}'")
        print(f"  → Deadline: '{result.get('deadline', 'None')}'")
        
        if 'assignee_similarity' in result:
            print(f"  → Similarity Matrix:")
            for user, score in result['assignee_similarity']:
                print(f"    - {user}: {score:.3f}")
        
        print(f"  → Success: {result.get('success', False)}")
        if result.get('errors'):
            print(f"  → Errors: {result['errors']}")
        print()

if __name__ == "__main__":
    test_user_mapping()
    print("\n" + "="*50 + "\n")
    test_task_parsing_with_mapping() 