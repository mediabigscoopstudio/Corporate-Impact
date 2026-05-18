from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages

from dash.models import (
    Newsletter,
    Enquiry,Author,team,HomepageBanner,HomepageAds
)

def index(request):

    category = get_object_or_404(
        Category,
        title="Simply Two",
        status="Enabled"
    )

    # HERO BANNERS
    hero_banners = HomepageBanner.objects.filter(
        status="Enabled"
    ).order_by(
        'display_order'
    )

    # HOMEPAGE ADS
    homepage_ads = HomepageAds.objects.filter(
        status="Enabled"
    ).order_by(
        'display_order'
    )

    # TEAM
    teams = team.objects.all()

    # LATEST NEWS
    latest_news = Article.objects.filter(
        category='7'
    )[:10]

    # SIMPLY TWO
    simply_two_category = Category.objects.filter(
        title="Simply Two",
        status="Enabled"
    ).first()

    simply_two_main_grid = None

    if simply_two_category:

        simply_two_main_grid = CategoryMainGrid.objects.filter(
            category=simply_two_category
        ).select_related(
            'featured_article',
            'editor_choice_1',
            'editor_choice_2',
            'editor_choice_3',
            'editor_choice_4'
        ).first()

    context = {

        'latest_articles': latest_news,

        'simply_two_category': simply_two_category,

        'simply_two_main_grid': simply_two_main_grid,

        'teams': teams,

        'hero_banners': hero_banners,

        'homepage_ads': homepage_ads,
    }

    return render(
        request,
        'main/index.html',
        context
    )

def about(request):
    return render(request,'main/about.html')

# Legal Section

def terms(request):
    return render(request,'main/legal/terms.html')

def privacy(request):
    return render(request,'main/legal/privacy.html')

def cookies(request):
    return render(request,'main/legal/cookies.html')

# Articles & Content 
from dash.models import Article,Category,CategoryMainGrid,HomepageBanner
def article(request, slug):

    # Main Article
    data = get_object_or_404(
        Article,
        slug=slug,
        status="Enabled"
    )

    # Increase Views
    data.views += 1
    data.save()

    # Latest Trending Articles
    trending_articles = Article.objects.filter(
        status="Enabled"
    ).exclude(
        id=data.id
    ).order_by(
        '-views',
        '-created_at'
    )[:10]

    # Related Articles From Same Category
    related_articles = Article.objects.filter(
        category=data.category,
        status="Enabled"
    ).exclude(
        id=data.id
    ).order_by(
        '-created_at'
    )[:6]

    # All Categories
    categories = Category.objects.filter(
        status="Enabled"
    ).order_by(
        'display_order'
    )

    return render(
        request,
        'main/articles/article.html',
        {
            'data': data,
            'categories': categories,
            'trending_articles': trending_articles,
            'related_articles': related_articles,
        }
    )

from django.core.paginator import Paginator

def category(request, slug):

    # Category
    data = get_object_or_404(
        Category,
        slug=slug,
        status="Enabled"
    )

    # Main Grid
    main_grid = CategoryMainGrid.objects.filter(
        category=data
    ).select_related(
        'featured_article',
        'editor_choice_1',
        'editor_choice_2',
        'editor_choice_3',
        'editor_choice_4'
    ).first()

    # Main Articles Grid
    articles = Article.objects.filter(
        category=data,
        status="Enabled"
    ).order_by(
        '-created_at'
    )

    # Pagination
    paginator = Paginator(articles, 12)

    page_number = request.GET.get('page')

    articles = paginator.get_page(page_number)

    # Trending Articles
    trending_articles = Article.objects.filter(
        status="Enabled"
    ).exclude(
        category=data
    ).order_by(
        '-views',
        '-created_at'
    )[:10]

    # Related Categories
    categories = Category.objects.filter(
        status="Enabled"
    ).exclude(
        id=data.id
    ).order_by(
        'display_order'
    )

    # Latest Articles
    latest_articles = Article.objects.filter(
        status="Enabled"
    ).exclude(
        category=data
    ).order_by(
        '-created_at'
    )[:8]

    # Total Count
    total_articles = Article.objects.filter(
        category=data,
        status="Enabled"
    ).count()

    return render(
        request,
        'main/articles/category.html',
        {
            'data': data,

            'main_grid': main_grid,

            'articles': articles,

            'trending_articles': trending_articles,

            'categories': categories,

            'latest_articles': latest_articles,

            'total_articles': total_articles,
        }
    )

def author(request, slug):

    # Author
    data = get_object_or_404(
        Author,
        slug=slug
    )

    # Author Articles
    articles = Article.objects.filter(
        author=data,
        status="Enabled"
    ).select_related(
        'category',
        'author'
    ).order_by(
        '-created_at'
    )

    # Pagination
    paginator = Paginator(
        articles,
        12
    )

    page_number = request.GET.get('page')

    articles = paginator.get_page(page_number)

    # Total Articles
    total_articles = Article.objects.filter(
        author=data,
        status="Enabled"
    ).count()

    # Total Views
    total_views = Article.objects.filter(
        author=data,
        status="Enabled"
    ).aggregate_total = sum(
        i.views for i in Article.objects.filter(
            author=data,
            status="Enabled"
        )
    )

    # Trending Articles
    trending_articles = Article.objects.filter(
        status="Enabled"
    ).exclude(
        author=data
    ).order_by(
        '-views',
        '-created_at'
    )[:8]

    # Latest Articles
    latest_articles = Article.objects.filter(
        status="Enabled"
    ).exclude(
        author=data
    ).order_by(
        '-created_at'
    )[:8]

    # Categories
    categories = Category.objects.filter(
        status="Enabled"
    ).order_by(
        'display_order'
    )

    return render(
        request,
        'main/articles/author.html',
        {
            'data': data,

            'articles': articles,

            'total_articles': total_articles,

            'total_views': total_views,

            'trending_articles': trending_articles,

            'latest_articles': latest_articles,

            'categories': categories,
        }
    )

# support and newsletter

def subscribe_form(request):

    if request.method == "POST":

        email = request.POST.get('email')

        # Prevent duplicate subscriptions
        if not Newsletter.objects.filter(email=email).exists():

            Newsletter.objects.create(
                email=email
            )

            messages.success(
                request,
                "Successfully subscribed."
            )

        else:

            messages.warning(
                request,
                "You are already subscribed."
            )

    return redirect('/thank_you')


# ---------------- THANK YOU PAGE ----------------

def thank_you(request):

    return render(
        request,
        'main/thank_you.html'
    )


# ---------------- SUPPORT PAGE ----------------

def support(request):

    if request.method == "POST":

        Enquiry.objects.create(

            name=request.POST.get('name'),

            email_id=request.POST.get('email'),

            phone_number=request.POST.get('phone'),

            subject=request.POST.get('subject'),

            message=request.POST.get('message'),
        )

        messages.success(
            request,
            "Your enquiry has been submitted."
        )

        return redirect('/thank_you')

    return render(
        request,
        'main/support.html'
    )

from dash.leads import  HomemakerLead,BylineLead

# ---------------- HOMEMAKER FORM ----------------

def homemaker_form(request):

    if request.method == "POST":

        HomemakerLead.objects.create(

            # Contact Details
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            city=request.POST.get('city'),

            # Story
            story_summary=request.POST.get('story_summary'),
            years_as_homemaker=request.POST.get('years_as_homemaker') or None,

            # Business
            is_entrepreneur=True if request.POST.get('is_entrepreneur') else False,
            business_name=request.POST.get('business_name'),

            # Social
            instagram_handle=request.POST.get('instagram_handle'),

            # Spotlight
            spotlight_type=request.POST.get('spotlight_type'),

            # Consent
            consent_publish=True if request.POST.get('consent_publish') else False,
        )

        messages.success(
            request,
            "Your homemaker application has been submitted successfully."
        )

        return redirect('/thank_you')

    return redirect('/')


# ---------------- BYLINE FORM ----------------

def byline_form(request):

    if request.method == "POST":

        BylineLead.objects.create(

            # Contact
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            city=request.POST.get('city'),

            # Professional
            organisation=request.POST.get('organisation'),
            designation=request.POST.get('designation'),

            # Program
            tier=request.POST.get('tier'),

            # Content
            topic_idea=request.POST.get('topic_idea'),
            writing_sample=request.POST.get('writing_sample'),

            # Online Presence
            linkedin_url=request.POST.get('linkedin_url'),
            website_url=request.POST.get('website_url'),

            # Brand Collab
            brand_name=request.POST.get('brand_name'),
            monthly_volume=request.POST.get('monthly_volume'),

            # Consent
            consent_publish=True if request.POST.get('consent_publish') else False,
        )

        messages.success(
            request,
            "Your byline application has been submitted successfully."
        )

        return redirect('/thank_you')

    return redirect('/')


def byline(request):
    return render(request,'main/leads/byline.html')

def homemaker(request):
    return render(request,'main/leads/homemaker.html')

from dash.models import WriterApplication

def career_form(request):
    if request.method == "POST":
        WriterApplication.objects.create(
            # Basic Details
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            location=request.POST.get('location'),
            # Professional Info
            experience=request.POST.get('experience'),
            track=request.POST.get('track'),
            # Links
            portfolio_links=request.POST.get('portfolio_links'),
            linkedin=request.POST.get('linkedin'),
            twitter=request.POST.get('twitter'),
            # Expertise
            beats=request.POST.get('beats'),
            # Why Bigstory
            why_bigstory=request.POST.get('why_bigstory'),
            # Resume
            resume=request.FILES.get('resume'),
            # Consent
            consent=True if request.POST.get('consent') else False,
        )
        messages.success(
            request,
            "Your application has been submitted successfully."
        )
        return redirect('/thank_you')
    return redirect('/')

def career(request):
    return render(request,'main/leads/career.html')


def custom_404(request, exception):

    # Latest Articles
    latest_articles = Article.objects.filter(
        status="Enabled"
    ).select_related(
        'category',
        'author'
    ).order_by(
        '-created_at'
    )[:6]

    # Categories
    categories = Category.objects.filter(
        status="Enabled"
    ).order_by(
        'display_order'
    )

    return render(
        request,
        'main/errors/404.html',
        {
            'latest_articles': latest_articles,

            'categories': categories,
        },
        status=404
    )


# ============================================
# CUSTOM 500 PAGE
# ============================================
def custom_500(request):

    latest_articles = Article.objects.filter(
        status="Enabled"
    ).select_related(
        'category',
        'author'
    ).order_by(
        '-created_at'
    )[:6]

    categories = Category.objects.filter(
        status="Enabled"
    ).order_by(
        'display_order'
    )

    return render(
        request,
        'main/errors/500.html',
        {
            'latest_articles': latest_articles,

            'categories': categories,
        },
        status=500
    )