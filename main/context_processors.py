from dash.models import (
    Category,
    HomepageBanner,
    CategoryMainGrid,
    Article
)


def global_content(request):

    #Global News
    live_wire = Article.objects.filter(category='7')[:10]

    # Header Categories
    header_categories = Category.objects.filter(
        status="Enabled"
    ).order_by('display_order')

    # Homepage Banners
    homepage_banners = HomepageBanner.objects.filter(
        status="Enabled"
    ).order_by('display_order')

    # Mega Menu Articles
    mega_menu = []

    for category in header_categories:

        latest_articles = Article.objects.filter(
            category=category,
            status="Enabled"
        ).order_by('-created_at')[:4]

        mega_menu.append({
            'category': category,
            'articles': latest_articles
        })

    # Main Grid Data
    category_grids = CategoryMainGrid.objects.select_related(
        'category',
        'featured_article',
        'editor_choice_1',
        'editor_choice_2',
        'editor_choice_3',
        'editor_choice_4'
    )

    return {
        'header_categories': header_categories,
        'homepage_banners': homepage_banners,
        'mega_menu': mega_menu,
        'category_grids': category_grids,
        'live_wire':live_wire,
    }