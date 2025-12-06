import os
import time
from supabase import create_client, Client
from app.core.config import settings

class SupabaseClient:
    def __init__(self):
        self.url = settings.SUPABASE_URL
        self.key = settings.SUPABASE_SERVICE_KEY
        if self.url and self.key:
            self.client: Client = create_client(self.url, self.key)
        else:
            self.client = None
            print("WARNING: Supabase credentials missing.")

    def upload_media(self, file_path: str, bucket: str = "memes") -> str:
        """
        Uploads a file to Supabase Storage and returns the public URL.
        """
        if not self.client:
            return f"https://stub-supabase.com/{file_path}"
        
        file_name = os.path.basename(file_path)
        try:
            with open(file_path, 'rb') as f:
                self.client.storage.from_(bucket).upload(file_name, f)
            
            return self.client.storage.from_(bucket).get_public_url(file_name)
        except Exception as e:
            print(f"Error uploading to Supabase: {e}")
            return f"error_uploading_{file_name}"

    def create_job(self, job_id: str, user_id: str, status: str = "queued") -> dict:
        """
        Creates a new job record in the 'jobs' table.
        """
        if not self.client:
            return {"id": job_id, "status": status}

        data = {
            "id": job_id,
            "user_id": user_id,
            "status": status,
            "created_at": "now()"
        }
        try:
            # Using data.insert() for supabase-py v2
            response = self.client.table("jobs").insert(data).execute()
            if response.data:
                return response.data[0]
            return data
        except Exception as e:
            print(f"Error creating job in Supabase: {e}")
            return data

    def update_job_status(self, job_id: str, status: str, result_url: str = None) -> dict:
        """
        Updates a job's status and result.
        """
        if not self.client:
            return {"id": job_id, "status": status}

        data = {"status": status}
        if result_url:
            data["result_url"] = result_url

        try:
            response = self.client.table("jobs").update(data).eq("id", job_id).execute()
            if response.data:
                return response.data[0]
            return {"id": job_id, "status": status}
        except Exception as e:
            print(f"Error updating job: {e}")
            return {"id": job_id, "status": status, "error": str(e)}
