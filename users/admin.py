from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "groups_list")  # <-- добавляем наше поле
    search_fields = ("email", "phone")

    @admin.display(description="Группы")  # отображение поля группы
    def groups_list(self, obj):
        if obj.groups.exists():
            return ", ".join(group.name for group in obj.groups.all())
        return "-"
