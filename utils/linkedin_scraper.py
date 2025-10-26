"""
LinkedIn profile scraper with fallback handling
"""

import re
import time
from typing import Dict, Any, Optional, Tuple
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import streamlit as st

from utils.groq_client import get_groq_client
from utils.validators import ProfileSchema, LinkedInValidator
from prompts.prompts import LINKEDIN_PARSER_PROMPT


class LinkedInScraper:
    """Scrape LinkedIn profiles (with legal/ethical considerations)"""

    def __init__(self):
        self.groq_client = get_groq_client()
        self.ua = UserAgent()

    def scrape_profile(self, linkedin_url: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Scrape LinkedIn profile HTML with retry logic

        Returns:
            (success, html_content, error_message)
        """
        # Validate URL
        if not LinkedInValidator.is_valid_linkedin_url(linkedin_url):
            return False, None, "Invalid LinkedIn URL format"

        # Normalize URL
        linkedin_url = LinkedInValidator.normalize_linkedin_url(linkedin_url)

        # Try multiple times with different strategies
        max_retries = 3

        for attempt in range(max_retries):
            try:
                # Add small random delay to mimic human behavior
                if attempt > 0:
                    delay = 2 + (attempt * 2)  # 2s, 4s, 6s
                    st.info(f"Retry attempt {attempt + 1}/{max_retries}. Waiting {delay}s...")
                    time.sleep(delay)

                # Create session for better connection handling
                session = requests.Session()

                # More comprehensive headers to mimic real browser
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                    'Cache-Control': 'max-age=0',
                    'Referer': 'https://www.google.com/',
                }

                # Make request with timeout
                response = session.get(
                    linkedin_url,
                    headers=headers,
                    timeout=15,
                    allow_redirects=True
                )

                if response.status_code == 200:
                    return True, response.text, None
                elif response.status_code == 999:
                    if attempt < max_retries - 1:
                        continue  # Retry
                    return False, None, "LinkedIn blocked the request (status 999). This is common for automated access."
                elif response.status_code == 403:
                    if attempt < max_retries - 1:
                        continue  # Retry
                    return False, None, "Access forbidden. LinkedIn may require login."
                elif response.status_code == 404:
                    return False, None, "Profile not found. Check the URL."
                else:
                    if attempt < max_retries - 1:
                        continue  # Retry
                    return False, None, f"Request failed with status {response.status_code}"

            except requests.Timeout:
                if attempt < max_retries - 1:
                    continue  # Retry
                return False, None, "Request timed out. Please try again."
            except requests.RequestException as e:
                if attempt < max_retries - 1:
                    continue  # Retry
                return False, None, f"Network error: {str(e)}"
            except Exception as e:
                if attempt < max_retries - 1:
                    continue  # Retry
                return False, None, f"Error scraping LinkedIn: {str(e)}"

        return False, None, "All retry attempts failed."

    def extract_profile_data(self, html_content: str, linkedin_url: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Extract structured text from LinkedIn HTML

        Returns:
            (success, extracted_text, error_message)
        """
        try:
            soup = BeautifulSoup(html_content, 'lxml')

            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()

            # Get text
            text = soup.get_text()

            # Clean up
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            if len(text) < 200:
                return False, None, "Could not extract profile data. Page may require login or have restricted access."

            # Add URL to text for context
            text = f"LinkedIn Profile URL: {linkedin_url}\n\n{text}"

            return True, text, None

        except Exception as e:
            return False, None, f"Error extracting profile data: {str(e)}"

    def parse_with_ai(self, profile_text: str, linkedin_url: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Parse LinkedIn profile text using Groq AI

        Returns:
            (success, parsed_data, error_message)
        """
        try:
            # Truncate if too long
            if len(profile_text) > 12000:
                profile_text = profile_text[:12000] + "\n\n[Truncated for length]"

            # Call Groq API
            parsed_json = self.groq_client.call_api_json(
                system_prompt=LINKEDIN_PARSER_PROMPT,
                user_prompt=f"LinkedIn profile content:\n\n{profile_text}",
                model="8b",
                temperature=0.2,
                max_tokens=2048
            )

            if not parsed_json:
                return False, None, "AI parsing failed - no response"

            # Ensure LinkedIn URL is in the data
            if not parsed_json.get("linkedin_url"):
                parsed_json["linkedin_url"] = linkedin_url

            # Validate with Pydantic
            try:
                profile = ProfileSchema(**parsed_json)
                validated_data = profile.model_dump()
                return True, validated_data, None
            except Exception as validation_error:
                # Return partial data even if validation fails
                st.warning(f"Validation warning: {validation_error}")
                parsed_json["linkedin_url"] = linkedin_url
                return True, parsed_json, None

        except Exception as e:
            return False, None, f"Error during AI parsing: {str(e)}"

    def scrape_and_parse(self, linkedin_url: str) -> Dict[str, Any]:
        """
        Main scraping and parsing function

        Returns:
            {
                "success": bool,
                "profile_data": dict or None,
                "raw_text": str,
                "confidence": float,
                "error": str or None,
                "blocked": bool  # True if LinkedIn blocked the request
            }
        """
        # Validate URL first
        if not LinkedInValidator.is_valid_linkedin_url(linkedin_url):
            return {
                "success": False,
                "profile_data": None,
                "raw_text": "",
                "confidence": 0.0,
                "error": "Invalid LinkedIn URL. Please check the format.",
                "blocked": False
            }

        # Scrape profile
        success, html_content, error = self.scrape_profile(linkedin_url)

        if not success:
            is_blocked = "blocked" in error.lower() or "999" in error or "403" in error
            return {
                "success": False,
                "profile_data": None,
                "raw_text": "",
                "confidence": 0.0,
                "error": error,
                "blocked": is_blocked
            }

        # Extract text from HTML
        success, profile_text, error = self.extract_profile_data(html_content, linkedin_url)

        if not success:
            return {
                "success": False,
                "profile_data": None,
                "raw_text": "",
                "confidence": 0.0,
                "error": error,
                "blocked": True  # Likely requires login
            }

        # Parse with AI
        success, parsed_data, error = self.parse_with_ai(profile_text, linkedin_url)

        if not success:
            return {
                "success": False,
                "profile_data": None,
                "raw_text": profile_text,
                "confidence": 0.0,
                "error": error,
                "blocked": False
            }

        # Estimate confidence (similar to resume parser)
        confidence = self.estimate_confidence(parsed_data)

        # Add metadata
        if parsed_data:
            parsed_data["original_resume_text"] = profile_text
            parsed_data["parsing_confidence"] = confidence
            parsed_data["parsing_method"] = "linkedin"

        return {
            "success": True,
            "profile_data": parsed_data,
            "raw_text": profile_text,
            "confidence": confidence,
            "error": None,
            "blocked": False
        }

    def parse_manual_text(self, profile_text: str, linkedin_url: str = "") -> Dict[str, Any]:
        """
        Parse manually provided LinkedIn profile text (no scraping)

        Args:
            profile_text: User-provided LinkedIn profile text
            linkedin_url: Optional LinkedIn URL for reference

        Returns:
            Same format as scrape_and_parse() for consistency
        """
        # Validate text length
        if not profile_text or len(profile_text.strip()) < 100:
            return {
                "success": False,
                "profile_data": None,
                "raw_text": "",
                "confidence": 0.0,
                "error": "Profile text too short. Please provide at least 100 characters.",
                "blocked": False
            }

        # Clean text
        profile_text = profile_text.strip()

        # Add LinkedIn URL if provided
        if linkedin_url:
            profile_text = f"LinkedIn Profile URL: {linkedin_url}\n\n{profile_text}"

        # Parse with AI
        success, parsed_data, error = self.parse_with_ai(profile_text, linkedin_url)

        if not success:
            return {
                "success": False,
                "profile_data": None,
                "raw_text": profile_text,
                "confidence": 0.0,
                "error": error,
                "blocked": False
            }

        # Estimate confidence
        confidence = self.estimate_confidence(parsed_data)

        # Add metadata
        if parsed_data:
            parsed_data["original_resume_text"] = profile_text
            parsed_data["parsing_confidence"] = confidence
            parsed_data["parsing_method"] = "linkedin_manual"
            if linkedin_url and not parsed_data.get("linkedin_url"):
                parsed_data["linkedin_url"] = linkedin_url

        return {
            "success": True,
            "profile_data": parsed_data,
            "raw_text": profile_text,
            "confidence": confidence,
            "error": None,
            "blocked": False
        }

    def estimate_confidence(self, parsed_data: Dict) -> float:
        """Estimate parsing confidence"""
        score = 0.0

        if parsed_data.get("name"):
            score += 0.25
        if parsed_data.get("linkedin_url"):
            score += 0.15
        if parsed_data.get("work_history") and len(parsed_data["work_history"]) > 0:
            score += 0.30
        if parsed_data.get("skills") and len(parsed_data["skills"]) > 0:
            score += 0.15
        if parsed_data.get("education") and len(parsed_data["education"]) > 0:
            score += 0.15

        return min(score, 1.0)


# Singleton instance
_linkedin_scraper = None


def get_linkedin_scraper() -> LinkedInScraper:
    """Get or create LinkedIn scraper singleton"""
    global _linkedin_scraper
    if _linkedin_scraper is None:
        _linkedin_scraper = LinkedInScraper()
    return _linkedin_scraper
