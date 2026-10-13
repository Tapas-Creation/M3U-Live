import os
import json
import re

rootDir = os.path.dirname(os.path.abspath(__file__))
excludeDirs = ['.git', '.github', 'images', 'node_modules']

DATA_USER = "Tapas-Creation"
DATA_REPO = "M3U-Live"

def generate_json():
    categories = [d for d in os.listdir(rootDir) if os.path.isdir(os.path.join(rootDir, d)) and d not in excludeDirs and not d.startswith('.')]
    
    all_playlist_data = {}

    for cat in categories:
        cat_path = os.path.join(rootDir, cat)
        items = os.listdir(cat_path)

        # শুধু .m3u বা অন্যান্য ফাইলগুলো ফিল্টার করা
        valid_files = [f for f in items if os.path.isfile(os.path.join(cat_path, f)) and not f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and not f.startswith('.')]

        # ক্যাটাগরি ফোল্ডারের ভেতর বা রুট থেকে ছবি খুঁজে বের করা
        images_dir = os.path.join(cat_path, 'images')
        images_list = []
        
        if os.path.exists(images_dir) and os.path.isdir(images_dir):
            images_list = [img for img in os.listdir(images_dir) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
        else:
            # যদি আলাদা images ফোল্ডার না থাকে, তবে একই ফোল্ডারের ভেতর থাকা ছবিগুলো নেব
            images_list = [img for img in items if os.path.isfile(os.path.join(cat_path, img)) and img.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

        cat_files = []
        for index, file_name in enumerate(valid_files):
            matched_img_name = None
            
            if images_list:
                # যদি একাধিক ছবি থাকে, তবে ফাইলগুলোর সাথে ক্রমানুসারে ছবিগুলো বাইন্ড করবে
                matched_img_name = images_list[index % len(images_list)]

            # টাইটেল ক্লিন করার লজিক
            raw_name_to_clean = matched_img_name if matched_img_name else file_name
            name_without_ext = os.path.splitext(raw_name_to_clean)[0]
            clean_base_name = re.sub(r'_[a-zA-Z0-9]+$', '', name_without_ext)
            title_text = re.sub(r'[-_]', ' ', clean_base_name).strip()

            # ফাইলের ডিসপ্লে নাম
            file_ext = os.path.splitext(file_name)[1]
            name_without_file_ext = os.path.splitext(file_name)[0]
            clean_file_name = re.sub(r'_[a-zA-Z0-9]+$', '', name_without_file_ext) + file_ext

            # ছবির সঠিক সিডিএন পাথ তৈরি (images ফোল্ডার থাকলে বা না থাকলে সে অনুযায়ী পাথ বানাবে)
            if matched_img_name:
                if os.path.exists(images_dir) and os.path.isdir(images_dir):
                    img_cdn_url = f"https://cdn.jsdelivr.net/gh/{DATA_USER}/{DATA_REPO}@main/{cat}/images/{matched_img_name}"
                else:
                    img_cdn_url = f"https://cdn.jsdelivr.net/gh/{DATA_USER}/{DATA_REPO}@main/{cat}/{matched_img_name}"
            else:
                img_cdn_url = "https://via.placeholder.com/300x160?text=No+Preview"

            cat_files.append({
                "name": file_name,
                "displayName": clean_file_name,
                "download_url": f"https://cdn.jsdelivr.net/gh/{DATA_USER}/{DATA_REPO}@main/{cat}/{file_name}",
                "image": img_cdn_url,
                "title": title_text or "Live Stream",
                "category": cat
            })

        all_playlist_data[cat] = cat_files

    with open(os.path.join(rootDir, 'playlist.json'), 'w', encoding='utf-8') as f:
        json.dump(all_playlist_data, f, ensure_ascii=False, indent=2)
    print("playlist.json generated successfully with robust image matching!")

if __name__ == '__main__':
    generate_json()
