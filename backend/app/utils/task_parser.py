"""
Task parser for VoiceTaskAI
Extracts structured task information from voice commands
"""
import re
import logging
from datetime import datetime
from typing import Dict, Optional, Any, List
import spacy
import dateparser
from difflib import SequenceMatcher

from app.config import settings

logger = logging.getLogger(__name__)


class TaskParser:
    """Parser for extracting task information from voice commands"""
    
    def __init__(self):
        """Initialize task parser with spaCy model"""
        self.nlp = None
        self._load_nlp_model()
        # Predefined user names for mapping from config
        self.predefined_users = settings.predefined_users_list
        # Predefined categories for mapping from config
        self.predefined_categories = settings.predefined_categories_list
    
    def _load_nlp_model(self):
        """Load spaCy NLP model"""
        try:
            logger.info(f"Loading spaCy model: {settings.spacy_model}")
            self.nlp = spacy.load(settings.spacy_model)
            logger.info(f"✅ spaCy model '{settings.spacy_model}' loaded successfully")
        except Exception as e:
            logger.error(f"❌ Failed to load spaCy model: {e}")
            raise
    
    def _map_user_name(self, transcribed_name: str) -> str:
        """
        Map transcribed user name to predefined user using similarity matching
        
        Args:
            transcribed_name: Raw transcribed name from voice
            
        Returns:
            Best matching predefined user name
        """
        if not transcribed_name or transcribed_name.strip() == "":
            return "Unknown"
        
        # Clean the transcribed name
        clean_name = transcribed_name.strip().lower()
        
        # Calculate similarity scores
        similarities = []
        for predefined_user in self.predefined_users:
            # Use SequenceMatcher for string similarity
            similarity = SequenceMatcher(None, clean_name, predefined_user.lower()).ratio()
            similarities.append((predefined_user, similarity))
        
        # Sort by similarity score (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        best_match, best_score = similarities[0]
        
        logger.info(f"User name mapping: '{transcribed_name}' -> '{best_match}' (similarity: {best_score:.3f})")
        
        # If similarity is too low, return the original with a warning
        if best_score < 0.3:
            logger.warning(f"Low similarity score ({best_score:.3f}) for user name '{transcribed_name}'")
            return transcribed_name
        
        return best_match
    
    def _calculate_similarity_matrix(self, transcribed_name: str) -> List[tuple]:
        """
        Calculate similarity matrix between transcribed name and predefined users
        
        Args:
            transcribed_name: Raw transcribed name
            
        Returns:
            List of tuples (user_name, similarity_score) sorted by score
        """
        clean_name = transcribed_name.strip().lower()
        similarities = []
        
        for predefined_user in self.predefined_users:
            similarity = SequenceMatcher(None, clean_name, predefined_user.lower()).ratio()
            similarities.append((predefined_user, similarity))
        
        # Sort by similarity score (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities
    
    def _map_category_name(self, transcribed_category: str) -> str:
        """
        Map transcribed category name to predefined category using similarity matching
        
        Args:
            transcribed_category: Raw transcribed category from voice
            
        Returns:
            Best matching predefined category name
        """
        if not transcribed_category or transcribed_category.strip() == "":
            return "Uncategorized"
        
        # Clean the transcribed category
        clean_category = transcribed_category.strip().lower()
        
        # Calculate similarity scores
        similarities = []
        for predefined_category in self.predefined_categories:
            # Use SequenceMatcher for string similarity
            similarity = SequenceMatcher(None, clean_category, predefined_category.lower()).ratio()
            similarities.append((predefined_category, similarity))
        
        # Sort by similarity score (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        best_match, best_score = similarities[0]
        
        logger.info(f"Category mapping: '{transcribed_category}' -> '{best_match}' (similarity: {best_score:.3f})")
        
        # If similarity is too low, return the original with a warning
        if best_score < 0.3:
            logger.warning(f"Low similarity score ({best_score:.3f}) for category '{transcribed_category}'")
            return transcribed_category
        
        return best_match
    
    def _calculate_category_similarity_matrix(self, transcribed_category: str) -> List[tuple]:
        """
        Calculate similarity matrix between transcribed category and predefined categories
        
        Args:
            transcribed_category: Raw transcribed category
            
        Returns:
            List of tuples (category_name, similarity_score) sorted by score
        """
        clean_category = transcribed_category.strip().lower()
        similarities = []
        
        for predefined_category in self.predefined_categories:
            similarity = SequenceMatcher(None, clean_category, predefined_category.lower()).ratio()
            similarities.append((predefined_category, similarity))
        
        # Sort by similarity score (highest first)
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities
    
    def parse_task_command(self, text: str) -> Dict[str, Any]:
        """
        Parse task command using spaCy NLP
        Handles formats like: assign "task name" to "user name" by "deadline"
        
        Args:
            text: Transcribed voice command
            
        Returns:
            Dict containing extracted task information
        """
        try:
            logger.info(f"Parsing task command: '{text}'")
            
            # Use spaCy for all parsing
            return self._extract_with_spacy(text)
            
        except Exception as e:
            logger.error(f"❌ Error parsing task command: {e}")
            return {
                "title": None,
                "assignee": None,
                "category": None,
                "deadline": None,
                "success": False,
                "errors": [str(e)]
            }
    
    def _parse_deadline(self, deadline_text: str) -> Optional[str]:
        """
        Parse deadline text into ISO format
        
        Args:
            deadline_text: Natural language deadline (e.g., "Friday", "next week")
            
        Returns:
            ISO format date string or None
        """
        try:
            logger.info(f"Parsing deadline: '{deadline_text}'")
            
            # Try dateparser first
            parsed_date = dateparser.parse(deadline_text)
            if parsed_date:
                return parsed_date.isoformat()
            
            # Common deadline patterns
            deadline_patterns = {
                r'today': datetime.now().isoformat(),
                r'tomorrow': (datetime.now().replace(day=datetime.now().day + 1)).isoformat(),
                r'next week': (datetime.now().replace(day=datetime.now().day + 7)).isoformat(),
                r'next month': (datetime.now().replace(month=datetime.now().month + 1)).isoformat(),
            }
            
            for pattern, date_str in deadline_patterns.items():
                if re.search(pattern, deadline_text.lower()):
                    return date_str
            
            logger.warning(f"Could not parse deadline: {deadline_text}")
            return None
            
        except Exception as e:
            logger.error(f"Error parsing deadline '{deadline_text}': {e}")
            return None
    
    def _extract_with_spacy(self, text: str) -> Dict[str, Any]:
        """
        Extract task information using spaCy NLP
        Args:
            text: Transcribed text
        Returns:
            Dict containing extracted task information
        """
        try:
            doc = self.nlp(text)
            task_info = {
                "title": None,
                "assignee": None,
                "category": None,
                "deadline": None,
                "success": False,
                "errors": []
            }

            # Define fault-tolerant keyword variations
            task_variations = ["task", "tasks", "tusk", "tack"]
            user_variations = ["user", "users", "youser", "yuser"]
            category_variations = ["category", "categories", "cat", "type", "kind"]
            deadline_variations = ["deadlin", "deadline", "dead line"]

            task_idx = None
            user_idx = None
            category_idx = None
            deadline_idx = None

            # First pass: find all keyword positions
            for i, token in enumerate(doc):
                token_text = token.text.lower()
                if task_idx is None and any(var in token_text for var in task_variations):
                    task_idx = i
                elif user_idx is None and any(var in token_text for var in user_variations):
                    user_idx = i
                elif category_idx is None and any(var in token_text for var in category_variations):
                    category_idx = i
                elif deadline_idx is None and any(var in token_text for var in deadline_variations):
                    deadline_idx = i

            # Extract task title (between 'task' and the next keyword)
            if task_idx is not None:
                # Find the next keyword after 'task'
                next_keyword_idx = None
                for idx in [user_idx, category_idx, deadline_idx]:
                    if idx is not None and idx > task_idx:
                        if next_keyword_idx is None or idx < next_keyword_idx:
                            next_keyword_idx = idx
                
                if next_keyword_idx is not None:
                    title_tokens = [doc[i].text for i in range(task_idx + 1, next_keyword_idx) if doc[i].text not in ['"', "'", 'the', 'a', 'an', ',']]
                    if title_tokens:
                        task_info["title"] = " ".join(title_tokens).strip()

            # Extract assignee (after 'user', before next keyword)
            if user_idx is not None:
                # Find the next keyword after 'user'
                next_keyword_idx = None
                for idx in [category_idx, deadline_idx]:
                    if idx is not None and idx > user_idx:
                        if next_keyword_idx is None or idx < next_keyword_idx:
                            next_keyword_idx = idx
                
                end_idx = next_keyword_idx if next_keyword_idx else len(doc)
                assignee_tokens = [doc[i].text for i in range(user_idx + 1, end_idx) if doc[i].text not in ['"', "'", 'the', 'a', 'an', ',']]
                if assignee_tokens:
                    raw_assignee = " ".join(assignee_tokens).strip()
                    # Map the transcribed name to predefined users
                    task_info["assignee"] = self._map_user_name(raw_assignee)
                    # Store the similarity matrix for debugging
                    task_info["assignee_similarity"] = self._calculate_similarity_matrix(raw_assignee)

            # Extract category (after 'category', before next keyword)
            if category_idx is not None:
                # Find the next keyword after 'category'
                next_keyword_idx = deadline_idx if deadline_idx and deadline_idx > category_idx else None
                end_idx = next_keyword_idx if next_keyword_idx else len(doc)
                category_tokens = [doc[i].text for i in range(category_idx + 1, end_idx) if doc[i].text not in ['"', "'", 'the', 'a', 'an', ',']]
                if category_tokens:
                    raw_category = " ".join(category_tokens).strip()
                    # Map the transcribed category to predefined categories
                    task_info["category"] = self._map_category_name(raw_category)
                    # Store the category similarity matrix for debugging
                    task_info["category_similarity"] = self._calculate_category_similarity_matrix(raw_category)

            # Extract deadline (after 'deadlin')
            if deadline_idx is not None:
                deadline_tokens = [doc[i].text for i in range(deadline_idx + 1, len(doc)) if doc[i].text not in ['"', "'", 'the', 'a', 'an']]
                if deadline_tokens:
                    deadline_text = " ".join(deadline_tokens).strip()
                    parsed_deadline = self._parse_deadline(deadline_text)
                    if parsed_deadline:
                        task_info["deadline"] = parsed_deadline
                    else:
                        task_info["errors"].append(f"Could not parse deadline: {deadline_text}")

            # Fallback: If not all fields found, try 'to' and 'by' as separators
            if not (task_info["title"] and task_info["assignee"]):
                # Try to find 'to' and 'by' as separators
                to_idx = None
                by_idx = None
                for i, token in enumerate(doc):
                    if token.text.lower() == "to":
                        to_idx = i
                    elif token.text.lower() == "by":
                        by_idx = i
                if to_idx is not None and by_idx is not None:
                    # Task title: before 'to'
                    title_tokens = [doc[i].text for i in range(0, to_idx) if doc[i].text not in ['"', "'", 'the', 'a', 'an']]
                    if title_tokens and not task_info["title"]:
                        task_info["title"] = " ".join(title_tokens).strip()
                    # Assignee: between 'to' and 'by'
                    assignee_tokens = [doc[i].text for i in range(to_idx + 1, by_idx) if doc[i].text not in ['"', "'", 'the', 'a', 'an']]
                    if assignee_tokens and not task_info["assignee"]:
                        raw_assignee = " ".join(assignee_tokens).strip()
                        # Map the transcribed name to predefined users
                        task_info["assignee"] = self._map_user_name(raw_assignee)
                        # Store the similarity matrix for debugging
                        task_info["assignee_similarity"] = self._calculate_similarity_matrix(raw_assignee)
                    # Deadline: after 'by'
                    deadline_tokens = [doc[i].text for i in range(by_idx + 1, len(doc)) if doc[i].text not in ['"', "'", 'the', 'a', 'an']]
                    if deadline_tokens and not task_info["deadline"]:
                        deadline_text = " ".join(deadline_tokens).strip()
                        parsed_deadline = self._parse_deadline(deadline_text)
                        if parsed_deadline:
                            task_info["deadline"] = parsed_deadline
                        else:
                            task_info["errors"].append(f"Could not parse deadline: {deadline_text}")

            # Set success if at least title and assignee found
            if task_info["title"] and task_info["assignee"]:
                task_info["success"] = True
                logger.info(f"✅ Task parsed successfully: {task_info}")
            return task_info
        except Exception as e:
            logger.error(f"Error in spaCy extraction: {e}")
            return {
                "title": None,
                "assignee": None,
                "category": None,
                "deadline": None,
                "success": False,
                "errors": [str(e)]
            }


# Global task parser instance
task_parser = TaskParser() 