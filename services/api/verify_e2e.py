import requests
import time
import os

API_URL = "http://localhost:8080"

def test_e2e():
    print("Starting E2E Test...")
    
    # 1. Create a dummy image
    with open("test_image.png", "wb") as f:
        f.write(os.urandom(1024)) # 1KB random noise
        
    try:
        # 2. Upload Image
        print("Uploading image...")
        files = {"file": ("test_image.png", open("test_image.png", "rb"), "image/png")}
        resp = requests.post(f"{API_URL}/upload", files=files)
        if resp.status_code != 200:
            print(f"Upload failed: {resp.text}")
            return
        
        upload_url = resp.json()["url"]
        print(f"Uploaded URL: {upload_url}")
        
        # 3. Generate Meme
        print("Requesting meme generation...")
        payload = {
            "user_id": "test-user",
            "media_url": upload_url,
            "mood_hint": "funny"
        }
        resp = requests.post(f"{API_URL}/generate-meme", json=payload)
        if resp.status_code != 200:
            print(f"Generate failed: {resp.text}")
            return
            
        job_id = resp.json()["job_id"]
        print(f"Job ID: {job_id}")
        
        # 4. Poll for completion
        # Note: Worker must be running!
        print("Polling for status (Worker must be running)...")
        for i in range(10):
            resp = requests.get(f"{API_URL}/jobs/{job_id}")
            data = resp.json()
            status = data["status"]
            print(f"Status: {status}")
            
            if status == "completed":
                print(f"Success! Result URL: {data['result_url']}")
                return
            if status == "failed":
                print("Job failed!")
                return
                
            time.sleep(2)
            
        print("Timed out waiting for job completion.")
        
    finally:
        if os.path.exists("test_image.png"):
            os.remove("test_image.png")

if __name__ == "__main__":
    test_e2e()
