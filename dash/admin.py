from django.contrib import admin
from .models import *
from .leads import *
from django.utils.html import format_html


class HomepageBannerAdmin(admin.TabularInline):
    model = HomepageBanner
    extra = 1

class CategoryMainGridAdmin(admin.TabularInline):
    model = CategoryMainGrid
    extra = 1

# ---------------- Inline Models ----------------

class ArticleFAQInline(admin.TabularInline):
    model = ArticleFAQ
    extra = 1


class ArticleHowToInline(admin.TabularInline):
    model = ArticleHowTo
    extra = 1


# ---------------- User Profile ----------------

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')


# ---------------- Category ----------------

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at')
    search_fields = ('title', 'meta_keywords')
    list_filter = ('status', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)


# ---------------- Author ----------------

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'email', 'status', 'created_at')
    search_fields = ('name', 'email', 'designation')
    list_filter = ('status', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('-created_at',)


# ---------------- Team ----------------

@admin.register(team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation')
    search_fields = ('name', 'designation')


# ---------------- Article ----------------

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'category',
        'status',
        'views',
        'likes',
        'created_at'
    )

    search_fields = (
        'title',
        'meta_keywords',
        'meta_title',
        'author__name',
        'category__title'
    )

    list_filter = (
        'status',
        'category',
        'author',
        'created_at'
    )

    prepopulated_fields = {'slug': ('title',)}

    

    readonly_fields = (
        'views',
        'likes',
        'created_at',
        'updated_at',
        'banner_preview',
        'thumbnail_preview',
    )

    inlines = [ArticleFAQInline, ArticleHowToInline]

    ordering = ('-created_at',)

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'title',
                'slug',
                'author',
                'category',
                'status'
            )
        }),

        ('Content', {
            'fields': (
                'description',
                'content',
                'tldr_title',
                'tldr'
            )
        }),

        ('SEO', {
            'fields': (
                'meta_title',
                'meta_description',
                'meta_keywords'
            )
        }),

        ('Design Settings', {
            'fields': (
                'title_colour',
                'banner_background_colour',
                'remaining_text_colour',
            )
        }),

        ('Images', {
            'fields': (
                'banner_image',
                'banner_preview',
                'thumbnail_image',
                'thumbnail_preview',
            )
        }),

        ('Stats', {
            'fields': (
                'views',
                'likes',
                'created_at',
                'updated_at'
            )
        }),
    )

    def banner_preview(self, obj):
        if obj.banner_image:
            return format_html(
                '<img src="{}" width="200" style="border-radius:10px;" />',
                obj.banner_image.url
            )
        return "No Image"

    banner_preview.short_description = "Banner Preview"

    def thumbnail_preview(self, obj):
        if obj.thumbnail_image:
            return format_html(
                '<img src="{}" width="120" style="border-radius:10px;" />',
                obj.thumbnail_image.url
            )
        return "No Image"

    thumbnail_preview.short_description = "Thumbnail Preview"


# ---------------- YouTube ----------------

@admin.register(youtube)
class YoutubeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'type', 'status')
    search_fields = ('title', 'category')
    list_filter = ('status', 'type', 'category')
    prepopulated_fields = {'slug': ('title',)}


# ---------------- Newsletter ----------------

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')
    search_fields = ('email',)
    ordering = ('-created_at',)


# ---------------- Ads ----------------

@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'clicks')
    search_fields = ('title', 'url')


# ---------------- Enquiry ----------------

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email_id',
        'phone_number',
        'subject',
        'status',
        'created_at'
    )

    search_fields = (
        'name',
        'email_id',
        'phone_number',
        'subject'
    )

    list_filter = ('status', 'created_at')
    ordering = ('-created_at',)


# ---------------- Writer Applications ----------------

@admin.register(WriterApplication)
class WriterApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'email',
        'phone',
        'experience',
        'track',
        'created_at'
    )

    search_fields = (
        'full_name',
        'email',
        'phone'
    )

    list_filter = (
        'experience',
        'track',
        'created_at'
    )

    ordering = ('-created_at',)

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'image_preview',
        'created_at'
    )

    search_fields = (
        'title',
        'alt_text'
    )

    readonly_fields = (
        'image_preview',
        'created_at'
    )

    ordering = ('-created_at',)

    fieldsets = (
        ('Gallery Information', {
            'fields': (
                'title',
                'alt_text',
                'image',
                'image_preview',
            )
        }),

        ('System Information', {
            'fields': (
                'created_at',
            )
        }),
    )

    def image_preview(self, obj):

        if obj.image:
            return format_html(
                '<img src="{}" width="180" style="border-radius:12px;border:1px solid #dee2e6;" />',
                obj.image.url
            )

        return "No Image"

    image_preview.short_description = "Preview"

@admin.register(BylineLead)
class BylineLeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'organisation', 'tier', 'status', 'assigned_to', 'created_at')
    list_filter = ('status', 'tier', 'consent_publish', 'created_at')
    list_editable = ('status', 'assigned_to')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('name', 'email', 'organisation')

@admin.register(HomemakerLead)
class HomemakerLeadAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'spotlight_type', 'status', 'created_at')
    list_filter = ('status', 'spotlight_type', 'is_entrepreneur', 'created_at')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    search_fields = ('name', 'email', 'city')


# ============================================
# HOMEPAGE ADS ADMIN
# ============================================
@admin.register(HomepageAds)
class HomepageAdsAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'display_order',
        'status',
        'created_at'
    )

    list_editable = (
        'display_order',
        'status'
    )

    list_filter = (
        'status',
        'created_at'
    )

    search_fields = (
        'title',
    )

    ordering = (
        'display_order',
    )

    readonly_fields = (
        'created_at',
    )


# ============================================
# FEATURED VIDEOS ADMIN
# ============================================
@admin.register(FeaturedVideo)
class FeaturedVideoAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'display_order',
        'status',
        'created_at'
    )

    list_editable = (
        'display_order',
        'status'
    )

    list_filter = (
        'status',
        'created_at'
    )

    search_fields = (
        'title',
        'youtube_url'
    )

    ordering = (
        'display_order',
    )

    readonly_fields = (
        'youtube_video_id',
        'created_at',
        'updated_at'
    )