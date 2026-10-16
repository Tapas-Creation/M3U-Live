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

def upload_to_supabase(file_content_bytes, file_name):
    try:
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
                'x-upsert': 'true'
            },
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            print(f"Successfully uploaded edited {file_name} to Supabase Storage inside '{TARGET_FOLDER}'!")
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
        
        # সোর্স ফাইলের পুরনো হেডার বা ইনফো রিমুভ করে শুধু চ্যানেল ও লিংকগুলো আলাদা করা
        lines = text_content.splitlines()
        channel_lines = []
        start_collecting = False
        
        for line in lines:
            if line.startswith("#EXTINF") or line.startswith("http://") or line.startswith("https://") or line.startswith("#EXTGRP"):
                start_collecting = True
            if start_collecting:
                channel_lines.append(line)
                
        clean_content = "\n".join(channel_lines) if channel_lines else text_content

        # বর্তমান সময় ও তারিখ
        current_time = datetime.now().strftime("%I:%M %p %d-%m-%Y")
        
        # আপনার কাস্টম হেডার ইনফরমেশন
        custom_header = f"""#EXTM3U
#PLAYLIST: {playlist_title}
#EXTENC: UTF-8

# Playlist Name: {playlist_title}
# Last Update: {current_time}
# Website: https://tapas-iptv.github.io/IPTV-Network.com/
# Facebook Page: www.facebook.com/iptvnetworkbd

"""
        
        # ফাইনাল এডিটেড ফাইল কন্টেন্ট প্রস্তুত করা
        final_content = custom_header + clean_content
        final_content_bytes = final_content.encode('utf-8')
        
        # ১. গিটহাবের লোকাল ফোল্ডারে এডিটেড ফাইলটি সেভ করা
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
        print(f"Saved edited file locally to GitHub folder: {save_path}")
        
        # ২. Supabase Storage-এর 'Auto Update' ফোল্ডারে ওই একই এডিটেড ফাইল আপলোড/রিপ্লেস করা
        upload_to_supabase(final_content_bytes, file_name)
        
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
