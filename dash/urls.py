from django.contrib import admin
from django.urls import path
from dash import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("login_view",views.login_view,name='login_view'),
    path("logout_view",views.logout_view,name='logout_view'),

    path("",views.index,name='index'),

    path("enquiry",                 views.enquiry,          name='enquiry'),
    path("view_details/<id>",       views.view_details,     name='view_details'),
    path("resolve_enquiry/<id>",    views.resolve_enquiry,  name='resolve_enquiry'),

    path("editors",                 views.editors,          name='editors'),
    path("editor_details/<id>",     views.editor_details,   name='editor_details'),
    path("add_editor",              views.add_editor,       name='add_editor'),
    path("disable_editor/<id>",     views.disable_editor,   name='disable_editor'),
    path("enable_editor/<id>",      views.enable_editor,    name='enable_editor'),
    path("delete_editor/<id>",      views.delete_editor,    name='delete_editor'),
    path("edit_editor/<id>",        views.edit_editor,      name='edit_editor'),
    path("profile/<id>",            views.profile,          name='profile'),

    path("categories",              views.categories,       name='categories'),
    path("add_category",            views.add_category,     name='add_category'),
    path("disable_category/<id>",   views.disable_category, name='disable_category'),
    path("enable_category/<id>",    views.enable_category,  name='enable_category'),
    path("delete_category/<id>",    views.delete_category,  name='delete_category'),
    path("edit_category/<id>",      views.edit_category,    name='edit_category'),

    path("articles",                        views.articles,             name='articles'),
    path('ajax/search_articles/',           views.search_articles,      name='search_articles'),
    path('upload_quill_image/',             views.upload_quill_image,   name='upload_quill_image'),
    path("add_article",                     views.add_article,          name='add_article'),
    path("disable_article/<id>",            views.disable_article,      name='disable_article'),
    path("enable_article/<id>",             views.enable_article,       name='enable_article'),
    path("delete_article/<id>",             views.delete_article,       name='delete_article'),
    path("edit_article/<id>",               views.edit_article,         name='edit_article'),

    path("youtube",                    views.bstv,             name='youtube'),
    path("add_youtube",                views.add_youtube,         name='add_youtube'),
    path("disable_youtube/<id>",       views.disable_youtube,     name='disable_youtube'),
    path("enable_youtube/<id>",        views.enable_youtube,      name='enable_youtube'),
    path("delete_youtube/<id>",        views.delete_youtube,      name='delete_youtube'),
    path("edit_youtube/<id>",          views.edit_youtube,        name='edit_youtube'),

    path("featured_videos",                 views.featured_videos,         name='featured_videos'),
    path("add_featured_video",              views.add_featured_video,      name='add_featured_video'),
    path("edit_featured_video/<id>",        views.edit_featured_video,     name='edit_featured_video'),
    path("disable_featured_video/<id>",     views.disable_featured_video,  name='disable_featured_video'),
    path("enable_featured_video/<id>",      views.enable_featured_video,   name='enable_featured_video'),
    path("delete_featured_video/<id>",      views.delete_featured_video,   name='delete_featured_video'),

    path("gallery",                    views.gallery,             name='gallery'),
    path('edit_gallery/<int:id>/', views.edit_gallery, name='edit_gallery'),
    path('delete_gallery/<int:id>/', views.delete_gallery, name='delete_gallery'),

    path("content_management/",views.content_management,name='content_management'),
    path("teams",views.teams,name='teams'),
    path('delete_team/<int:id>/',views.delete_team,name='delete_team'),
    path('disable_team/<int:id>/',views.disable_team,name='disable_team'),
    path('enable_team/<int:id>/',views.enable_team,name='enable_team'),

    path('leads/',views.leads,name='leads'),
    path('view_lead/<str:lead_type>/<int:id>/',views.view_lead,name='view_lead'),
    
    path('careers/',views.careers,name='careers'),
    path('view_career/<int:id>/',views.view_career,name='view_career'),

    path('delete_ads/<int:id>/',views.delete_ads,name='delete_ads'),
    path('delete_banner/<int:id>/',views.delete_banner,name='delete_banner'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)