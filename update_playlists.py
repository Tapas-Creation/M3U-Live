import urllib.request
import urllib.error
import urllib.parse
import os
from datetime import datetime

# ১. আপনার প্রথম গিটহাবের ফাইলের Raw Link
RAW_URL_1 = "https://raw.githubusercontent.com/ahan443/FAST-IPTV/refs/heads/main/z.m3u"

# ২. আপনার দ্বিতীয় গিটহাবের ফাইলের Raw Link
RAW_URL_2 = "https://raw.githubusercontent.com/shidul100/Iptv/refs/heads/main/playlist.m3u"

# ৩. গন্তব্য ফোল্ডারের নাম (গিটহাব ও সুপাবেসের জন্য)
TARGET_FOLDER = "Auto Update"
FILE_NAME_1 = "playlist_one.m3u"
FILE_NAME_2 = "playlist_two.m3u"

# ৪. Supabase স্টোরেজ কনফিগারেশন
SUPABASE_URL = "https://liljnnprtqwoimmsjuhy.supabase.co"
SUPABASE_KEY = "sb_publishable_1HibJOEynpqyB-xuwZnruw_CvwaA3Dd"
BUCKET_NAME = "IPTV-Network"

def upload_file_to_supabase(local_file_path, file_name):
    try:
        # লোকাল গিটহাব ফোল্ডারে যে এডিটেড ফাইলটি সেভ হয়েছে, সেটি রিড করা
        if not os.path.exists(local_file_path):
            print(f"Error: Local file not found for Supabase upload: {local_file_path}")
            return False
            
        with open(local_file_path, 'rb') as f:
            file_content_bytes = f.read()

        folder_encoded = urllib.parse.quote(TARGET_FOLDER)
        file_encoded = urllib.parse.quote(file_name)
        
        upload_url = f"{SUPABASE_URL}/storage/v1/object/{BUCKET_NAME}/{folder_encoded}/{file_encoded}"
        
        req = urllib.request.Request(
            upload_url,
            data=file_content_bytes,
            headers={
                'apikey': SUPABASE_KEY,
                'Authorization': f'Bearer {SUPABASE_KEY}',
                'Content-Type': 'audio/x-mpegurl',
                'x-upsert': 'true' # Supabase-এ আগের ফাইল থাকলে ওভাররাইট বা রিপ্লেস করবে
            },
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            print(f"Successfully uploaded the GitHub-saved file '{file_name}' to Supabase Storage!")
            return True
    except urllib.error.HTTPError as e:
        error_message = e.read().decode('utf-8', errors='ignore')
        print(f"HTTP Error uploading to Supabase ({file_name}): {e.code} - {error_message}")
        return False
    except Exception as e:
        print(f"Error uploading to Supabase ({file_name}): {e}")
        return False

def process_and_save(url, save_path, file_name, playlist_title):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            content_bytes = response.read()
            
        text_content = content_bytes.decode('utf-8', errors='ignore')
        
        lines = text_content.splitlines()
        channel_lines = []
        skip_header = True
        
        for line in lines:
            if line.startswith("#EXTINF") or line.startswith("#EXTGRP"):
                skip_header = False
            if not skip_header:
                channel_lines.append(line)
                
        if not channel_lines and len(lines) > 3:
            channel_lines = lines[3:]
        elif not channel_lines:
            channel_lines = lines

        clean_content = "\n".join(channel_lines)

        current_time = datetime.now().strftime("%I:%M %p %d-%m-%Y")
        
        custom_header = f"""#EXTM3U
#PLAYLIST: {playlist_title}
#EXTENC: UTF-8

# Playlist Name: {playlist_title}
# Last Update: {current_time}
# Website: https://tapas-iptv.github.io/IPTV-Network.com/
# Facebook Page: www.facebook.com/iptvnetworkbd

"""
        
        final_content = custom_header + clean_content
        
        # ১. প্রথমে গিটহাবের লোকাল ফোল্ডারে এডিটেড ফাইলটি পার্মানেন্টলি সেভ করা
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        print(f"Successfully saved and edited locally: {save_path}")
        
        # ২. গিটহাবে সেভ হওয়ার পর ঠিক ওই লোকাল এডিটেড ফাইলটিই Supabase-এ পাঠিয়ে দেওয়া
        upload_file_to_supabase(save_path, file_name)
        
        return True
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return False

if __name__ == "__main__":
    os.makedirs(TARGET_FOLDER, exist_ok=True)
    
    path_1 = os.path.join(TARGET_FOLDER, FILE_NAME_1)
    path_2 = os.path.join(TARGET_FOLDER, FILE_NAME_2)
    
    print("Processing Playlist One...")
    process_and_save(RAW_URL_1, path_1, FILE_NAME_1, "IPTV-NETWORK - Playlist One")
    
    print("Processing Playlist Two...")
    process_and_save(RAW_URL_2, path_2, FILE_NAME_2, "IPTV-NETWORK - Playlist Two")
    
    print("All GitHub and Supabase sync processes completed.")
