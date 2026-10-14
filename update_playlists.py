import urllib.request
import os

# ১. আপনার প্রথম গিটহাবের ফাইলের Raw Link এখানে দিন
RAW_URL_1 = "https://raw.githubusercontent.com/ahan443/FAST-IPTV/refs/heads/main/z.m3u"

# ২. আপনার দ্বিতীয় গিটহাবের ফাইলের Raw Link এখানে দিন
RAW_URL_2 = "https://raw.githubusercontent.com/shidul100/Iptv/refs/heads/main/playlist.m3u"

# ৩. আপনার গন্তব্য রিপোজিটরির যে ফোল্ডারে ফাইলগুলো জমা হবে তার নাম দিন (যেমন: "my_playlists")
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
        with urllib.request.urlopen(req) as response:
            content = response.read()
        
        with open(save_path, 'wb') as f:
            f.write(content)
        print(f"Successfully downloaded and saved: {save_path}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        exit(1)

if __name__ == "__main__":
    # ফোল্ডার না থাকলে তৈরি করে নেওয়া
    os.makedirs(TARGET_FOLDER, exist_ok=True)
    
    path_1 = os.path.join(TARGET_FOLDER, FILE_NAME_1)
    path_2 = os.path.join(TARGET_FOLDER, FILE_NAME_2)
    
    print("Fetching Playlist One...")
    download_file(RAW_URL_1, path_1)
    
    print("Fetching Playlist Two...")
    download_file(RAW_URL_2, path_2)
