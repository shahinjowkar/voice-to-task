#!/usr/bin/env python3
"""
Test script for category mapping functionality
Demonstrates similarity matching between transcribed categories and predefined categories
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.task_parser import TaskParser

def test_category_mapping():
    """Test category mapping with various transcribed categories"""
    
    print("🏷️ Category Mapping Test")
    print("=" * 50)
    
    # Initialize parser
    parser = TaskParser()
    
    # Test cases with various transcribed categories
    test_cases = [
        "Development",
        "development", 
        "develop",
        "developing",
        "dev",
        "Design",
        "design",
        "designing",
        "Marketing",
        "marketing",
        "market",
        "Testing",
        "testing",
        "test",
        "Documentation",
        "documentation",
        "docs",
        "doc",
        "unknown_category",
        "xyz",
        ""
    ]
    
    print(f"Predefined categories: {parser.predefined_categories}")
    print()
    
    for test_category in test_cases:
        print(f"Testing: '{test_category}'")
        
        # Get mapped category
        mapped_category = parser._map_category_name(test_category)
        
        # Get similarity matrix
        similarity_matrix = parser._calculate_category_similarity_matrix(test_category)
        
        print(f"  → Mapped to: '{mapped_category}'")
        print(f"  → Similarity scores:")
        for category, score in similarity_matrix:
            print(f"    - {category}: {score:.3f}")
        print()

def test_task_parsing_with_categories():
    """Test full task parsing with category mapping"""
    
    print("🏷️ Task Parsing with Category Mapping Test")
    print("=" * 50)
    
    parser = TaskParser()
    
    # Test cases that include categories
    test_commands = [
        "Task finalizing the reports for the app user Ali category Development deadline January 3rd, 2000.",
        "Task review UI design user Alice category Design deadline tomorrow.",
        "Task create marketing campaign user Bob category Marketing deadline Friday.",
        "Task run unit tests user Charlie category Testing deadline next week.",
        "Task write API documentation user Ali category Documentation deadline today.",
        "Task inspect balcony user address category Development deadline January 3rd 2025.",
    ]
    
    for command in test_commands:
        print(f"Command: '{command}'")
        result = parser.parse_task_command(command)
        
        print(f"  → Title: '{result.get('title', 'None')}'")
        print(f"  → Assignee: '{result.get('assignee', 'None')}'")
        print(f"  → Category: '{result.get('category', 'None')}'")
        print(f"  → Deadline: '{result.get('deadline', 'None')}'")
        
        if 'assignee_similarity' in result:
            print(f"  → Assignee Similarity Matrix:")
            for user, score in result['assignee_similarity']:
                print(f"    - {user}: {score:.3f}")
        
        if 'category_similarity' in result:
            print(f"  → Category Similarity Matrix:")
            for category, score in result['category_similarity']:
                print(f"    - {category}: {score:.3f}")
        
        print(f"  → Success: {result.get('success', False)}")
        if result.get('errors'):
            print(f"  → Errors: {result['errors']}")
        print()

if __name__ == "__main__":
    test_category_mapping()
    print("\n" + "="*50 + "\n")
    test_task_parsing_with_categories() 