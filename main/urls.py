from django.contrib import admin
from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
handler404 = 'main.views.custom_404'
handler500 = 'main.views.custom_500'
urlpatterns = [
    path("",views.index,name='index'),
    path("about",views.about,name='about'),
    #legal
    path("terms",views.terms,name='terms'),
    path("privacy",views.privacy,name='privacy'),
    path("cookies",views.cookies,name='cookies'),
    #content
    path("article/<slug:slug>/",views.article,name='article'),
    path("category/<slug:slug>/",views.category,name='category'),
    path("author/<slug:slug>/",views.author,name='author'),
    #support and newsletter
    path("subscribe_form",views.subscribe_form,name='subscribe_form'),
    path("homemaker_form",views.homemaker_form,name='homemaker_form'),
    path("byline_form",views.byline_form,name='byline_form'),
    path("thank_you",views.thank_you,name='thank_you'),
    path("contact",views.support,name='contact'),
    #leads
    path("byline",views.byline,name='byline'),
    path("homemaker",views.homemaker,name='homemaker'),
    path("career_form",views.career_form,name='career_form'),
    path("career",views.career,name='career'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)