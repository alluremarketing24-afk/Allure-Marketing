from django import forms
from .models import Contact, Video, Service, ServiceIcon

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'name', 'contact', 'business_name', 'insta_id', 'city', 'services',
            'email', 'message'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-white/5 border border-yellow-500/30 text-white placeholder-gray-400 focus:border-yellow-500/80 focus:outline-none transition-all',
                'placeholder': 'Your Name *'
            }),
            'contact': forms.TextInput(attrs={
                'type': 'tel',
                'pattern': r'^\d{9,10}$',
                'title': 'Contact number must be 9 or 10 digits.',
                'class': 'w-full px-4 py-3 rounded-lg bg-white/5 border border-yellow-500/30 text-white placeholder-gray-400 focus:border-yellow-500/80 focus:outline-none transition-all',
                'placeholder': 'Your Contact Number *'
            }),
            'business_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-white/5 border border-yellow-500/30 text-white placeholder-gray-400 focus:border-yellow-500/80 focus:outline-none transition-all',
                'placeholder': 'Business Name'
            }),
            'insta_id': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-white/5 border border-yellow-500/30 text-white placeholder-gray-400 focus:border-yellow-500/80 focus:outline-none transition-all',
                'placeholder': 'Instagram ID'
            }),
            'city': forms.TextInput(attrs={
                'id': 'city',
                'class': 'w-full px-4 py-3 rounded-lg bg-white/5 border border-yellow-500/30 text-white placeholder-gray-400 focus:border-yellow-500/80 focus:outline-none transition-all',
                'placeholder': 'City *'
            }),
            'services': forms.CheckboxSelectMultiple(attrs={
                'class': 'grid grid-cols-1 sm:grid-cols-2 gap-2 text-white',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-white/5 border border-yellow-500/30 text-white placeholder-gray-400 focus:border-yellow-500/80 focus:outline-none transition-all',
                'placeholder': 'Your Email *'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg bg-white/5 border border-yellow-500/30 text-white placeholder-gray-400 focus:border-yellow-500/80 focus:outline-none transition-all',
                'placeholder': 'Your Message',
                'rows': 4
            }),
        }
            # ✅ Add this below Meta
    def clean_contact(self):
        contact = self.cleaned_data.get('contact')

        if not contact.isdigit():
            raise forms.ValidationError("Contact number must contain only digits.")

        if len(contact) not in [9, 10]:
            raise forms.ValidationError("Contact number must be 9 or 10 digits long.")

        return contact
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: order services alphabetically
        if 'services' in self.fields:
            self.fields['services'].queryset = Service.objects.filter(is_active=True).order_by('name')

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = [
            'video_name',
            'video_type',
            'video_description',
            'video_file',
            'video_url',
            'thumbnail_file',   # ✅ updated
            'thumbnail_url',    # ✅ include if you want manual URL input
            'is_featured',
            'order'
        ]
        widgets = {
            'video_description': forms.Textarea(attrs={'rows': 4}),
        }
        help_texts = {
            'video_file': 'Upload a video file OR provide a video URL below',
            'video_url': 'External video URL (YouTube, Vimeo, etc.) OR leave blank if uploading file',
            'thumbnail_file': 'Upload a thumbnail image (stored in S3)',
            'thumbnail_url': 'Or paste an external thumbnail URL (optional)',
        }

