from django.db import migrations, models


def forwards_copy_service_to_m2m(apps, schema_editor):
    Contact = apps.get_model('core', 'Contact')
    Service = apps.get_model('core', 'Service')
    # If service_type column still exists in DB, copy values to M2M
    # Some DB backends may error if column removed earlier; this assumes order: add M2M, copy, then remove field
    try:
        for contact in Contact.objects.all().iterator():
            service_id = getattr(contact, 'service_type_id', None)
            if service_id:
                try:
                    contact.services.add(service_id)
                except Exception:
                    # Fallback: resolve object
                    svc = Service.objects.filter(id=service_id).first()
                    if svc:
                        contact.services.add(svc)
    except Exception:
        # If column was already removed, skip silently
        pass


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0007_remove_video_thumbnail_remove_video_upload_thumbnail_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='services',
            field=models.ManyToManyField(blank=True, related_name='contacts', to='core.service'),
        ),
        migrations.RunPython(forwards_copy_service_to_m2m, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='contact',
            name='service_type',
        ),
    ]


