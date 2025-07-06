import os
from duckduckgo_search import DDGS
import requests
import time
import ast
import re
def sanitize_filename(text):
    # Remove characters that can't be in filenames
    return re.sub(r'[\\/*?:"<>|]', "", text)
def save_img(titles):
    os.makedirs("news_images", exist_ok=True)
    results = []

    with DDGS() as ddgs:
        for idx, title in enumerate(titles):
            print(f"🔍 Searching image for: {title}")
            result = list(ddgs.images(
                keywords=title,
                safesearch='off',
                max_results=1
            ))
            time.sleep(1.5)
            if result:
                results.append(result[0]['image'])
            else:
                results.append(None)
                print(f"❌ No image found for: {title}")

    for idx, img_url in enumerate(results):
        title_clean = sanitize_filename(titles[idx])
        if img_url:
            try:
                img_data = requests.get(img_url, timeout=10).content
                with open(f"news_images/{title_clean}.jpg", "wb") as img_file:
                    img_file.write(img_data)
                print(f"✅ Saved: news_images/{title_clean}.jpg")
            except Exception as e:
                print(f"❌ Failed to download image {idx+1} - {e}")
        else:
            print(f"⚠️ Skipping image {idx+1}, no URL.")
def get_titles_from_extracted_words(file_path="extracted_words.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    try:
        data_dict = ast.literal_eval(content)  # Safely convert string to dict
        if isinstance(data_dict, dict):
            return list(data_dict.keys())  # Return only the keys (titles)
        else:
            raise ValueError("Content is not a valid dictionary.")
    except Exception as e:
        print(f"❌ Error reading dictionary from {file_path}: {e}")
        return []

if __name__ == "__main__":
    titles = get_titles_from_extracted_words()
    if titles:
        print(f"Found {len(titles)} titles to search for images.")
        save_img(titles)
    else:
        print("No titles found to search for images.")

   

