from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserCode


@admin.register(User)
class UserAdminView(UserAdmin):
    ordering = ("-date_joined",)
    list_display = (
        "email",
        "username",
        "is_active",
        "is_staff",
        "is_verify"
    )
    list_display_links = ("email",)

    # fieldsets = (
    #     (
    #         (
    #             "Additional",
    #             {
    #                 "fields": (
    #                     "is_verify",
    #                 ),
    #             },
    #         ),
    #     )
    # )


@admin.register(UserCode)
class UserCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "code")
    list_display_links = ("user", )
