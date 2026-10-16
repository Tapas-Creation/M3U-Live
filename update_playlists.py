import urllib.request
import os

# ১. আপনার প্রথম গিটহাবের ফাইলের Raw Link
RAW_URL_1 = "https://raw.githubusercontent.com/ahan443/FAST-IPTV/refs/heads/main/z.m3u"

# ২. আপনার দ্বিতীয় গিটহাবের ফাইলের Raw Link
RAW_URL_2 = "https://raw.githubusercontent.com/shidul100/Iptv/refs/heads/main/playlist.m3u"

# ৩. গন্তব্য ফোল্ডারের নাম
TARGET_FOLDER = "Auto Update"

# ফাইল দুটির নাম যা সেভ হবে
FILE_NAME_1 = "playlist_one.m3u"
FILE_NAME_2 = "playlist_two.m3u"

def download_file(url, save_path):
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read()
        
        with open(save_path, 'wb') as f:
            f.write(content)
        print(f"Successfully downloaded and saved: {save_path}")
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
    success_1 = download_file(RAW_URL_1, path_1)
    
    print("Fetching Playlist Two...")
    success_2 = download_file(RAW_URL_2, path_2)
    
    # যদি দুটির একটিও ডাউনলোড না হয় তবেই কেবল প্রোগ্রাম ফেইল করাবে
    if not success_1 and not success_2:
        print("Error: Both playlists failed to download.")
        exit(1)
    else:
        print("Download process completed.")
