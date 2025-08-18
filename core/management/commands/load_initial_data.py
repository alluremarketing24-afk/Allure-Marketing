from django.core.management.base import BaseCommand
from core.models import VideoType, Service, SiteSettings, ServiceIcon

class Command(BaseCommand):
    help = 'Load initial data for Allure Marketing website'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Loading initial data...'))
        
        # Create Service Icons
        icons_data = [
            {'name': 'Code', 'icon_class': 'code', 'is_lucide': True},
            {'name': 'Search', 'icon_class': 'search', 'is_lucide': True},
            {'name': 'Pen Tool', 'icon_class': 'pen-tool', 'is_lucide': True},
            {'name': 'Share', 'icon_class': 'share-2', 'is_lucide': True},
            {'name': 'Megaphone', 'icon_class': 'megaphone', 'is_lucide': True},
            {'name': 'Badge', 'icon_class': 'badge', 'is_lucide': True},
            {'name': 'Star', 'icon_class': 'star', 'is_lucide': True},
            {'name': 'Heart', 'icon_class': 'heart', 'is_lucide': True},
            {'name': 'Zap', 'icon_class': 'zap', 'is_lucide': True},
            {'name': 'Target', 'icon_class': 'target', 'is_lucide': True},
        ]

        for icon_data in icons_data:
            icon, created = ServiceIcon.objects.get_or_create(
                name=icon_data['name'],
                defaults=icon_data
            )
            if created:
                self.stdout.write(f"Created service icon: {icon.name}")

        # Create Video Types
        video_types = [
            {'name': 'Brand Stories', 'description': 'Brand storytelling and promotional content'},
            {'name': 'Product Showcase', 'description': 'Brand storytelling and promotional content'},
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
                self.stdout.write(f"Created video type: {video_type.name}")

        # Get icons for services
        code_icon = ServiceIcon.objects.get(name='Code')
        search_icon = ServiceIcon.objects.get(name='Search')
        pen_icon = ServiceIcon.objects.get(name='Pen Tool')
        share_icon = ServiceIcon.objects.get(name='Share')
        megaphone_icon = ServiceIcon.objects.get(name='Megaphone')
        badge_icon = ServiceIcon.objects.get(name='Badge')

        # Create Services
        services_data = [
            {
                'name': 'Website Development',
                'description': 'Custom-coded websites and premium landing pages tailored for elegant performance, speed, and visual experience.',
                'icon': code_icon,
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
                'icon': search_icon,
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
                'icon': pen_icon,
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
                'icon': share_icon,
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
                'icon': megaphone_icon,
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
                'icon': badge_icon,
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
                self.stdout.write(f"Created service: {service.name}")

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
            self.stdout.write("Created site settings")

        self.stdout.write(self.style.SUCCESS('Initial data loaded successfully!'))
