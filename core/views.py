from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from .tasks import send_contact_email
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Video, VideoType, Service, Contact, SiteSettings, ServiceIcon
from .forms import ContactForm
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from datetime import datetime
from django.views.decorators.http import require_http_methods  # ✅ Add this


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.timezone import now

from django.core.cache import cache
from .models import Video, Service, VideoType, SiteSettings
from .forms import ContactForm

from django.core.cache import cache
from .models import Video, Service, VideoType, SiteSettings
from .forms import ContactForm

def home(request):
    """Optimized Home page view with caching & fewer DB hits"""

    # ✅ Cache site settings (only 1 row, rarely changes)
    site_settings = cache.get("site_settings")
    if site_settings is None:
        site_settings = SiteSettings.objects.first()
        cache.set("site_settings", site_settings, 60 * 5)  # 5 min cache

    # ✅ Cache featured videos (since usually static)
    videos = cache.get("featured_videos")
    if videos is None:
        videos = (
            Video.objects.filter(is_featured=True)
            .select_related("video_type")  # avoids extra query if you show video_type
            .order_by("order", "-video_created_at")[:6]
        )
        cache.set("featured_videos", list(videos), 60 * 5)  # cast to list for caching

    # ✅ Cache video types (small table, still saves a query per request)
    video_types = cache.get("video_types")
    if video_types is None:
        video_types = list(VideoType.objects.all())
        cache.set("video_types", video_types, 60 * 5)

    # ✅ Services (dynamic, but we optimize query with select_related)
    services = (
        Service.objects.filter(is_active=True)
        .select_related("icon")  # avoids N+1 queries for icons
        .order_by("order", "name")
    )

    # Contact form
    form = ContactForm()

    context = {
        "videos": videos,
        "services": services,
        "video_types": video_types,
        "site_settings": site_settings,
        "form": form,
    }
    return render(request, "core/home.html", context)


@csrf_exempt
@require_http_methods(["POST"])
def contact_ajax(request):
    """AJAX endpoint for contact form submission"""
    if request.method != "POST":
        return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        form = ContactForm(data)

        if form.is_valid():
            # Server-side validation for decision maker fields
            # is_dm = form.cleaned_data.get('is_decision_maker')
            # email = form.cleaned_data.get('decision_maker_email')
            # phone = form.cleaned_data.get('decision_maker_contact')

            # if is_dm == 'no' and (not email or not phone):
            #     return JsonResponse({
            #         'success': False,
            #         'errors': {
            #             'decision_maker_email': ['Required when not a decision maker.'],
            #             'decision_maker_contact': ['Required when not a decision maker.']
            #         }
            #     })

            # Save form
            contact = form.save()

            # Build email content
            subject = f'New Contact Form Submission - {contact.name}'
            message = f"""
New contact form submission received:

Name: {contact.name}
Email: {contact.email}
Phone: {contact.contact}
Business Name: {contact.business_name or 'Not provided'}
Instagram ID: {contact.insta_id or 'Not provided'}
City: {contact.city or 'Not provided'}
Service Type: {contact.service_type}
Message: {contact.message or 'No message provided'}

Submitted at: {contact.created_at.strftime('%Y-%m-%d %H:%M:%S')}
"""
# # Decision Maker: {contact.get_is_decision_maker_display()}
# Decision Maker Email: {contact.decision_maker_email or 'N/A'}
# Decision Maker Contact: {contact.decision_maker_contact or 'N/A'}

            # Send email via Celery
            try:
                print("Submitting task to Celery...")
                send_contact_email.delay(subject, message, [settings.ADMIN_EMAIL])
            except Exception as e:
                print(f"Email sending failed: {e}")

            return JsonResponse({
                'success': True,
                'message': 'Thank you for your interest! We will contact you within 24 hours to discuss your premium project.'
            })

        else:
            # Form is not valid
            return JsonResponse({'success': False, 'errors': form.errors})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON data'})
    except Exception as e:
        print("Error in contact_ajax:", e)
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})
    
    
def video_detail(request, pk):
    """Video detail view"""
    video = get_object_or_404(Video, pk=pk)
    return JsonResponse({
        'video_name': video.video_name,
        'video_description': video.video_description,
        'video_url': video.get_video_url(),
        'embed_url': video.get_embed_url(),
        'is_youtube': video.is_youtube(),
        'is_vimeo': video.is_vimeo(),
        'is_local_file': video.is_local_file(),
        'thumbnail': video.thumbnail.url if video.thumbnail else None,
    })

def get_videos_by_type(request, type_id):
    videos = Video.objects.filter(video_type_id=type_id)
    video_data = []
    for video in videos:
        video_data.append({
            'id': video.id,
            'video_name': video.video_name,
            'video_description': video.video_description,
            'thumbnail': video.thumbnail.url if video.thumbnail else None,
            'video_url': video.get_video_url(),
        })
    return JsonResponse({'videos': video_data})

# Custom Admin Panel Views
@staff_member_required
def custom_admin_dashboard(request):
    context = {
        'total_videos': Video.objects.count(),
        'total_contacts': Contact.objects.count(),
        'uncontacted_leads': Contact.objects.filter(is_contacted=False).count(),
        'total_services': Service.objects.count(),
        'recent_contacts': Contact.objects.order_by('-created_at')[:5],
        'recent_videos': Video.objects.order_by('-video_created_at')[:5],
    }
    return render(request, 'admin/custom_dashboard.html', context)

@staff_member_required
def custom_admin_videos(request):
    videos = Video.objects.filter(is_featured=True).order_by('order', '-video_created_at')
    video_types = VideoType.objects.all()
    context = {
        'videos': videos,
        'video_types': video_types,
    }
    return render(request, 'admin/videos.html', context)

@staff_member_required
def custom_admin_contacts(request):
    contacts = Contact.objects.all().order_by('-created_at')
    context = {
        'contacts': contacts,
    }
    return render(request, 'admin/contacts.html', context)

@staff_member_required
def custom_admin_services(request):
    services = Service.objects.all().order_by('order')
    icons = ServiceIcon.objects.all()
    context = {
        'services': services,
        'icons': icons,
    }
    return render(request, 'admin/services.html', context)

@staff_member_required
def export_contacts_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Contact Submissions"

    headers = [
        'Name', 'Email', 'Contact', 'Business Name', 'Instagram ID',
        'Service Type', 'City', 'Message', 'Submitted Date', 'Contacted', 'Notes'
    ]

    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")

    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment

    contacts = Contact.objects.all().order_by('-created_at')
    for row, contact in enumerate(contacts, 2):
        ws.cell(row=row, column=1,  value=contact.name)
        ws.cell(row=row, column=2,  value=contact.email)
        ws.cell(row=row, column=3,  value=contact.contact)
        ws.cell(row=row, column=4,  value=contact.business_name)
        ws.cell(row=row, column=5,  value=contact.insta_id)
        ws.cell(row=row, column=6,  value=str(contact.service_type) if contact.service_type else '')
        ws.cell(row=row, column=7,  value=contact.city)
        ws.cell(row=row, column=8,  value=contact.message)
        ws.cell(row=row, column=9,  value=contact.created_at.strftime('%Y-%m-%d %H:%M'))
        ws.cell(row=row, column=10, value="Yes" if contact.is_contacted else "No")
        ws.cell(row=row, column=11, value=contact.notes)

    # autosize columns (unchanged) ...
    for column in ws.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                max_length = max(max_length, len(str(cell.value)))
            except:
                pass
        ws.column_dimensions[column_letter].width = min(max_length + 2, 50)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=contacts_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    wb.save(response)
    return response


from django.shortcuts import render

def error_page(request, code, title, message, status):
    return render(request, "admin/error.html", {
        "code": code,
        "title": title,
        "message": message
    }, status=status)

def custom_404(request, exception):
    return error_page(request, 404, "Page Not Found", "Sorry, the page you’re looking for doesn’t exist.", 404)

def custom_500(request):
    return error_page(request, 500, "Server Error", "Something went wrong on our end. Please try again later.", 500)

def custom_403(request, exception):
    return error_page(request, 403, "Forbidden", "You don’t have permission to access this page.", 403)
