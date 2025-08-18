# Django shell script to load initial data
from core.models import VideoType, Service, SiteSettings

# Create Video Types
video_types = [
    {'name': 'Brand Stories', 'description': 'Brand storytelling and promotional content'},
    {'name': 'Product Showcase', 'description': 'Product demonstrations and features'},
    {'name': 'Social Media', 'description': 'Social media content and reels'},
    {'name': 'Commercial', 'description': 'Commercial advertisements and campaigns'},
]

for vt_data in video_types:
    video_type, created = VideoType.objects.get_or_create(
        name=vt_data['name'],
        defaults={'description': vt_data['description']}
    )
    if created:
        print(f"Created video type: {video_type.name}")

# Create Services
services_data = [
    {
        'name': 'Website Development',
        'description': 'Custom-coded websites and premium landing pages tailored for elegant performance, speed, and visual experience.',
        'icon': 'code',
        'key_points': [
            'Responsive Multi-Page Design',
            'SEO Optimization & Speed',
            'Advanced CMS Integration',
            'Custom Development',
            'Mobile-First Approach',
            'Performance Optimization'
        ]
    },
    {
        'name': 'Google Ads Marketing',
        'description': 'Targeted Google Ad campaigns that maximize ROI through keyword strategy, bidding optimization, and market analytics.',
        'icon': 'search',
        'key_points': [
            'Keyword & Competitor Research',
            'Conversion-Optimized Ad Creatives',
            'Analytics & Performance Reports',
            'Budget Optimization',
            'Landing Page Integration',
            'ROI Tracking'
        ]
    },
    {
        'name': 'Content Creation',
        'description': 'Engaging photo, video, and copy content crafted to captivate audiences and reflect premium brand aesthetics.',
        'icon': 'pen-tool',
        'key_points': [
            'Reel & Short Video Production',
            'Branded Product Photography',
            'High-Converting Copywriting',
            'Social Media Graphics',
            'Brand Storytelling',
            'Content Strategy'
        ]
    },
    {
        'name': 'Social Media Management',
        'description': 'Strategic management of your brand\'s social media presence to increase reach, engagement, and brand consistency.',
        'icon': 'share-2',
        'key_points': [
            'Post Scheduling & Automation',
            'Creative Content Calendar',
            'Growth Analytics & Engagement',
            'Community Management',
            'Influencer Collaborations',
            'Brand Voice Development'
        ]
    },
    {
        'name': 'Meta Ads Marketing',
        'description': 'High-converting Meta (Facebook & Instagram) ad strategies to drive awareness, engagement, and upscale conversions.',
        'icon': 'megaphone',
        'key_points': [
            'Pixel & Audience Setup',
            'Retargeting & Funnel Strategy',
            'Ad Creative Design & A/B Testing',
            'Conversion Optimization',
            'Custom Audiences',
            'Performance Analytics'
        ]
    },
    {
        'name': 'Branding',
        'description': 'End-to-end branding from logo design to brand voice, creating a strong identity that resonates with premium audiences.',
        'icon': 'badge',
        'key_points': [
            'Luxury Logo & Typography',
            'Color Palette & Moodboards',
            'Brand Voice & Visual Language',
            'Brand Guidelines',
            'Marketing Collateral',
            'Brand Strategy'
        ]
    }
]

for service_data in services_data:
    key_points = service_data.pop('key_points')
    service, created = Service.objects.get_or_create(
        name=service_data['name'],
        defaults=service_data
    )
    
    if created:
        # Add key points
        for i, point in enumerate(key_points[:6], 1):  # Max 6 points
            setattr(service, f'key_point_{i}', point)
        service.save()
        print(f"Created service: {service.name}")

# Create Site Settings
site_settings, created = SiteSettings.objects.get_or_create(
    id=1,
    defaults={
        'site_name': 'Allure Marketing',
        'tagline': 'Premium Branding & Design',
        'hero_title': 'Allure Marketing That Elevates',
        'hero_subtitle': 'ELEVATE YOUR BRAND WITH STUNNING DIGITAL SOLUTIONS. Allure Marketing crafts premium content, high-ROI Meta ads, and strategic influencer campaigns to drive real growth.',
        'contact_email': 'alluremarketing24@gmail.com',
        'contact_phone': '+919548190688',
        'whatsapp_number': '919548190688',
        'address': 'India',
        'about_text': 'Allure Marketing crafts premium content, high-ROI Meta ads, and strategic influencer campaigns to drive real growth.',
        'meta_description': 'Allure Marketing offers premium branding, design, and marketing solutions that drive business growth.',
        'meta_keywords': 'branding, marketing, design, premium content, influencer marketing, social media marketing, advertising agency'
    }
)

if created:
    print("Created site settings")

print("Initial data loaded successfully!")
