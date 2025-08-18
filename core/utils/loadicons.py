def load_service_icons():
    from core.models import ServiceIcon

    # Clear old data
    ServiceIcon.objects.all().delete()

    icons = [
        ("Business & Consulting", "briefcase"),
        ("Software Development", "code"),
        ("Design & Branding", "paintbrush"),
        ("Photography & Videography", "camera"),
        ("Startup & Innovation", "rocket"),
        ("Global Services", "globe"),
        ("Security & Compliance", "shield"),
        ("Creative Ideas", "lightbulb"),
        ("Cloud & Hosting", "server"),
        ("E-commerce Solutions", "shopping-cart"),
        ("Analytics & Marketing", "bar-chart"),
        ("Health & Wellness", "heart"),
        ("Education & Training", "graduation-cap"),
        ("Music & Entertainment", "music"),
        ("Location-based Services", "map-pin"),
    ]

    for name, icon_class in icons:
        ServiceIcon.objects.create(
            name=name,
            icon_class=icon_class,
            is_lucide=True
        )

    print("Service icons loaded successfully.")
