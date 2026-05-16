import os
import re
import django
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.request import urlretrieve
from django.core.files import File

# ==========================================
# DJANGO SETUP
# ==========================================

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "corporate.settings"
)

django.setup()

# ==========================================
# IMPORT MODELS
# ==========================================

from dash.models import (
    Article,
    Category,
    Author
)

# ==========================================
# WORDPRESS CONFIG
# ==========================================

WORDPRESS_URL = "https://digicorporate70.com"
API_BASE = f"{WORDPRESS_URL}/wp-json/wp/v2"

PER_PAGE = 100

# ==========================================
# HELPERS
# ==========================================

def clean_html(content):

    if not content:
        return ""

    # Remove Gutenberg comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    soup = BeautifulSoup(content, "html.parser")

    return str(soup)


def download_image(image_url, filename="temp.jpg"):

    try:
        urlretrieve(image_url, filename)
        return filename
    except Exception as e:
        print(f"Image download failed: {e}")
        return None


def get_featured_media(media_id):

    if not media_id:
        return None

    try:
        response = requests.get(
            f"{API_BASE}/media/{media_id}"
        )

        if response.status_code == 200:
            data = response.json()
            return data.get("source_url")

    except Exception as e:
        print("Media fetch error:", e)

    return None

# ==========================================
# IMPORT CATEGORIES
# ==========================================

print("\n==============================")
print("IMPORTING CATEGORIES")
print("==============================\n")

page = 1

while True:

    response = requests.get(
        f"{API_BASE}/categories",
        params={
            "per_page": PER_PAGE,
            "page": page
        }
    )

    if response.status_code != 200:
        break

    categories = response.json()

    if not categories:
        break

    for cat in categories:

        category, created = Category.objects.get_or_create(
            slug=cat["slug"],
            defaults={
                "title": cat["name"],
                "description": cat.get("description", ""),
                "meta_title": cat["name"],
                "meta_description": cat.get("description", ""),
                "meta_keywords": cat["name"],
                "status": "Enabled"
            }
        )

        if created:
            print(f"✅ Category Created: {category.title}")
        else:
            print(f"⏩ Category Exists: {category.title}")

    page += 1

# ==========================================
# IMPORT AUTHORS
# ==========================================

print("\n==============================")
print("IMPORTING AUTHORS")
print("==============================\n")

response = requests.get(
    f"{API_BASE}/users"
)

if response.status_code == 200:

    users = response.json()

    for user in users:

        author, created = Author.objects.get_or_create(
            slug=user["slug"],
            defaults={
                "name": user["name"],
                "designation": "Author",
                "description": user.get("description", ""),
                "email": f'{user["slug"]}@example.com',
                "status": "Enabled"
            }
        )

        if created:
            print(f"✅ Author Created: {author.name}")
        else:
            print(f"⏩ Author Exists: {author.name}")

# ==========================================
# IMPORT POSTS
# ==========================================

print("\n==============================")
print("IMPORTING POSTS")
print("==============================\n")

page = 1
while True:

    response = requests.get(
        f"{API_BASE}/posts",
        params={
            "per_page": PER_PAGE,
            "page": page,
            "_embed": True
        }
    )

    if response.status_code != 200:
        print("Post fetch stopped")
        break

    posts = response.json()

    if not posts:
        break

    for post in posts:

        try:

            title = post["title"]["rendered"]
            slug = post["slug"]
            content = clean_html(
                post["content"]["rendered"]
            )

            excerpt = BeautifulSoup(
                post["excerpt"]["rendered"],
                "html.parser"
            ).text

            # =====================================
            # CATEGORY
            # =====================================

            wp_categories = post.get("categories", [])

            category = None

            if wp_categories:
                try:
                    wp_cat_id = wp_categories[0]

                    cat_response = requests.get(
                        f"{API_BASE}/categories/{wp_cat_id}"
                    )
                    if cat_response.status_code == 200:

                        cat_data = cat_response.json()

                        category = Category.objects.filter(
                            slug=cat_data["slug"]
                        ).first()

                except Exception as e:
                    print("Category mapping error:", e)

            if not category:
                category = Category.objects.first()

            # =====================================
            # AUTHOR
            # =====================================

            author = Author.objects.first()

            # =====================================
            # CREATE ARTICLE
            # =====================================
            article, created = Article.objects.get_or_create(
                slug=slug,
                defaults={
                    "title": title,
                    "author": author,
                    "category": category,
                    "description": excerpt,
                    "meta_title": title,
                    "meta_description": excerpt[:300],
                    "meta_keywords": title,
                    "content": content,
                    "status": "Enabled"
                }
            )

            # =====================================
            # FEATURED IMAGE
            # =====================================

            media_id = post.get("featured_media")
            if media_id:

                image_url = get_featured_media(media_id)

                if image_url:

                    parsed = urlparse(image_url)
                    filename = os.path.basename(parsed.path)

                    temp_file = download_image(
                        image_url,
                        filename
                    )

                    if temp_file:

                        with open(temp_file, "rb") as f:

                            article.thumbnail_image.save(
                                filename,
                                File(f),
                                save=True
                            )
                            article.banner_image.save(
                                filename,
                                File(f),
                                save=True
                            )

                        os.remove(temp_file)

            if created:
                print(f"✅ Imported: {article.title}")
            else:
                print(f"⏩ Already Exists: {article.title}")

        except Exception as e:
            print(f"❌ Error importing post: {e}")

    page += 1

print("\n==============================")
print("MIGRATION COMPLETED")
print("==============================\n")