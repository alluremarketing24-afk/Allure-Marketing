from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
import os
from django.core.files.storage import default_storage
from django.db import models
from django.core.validators import FileExtensionValidator
from django.db import models
from django.core.validators import FileExtensionValidator
from storages.backends.s3boto3 import S3Boto3Storage
s3_storage = S3Boto3Storage()


class VideoType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']





class Video(models.Model):
    video_name = models.CharField(max_length=200)
    video_type = models.ForeignKey("VideoType", on_delete=models.CASCADE, related_name='videos')
    video_description = models.TextField()

    # Upload directly to S3
    video_file = models.FileField(
        upload_to='videos/',
        storage=s3_storage,
        validators=[FileExtensionValidator(
            allowed_extensions=['mp4', 'avi', 'mov', 'wmv', 'flv', 'webm', 'mkv']
        )],
        blank=True, null=True
    )
    thumbnail_file = models.ImageField(
        upload_to='thumbnails/',
        storage=s3_storage,
        blank=True, null=True
    )

    # Auto-filled URL fields (saved permanently in DB)
    video_url = models.URLField(blank=True)
    thumbnail_url = models.URLField(blank=True)

    is_featured = models.BooleanField(default=False)
    video_created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        """Ensure URLs always point to S3 links after upload"""
        if self.video_file:
            self.video_url = self.video_file.url
        if self.thumbnail_file:
            self.thumbnail_url = self.thumbnail_file.url
        super().save(*args, **kwargs)

    def get_video_url(self):
        """Return the proper S3 URL with region"""
        if self.video_file:
            return self.video_file.url
        return self.video_url

    def get_thumbnail_url(self):
        """Return the proper S3 URL with region"""
        if self.thumbnail_file:
            return self.thumbnail_file.url
        return self.thumbnail_url

    def __str__(self):
        return self.video_name

    class Meta:
        ordering = ['order', '-video_created_at']


class ServiceIcon(models.Model):
    ICON_CHOICES = [
        ("lucide-briefcase", "Business & Consulting"),
        ("lucide-code", "Software Development"),
        ("lucide-paintbrush", "Design & Branding"),
        ("lucide-camera", "Photography & Videography"),
        ("lucide-rocket", "Startup & Innovation"),
        ("lucide-globe", "Global Services"),
        ("lucide-shield", "Security & Compliance"),
        ("lucide-lightbulb", "Creative Ideas"),
        ("lucide-server", "Cloud & Hosting"),
        ("lucide-shopping-cart", "E-commerce Solutions"),
        ("lucide-bar-chart", "Analytics & Marketing"),
        ("lucide-heart", "Health & Wellness"),
        ("lucide-graduation-cap", "Education & Training"),
        ("lucide-music", "Music & Entertainment"),
        ("lucide-map-pin", "Location-based Services"),
    ]

    name = models.CharField(max_length=100)
    icon_class = models.CharField(
        max_length=100,
        choices=ICON_CHOICES,
        help_text="Select a predefined Lucide icon"
    )
    icon_image = models.ImageField(upload_to='service_icons/', blank=True, null=True)
    is_lucide = models.BooleanField(
        default=True,
        help_text="Is this a Lucide icon?"
    )

    def __str__(self):
        return f"{self.name} ({self.get_icon_class_display()})"

    class Meta:
        ordering = ['name']


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ForeignKey(ServiceIcon, on_delete=models.SET_NULL, null=True, blank=True)
    key_point_1 = models.CharField(max_length=200, blank=True)
    key_point_2 = models.CharField(max_length=200, blank=True)
    key_point_3 = models.CharField(max_length=200, blank=True)
    key_point_4 = models.CharField(max_length=200, blank=True)
    key_point_5 = models.CharField(max_length=200, blank=True)
    key_point_6 = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_key_points(self):
        points = []
        for i in range(1, 7):
            point = getattr(self, f'key_point_{i}', '')
            if point:
                points.append(point)
        return points
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order', 'name']

class Contact(models.Model):
    # DECISION_MAKER_CHOICES = [
    #     ('yes', 'Yes'),
    #     ('no', 'No'),
    # ]

    
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=20)
    business_name = models.CharField(max_length=200, blank=True)
    insta_id = models.CharField(max_length=100, blank=True, verbose_name="Instagram ID")
    city = models.CharField(max_length=100, blank=True)
    # is_decision_maker = models.CharField(
    #     max_length=3, 
    #     choices=DECISION_MAKER_CHOICES,
    #     verbose_name="Are you a decision maker?"
    # )
    # decision_maker_email = models.EmailField(
    #     blank=True, 
    #     verbose_name="Decision Maker Email",
    #     help_text="Required if you're not the decision maker"
    # )
    # decision_maker_contact = models.CharField(
    #     max_length=20, 
    #     blank=True,
    #     verbose_name="Decision Maker Contact",
    #     help_text="Required if you're not the decision maker"
    # )
    services = models.ManyToManyField(
        Service,
        blank=True,
        related_name='contacts'
    )
    email = models.EmailField()
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    
    # def clean(self):
    #     from django.core.exceptions import ValidationError
    #     if self.is_decision_maker == 'no':
    #         if not self.decision_maker_email:
    #             raise ValidationError({'decision_maker_email': 'Decision maker email is required when you are not the decision maker.'})
    #         if not self.decision_maker_contact:
    #             raise ValidationError({'decision_maker_contact': 'Decision maker contact is required when you are not the decision maker.'})
    
    def __str__(self):
        return f"{self.name} - {self.email}"
    
    
    
    class Meta:
        ordering = ['-created_at']
        

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Allure Marketing")
    tagline = models.CharField(max_length=200, default="Premium Branding & Design")
    hero_title = models.CharField(max_length=200)
    hero_subtitle = models.TextField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20)
    address = models.TextField()
    about_text = models.TextField()
    meta_description = models.TextField()
    meta_keywords = models.TextField()
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    
    def __str__(self):
        return self.site_name
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
