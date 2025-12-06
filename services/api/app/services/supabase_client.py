class SupabaseClient:
    def __init__(self, url: str, key: str):
        self.url = url
        self.key = key

    def upload_media(self, file_path: str) -> str:
        return f"https://stub-supabase.com/{file_path}"
