
import os
import django
import random
import requests
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile

# ---------------- DJANGO SETUP ----------------
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'corporate.settings')
django.setup()

from dash.models import Category, Article, Author


# ---------------- PEXELS API ----------------
PEXELS_API_KEY = "d1s4dNiazU1bccOfyB5jPaNOyVEnWRgdYMwVvPErmR83Umu6ikDHiYnR"

headers = {
    "Authorization": PEXELS_API_KEY
}


# ---------------- AUTHOR ----------------
author = Author.objects.first()

if not author:
    raise Exception("Please create at least one author first.")


# ---------------- ARTICLE TOPICS ----------------
article_topics = {
    "Cover Story": [
        "India's New Era of Business Leadership",
        "How Indian CEOs Are Reshaping Global Markets",
        "The Future of Corporate Innovation in India",
        "The Rise of Purpose Driven Companies",
        "India's Most Influential Business Leaders",
        "Why Leadership Culture Matters Today",
        "How Modern Businesses Build Trust",
        "The Corporate Revolution Transforming India",
        "Inside India's Fastest Growing Companies",
        "The Evolution of Executive Leadership"
    ],

    "Simply Two": [
        "Two Questions That Define Great Leadership",
        "The Simplicity Behind Success",
        "How Honest Conversations Build Influence",
        "The Psychology of Powerful Interviews",
        "Why Authenticity Matters in Leadership",
        "Conversations That Changed Careers",
        "Inside the Minds of Visionaries",
        "The Art of Asking Better Questions",
        "Minimal Conversations Maximum Impact",
        "How Great Leaders Think Differently"
    ],

    "Prime Personality": [
        "India's Emerging Visionary Leaders",
        "The Habits of Extraordinary Entrepreneurs",
        "How Influence Shapes Industries",
        "Profiles of India's Top Innovators",
        "The Journey From Startup to Success",
        "Women Leaders Creating Impact",
        "The New Faces of Business Excellence",
        "Leaders Redefining Modern India",
        "Building Legacy Through Leadership",
        "The Personality Traits of High Achievers"
    ],

    "Brand Spotlight": [
        "Brands Changing Consumer Behavior",
        "The Rise of Sustainable Branding",
        "How Startups Build Brand Authority",
        "The Power of Digital Brand Storytelling",
        "India's Most Trusted Brands",
        "The Psychology Behind Great Branding",
        "How Modern Brands Win Attention",
        "The Future of Brand Innovation",
        "Building Emotional Connection With Customers",
        "The Evolution of Corporate Branding"
    ],

    "CSR Impact": [
        "Corporate India and Rural Development",
        "How CSR Is Transforming Education",
        "Businesses Creating Sustainable Change",
        "The Future of Corporate Social Responsibility",
        "CSR Projects Making Real Impact",
        "How Companies Are Supporting Healthcare",
        "Sustainability and Modern Corporations",
        "The Rise of Conscious Capitalism",
        "Environmental Responsibility in Business",
        "CSR Strategies That Truly Work"
    ],

    "Health & Wellness": [
        "Why Mental Health Matters in Leadership",
        "The Science of Workplace Wellness",
        "How CEOs Avoid Burnout",
        "The Connection Between Fitness and Success",
        "Building Healthy Corporate Cultures",
        "The Future of Wellness at Work",
        "Healthy Habits of Successful People",
        "The Importance of Work Life Balance",
        "Nutrition and Productivity Explained",
        "Modern Wellness Trends in India"
    ]
}


# ---------------- CONTENT GENERATOR ----------------
def generate_article_html(title, category_name):

    paragraphs = []

    intro = f'''
    <p>
    {title} is becoming one of the most discussed subjects in modern India. Businesses, leaders, and organizations are increasingly focusing on innovation, sustainability, leadership, and long-term impact. In today's rapidly evolving world, understanding the importance of {category_name.lower()} has become essential for professionals, entrepreneurs, and decision-makers.
    </p>
    '''

    paragraphs.append(intro)

    sections = [
        "Why This Topic Matters",
        "Current Industry Trends",
        "Challenges and Opportunities",
        "The Indian Perspective",
        "Future Outlook"
    ]

    for section in sections:

        content = f'''
        <h2>{section}</h2>

        <p>
        {title} continues to influence industries across India and globally. Experts believe that organizations focusing on strategic innovation, digital transformation, and long-term planning are more likely to achieve sustainable success in competitive environments.
        </p>

        <p>
        Companies are now investing heavily in technology, employee well-being, leadership development, customer trust, and responsible growth models. These efforts are helping businesses adapt to changing consumer behavior while improving operational efficiency.
        </p>

        <ul>
            <li>Growing focus on innovation and technology</li>
            <li>Increasing emphasis on sustainability</li>
            <li>Rising importance of leadership and culture</li>
            <li>Better consumer engagement strategies</li>
            <li>Long-term business transformation initiatives</li>
        </ul>

        <p>
        Industry analysts suggest that the next decade will witness major transformation in the way organizations operate. Businesses that embrace adaptability, digital intelligence, and strategic planning are expected to remain ahead in the market.
        </p>
        '''

        paragraphs.append(content)

    outro = f'''
    <h2>Conclusion</h2>

    <p>
    {title} represents more than just a trend. It reflects the changing priorities of businesses, consumers, and society. As industries continue evolving, organizations that prioritize innovation, trust, sustainability, and long-term vision will shape the future of India's growth story.
    </p>
    '''

    paragraphs.append(outro)

    final_content = "\n".join(paragraphs)

    word_count = len(final_content.split())

    while word_count < 800:
        final_content += f'''
        <p>
        Businesses across sectors are continuously exploring new strategies to improve efficiency, strengthen market position, and create long-term value for stakeholders. Experts believe that adaptability and innovation will remain critical success factors in the coming years.
        </p>
        '''

        word_count = len(final_content.split())

    return final_content


# ---------------- IMAGE DOWNLOAD ----------------
def get_pexels_image(query):

    url = f"https://api.pexels.com/v1/search?query={query}&per_page=1"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None

    data = response.json()

    photos = data.get('photos')

    if not photos:
        return None

    image_url = photos[0]['src']['large']

    image_response = requests.get(image_url)

    if image_response.status_code != 200:
        return None

    img = Image.open(BytesIO(image_response.content)).convert("RGB")

    img = img.resize((1200, 900))

    webp_io = BytesIO()

    img.save(webp_io, format='WEBP', quality=85)

    return ContentFile(webp_io.getvalue(), name=f"{query.replace(' ', '_')}.webp")


# ---------------- CREATE ARTICLES ----------------
for category_name, topics in article_topics.items():

    try:
        category = Category.objects.get(title=category_name)
    except:
        print(f"Category not found: {category_name}")
        continue

    for title in topics:

        if Article.objects.filter(title=title).exists():
            print(f"Already Exists: {title}")
            continue

        print(f"Creating: {title}")

        description = f"Explore insights about {title.lower()} shaping modern industries today."

        content = generate_article_html(title, category_name)

        keywords = f"{title.lower()}, {category_name.lower()}, business, leadership, innovation, india"

        banner = get_pexels_image(title)
        thumbnail = get_pexels_image(category_name)

        article = Article.objects.create(
            title=title,
            author=author,
            category=category,
            description=description[:120],
            tldr_title="Quick Summary",
            tldr=f"A detailed overview of {title.lower()} and its growing impact.",
            meta_title=f"{title} | Corporate Impact",
            meta_description=description[:155],
            meta_keywords=keywords,
            content=content,
            status="Enabled"
        )

        if banner:
            article.banner_image = banner

        if thumbnail:
            article.thumbnail_image = thumbnail

        article.save()

        print(f"Created Successfully: {title}")

print("\nAll articles generated successfully.")
