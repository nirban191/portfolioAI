"""
Supabase client and helper functions
"""

import os
import json
from typing import Optional, Dict, Any, List
from supabase import create_client, Client
from datetime import datetime
import streamlit as st


class SupabaseClient:
    """Wrapper for Supabase operations"""

    def __init__(self):
        """Initialize Supabase client"""
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")

        if not url or not key:
            raise ValueError("Missing Supabase credentials. Check .env file.")

        # Create client with explicit options for newer supabase-py version
        self.client: Client = create_client(
            supabase_url=url,
            supabase_key=key
        )
        self.storage = self.client.storage

    # ========================================
    # AUTH OPERATIONS
    # ========================================

    def signup(self, email: str, password: str) -> Dict[str, Any]:
        """Sign up a new user"""
        try:
            response = self.client.auth.sign_up({
                "email": email,
                "password": password
            })
            return {"success": True, "user": response.user, "session": response.session}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Log in existing user"""
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return {"success": True, "user": response.user, "session": response.session}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def logout(self) -> Dict[str, Any]:
        """Log out current user"""
        try:
            self.client.auth.sign_out()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def reset_password(self, email: str) -> Dict[str, Any]:
        """Send password reset email"""
        try:
            self.client.auth.reset_password_for_email(email)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_current_user(self):
        """Get currently logged in user"""
        try:
            user = self.client.auth.get_user()
            return user
        except:
            return None

    # ========================================
    # USER OPERATIONS
    # ========================================

    def create_user_record(self, user_id: str, email: str, subdomain: str) -> Dict[str, Any]:
        """Create user record in users table"""
        try:
            data = {
                "id": user_id,
                "email": email,
                "subdomain": subdomain,
                "last_login": datetime.now().isoformat()
            }
            response = self.client.table("users").insert(data).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update_last_login(self, user_id: str) -> Dict[str, Any]:
        """Update user's last login timestamp"""
        try:
            response = self.client.table("users").update({
                "last_login": datetime.now().isoformat()
            }).eq("id", user_id).execute()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_user_subdomain(self, user_id: str) -> Optional[str]:
        """Get user's subdomain"""
        try:
            response = self.client.table("users").select("subdomain").eq("id", user_id).single().execute()
            return response.data.get("subdomain") if response.data else None
        except:
            return None

    # ========================================
    # PROFILE OPERATIONS
    # ========================================

    def save_profile(self, user_id: str, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Save or update user profile"""
        try:
            # Check if profile exists
            existing = self.client.table("profiles").select("id").eq("user_id", user_id).execute()

            data = {
                "user_id": user_id,
                "name": profile_data.get("name"),
                "email": profile_data.get("email"),
                "phone": profile_data.get("phone"),
                "linkedin_url": profile_data.get("linkedin_url"),
                "work_history": json.dumps(profile_data.get("work_history", [])),
                "skills": json.dumps(profile_data.get("skills", [])),
                "education": json.dumps(profile_data.get("education", [])),
                "projects": json.dumps(profile_data.get("projects", [])),
                "contact_info": json.dumps(profile_data.get("contact_info", {})),
                "original_resume_text": profile_data.get("original_resume_text"),
                "parsing_confidence": profile_data.get("parsing_confidence", 1.0),
                "parsing_method": profile_data.get("parsing_method", "pdf"),
                "updated_at": datetime.now().isoformat()
            }

            if existing.data:
                # Update
                response = self.client.table("profiles").update(data).eq("user_id", user_id).execute()
            else:
                # Insert
                response = self.client.table("profiles").insert(data).execute()

            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user profile"""
        try:
            response = self.client.table("profiles").select("*").eq("user_id", user_id).single().execute()
            if response.data:
                # Parse JSON fields
                data = response.data
                data["work_history"] = json.loads(data.get("work_history", "[]"))
                data["skills"] = json.loads(data.get("skills", "[]"))
                data["education"] = json.loads(data.get("education", "[]"))
                data["projects"] = json.loads(data.get("projects", "[]"))
                data["contact_info"] = json.loads(data.get("contact_info", "{}"))
                return data
            return None
        except Exception as e:
            print(f"Error getting profile: {e}")
            return None

    # ========================================
    # PORTFOLIO OPERATIONS
    # ========================================

    def save_portfolio(self, user_id: str, subdomain: str, html_content: str,
                      css_content: str = "", live_url: str = "") -> Dict[str, Any]:
        """Save or update portfolio"""
        try:
            # Check if portfolio exists
            existing = self.client.table("portfolios").select("id, version").eq("user_id", user_id).execute()

            data = {
                "user_id": user_id,
                "subdomain": subdomain,
                "html_content": html_content,
                "css_content": css_content,
                "live_url": live_url,
                "last_updated": datetime.now().isoformat()
            }

            if existing.data:
                # Update and increment version
                version = existing.data[0].get("version", 1) + 1
                data["version"] = version
                response = self.client.table("portfolios").update(data).eq("user_id", user_id).execute()
            else:
                # Insert
                data["version"] = 1
                response = self.client.table("portfolios").insert(data).execute()

            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_portfolio(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user portfolio"""
        try:
            response = self.client.table("portfolios").select("*").eq("user_id", user_id).single().execute()
            return response.data if response.data else None
        except:
            return None

    # ========================================
    # RESUME OPERATIONS
    # ========================================

    def save_resume(self, user_id: str, pdf_url: str = "", docx_url: str = "",
                   content_text: str = "", ats_score: int = 0) -> Dict[str, Any]:
        """Save resume metadata"""
        try:
            data = {
                "user_id": user_id,
                "pdf_url": pdf_url,
                "docx_url": docx_url,
                "content_text": content_text,
                "ats_score": ats_score,
                "version": 1
            }
            response = self.client.table("resumes").insert(data).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_latest_resume(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's latest resume"""
        try:
            response = self.client.table("resumes").select("*").eq(
                "user_id", user_id
            ).order("created_at", desc=True).limit(1).execute()
            return response.data[0] if response.data else None
        except:
            return None

    # ========================================
    # COVER LETTER OPERATIONS
    # ========================================

    def save_cover_letter(self, user_id: str, job_description: str,
                         letter_text: str, tone: str) -> Dict[str, Any]:
        """Save cover letter"""
        try:
            data = {
                "user_id": user_id,
                "job_description_text": job_description,
                "generated_letter_text": letter_text,
                "tone_preset": tone
            }
            response = self.client.table("cover_letters").insert(data).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_cover_letters(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get user's cover letters"""
        try:
            response = self.client.table("cover_letters").select("*").eq(
                "user_id", user_id
            ).order("created_at", desc=True).limit(limit).execute()
            return response.data if response.data else []
        except:
            return []

    # ========================================
    # OPTIMIZER OPERATIONS
    # ========================================

    def save_optimizer_run(self, user_id: str, job_description: str, score: int,
                          missing_keywords: List[str], suggestions: List[Dict]) -> Dict[str, Any]:
        """Save optimizer run"""
        try:
            data = {
                "user_id": user_id,
                "job_description": job_description,
                "score": score,
                "missing_keywords": missing_keywords,
                "suggestions": json.dumps(suggestions)
            }
            response = self.client.table("optimizer_runs").insert(data).execute()
            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ========================================
    # JOB ALERTS OPERATIONS
    # ========================================

    def save_job_alerts(self, user_id: str, keywords: List[str], sources: List[str],
                       frequency: str) -> Dict[str, Any]:
        """Save job alert preferences"""
        try:
            # Check if exists
            existing = self.client.table("job_alerts").select("id").eq("user_id", user_id).execute()

            data = {
                "user_id": user_id,
                "keywords": keywords,
                "sources": sources,
                "frequency": frequency,
                "is_active": True
            }

            if existing.data:
                response = self.client.table("job_alerts").update(data).eq("user_id", user_id).execute()
            else:
                response = self.client.table("job_alerts").insert(data).execute()

            return {"success": True, "data": response.data}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ========================================
    # ANALYTICS OPERATIONS
    # ========================================

    def track_event(self, event_type: str, user_id: Optional[str] = None,
                   properties: Optional[Dict] = None) -> Dict[str, Any]:
        """Track analytics event"""
        try:
            data = {
                "event_type": event_type,
                "user_id": user_id,
                "properties": json.dumps(properties or {})
            }
            response = self.client.table("analytics_events").insert(data).execute()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ========================================
    # STORAGE OPERATIONS
    # ========================================

    def upload_file(self, bucket: str, file_path: str, file_data: bytes,
                   content_type: str = "application/octet-stream") -> Dict[str, Any]:
        """Upload file to Supabase Storage"""
        try:
            response = self.storage.from_(bucket).upload(
                file_path,
                file_data,
                {"content-type": content_type}
            )
            # Get public URL
            public_url = self.storage.from_(bucket).get_public_url(file_path)
            return {"success": True, "url": public_url}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def download_file(self, bucket: str, file_path: str) -> Optional[bytes]:
        """Download file from Supabase Storage"""
        try:
            response = self.storage.from_(bucket).download(file_path)
            return response
        except:
            return None

    def delete_file(self, bucket: str, file_path: str) -> Dict[str, Any]:
        """Delete file from Supabase Storage"""
        try:
            self.storage.from_(bucket).remove([file_path])
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Singleton instance
_supabase_client = None


def get_supabase_client() -> SupabaseClient:
    """Get or create Supabase client singleton"""
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = SupabaseClient()
    return _supabase_client
