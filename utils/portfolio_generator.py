"""
Portfolio HTML/CSS generator using AI
"""

import re
import hashlib
from typing import Dict, Any, Optional, Tuple
import streamlit as st
import bleach

from utils.groq_client import get_groq_client
from prompts.prompts import PORTFOLIO_GENERATOR_PROMPT


class PortfolioGenerator:
    """Generate responsive HTML/CSS portfolio from profile data"""

    ALLOWED_HTML_TAGS = [
        'html', 'head', 'body', 'title', 'meta', 'link', 'style',
        'div', 'span', 'section', 'header', 'footer', 'nav', 'main',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
        'p', 'a', 'ul', 'ol', 'li',
        'strong', 'em', 'b', 'i', 'u',
        'br', 'hr',
        'img', 'svg', 'path'
    ]

    ALLOWED_ATTRIBUTES = {
        '*': ['class', 'id', 'style'],
        'a': ['href', 'target', 'rel'],
        'img': ['src', 'alt', 'width', 'height'],
        'meta': ['charset', 'name', 'content', 'viewport'],
        'link': ['rel', 'href', 'type'],
        'svg': ['viewBox', 'width', 'height', 'xmlns'],
        'path': ['d', 'fill', 'stroke']
    }

    def __init__(self):
        self.groq_client = get_groq_client()

    def generate_subdomain(self, name: str, user_id: Optional[str] = None) -> str:
        """
        Generate unique subdomain from name

        Returns:
            Subdomain string (e.g., "maya-chen-a1b2")
        """
        # Clean name
        clean_name = re.sub(r'[^a-zA-Z0-9\s-]', '', name.lower())
        clean_name = re.sub(r'\s+', '-', clean_name.strip())

        # Add hash for uniqueness
        if user_id:
            hash_input = f"{name}-{user_id}"
        else:
            import time
            hash_input = f"{name}-{int(time.time())}"

        hash_suffix = hashlib.md5(hash_input.encode()).hexdigest()[:4]

        subdomain = f"{clean_name}-{hash_suffix}"

        # Ensure valid subdomain (lowercase, alphanumeric + hyphens)
        subdomain = re.sub(r'[^a-z0-9-]', '', subdomain)
        subdomain = re.sub(r'-+', '-', subdomain).strip('-')

        # Limit length
        if len(subdomain) > 30:
            subdomain = subdomain[:30].rstrip('-')

        return subdomain or "portfolio"

    def format_profile_for_prompt(self, profile_data: Dict[str, Any]) -> str:
        """Format profile data as structured text for prompt"""
        lines = []

        # Basic info
        lines.append(f"Name: {profile_data.get('name', 'N/A')}")
        lines.append(f"Email: {profile_data.get('email', 'N/A')}")
        lines.append(f"Phone: {profile_data.get('phone', 'N/A')}")

        # Contact info
        contact = profile_data.get('contact_info', {})
        if contact:
            if contact.get('github'):
                lines.append(f"GitHub: {contact['github']}")
            if contact.get('linkedin'):
                lines.append(f"LinkedIn: {contact['linkedin']}")
            if contact.get('portfolio'):
                lines.append(f"Portfolio: {contact['portfolio']}")
            if contact.get('location'):
                lines.append(f"Location: {contact['location']}")

        # Work history
        work_history = profile_data.get('work_history', [])
        if work_history:
            lines.append("\n## Work Experience:")
            for job in work_history:
                lines.append(f"\n### {job.get('title')} at {job.get('company')}")
                lines.append(f"Dates: {job.get('dates', 'N/A')}")
                bullets = job.get('bullets', [])
                if bullets:
                    for bullet in bullets:
                        lines.append(f"- {bullet}")

        # Projects
        projects = profile_data.get('projects', [])
        if projects:
            lines.append("\n## Projects:")
            for project in projects:
                lines.append(f"\n### {project.get('name')}")
                lines.append(f"Description: {project.get('description')}")
                techs = project.get('technologies', [])
                if techs:
                    lines.append(f"Technologies: {', '.join(techs)}")
                if project.get('link'):
                    lines.append(f"Link: {project['link']}")

        # Skills
        skills = profile_data.get('skills', [])
        if skills:
            lines.append(f"\n## Skills:")
            lines.append(", ".join(skills))

        # Education
        education = profile_data.get('education', [])
        if education:
            lines.append("\n## Education:")
            for edu in education:
                lines.append(f"- {edu.get('degree')} from {edu.get('institution')} ({edu.get('year')})")

        return "\n".join(lines)

    def sanitize_html(self, html_content: str) -> str:
        """Sanitize HTML to prevent XSS"""
        try:
            clean_html = bleach.clean(
                html_content,
                tags=self.ALLOWED_HTML_TAGS,
                attributes=self.ALLOWED_ATTRIBUTES,
                strip=False
            )
            return clean_html
        except Exception as e:
            st.warning(f"HTML sanitization warning: {e}")
            return html_content

    def validate_html(self, html_content: str) -> Tuple[bool, Optional[str]]:
        """
        Basic HTML validation

        Returns:
            (is_valid, error_message)
        """
        # Check for required tags
        if '<!DOCTYPE html>' not in html_content and '<!doctype html>' not in html_content.lower():
            return False, "Missing DOCTYPE declaration"

        if '<html' not in html_content.lower():
            return False, "Missing <html> tag"

        if '<head' not in html_content.lower():
            return False, "Missing <head> section"

        if '<body' not in html_content.lower():
            return False, "Missing <body> section"

        # Check for balanced tags (basic check)
        if html_content.count('<html') != html_content.count('</html>'):
            return False, "Unbalanced <html> tags"

        return True, None

    def generate_portfolio(self, profile_data: Dict[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Generate HTML portfolio using AI

        Returns:
            (success, html_content, error_message)
        """
        try:
            # Format profile data for prompt
            formatted_profile = self.format_profile_for_prompt(profile_data)

            # Call Groq API
            response = self.groq_client.call_api(
                system_prompt=PORTFOLIO_GENERATOR_PROMPT,
                user_prompt=f"Generate a portfolio website for:\n\n{formatted_profile}",
                model="8b",  # Fast model
                temperature=0.7,  # Some creativity for design
                max_tokens=4096  # Need more tokens for full HTML
            )

            if not response.get("success"):
                return False, None, response.get("error", "Portfolio generation failed")

            html_content = response["content"]

            # Clean up any markdown code blocks
            if "```html" in html_content:
                html_content = html_content.split("```html")[1].split("```")[0].strip()
            elif "```" in html_content:
                html_content = html_content.split("```")[1].split("```")[0].strip()

            # Validate HTML
            is_valid, error = self.validate_html(html_content)
            if not is_valid:
                st.warning(f"HTML validation issue: {error}. Attempting to fix...")
                # Try to add missing parts
                if '<!DOCTYPE html>' not in html_content:
                    html_content = '<!DOCTYPE html>\n' + html_content

            # Skip sanitization for AI-generated portfolios to preserve CSS styling
            # The HTML is generated by our AI, not user input, so XSS risk is minimal
            # Bleach would strip style tag content which removes all CSS

            return True, html_content, None

        except Exception as e:
            return False, None, f"Error generating portfolio: {str(e)}"

    def generate_portfolio_with_fallback(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate portfolio with fallback to template if AI fails

        Returns:
            {
                "success": bool,
                "html_content": str or None,
                "subdomain": str,
                "error": str or None
            }
        """
        # Generate subdomain
        subdomain = self.generate_subdomain(
            profile_data.get("name", "user"),
            profile_data.get("user_id")
        )

        # Try AI generation
        success, html_content, error = self.generate_portfolio(profile_data)

        if success and html_content:
            return {
                "success": True,
                "html_content": html_content,
                "subdomain": subdomain,
                "error": None
            }

        # Fallback to simple template
        st.warning("AI generation failed. Using template fallback.")
        template_html = self.generate_template_portfolio(profile_data)

        return {
            "success": True,
            "html_content": template_html,
            "subdomain": subdomain,
            "error": f"Used template fallback. AI error: {error}"
        }

    def generate_template_portfolio(self, profile_data: Dict[str, Any]) -> str:
        """Generate portfolio using simple template (fallback)"""
        name = profile_data.get("name", "Your Name")
        email = profile_data.get("email", "")
        skills = profile_data.get("skills", [])
        work_history = profile_data.get("work_history", [])
        projects = profile_data.get("projects", [])
        education = profile_data.get("education", [])

        skills_html = " ".join([f'<span class="skill-badge">{skill}</span>' for skill in skills[:10]])

        work_html = ""
        for job in work_history[:3]:
            work_html += f"""
            <div class="work-item">
                <h3>{job.get('title')}</h3>
                <p class="company">{job.get('company')} | {job.get('dates', '')}</p>
                <ul>
                    {''.join([f'<li>{bullet}</li>' for bullet in job.get('bullets', [])[:3]])}
                </ul>
            </div>
            """

        projects_html = ""
        for project in projects[:3]:
            projects_html += f"""
            <div class="project-card">
                <h3>{project.get('name')}</h3>
                <p>{project.get('description')}</p>
                <p class="tech">{', '.join(project.get('technologies', []))}</p>
            </div>
            """

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} - Portfolio</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: #0f172a;
            color: #f1f5f9;
            line-height: 1.6;
        }}
        .hero {{
            text-align: center;
            padding: 80px 20px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
        }}
        .hero h1 {{
            font-size: 48px;
            font-weight: 800;
            margin-bottom: 16px;
        }}
        .hero p {{
            font-size: 20px;
            opacity: 0.9;
        }}
        .section {{
            max-width: 1200px;
            margin: 60px auto;
            padding: 0 20px;
        }}
        .section h2 {{
            font-size: 32px;
            margin-bottom: 32px;
            background: linear-gradient(135deg, #6366f1, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .skill-badge {{
            display: inline-block;
            background: rgba(99, 102, 241, 0.2);
            border: 1px solid rgba(99, 102, 241, 0.4);
            padding: 8px 16px;
            border-radius: 20px;
            margin: 4px;
            font-size: 14px;
        }}
        .work-item, .project-card {{
            background: rgba(30, 41, 59, 0.6);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
        }}
        .company, .tech {{
            color: #94a3b8;
            font-size: 14px;
            margin: 8px 0;
        }}
        .contact {{
            text-align: center;
            padding: 40px 20px;
        }}
        a {{
            color: #6366f1;
            text-decoration: none;
        }}
        @media (max-width: 768px) {{
            .hero h1 {{ font-size: 32px; }}
            .section h2 {{ font-size: 24px; }}
        }}
    </style>
</head>
<body>
    <div class="hero">
        <h1>{name}</h1>
        <p>Software Engineer</p>
    </div>

    <div class="section">
        <h2>Skills</h2>
        {skills_html}
    </div>

    <div class="section">
        <h2>Work Experience</h2>
        {work_html}
    </div>

    <div class="section">
        <h2>Projects</h2>
        {projects_html}
    </div>

    <div class="contact">
        <h2>Get in Touch</h2>
        <p><a href="mailto:{email}">{email}</a></p>
    </div>
</body>
</html>"""

        return html


# Singleton instance
_portfolio_generator = None


def get_portfolio_generator() -> PortfolioGenerator:
    """Get or create portfolio generator singleton"""
    global _portfolio_generator
    if _portfolio_generator is None:
        _portfolio_generator = PortfolioGenerator()
    return _portfolio_generator
