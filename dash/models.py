from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# ---------------- User Profile ----------------
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='profiles/')
    def __str__(self):
        return self.user.username


# ---------------- Categories ----------------
class Category(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    meta_title = models.CharField(max_length=255)
    meta_description = models.TextField()
    meta_keywords = models.CharField(max_length=255)

    slug = models.SlugField(unique=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    status = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default="Enabled"
    )

    display_order = models.PositiveIntegerField(
        default=0,
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)

        # Auto append new categories at end
        if not self.pk:

            last_order = Category.objects.order_by(
                '-display_order'
            ).first()

            self.display_order = (
                last_order.display_order + 1
                if last_order else 1
            )

        super().save(*args, **kwargs)


# ---------------- Authors ----------------
class Author(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="author_profile",
        null=True,
        blank=True
    )
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    description = models.TextField()
    email = models.EmailField(unique=True,blank=True, null=True)
    DOB = models.DateField(unique=True,blank=True, null=True)
    location = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='authors/')
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100,blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.slug or self.slug == '':  # Generate slug only if it's empty
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1
            while Author.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base_slug}-{count}'
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('author', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

class team(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='about_us/')
    def __str__(self):
        return self.name

# ---------------- Articles ----------------
class Article(models.Model):
    title = models.CharField(max_length=1500)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True,null=True)
    tldr_title = models.CharField(max_length=1500,blank=True, null=True)
    tldr = models.TextField(blank=True,null=True)
    meta_title = models.CharField(max_length=1500)
    meta_description = models.TextField()
    meta_keywords = models.CharField(max_length=1500)
    content = models.TextField(blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(unique=True, blank=True,max_length=1500)
    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=100,blank=True, null=True,default="Enabled")
    title_colour = models.CharField(max_length=100,blank=True)
    banner_background_colour = models.CharField(max_length=100,blank=True)
    remaining_text_colour = models.CharField(max_length=100,blank=True)
    banner_image = models.ImageField(upload_to='articles/banners/', blank=True, null=True)
    thumbnail_image = models.ImageField(upload_to='articles/thumbnails/', blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        # Create slug if missing
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1
            while Article.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        # ✅ Ensure Django actually saves the object
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('content', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

class ArticleFAQ(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="faqs")
    question = models.CharField(max_length=500)
    answer = models.TextField()

    def __str__(self):
        return self.question
    
class ArticleHowTo(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="howto_steps")
    step_name = models.CharField(max_length=300)
    step_text = models.TextField()

    def __str__(self):
        return self.step_name


class youtube(models.Model):
    title = models.CharField(max_length=3000)
    link = models.URLField()
    category = models.CharField(max_length=255)
    type = models.CharField(max_length=255,default="Reel")
    description = models.TextField()
    status = models.CharField(max_length=100,blank=True, null=True,default="Enabled")
    slug = models.SlugField(unique=True, blank=True)
    thumbnail_image = models.ImageField(upload_to='bstv/thumbnails/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            count = 1
            while Article.objects.filter(slug=slug).exists():
                slug = f'{base_slug}-{count}'
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# ---------------- Newsletter ----------------
class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email


# ---------------- Ad Management ----------------
class Ad(models.Model):
    title = models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to='ads/')
    url = models.URLField()
    clicks = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f"{self.type} - {self.url}"


# ---------------- Enquiry ----------------
class Enquiry(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
        ('Closed', 'Closed'),
    ]

    name = models.CharField(max_length=100)
    email_id = models.EmailField()
    phone_number = models.CharField(max_length=15)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    status = models.CharField(max_length=20, default='Pending', choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    

    
class WriterApplication(models.Model):
    EXPERIENCE_CHOICES = [
        ("student", "Student / Campus"),
        ("fresher", "Fresher (0–1 year)"),
        ("junior", "1–3 years"),
        ("mid", "3+ years"),
    ]

    TRACK_CHOICES = [
        ("breaking", "Daily news / breaking"),
        ("explainer", "Explainers & analysis"),
        ("opinion", "Opinion & columns"),
        ("features", "Features & longform"),
        ("script", "Video scripts / BSTV"),
        ("open", "Open to anything exciting"),
    ]

    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=120, blank=True, null=True)

    experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, blank=True, null=True)
    track = models.CharField(max_length=20, choices=TRACK_CHOICES, blank=True, null=True)

    portfolio_links = models.TextField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)

    beats = models.CharField(max_length=300, blank=True, null=True)

    why_bigstory = models.TextField()

    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    consent = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.email})"
    
class Gallery(models.Model):
    title = models.CharField(max_length=255)
    alt_text = models.CharField(max_length=255)
    image = models.ImageField(upload_to='gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class HomepageBanner(models.Model):

    title = models.CharField(max_length=255)

    image = models.ImageField(
        upload_to='homepage/banners/'
    )

    redirect_url = models.URLField()

    display_order = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=50,
        default="Enabled"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        # Auto place new banner at end
        if not self.pk:

            last_order = HomepageBanner.objects.order_by(
                '-display_order'
            ).first()

            self.display_order = (
                last_order.display_order + 1
                if last_order else 1
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



# ---------------- Category Main Grid ----------------

class CategoryMainGrid(models.Model):

    category = models.OneToOneField(
        Category,
        on_delete=models.CASCADE,
        related_name="main_grid"
    )

    featured_article = models.ForeignKey(
        Article,
        on_delete=models.SET_NULL,
        null=True,
        related_name="featured_main_article"
    )

    editor_choice_1 = models.ForeignKey(
        Article,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="editor_choice_1"
    )

    editor_choice_2 = models.ForeignKey(
        Article,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="editor_choice_2"
    )

    editor_choice_3 = models.ForeignKey(
        Article,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="editor_choice_3"
    )

    editor_choice_4 = models.ForeignKey(
        Article,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="editor_choice_4"
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.category.title
    
# ============================================
# HOMEPAGE ADS
# ============================================
class HomepageAds(models.Model):

    title = models.CharField(
        max_length=255
    )

    image = models.ImageField(
        upload_to='homepage_ads/'
    )

    redirect_url = models.URLField(
        blank=True,
        null=True
    )

    display_order = models.PositiveIntegerField(
        default=1
    )

    status = models.CharField(
        max_length=50,
        choices=[
            ('Enabled', 'Enabled'),
            ('Disabled', 'Disabled')
        ],
        default='Enabled'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.title