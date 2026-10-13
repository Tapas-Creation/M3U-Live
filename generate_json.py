import os
import json
import re

rootDir = os.path.dirname(os.path.abspath(__file__))
excludeDirs = ['.git', '.github', 'images', 'node_modules']

def extract_hash_id(filename):
    name_without_ext = os.path.splitext(filename)[0]
    match = re.search(r'_([a-zA-Z0-9]+)$', name_without_ext)
    return match.group(1).strip() if match else None

def generate_json():
    categories = [d for d in os.listdir(rootDir) if os.path.isdir(os.path.join(rootDir, d)) and d not in excludeDirs and not d.startswith('.')]
    
    all_playlist_data = {}

    for cat in categories:
        cat_path = os.path.join(rootDir, cat)
        items = os.listdir(cat_path)

        valid_files = [f for f in items if os.path.isfile(os.path.join(cat_path, f)) and not f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')) and not f.startswith('.')]

        images_dir = os.path.join(cat_path, 'images')
        images_list = []
        if os.path.exists(images_dir) and os.path.isdir(images_dir):
            images_list = [img for img in os.listdir(images_dir) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]

        images_map = {}
        for img in images_list:
            hash_id = extract_hash_id(img)
            if hash_id:
                images_map[hash_id] = img

        cat_files = []
        for index, file_name in enumerate(valid_files):
            file_hash_id = extract_hash_id(file_name)
            matched_img_name = None
            
            # আইডি ম্যাচিং লজিক (হুবহু আপনার আগের নিয়মে)
            if file_hash_id and file_hash_id in images_map:
                matched_img_name = images_map[file_hash_id]
            elif images_list:
                fallback_img = images_list[index % len(images_list)]
                matched_img_name = fallback_img

            # টাইটেল ক্লিন করার লজিক
            raw_name_to_clean = matched_img_name if matched_img_name else file_name
            name_without_ext = os.path.splitext(raw_name_to_clean)[0]
            clean_base_name = re.sub(r'_[a-zA-Z0-9]+$', '', name_without_ext)
            title_text = re.sub(r'[-_]', ' ', clean_base_name).strip()

            # ফাইলের ডিসপ্লে নাম (এক্সটেনশন থাকবে, শেষের আইডি _8 বাদ যাবে)
            file_ext = os.path.splitext(file_name)[1]
            name_without_file_ext = os.path.splitext(file_name)[0]
            clean_file_name = re.sub(r'_[a-zA-Z0-9]+$', '', name_without_file_ext) + file_ext

            # ছবির সঠিক রিলাটিভ পাথ
            img_path = f"{cat}/images/{matched_img_name}" if matched_img_name else ""

            cat_files.append({
                "name": file_name,
                "displayName": clean_file_name,
                "download_url": f"{cat}/{file_name}",
                "image": img_path,
                "title": title_text or "Live Stream",
                "category": cat
            })

        all_playlist_data[cat] = cat_files

    with open(os.path.join(rootDir, 'playlist.json'), 'w', encoding='utf-8') as f:
        json.dump(all_playlist_data, f, ensure_ascii=False, indent=2)
    print("playlist.json generated successfully!")

if __name__ == '__main__':
    generate_json()
