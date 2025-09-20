import os
import requests
import logging

logger = logging.getLogger(__name__)

class AIAssistantService:
    """
    A service to interact with a Large Language Model via OpenRouter API.
    """
    API_URL = "https://openrouter.ai/api/v1/chat/completions"
    API_KEY = os.getenv("OPENROUTER_API_KEY")

    def get_answer(self, question: str, context: dict) -> str:
        """
        Gets a context-aware answer from the AI model.

        Args:
            question: The student's question.
            context: A dictionary containing contextual information like
                     {'course_title': '...', 'lesson_title': '...', 'lesson_content': '...'}.

        Returns:
            The AI-generated answer as a string.
        """
        if not self.API_KEY:
            logger.error("OPENROUTER_API_KEY is not set. AI Assistant is disabled.")
            return "The AI Assistant is currently unavailable. Please contact your instructor."

        # Construct a detailed, context-aware prompt [cite: 681, 682]
        prompt = (
            f"You are an expert teaching assistant for the course titled '{context.get('course_title', 'N/A')}'. "
            f"A student is currently in a lesson named '{context.get('lesson_title', 'N/A')}'.\n"
            f"Here is the relevant content from the lesson:\n---START OF CONTENT---\n"
            f"{context.get('lesson_content', 'No content available.')}\n---END OF CONTENT---\n\n"
            f"Based on this context ONLY, please answer the following student's question clearly and concisely.\n"
            f"Student's Question: \"{question}\""
        )

        headers = {
            "Authorization": f"Bearer {self.API_KEY}",
            "Content-Type": "application/json"
        }
        
        # Data payload for the API request
        data = {
            "model": "mistralai/mistral-7b-instruct", # Example model, can be configured
            "messages": [
                {"role": "system", "content": "You are a helpful teaching assistant."},
                {"role": "user", "content": prompt}
            ]
        }

        try:
            response = requests.post(self.API_URL, headers=headers, json=data, timeout=20)
            response.raise_for_status()
            
            response_json = response.json()
            answer = response_json['choices'][0]['message']['content']
            return answer.strip()

        except requests.exceptions.RequestException as e:
            logger.error(f"AI Assistant API request failed: {e}")
            return "Sorry, I encountered an error while processing your request. Please try again later."
        except (KeyError, IndexError) as e:
            logger.error(f"AI Assistant API response was malformed: {e}")
            return "Sorry, I received an unexpected response. Please try again."