import asyncio
import os
import uuid
import aiohttp
from app.services.db import db
from app.services.supabase_client import SupabaseClient
from app.agents.pipeline import run_meme_pipeline

async def download_file(url: str, dest_path: str):
    print(f"Downloading {url} to {dest_path}...")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                with open(dest_path, 'wb') as f:
                    f.write(await response.read())
                print("Download successful.")
            else:
                raise Exception(f"Failed to download file from {url}. Status: {response.status}")

async def process_job(job):
    print(f"Processing job {job.id}...")
    
    # Update status to processing
    await db.job.update(where={"id": job.id}, data={"status": "processing"})
    
    temp_input = f"temp_input_{job.id}.png"
    temp_output = None
    
    try:
        # Download source image
        # If source_url is a Supabase URL, it might be accessible. 
        # If it's a local path (from emulator?), we might have issues.
        # Assuming it's a public URL (uploaded via /upload endpoint).
        if not job.source_url:
             raise Exception("No source URL provided")

        await download_file(job.source_url, temp_input)
        
        import os
        print(f"DEBUG: CWD: {os.getcwd()}")
        print(f"DEBUG: temp_input absolute: {os.path.abspath(temp_input)}")
        print(f"DEBUG: Exists? {os.path.exists(temp_input)}")

        # Run Pipeline
        # Note: run_meme_pipeline is likely synchronous or blocking if it uses PIL/Gemini sync. 
        # If it's CPU bound, we might want to run in executor, but for now direct call.
        result = run_meme_pipeline(temp_input)
        
        if result["status"] == "completed":
            local_result_path = result["result_path"]
            temp_output = local_result_path
            
            # Upload Result
            supabase = SupabaseClient()
            result_filename = f"result_{job.id}.png"
            # We use the updated upload_media which handles paths
            public_url = supabase.upload_media(local_result_path, file_name=result_filename)
            
            # Update Job
            await db.job.update(where={"id": job.id}, data={
                "status": "completed",
                "result_url": public_url
            })
            print(f"Job {job.id} completed. Result: {public_url}")
            
        else:
             raise Exception("Pipeline failed")

    except Exception as e:
        print(f"Job {job.id} failed: {e}")
        await db.job.update(where={"id": job.id}, data={"status": "failed"})
    finally:
        # Cleanup
        if os.path.exists(temp_input):
            os.remove(temp_input)
        # result path from pipeline currently returns a path, usually in /tmp or local.
        # If pipeline creates a file, we should clean it up.
        if temp_output and os.path.exists(temp_output):
            os.remove(temp_output)


async def main():
    print("Worker started. Waiting for DB connection...")
    await db.connect()
    print("DB connected. Polling for jobs...")
    
    try:
        while True:
            # Poll for queued jobs
            job = await db.job.find_first(where={"status": "queued"})
            
            if job:
                await process_job(job)
            else:
                await asyncio.sleep(2)
    except KeyboardInterrupt:
        print("Stopping worker...")
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
