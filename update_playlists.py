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

def download_and_update(url, save_path):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8', errors='ignore')
        
        # প্রতিবার ডাউনলোডের সময় বর্তমান তারিখ ও সময় দিয়ে একটি কমেন্ট তৈরি করা
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_comment = f"\n# Last Auto-Updated: {current_time}\n"
        
        # ফাইলের শেষে টাইমস্ট্যাম্প যুক্ত করা, যাতে প্রতিবার ফাইলে নতুন পরিবর্তন থাকে এবং গিট নিশ্চিতভাবে কমিট করে
        updated_content = content + timestamp_comment
        
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
            
        print(f"Successfully downloaded, updated timestamp and saved: {save_path}")
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

if __name__ == "__main__":
    # ফোল্ডার না থাকলে তৈরি করে নেওয়া
    os.makedirs(TARGET_FOLDER, exist_ok=True)
    
    path_1 = os.path.join(TARGET_FOLDER, FILE_NAME_1)
    path_2 = os.path.join(TARGET_FOLDER, FILE_NAME_2)
    
    print("Fetching Playlist One...")
    download_and_update(RAW_URL_1, path_1)
    
    print("Fetching Playlist Two...")
    download_and_update(RAW_URL_2, path_2)
    
    print("Download and sync process completed.")
