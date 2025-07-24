from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.apps import apps
from .models import User

try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

@admin.register(User)
class CustomUserAdmin(DefaultUserAdmin):
    model = User

    list_display = (
        "username", "email", "first_name", "last_name",
        "is_staff", "is_active", "xp", "level_display"
    )
    list_filter = ("is_staff", "is_superuser", "is_active")

    readonly_fields = ("xp", "level_display", "card_theme_display")

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal Info", {
            "fields": (
                "first_name", "last_name", "email", "profile_picture_url", "cover_photo_url"
            )
        }),
        ("Game Progress", {
            "fields": ("xp", "level_display", "card_theme_display")
        }),
        ("Permissions", {
            "fields": (
                "is_active", "is_staff", "is_superuser", "groups", "user_permissions"
            )
        }),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2"),
        }),
    )

    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)

    def level_display(self, obj):
        return obj.level
    level_display.short_description = "Level"

    def card_theme_display(self, obj):
        return obj.card_theme
    card_theme_display.short_description = "Card Theme"

app = apps.get_app_config("player")
for model_name, model in app.models.items():
    if model is User:
        continue
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
