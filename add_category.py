import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'corporate.settings')
django.setup()

from dash.models import Category

categories = [
    {
        "title": "Cover Story",
        "description": "In-depth flagship stories featuring influential leaders, groundbreaking ideas, and transformative narratives shaping industries, businesses, and society.",
        "meta_title": "Cover Story | Corporate Impact",
        "meta_description": "Explore Corporate Impact's flagship cover stories featuring leaders, innovators, and powerful narratives shaping modern India.",
        "meta_keywords": "cover story, business leaders, india business magazine, corporate leadership, innovation stories"
    },

    {
        "title": "Simply Two",
        "description": "An intimate interview series where influential personalities answer only two powerful questions, revealing raw, honest, and thought-provoking insights.",
        "meta_title": "Simply Two Interviews | Corporate Impact",
        "meta_description": "Discover candid interviews with India’s most fascinating personalities through the unique Simply Two format.",
        "meta_keywords": "simply two, celebrity interviews, entrepreneur interviews, leadership conversations, india personalities"
    },

    {
        "title": "Prime Personality",
        "description": "Profiles of exceptional personalities whose leadership, influence, and achievements are shaping industries and inspiring change.",
        "meta_title": "Prime Personality | Corporate Impact",
        "meta_description": "Read inspiring stories of leaders, entrepreneurs, and influential personalities driving impact across India.",
        "meta_keywords": "prime personality, business leaders, influential people, entrepreneur profiles, corporate leaders"
    },

    {
        "title": "Brand Spotlight",
        "description": "Highlighting brands, startups, and businesses making a meaningful impact through innovation, leadership, and market influence.",
        "meta_title": "Brand Spotlight | Corporate Impact",
        "meta_description": "Explore innovative brands and businesses redefining industries through creativity, growth, and leadership.",
        "meta_keywords": "brand spotlight, startups india, business brands, innovation, corporate branding"
    },

    {
        "title": "CSR Impact",
        "description": "Stories showcasing how organizations are driving positive social change through sustainability, education, healthcare, and community development initiatives.",
        "meta_title": "CSR Impact | Corporate Impact",
        "meta_description": "Discover how corporations are creating meaningful social impact through CSR and sustainability initiatives.",
        "meta_keywords": "csr impact, sustainability, corporate social responsibility, rural development, social impact"
    },

    {
        "title": "Health & Wellness",
        "description": "Insights into physical, mental, and emotional well-being, featuring expert advice, leadership wellness stories, and healthy lifestyle strategies.",
        "meta_title": "Health & Wellness | Corporate Impact",
        "meta_description": "Explore wellness insights, mental health stories, nutrition, fitness, and healthy living advice.",
        "meta_keywords": "health and wellness, mental health, fitness, nutrition, work life balance"
    }
]

for cat in categories:

    if not Category.objects.filter(title=cat['title']).exists():

        Category.objects.create(
            title=cat["title"],
            description=cat["description"],
            meta_title=cat["meta_title"],
            meta_description=cat["meta_description"],
            meta_keywords=cat["meta_keywords"]
        )

        print(f"Added: {cat['title']}")

    else:
        print(f"Already Exists: {cat['title']}")

print("Done.")