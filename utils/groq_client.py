"""
Groq AI client wrapper with retry logic
"""

import os
import json
import time
from typing import Optional, Dict, Any, List
from groq import Groq
import streamlit as st


class GroqClient:
    """Wrapper for Groq AI API operations"""

    # Model configurations
    MODELS = {
        "8b": "llama-3.1-8b-instant",  # Fast, for speed tasks
        "70b": "llama-3.3-70b-versatile",  # Quality, for nuanced tasks (updated from 3.1 to 3.3)
        "mixtral": "mixtral-8x7b-32768"  # Alternative
    }

    def __init__(self):
        """Initialize Groq client"""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("Missing GROQ_API_KEY. Check .env file.")

        self.client = Groq(api_key=api_key)
        self.default_model = self.MODELS["8b"]  # Fast by default

    def call_api(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "8b",
        temperature: float = 0.3,
        max_tokens: int = 2048,
        response_format: Optional[Dict] = None,
        max_retries: int = 3,
        retry_delay: float = 2.0  # Increased from 1.0 to 2.0 seconds
    ) -> Dict[str, Any]:
        """
        Call Groq API with retry logic

        Args:
            system_prompt: System instructions
            user_prompt: User input
            model: Model key ('8b', '70b', or 'mixtral')
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            response_format: Force JSON output if {"type": "json_object"}
            max_retries: Number of retry attempts
            retry_delay: Delay between retries (seconds)

        Returns:
            {
                "success": bool,
                "content": str,  # Response text
                "usage": dict,   # Token usage stats
                "error": str     # Error message if failed
            }
        """
        model_name = self.MODELS.get(model, self.default_model)

        for attempt in range(max_retries):
            try:
                # Prepare messages
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]

                # API call parameters
                params = {
                    "model": model_name,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }

                # Add JSON format if requested
                if response_format:
                    params["response_format"] = response_format

                # Make API call
                response = self.client.chat.completions.create(**params)

                # Extract response
                content = response.choices[0].message.content
                usage = {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }

                return {
                    "success": True,
                    "content": content,
                    "usage": usage
                }

            except Exception as e:
                error_msg = str(e)

                # Check for rate limit
                if "rate_limit" in error_msg.lower() or "429" in error_msg:
                    if attempt < max_retries - 1:
                        # Exponential backoff with longer delays for rate limits
                        wait_time = retry_delay * (3 ** attempt)  # More aggressive backoff
                        st.warning(f"⏳ Rate limit hit. Waiting {wait_time:.0f}s before retry...")
                        time.sleep(wait_time)
                        continue
                    else:
                        return {
                            "success": False,
                            "content": "",
                            "error": "⚠️ Groq API rate limit exceeded. Please wait a minute and try again."
                        }

                # Check for timeout
                elif "timeout" in error_msg.lower():
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    else:
                        return {
                            "success": False,
                            "content": "",
                            "error": "API timeout. Please try again."
                        }

                # Other errors
                else:
                    return {
                        "success": False,
                        "content": "",
                        "error": f"API error: {error_msg}"
                    }

        return {
            "success": False,
            "content": "",
            "error": "Max retries exceeded"
        }

    def parse_json_response(self, response: Dict[str, Any]) -> Optional[Dict]:
        """
        Parse JSON from API response

        Returns:
            Parsed JSON dict or None if parsing fails
        """
        if not response.get("success"):
            return None

        try:
            content = response["content"]

            # Try direct JSON parse
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Try extracting JSON from markdown code blocks
                if "```json" in content:
                    json_str = content.split("```json")[1].split("```")[0].strip()
                    return json.loads(json_str)
                elif "```" in content:
                    json_str = content.split("```")[1].split("```")[0].strip()
                    return json.loads(json_str)
                else:
                    # Try cleaning and parsing
                    cleaned = content.strip()
                    return json.loads(cleaned)

        except Exception as e:
            st.error(f"Failed to parse JSON response: {e}")
            return None

    def call_api_json(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str = "8b",
        temperature: float = 0.3,
        max_tokens: int = 2048,
        max_retries: int = 3
    ) -> Optional[Dict]:
        """
        Call API and parse JSON response

        Returns:
            Parsed JSON dict or None if failed
        """
        response = self.call_api(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"},
            max_retries=max_retries
        )

        if not response.get("success"):
            st.error(f"API call failed: {response.get('error')}")
            return None

        return self.parse_json_response(response)

    def estimate_tokens(self, text: str) -> int:
        """
        Estimate token count (rough approximation)

        Rule of thumb: ~4 characters = 1 token for English text
        """
        return len(text) // 4

    def check_token_limit(self, text: str, max_tokens: int = 32000) -> bool:
        """Check if text is within token limit"""
        estimated = self.estimate_tokens(text)
        return estimated < max_tokens

    def truncate_to_token_limit(self, text: str, max_tokens: int = 32000) -> str:
        """Truncate text to fit within token limit"""
        estimated = self.estimate_tokens(text)
        if estimated <= max_tokens:
            return text

        # Truncate with buffer
        target_chars = max_tokens * 4 * 0.9  # 90% of limit for safety
        return text[:int(target_chars)] + "\n\n[Text truncated due to length]"


# Singleton instance
_groq_client = None


def get_groq_client() -> GroqClient:
    """Get or create Groq client singleton"""
    global _groq_client
    if _groq_client is None:
        _groq_client = GroqClient()
    return _groq_client


# Convenience functions for common patterns
def quick_parse_json(system_prompt: str, user_prompt: str, model: str = "8b") -> Optional[Dict]:
    """Quick JSON parsing with default settings"""
    client = get_groq_client()
    return client.call_api_json(system_prompt, user_prompt, model=model)


def quick_generate_text(system_prompt: str, user_prompt: str, model: str = "8b") -> Optional[str]:
    """Quick text generation with default settings"""
    client = get_groq_client()
    response = client.call_api(system_prompt, user_prompt, model=model)

    if response.get("success"):
        return response["content"]
    else:
        st.error(f"Generation failed: {response.get('error')}")
        return None


def stream_response(system_prompt: str, user_prompt: str, model: str = "70b"):
    """
    Stream API response for chat interfaces

    Note: Groq SDK supports streaming, but we'll use simple non-streaming for MVP
    Can add streaming in post-MVP for career coach chat
    """
    # For MVP, just use regular call and display
    return quick_generate_text(system_prompt, user_prompt, model=model)
