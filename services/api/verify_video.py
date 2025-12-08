import requests
import time
import sys
import os

API_URL = "http://localhost:8080" # Assuming running via start_dev.sh
TEST_IMAGE_PATH = "/Users/harshit/Documents/projects/mememind/services/api/static/uploads/test_meme.jpg"

# Ensure there is a test image
if not os.path.exists(TEST_IMAGE_PATH):
    # Try creating a dummy image if not exists
    from PIL import Image
    os.makedirs(os.path.dirname(TEST_IMAGE_PATH), exist_ok=True)
    img = Image.new('RGB', (500, 500), color = 'red')
    img.save(TEST_IMAGE_PATH)

def verify_video_flow():
    print(f"--- Starting Video Verification ---")
    
    # 1. Upload
    print(f"1. Uploading image from {TEST_IMAGE_PATH}...")
    with open(TEST_IMAGE_PATH, 'rb') as f:
        files = {'file': f}
        r = requests.post(f"{API_URL}/upload", files=files)
        if r.status_code != 200:
            print(f"Upload failed: {r.text}")
            return False
            
    media_url = r.json()['url']
    print(f"   Uploaded: {media_url}")
    
    # 2. Generate Video
    print(f"2. Requesting VIDEO generation...")
    payload = {
        "user_id": "test_script_video",
        "mood_hint": "Chaotic",
        "media_url": media_url,
        "type": "video"
    }
    
    r = requests.post(f"{API_URL}/generate-meme", json=payload)
    if r.status_code != 200:
        print(f"Generate failed: {r.text}")
        return False
        
    job_id = r.json()['job_id']
    status = r.json()['status']
    print(f"   Job Created: {job_id} ({status})")
    
    # 3. Poll
    print(f"3. Polling for completion...")
    attempts = 0
    while attempts < 60: # 60 * 2 = 2 min max
        r = requests.get(f"{API_URL}/jobs/{job_id}")
        data = r.json()
        status = data['status']
        print(f"   Status: {status}...")
        
        if status == 'completed':
            result_url = data['result_url']
            print(f"   SUCCESS! Result: {result_url}")
            if result_url.endswith('.mp4'):
                print("   Verified extension is .mp4")
                return True
            else:
                print(f"   FAILURE! Result extension is not .mp4: {result_url}")
                return False
        
        if status == 'failed':
            print("   Job FAILED.")
            return False
            
        time.sleep(2)
        attempts += 1
        
    print("   Timeout waiting for job.")
    return False

if __name__ == "__main__":
    success = verify_video_flow()
    if not success:
        sys.exit(1)
