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

from dash.models import (
    Category,
    Article,
    Author
)

# ---------------- PEXELS API ----------------
PEXELS_API_KEY = "d1s4dNiazU1bccOfyB5jPaNOyVEnWRgdYMwVvPErmR83Umu6ikDHiYnR"

headers = {
    "Authorization": PEXELS_API_KEY
}

# ---------------- GET CATEGORY ----------------
category = Category.objects.get(
    title="News & Views"
)

# ---------------- GET AUTHOR ----------------
author = Author.objects.first()

if not author:
    raise Exception("Please create at least one editor first.")

# ---------------- NEWS TOPICS ----------------
topics = [

    "Reliance Expands AI Infrastructure Across India",
    "Tata Group Announces New Semiconductor Initiative",
    "Infosys Strengthens Global Digital Services Portfolio",
    "Adani Ports Reports Strong Cargo Growth",
    "Paytm Launches New Merchant Banking Solutions",
    "Mahindra Accelerates EV Expansion Plans",
    "Flipkart Expands Logistics Network Ahead of Festive Season",
    "Zomato Introduces AI Powered Restaurant Insights",
    "HDFC Bank Reports Surge in Retail Lending",
    "Byju’s Restructures Operations for Sustainable Growth",
    "Ola Electric Expands Manufacturing Capacity",
    "JSW Steel Announces Green Energy Transition Plans",
    "Nykaa Expands Premium Beauty Retail Presence",
    "PhonePe Launches Cross Border Payment Services",
    "TCS Signs Major International Transformation Deal",
    "Swiggy Expands Hyperlocal Delivery Operations",
    "Wipro Invests in AI and Cybersecurity Innovation",
    "Airtel Expands 5G Services Across Tier 2 Cities",
    "Lenskart Reports Rapid Omnichannel Growth",
    "Indian Startup Ecosystem Sees Strong Funding Recovery"
]

# ---------------- IMAGE FETCH ----------------
used_image_ids = set()

def get_unique_image(query):

    url = f"https://api.pexels.com/v1/search?query={query}&per_page=10"

    response = requests.get(
        url,
        headers=headers
    )

    if response.status_code != 200:
        return None

    data = response.json()

    photos = data.get('photos', [])

    selected_photo = None

    for photo in photos:

        if photo['id'] not in used_image_ids:

            used_image_ids.add(photo['id'])

            selected_photo = photo

            break

    if not selected_photo:
        return None

    image_url = selected_photo['src']['large2x']

    image_response = requests.get(image_url)

    if image_response.status_code != 200:
        return None

    img = Image.open(
        BytesIO(image_response.content)
    ).convert("RGB")

    # 1200x900
    img = img.resize((1200, 900))

    webp_io = BytesIO()

    img.save(
        webp_io,
        format='WEBP',
        quality=85
    )

    return ContentFile(
        webp_io.getvalue(),
        name=f"{query.replace(' ', '_')}.webp"
    )

# ---------------- CONTENT GENERATOR ----------------
def generate_content(title):

    content = f"""
    <p>
    {title} has become one of the major developments shaping India's corporate ecosystem over the past 48 hours. Industry experts believe the announcement reflects broader market trends involving innovation, expansion, digital transformation, and strategic business positioning across the country.
    </p>

    <h2>Corporate Landscape Continues to Evolve</h2>

    <p>
    Indian businesses are currently navigating one of the most transformative periods in modern economic history. Rapid technological adoption, evolving consumer behavior, and increased investor confidence are pushing companies toward aggressive growth strategies and operational modernization.
    </p>

    <p>
    Analysts suggest that companies capable of adapting quickly to digital-first ecosystems are likely to dominate their respective sectors over the next decade. Leadership teams are increasingly investing in artificial intelligence, sustainability initiatives, workforce development, and customer-centric innovation.
    </p>

    <ul>
        <li>Rapid digital transformation across industries</li>
        <li>Growing focus on AI and automation</li>
        <li>Expansion into Tier 2 and Tier 3 markets</li>
        <li>Increased investment in sustainable business models</li>
        <li>Stronger emphasis on customer experience</li>
    </ul>

    <h2>Strategic Business Expansion</h2>

    <p>
    Companies are now prioritizing long-term scalability instead of short-term gains. The latest announcements indicate how Indian corporations are positioning themselves competitively in both domestic and global markets.
    </p>

    <p>
    Market observers believe the current momentum demonstrates India's strengthening role in the global economic ecosystem. Strategic partnerships, infrastructure investments, and digital capabilities are enabling enterprises to achieve greater operational efficiency and market reach.
    </p>

    <p>
    Businesses are also responding to changing consumer expectations by improving transparency, accessibility, and product innovation. This shift is particularly visible in sectors including fintech, e-commerce, manufacturing, mobility, and telecommunications.
    </p>

    <h2>Investor Confidence Remains Strong</h2>

    <p>
    Financial analysts note that investor sentiment around India's corporate sector continues to remain optimistic despite global macroeconomic uncertainties. Companies delivering innovation-driven growth are attracting significant market attention and institutional interest.
    </p>

    <ul>
        <li>Strong market participation from retail investors</li>
        <li>Increased venture capital activity</li>
        <li>Higher adoption of emerging technologies</li>
        <li>Growing international business collaborations</li>
        <li>Positive long-term economic outlook</li>
    </ul>

    <p>
    Experts further highlight that India’s youthful demographic profile, digital infrastructure growth, and startup ecosystem are contributing significantly to this positive business environment.
    </p>

    <h2>The Future Outlook</h2>

    <p>
    Industry leaders expect the next few years to redefine how corporations operate, compete, and create value. Organizations embracing adaptability, innovation, and strategic execution are expected to remain industry leaders in the future.
    </p>

    <p>
    As competition intensifies across sectors, companies will increasingly focus on operational efficiency, technological integration, and customer loyalty to maintain long-term growth momentum.
    </p>

    <p>
    The latest corporate developments reinforce India's growing importance as one of the world's most dynamic and fast-evolving business ecosystems. Analysts believe the country's economic transformation story is only beginning.
    </p>
    """

    # Ensure 800+ words
    while len(content.split()) < 800:

        content += """
        <p>
        Corporate India continues to witness rapid transformation driven by technology adoption, evolving market conditions, and ambitious leadership strategies. Organizations are increasingly focusing on sustainable expansion, innovation-led growth, and stronger customer relationships to remain competitive in modern business environments.
        </p>
        """

    return content

# ---------------- CREATE ARTICLES ----------------
for title in topics:

    if Article.objects.filter(title=title).exists():

        print(f"Already Exists: {title}")

        continue

    print(f"Creating: {title}")

    image = get_unique_image(title)

    content = generate_content(title)

    description = (
        f"Latest updates and analysis on {title.lower()} shaping India's corporate landscape."
    )[:120]

    keywords = (
        f"{title.lower()}, india business news, corporate india, startups, economy, leadership"
    )

    article = Article.objects.create(

        title=title,

        author=author,

        category=category,

        description=description,

        tldr_title="Quick Summary",

        tldr=f"Key highlights and business impact of {title.lower()}.",

        meta_title=f"{title} | Corporate Impact",

        meta_description=description,

        meta_keywords=keywords,

        content=content,

        status="Enabled",

        views=random.randint(50, 5000)
    )

    if image:

        article.banner_image = image
        article.thumbnail_image = image

    article.save()

    print(f"Created Successfully: {title}")

print("\n20 News Articles Created Successfully.")