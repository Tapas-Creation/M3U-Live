from datetime import datetime
import json
import os
import subprocess
import re

DATA_USER = "Tapas-Creation"
DATA_REPO = "M3U-Live"
ROOT_DIR = "."  # বর্তমান রুট ফোল্ডার

def get_git_commit_time(file_path):
    try:
        cmd = ["git", "log", "-1", "--format=%ct", "--", file_path]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return int(result.stdout.strip()) * 1000  # মিলিিসেকেন্ডে রূপান্তর
    except Exception:
        pass
    return 0

def extract_hash_id(filename):
    name_without_ext = os.path.splitext(filename)[0]
    match = re.search(r"_([a-zA-Z0-9]+)$", name_without_ext)
    return match.group(1).strip() if match else None

def generate_data():
    categories = []
    collected_files = []

    # রুট ফোল্ডারের সব ফোল্ডার স্ক্যান করা
    for item in os.listdir(ROOT_DIR):
        item_path = os.path.join(ROOT_DIR, item)
        if os.path.isdir(item_path) and item.lower() != "images" and not item.startswith('.') and item != ".github":
            categories.append(item)

    if not categories:
        categories = ["Movies", "Sports", "Skym3u.dev"]

    for cat_name in categories:
        cat_path = os.path.join(ROOT_DIR, cat_name)
        if not os.path.exists(cat_path) or not os.path.isdir(cat_path):
            continue

        folder_items = os.listdir(cat_path)
        valid_files = []
        images_list = []
        images_dir = os.path.join(cat_path, "images")

        # ইমেজ ফোল্ডার স্ক্যান করা
        if os.path.exists(images_dir) and os.path.isdir(images_dir):
            for img_name in os.listdir(images_dir):
                if img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    images_list.append({
                        "name": img_name,
                        "download_url": f"https://cdn.jsdelivr.net/gh/{DATA_USER}/{DATA_REPO}@main/{cat_name}/images/{img_name}"
                    })

        # ইমেজগুলোর ম্যাপ তৈরি করা আইডি দিয়ে
        images_map = {}
        for img in images_list:
            hash_id = extractHashId(img["name"])
            if hash_id:
                images_map[hash_id] = img

        # ফোল্ডারের ফাইলগুলো স্ক্যান করা
        for f_name in folder_items:
            f_path = os.path.join(cat_path, f_name)
            if os.path.isfile(f_path):
                f_lower = f_name.lower()
                if f_lower.endswith(('.png', '.jpg', '.jpeg', '.webp')) or f_name.startswith('.'):
                    continue  # ছবি বা হিডেন ফাইল বাদ

                rel_path = f"{cat_name}/{f_name}"
                commit_time = get_git_commit_time(rel_path)
                download_url = f"https://cdn.jsdelivr.net/gh/{DATA_USER}/{DATA_REPO}@main/{cat_name}/{f_name}"

                # আইডি ম্যাচিং
                file_hash_id = extractHashId(f_name)
                matched_img_obj = images_map.get(file_hash_id) if file_hash_id else None

                # ফলব্যাক ইমেজ যদি আইডি না মেলে
                if not matched_img_obj and images_list:
                    idx = len(valid_files) % len(images_list)
                    matched_img_obj = images_list[idx]

                matched_img_url = matched_img_obj["download_url"] if matched_img_obj else "https://via.placeholder.com/300x160?text=No+Preview"
                raw_name_to_clean = matched_img_obj["name"] if matched_img_obj else f_name
                name_without_ext = os.path.splitext(raw_name_to_clean)[0]

                clean_base_name = re.sub(r"_[a-zA-Z0-9]+$", "", name_without_ext)
                title_text = re.sub(r"[-_]", " ", clean_base_name).strip()

                # ডিসপ্লে নেম (আন্ডারস্কোর ট্যাগ রিমুভ করা)
                ext_match = os.path.splitext(f_name)[1]
                name_without_file_ext = os.path.splitext(f_name)[0]
                clean_file_name = re.sub(r"_[a-zA-Z0-9]+$", "", name_without_file_ext) + ext_match

                collected_files.append({
                    "name": f_name,
                    "displayName": clean_file_name,
                    "download_url": download_url,
                    "category": cat_name,
                    "image": matched_img_url,
                    "title": title_text if title_text else "Live Stream",
                    "timestamp": commit_time
                })

    # টাইমস্ট্যাম্প অনুযায়ী সর্টিং (নতুন থেকে পুরোনো)
    collected_files.sort(key=lambda x: x["timestamp"], reverse=True)

    output_data = {
        "categories": categories,
        "files": collected_files
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print("data.json generated successfully!")

if __name__ == "__main__":
    generate_data()
