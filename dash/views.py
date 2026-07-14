from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .models import UserProfile,Enquiry,Article,ArticleFAQ,ArticleHowTo,Author,Ad,WriterApplication,youtube,Newsletter,Category,Gallery,FeaturedVideo
def superadmin_required(user):
    return user.is_superuser 

def login_view(request):
    if request.method == 'POST':  
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')

    return render(request, 'dash/signin.html')

def logout_view(request):
    logout(request)
    return redirect('/login_view')

@user_passes_test(superadmin_required, login_url='/login_view') 
def index(request):
    return render(request,'dash/index.html')

@user_passes_test(superadmin_required, login_url='/login_view') 
def news_letters(request):
     subscribers = Newsletter.objects.all()
     return render(request,'dash/subscribers/newsletters.html',{'subscribers':subscribers})

@user_passes_test(superadmin_required, login_url='/login_view') 
def enquiry(request):
     enquiries = Enquiry.objects.all()
     return render(request,'dash/enquiry/enquiries.html',{'enquiries':enquiries})

@user_passes_test(superadmin_required, login_url='/login_view') 
def view_details(request,id):
     data = get_object_or_404(Enquiry,id=id)
     return render(request,'dash/enquiry/view_details.html',{'data':data})

def resolve_enquiry(request,id):
     data = get_object_or_404(Enquiry,id=id)
     data.status = "Resolved"
     data.save()
     return redirect('/enquiry')


@user_passes_test(superadmin_required, login_url='/login_view') 
def editors(request):
     editors = Author.objects.all()
     return render(request,'dash/editors/editors.html',{'editors':editors})

@user_passes_test(superadmin_required, login_url='/login_view') 
def editor_details(request,id):
     data = get_object_or_404(Author,id=id)
     return render(request,'dash/editors/editor_details.html',{'data':data})

@user_passes_test(superadmin_required, login_url='/login_view') 
def profile(request,id):
     profile = get_object_or_404(Author,id=id)
     return render(request,'dash/editors/profile.html',{'profile':profile})

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os

@user_passes_test(superadmin_required, login_url='/login_view')
def add_editor(request):
    if request.method == 'POST':
        # USER DATA
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')

        # AUTHOR DATA
        name = request.POST.get('name')
        designation = request.POST.get('designation')
        description = request.POST.get('description')
        DOB = request.POST.get('DOB') or None
        location = request.POST.get('location')
        image = request.FILES.get('image')
        facebook_url = request.POST.get('facebook_url')
        instagram_url = request.POST.get('instagram_url')
        linkedin_url = request.POST.get('linkedin_url')
        twitter_url = request.POST.get('twitter_url')
        status = "Enabled"

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('/editors/add')
        
        if image:
            img = Image.open(image).convert("RGB")
            img = img.resize((500, 500))
            webp_io = BytesIO()
            img.save(webp_io, format='WEBP', quality=85)
            image = ContentFile(
                webp_io.getvalue(),
                name=f"{os.path.splitext(image.name)[0]}.webp"
            )

        # CREATE USER (ACTIVE)
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
            is_superuser=True,
        )

        # CREATE AUTHOR
        Author.objects.create(
            user=user,
            name=name,
            designation=designation,
            description=description,
            email=email,
            DOB=DOB,
            location=location,
            image=image,
            facebook_url=facebook_url,
            instagram_url=instagram_url,
            linkedin_url=linkedin_url,
            twitter_url=twitter_url,
            status=status
        )

        messages.success(request, 'Editor registered successfully and activated.')
        return redirect('/editors')

    return render(request, 'dash/editors/add_editor.html')

@user_passes_test(superadmin_required, login_url='/login_view') 
def edit_editor(request,id):
     data = get_object_or_404(Author,id=id)
     if request.method == 'POST':
        data.name = request.POST.get('name')
        data.designation = request.POST.get('designation')
        data.description = request.POST.get('description')
        data.email = request.POST.get('email')
        data.DOB = request.POST.get('DOB')
        data.location = request.POST.get('location')
        data.image = request.FILES.get('image')
        data.facebook_url = request.POST.get('facebook_url')
        data.instagram_url = request.POST.get('instagram_url')
        data.linkedin_url = request.POST.get('linkedin_url')
        data.twitter_url = request.POST.get('twitter_url')
        data.save()
        return redirect('/editors')
     
     return render(request,'dash/editors/edit_editors.html',{'data':data})

def disable_editor(request,id):
     data = get_object_or_404(Author,id=id)
     data.status = "Disabled"
     data.save()
     return redirect('/editors')

def enable_editor(request,id):
     data = get_object_or_404(Author,id=id)
     data.status = "Enabled"
     data.save()
     return redirect('/editors')

def delete_editor(request,id):
     data = get_object_or_404(Author,id=id)
     data.delete()
     return redirect('/editors')

@user_passes_test(superadmin_required, login_url='/login_view') 
def categories(request):
     categories = Category.objects.all()
     return render(request,'dash/category/categories.html',{'categories':categories})

@user_passes_test(superadmin_required, login_url='/login_view') 
def add_category(request):
     if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        meta_title = request.POST.get('meta_title')
        meta_description = request.POST.get('meta_description')
        meta_keywords = request.POST.get('meta_keywords')

        Category.objects.create(
                title=title,
                description=description,
                meta_title=meta_title,
                meta_description=meta_description,
                meta_keywords=meta_keywords,
                show_in_nav='show_in_nav' in request.POST,
            )
        return redirect('/categories') 

     return render(request, 'dash/category/add_category.html') 


def disable_category(request,id):
     data = get_object_or_404(Category,id=id)
     data.status = "Disabled"
     data.save()
     return redirect('/categories')

def enable_category(request,id):
     data = get_object_or_404(Category,id=id)
     data.status = "Enabled"
     data.save()
     return redirect('/categories')

def delete_category(request,id):
     data = get_object_or_404(Category,id=id)
     data.delete()
     return redirect('/categories')

@user_passes_test(superadmin_required, login_url='/login_view') 
def edit_category(request,id):
     data = get_object_or_404(Category,id=id)
     if request.method == 'POST':
        data.title = request.POST.get('title')
        data.description = request.POST.get('description')
        data.meta_title = request.POST.get('meta_title')
        data.meta_description = request.POST.get('meta_description')
        data.meta_keywords = request.POST.get('meta_keywords')
        data.show_in_nav = 'show_in_nav' in request.POST
        data.save()
        return redirect('/categories') 

     return render(request, 'dash/category/edit_category.html',{'data':data}) 


@user_passes_test(superadmin_required, login_url='/login_view') 
def articles(request):
     articles = Article.objects.all().order_by('-created_at')
     return render(request,'dash/articles/article.html',{'articles':articles})

from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse

def search_articles(request):
    term = request.GET.get('term', '')
    articles = Article.objects.filter(title__icontains=term).values('id', 'title')[:20]  # top 20 matches
    data = [{"label": a["title"], "value": a["id"]} for a in articles]
    return JsonResponse(data, safe=False)

@user_passes_test(superadmin_required, login_url='/login_view') 
def add_article(request):
    authors = Author.objects.all()
    categories = Category.objects.all()

    if request.method == 'POST':
        # Create Article
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        tldr_title = request.POST.get('tldr_title')
        tldr = request.POST.get('tldr')
        meta_title = request.POST.get('meta_title')
        meta_description = request.POST.get('meta_description')
        meta_keywords = request.POST.get('meta_keywords')
        content = request.POST.get('content')
        status = request.POST.get('status', 'Enabled')
        
        author = Author.objects.get(id=author_id)
        category = Category.objects.get(id=category_id)

        article = Article.objects.create(
            title=title,
            author=author,
            category=category,
            description=description,
            tldr_title=tldr_title,
            tldr=tldr,
            meta_title=meta_title,
            meta_description=meta_description,
            meta_keywords=meta_keywords,
            content=content,
            status=status,
            title_colour=request.POST.get('title_colour'),
            banner_background_colour=request.POST.get('banner_background_colour'),
            remaining_text_colour=request.POST.get('remaining_text_colour'),
            banner_image=request.FILES.get('banner_image'),
            thumbnail_image=request.FILES.get('thumbnail_image'),
        )


        # ------------------------
        # SAVE FAQ ENTRIES
        # ------------------------
        faq_indexes = request.POST.getlist("faq_index")

        for index in faq_indexes:
            q = request.POST.get(f"faq_question_{index}")
            a = request.POST.get(f"faq_answer_{index}")
            if q and a:
                ArticleFAQ.objects.create(
                    article=article,
                    question=q,
                    answer=a
                )

        # ------------------------
        # SAVE HOWTO STEPS
        # ------------------------
        howto_indexes = request.POST.getlist("howto_index")

        for index in howto_indexes:
            name = request.POST.get(f"howto_name_{index}")
            text = request.POST.get(f"howto_text_{index}")

            if name and text:
                ArticleHowTo.objects.create(
                    article=article,
                    step_name=name,
                    step_text=text
                )

        return redirect('/articles')

    return render(request, 'dash/articles/add_article.html', {
        'authors': authors,
        'categories': categories,
    })


from django.conf import settings
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def upload_quill_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        image_name = image.name
        save_path = os.path.join(settings.MEDIA_ROOT, 'quill_uploads', image_name)

        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb+') as f:
            for chunk in image.chunks():
                f.write(chunk)

        image_url = settings.MEDIA_URL + 'quill_uploads/' + image_name
        return JsonResponse({'url': image_url})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@user_passes_test(superadmin_required, login_url='/login_view') 
def edit_article(request, id):
    authors = Author.objects.all()
    categories = Category.objects.all()
    data = get_object_or_404(Article, id=id)

    if request.method == 'POST':
        # Update article main fields...
        data.title = request.POST.get('title')
        data.description = request.POST.get('description')
        data.tldr_title = request.POST.get('tldr_title')
        data.tldr = request.POST.get('tldr')
        data.meta_title = request.POST.get('meta_title')
        data.meta_description = request.POST.get('meta_description')
        data.meta_keywords = request.POST.get('meta_keywords')
        data.content = request.POST.get('content')
        data.status = request.POST.get('status', 'Enabled')

        data.author = Author.objects.get(id=request.POST.get('author'))
        data.category = Category.objects.get(id=request.POST.get('category'))

        # Save images only if new uploaded
        if request.FILES.get('banner_image'):
            data.banner_image = request.FILES.get('banner_image')

        if request.FILES.get('thumbnail_image'):
            data.thumbnail_image = request.FILES.get('thumbnail_image')

        data.save()

        # ==============================
        # UPDATE EXISTING FAQS
        # ==============================
        for faq in data.faqs.all():
            if request.POST.get(f"faq_delete_{faq.id}"):
                faq.delete()
                continue

            faq.question = request.POST.get(f"faq_question_existing_{faq.id}")
            faq.answer = request.POST.get(f"faq_answer_existing_{faq.id}")
            faq.save()

        # ADD NEW FAQS
        new_faq_indexes = request.POST.getlist("faq_new_index")
        for index in new_faq_indexes:
            q = request.POST.get(f"faq_question_new_{index}")
            a = request.POST.get(f"faq_answer_new_{index}")
            if q and a:
                ArticleFAQ.objects.create(article=data, question=q, answer=a)

        # ==============================
        # UPDATE EXISTING HOWTO STEPS
        # ==============================
        for step in data.howto_steps.all():
            if request.POST.get(f"howto_delete_{step.id}"):
                step.delete()
                continue

            step.step_name = request.POST.get(f"howto_name_existing_{step.id}")
            step.step_text = request.POST.get(f"howto_text_existing_{step.id}")
            step.save()

        # ADD NEW HOWTO STEPS
        new_step_indexes = request.POST.getlist("howto_new_index")
        for index in new_step_indexes:
            name = request.POST.get(f"howto_name_new_{index}")
            text = request.POST.get(f"howto_text_new_{index}")
            if name and text:
                ArticleHowTo.objects.create(article=data, step_name=name, step_text=text)

        return redirect('/articles')

    return render(request, 'dash/articles/edit_article.html', {
        'authors': authors,
        'categories': categories,
        'data': data
    })

def disable_article(request,id):
     data = get_object_or_404(Article,id=id)
     data.status = "Disabled"
     data.save()
     return redirect('/articles')

def enable_article(request,id):
     data = get_object_or_404(Article,id=id)
     data.status = "Enabled"
     data.save()
     return redirect('/articles')

def delete_article(request,id):
     data = get_object_or_404(Article,id=id)
     data.delete()
     return redirect('/articles')


@user_passes_test(superadmin_required, login_url='/login_view') 
def ad_manager(request):
     adv = Ad.objects.all()
     return render(request,'dash/ad_manager/ads.html',{'adv':adv})

def add_ad(request):
     if request.method == 'POST':
        title = request.POST.get('title')
        image = request.FILES.get('image')
        url = request.POST.get('url')
        Ads =  Ad.objects.create(
            title=title,
            image =  image,
            url = url,
        )
        return redirect('/ad_manager')
     return render(request,'dash/ad_manager/add_ad.html')

def edit_ad(request,id):
     data = get_object_or_404(Ad,id=id)
     if request.method == 'POST':
        data.title = request.POST.get('title')
        data.image = request.FILES.get('image')
        data.url = request.POST.get('url')
        data.save()
        return redirect('/ad_manager')
     return render(request,'dash/ad_manager/edit_ad.html',{'data':data})

def delete_ad(request,id):
     data = get_object_or_404(Ad,id=id)
     data.delete()
     return redirect('/ad_manager')


@user_passes_test(superadmin_required, login_url='/login_view') 
def bstv(request):
     contents = youtube.objects.all()
     return render(request,'dash/youtube/youtube.html',{'contents':contents})

@user_passes_test(superadmin_required, login_url='/login_view') 
def add_youtube(request):
     categories = Category.objects.all()
     if request.method == 'POST':
        title = request.POST.get('title')
        link = request.POST.get('link')
        description = request.POST.get('description')
        type = request.POST.get('type')
        category = request.POST.get('category')
        status = "Enabled"
        bstv = youtube.objects.create(
                title=title,
                link=link,
                description=description,
                type=type,
                category=get_object_or_404(Category,id=category),
                status=status,
                thumbnail_image= request.FILES.get('thumbnail_image'),
            )
        return redirect('/youtube')

     return render(request,'dash/youtube/add_youtube.html',{'categories':categories})


def disable_youtube(request,id):
     data = get_object_or_404(youtube,id=id)
     data.status = "Disabled"
     data.save()
     return redirect('/youtube')

def enable_youtube(request,id):
     data = get_object_or_404(youtube,id=id)
     data.status = "Enabled"
     data.save()
     return redirect('/youtube')

def delete_youtube(request,id):
     data = get_object_or_404(youtube,id=id)
     data.delete()
     return redirect('/youtube')

@user_passes_test(superadmin_required, login_url='/login_view') 
def edit_youtube(request,id):
    categories = Category.objects.all()
    data = get_object_or_404(youtube,id=id)
    if request.method == 'POST':
        data.title = request.POST.get('title')
        data.link = request.POST.get('link')
        data.description = request.POST.get('description')
        data.type = request.POST.get('type')
        # ✅ Correct category assignment
        category_id = request.POST.get('category')
        if category_id:
            data.category = category_id

        # ✅ Correct image assignment
        file = request.FILES.get('thumbnail_image')
        if file:
            data.thumbnail_image = file

        data.save()
        return redirect('/youtube')
    return render(request,'dash/youtube/edit_youtube.html',{'data':data,'categories':categories})


@user_passes_test(superadmin_required, login_url='/login_view') 
def gallery(request):
    # ADD IMAGE
    if request.method == "POST":

        image = request.FILES.get('image')
        title = request.POST.get('title')
        alt_text = request.POST.get('alt_text')

        if image:

            img = Image.open(image).convert("RGB")
            img = img.resize((900, 400))

            webp_io = BytesIO()
            img.save(webp_io, format='WEBP', quality=85)

            image = ContentFile(
                webp_io.getvalue(),
                name=f"{os.path.splitext(image.name)[0]}.webp"
            )

        Gallery.objects.create(
            title=title,
            alt_text=alt_text,
            image=image
        )

        return redirect('/gallery')

    images = Gallery.objects.all().order_by('-created_at')
    return render(request,'dash/gallery/gallery.html',{'images':images})

@user_passes_test(superadmin_required, login_url='/login_view')
def edit_gallery(request, id):

    image_data = get_object_or_404(Gallery, id=id)

    if request.method == "POST":

        image_data.title = request.POST.get('title')
        image_data.alt_text = request.POST.get('alt_text')

        image = request.FILES.get('image')

        if image:

            img = Image.open(image).convert("RGB")
            img = img.resize((900, 400))

            webp_io = BytesIO()
            img.save(webp_io, format='WEBP', quality=85)

            image = ContentFile(
                webp_io.getvalue(),
                name=f"{os.path.splitext(image.name)[0]}.webp"
            )

            image_data.image = image

        image_data.save()

        return redirect('/gallery')

    return redirect('/gallery')


@user_passes_test(superadmin_required, login_url='/login_view')
def delete_gallery(request, id):

    image = get_object_or_404(Gallery, id=id)

    image.delete()

    return redirect('/gallery')

from dash.models import HomepageBanner,CategoryMainGrid

@user_passes_test(superadmin_required, login_url='/login_view')
def content_management(request):

    # Categories
    categories = Category.objects.all().order_by(
        'display_order'
    )

    # Teams
    teams_list = team.objects.all().order_by(
        'display_order'
    )

    # Homepage Banners
    banners = HomepageBanner.objects.all().order_by(
        'display_order'
    )
    # Homepage Ads
    ads = HomepageAds.objects.all().order_by(
    'display_order'
    )

    # Articles
    articles = Article.objects.filter(
        status="Enabled"
    ).order_by(
        '-created_at'
    )

    # ---------------- POST ACTIONS ----------------
    if request.method == "POST":

        action = request.POST.get('action')

        # =========================================
        # ADD HOMEPAGE BANNER
        # =========================================
        if action == "save_banner":

            HomepageBanner.objects.create(

                title=request.POST.get('title'),

                redirect_url=request.POST.get(
                    'redirect_url'
                ),

                image=request.FILES.get('image'),

                display_order=request.POST.get(
                    'display_order'
                ) or 1,

                status="Enabled"
            )

            return redirect('content_management')
        
        elif action == "save_ads":
            HomepageAds.objects.create(

            title=request.POST.get('title'),

            redirect_url=request.POST.get(
            'redirect_url'
            ),

            image=request.FILES.get('image'),

            display_order=request.POST.get(
            'display_order'
            ) or 1,

            status="Enabled"
            )



        # =========================================
        # UPDATE CATEGORY ORDER
        # =========================================
        elif action == "update_category_order":

            for category in categories:

                new_order = request.POST.get(
                    f'order_{category.id}'
                )

                if new_order:

                    category.display_order = int(
                        new_order
                    )

                    category.save()

            return redirect('content_management')


        # =========================================
        # UPDATE TEAM ORDER
        # =========================================
        elif action == "update_team_order":

            for member in teams_list:

                new_order = request.POST.get(
                    f'order_{member.id}'
                )

                if new_order:

                    member.display_order = int(
                        new_order
                    )

                    member.save()

            return redirect('content_management')


        # =========================================
        # SAVE CATEGORY MAIN GRID
        # =========================================
        elif action == "save_main_grid":

            category = Category.objects.get(
                id=request.POST.get(
                    'category_id'
                )
            )

            obj, created = CategoryMainGrid.objects.get_or_create(
                category=category
            )

            obj.featured_article_id = request.POST.get(
                'featured_article'
            )

            obj.editor_choice_1_id = request.POST.get(
                'editor_choice_1'
            )

            obj.editor_choice_2_id = request.POST.get(
                'editor_choice_2'
            )

            obj.editor_choice_3_id = request.POST.get(
                'editor_choice_3'
            )

            obj.editor_choice_4_id = request.POST.get(
                'editor_choice_4'
            )

            obj.save()

            return redirect('/content_management')


    # ---------------- RENDER ----------------
    return render(
        request,
        'dash/content_management.html',
        {
            'categories': categories,

            'teams_list': teams_list,

            'banners': banners,

            'ads': ads,

            'articles': articles,
        }
    )



# =============================================
# DELETE HOMEPAGE BANNER
# =============================================
@user_passes_test(
    superadmin_required,
    login_url='/login_view'
)
def delete_banner(request, id):

    banner = get_object_or_404(
        HomepageBanner,
        id=id
    )

    banner.delete()

    return redirect('/content_management')


@user_passes_test(
    superadmin_required,
    login_url='/login_view'
)
def delete_ads(request, id):

    ad = get_object_or_404(
        HomepageAds,
        id=id
    )

    ad.delete()

    return redirect('content_management') 

from dash.models import team
def teams(request):

    members = team.objects.all().order_by('display_order')

    # ADD MEMBER
    if request.method == "POST":

        action = request.POST.get('action')

        # ADD
        if action == "add":

            team.objects.create(
                name=request.POST.get('name'),
                designation=request.POST.get('designation'),
                image=request.FILES.get('image'),
                status=request.POST.get('status') or "Enabled",
            )

            return redirect('teams')

        # EDIT
        elif action == "edit":

            obj = get_object_or_404(
                team,
                id=request.POST.get('member_id')
            )

            obj.name = request.POST.get('name')

            obj.designation = request.POST.get('designation')

            obj.status = request.POST.get('status') or obj.status

            if request.FILES.get('image'):
                obj.image = request.FILES.get('image')

            obj.save()

            return redirect('/teams')

    return render(
        request,
        'dash/teams.html',
        {
            'members': members
        }
    )


@user_passes_test(superadmin_required, login_url='/login_view')
def delete_team(request, id):

    obj = get_object_or_404(
        team,
        id=id
    )

    obj.delete()

    return redirect('/teams')


def disable_team(request, id):

    data = get_object_or_404(team, id=id)
    data.status = "Disabled"
    data.save()
    return redirect('/teams')


def enable_team(request, id):

    data = get_object_or_404(team, id=id)
    data.status = "Enabled"
    data.save()
    return redirect('/teams')


from itertools import chain

from django.contrib.auth.decorators import (
    user_passes_test
)

from dash.leads import (
    HomemakerLead,
    BylineLead
)

# ============================================
# ALL LEADS
# ============================================
@user_passes_test(
    superadmin_required,
    login_url='/login_view'
)
def leads(request):

    homemaker_leads = HomemakerLead.objects.all()

    byline_leads = BylineLead.objects.all()

    combined_leads = sorted(
        chain(
            homemaker_leads,
            byline_leads
        ),
        key=lambda x: x.created_at,
        reverse=True
    )

    return render(
        request,
        'dash/leads/leads.html',
        {
            'leads': combined_leads
        }
    )


# ============================================
# VIEW SINGLE LEAD
# ============================================
@user_passes_test(
    superadmin_required,
    login_url='/login_view'
)
def view_lead(request, lead_type, id):

    if lead_type == "homemaker":

        data = get_object_or_404(
            HomemakerLead,
            id=id
        )

    else:

        data = get_object_or_404(
            BylineLead,
            id=id
        )

    return render(
        request,
        'dash/leads/view_lead.html',
        {
            'data': data,
            'lead_type': lead_type
        }
    )

# ============================================
# CAREER APPLICATIONS
# ============================================
@user_passes_test(
    superadmin_required,
    login_url='/login_view'
)
def careers(request):

    applications = WriterApplication.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'dash/careers/careers.html',
        {
            'applications': applications
        }
    )


# ============================================
# VIEW CAREER APPLICATION
# ============================================
@user_passes_test(
    superadmin_required,
    login_url='/login_view'
)
def view_career(request, id):

    data = get_object_or_404(
        WriterApplication,
        id=id
    )

    return render(
        request,
        'dash/careers/view_career.html',
        {
            'data': data
        }
    )

from .models import HomepageAds


# ============================================
# FEATURED VIDEOS (Homepage "Watch" strip)
# ============================================
@user_passes_test(superadmin_required, login_url='/login_view')
def featured_videos(request):
    videos = FeaturedVideo.objects.all().order_by('display_order')
    return render(
        request,
        'dash/featured_videos/featured_videos.html',
        {'videos': videos}
    )


@user_passes_test(superadmin_required, login_url='/login_view')
def add_featured_video(request):
    if request.method == 'POST':
        FeaturedVideo.objects.create(
            title=request.POST.get('title'),
            youtube_url=request.POST.get('youtube_url'),
            thumbnail_image=request.FILES.get('thumbnail_image'),
            display_order=request.POST.get('display_order') or 0,
            status=request.POST.get('status', 'Enabled'),
        )
        return redirect('/featured_videos')

    return render(request, 'dash/featured_videos/add_featured_video.html')


@user_passes_test(superadmin_required, login_url='/login_view')
def edit_featured_video(request, id):
    data = get_object_or_404(FeaturedVideo, id=id)

    if request.method == 'POST':
        data.title = request.POST.get('title')
        data.youtube_url = request.POST.get('youtube_url')
        data.display_order = request.POST.get('display_order') or 0
        data.status = request.POST.get('status', 'Enabled')

        file = request.FILES.get('thumbnail_image')
        if file:
            data.thumbnail_image = file

        data.save()
        return redirect('/featured_videos')

    return render(
        request,
        'dash/featured_videos/edit_featured_video.html',
        {'data': data}
    )


def disable_featured_video(request, id):
    data = get_object_or_404(FeaturedVideo, id=id)
    data.status = "Disabled"
    data.save()
    return redirect('/featured_videos')


def enable_featured_video(request, id):
    data = get_object_or_404(FeaturedVideo, id=id)
    data.status = "Enabled"
    data.save()
    return redirect('/featured_videos')


def delete_featured_video(request, id):
    data = get_object_or_404(FeaturedVideo, id=id)
    data.delete()
    return redirect('/featured_videos')

