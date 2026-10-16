import urllib.request
import os
from datetime import datetime

# ১. আপনার প্রথম গিটহাবের ফাইলের Raw Link
RAW_URL_1 = "https://raw.githubusercontent.com/ahan443/FAST-IPTV/refs/heads/main/z.m3u"

# ২. আপনার দ্বিতীয় গিটহাবের ফাইলের Raw Link
RAW_URL_2 = "https://raw.githubusercontent.com/shidul100/Iptv/refs/heads/main/playlist.m3u"

# ৩. গন্তব্য ফোল্ডারের নাম
TARGET_FOLDER = "Auto Update"

# ফাইল দুটির নাম যা সেভ হবে
FILE_NAME_1 = "playlist_one.m3u"
FILE_NAME_2 = "playlist_two.m3u"

def process_and_save(url, save_path, playlist_title):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            content_bytes = response.read()
            
        text_content = content_bytes.decode('utf-8', errors='ignore')
        
        # সোর্স ফাইলের পুরনো হেডার বাদ দিয়ে শুধু চ্যানেল এবং স্ট্রিম লিংকগুলো আলাদা করা
        lines = text_content.splitlines()
        channel_lines = []
        start_collecting = False
        
        for line in lines:
            if line.startswith("#EXTINF") or line.startswith("http://") or line.startswith("https://") or line.startswith("#EXTGRP"):
                start_collecting = True
            if start_collecting:
                channel_lines.append(line)
                
        clean_content = "\n".join(channel_lines) if channel_lines else text_content

        # বর্তমান সময় ও তারিখ (আপনার স্ক্রিনশটের ফরম্যাট অনুযায়ী)
        current_time = datetime.now().strftime("%I:%M %p %d-%m-%Y")
        
        # আপনার নিজস্ব কাস্টম হেডার ইনফরমেশন
        custom_header = f"""#EXTM3U
#PLAYLIST: {playlist_title}
#EXTENC: UTF-8

# Playlist Name: {playlist_title}
# Last Update: {current_time}
# Website: https://tapas-iptv.github.io/IPTV-Network.com/
# Facebook Page: www.facebook.com/iptvnetworkbd

"""
        
        # নতুন হেডার এবং চ্যানেল লিস্ট এক করা
        final_content = custom_header + clean_content
        
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(final_content)
            
        print(f"Successfully processed and saved: {save_path}")
        return True
    except Exception as e:
        print(f"Error processing {url}: {e}")
        return False

if __name__ == "__main__":
    # ফোল্ডার না থাকলে তৈরি করে নেওয়া
    os.makedirs(TARGET_FOLDER, exist_ok=True)
    
    path_1 = os.path.join(TARGET_FOLDER, FILE_NAME_1)
    path_2 = os.path.join(TARGET_FOLDER, FILE_NAME_2)
    
    print("Fetching and updating Playlist One...")
    process_and_save(RAW_URL_1, path_1, "IPTV-NETWORK - Playlist One")
    
    print("Fetching and updating Playlist Two...")
    process_and_save(RAW_URL_2, path_2, "IPTV-NETWORK - Playlist Two")
    
    print("All playlist sync and header update process completed.")
