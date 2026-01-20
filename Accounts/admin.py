# Accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.forms import TextInput, Textarea

from .models import User, StudentUser, TeacherUser, LibrarianUser
from profiles.models import StudentProfile, TeacherProfile, AdminProfile


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = "Profil de l'étudiant"
    fk_name = "user"


class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    can_delete = False
    verbose_name_plural = "Profil de l'enseignant"
    fk_name = "user"


class AdminProfileInline(admin.StackedInline):
    model = AdminProfile
    can_delete = False
    verbose_name_plural = "Profil d'administrateur"
    fk_name = "user"


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("email", "first_name", "last_name", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    actions = ["make_student", "make_teacher", "make_librarian", "set_staff", "unset_staff"]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Informations personnelles", {"fields": ("first_name", "last_name", "phone")}),
        ("Rôle", {"fields": ("role",)}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser")}),
        ("Dates importantes", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role", "is_staff", "is_active"),
        }),
    )

    search_fields = ("email",)
    ordering = ("email",)

    def get_inlines(self, request, obj):
        if not obj:
            return []
        if obj.role == User.STUDENT:
            return [StudentProfileInline]
        if obj.role == User.TEACHER:
            return [TeacherProfileInline]
        if obj.role == User.ADMIN:
            return [AdminProfileInline]
        return []

    def make_student(self, request, queryset):
        updated = queryset.update(role=User.STUDENT)
        self.message_user(request, f"{updated} compte(s) mis à jour en 'Étudiant'.")
    make_student.short_description = "Définir le rôle sur Étudiant"

    def make_teacher(self, request, queryset):
        updated = queryset.update(role=User.TEACHER)
        self.message_user(request, f"{updated} compte(s) mis à jour en 'Enseignant'.")
    make_teacher.short_description = "Définir le rôle sur Enseignant"

    def make_librarian(self, request, queryset):
        # If LIBRARIAN constant exists on model
        if hasattr(User, 'LIBRARIAN'):
            updated = queryset.update(role=User.LIBRARIAN)
            self.message_user(request, f"{updated} compte(s) mis à jour en 'Bibliothécaire'.")
        else:
            self.message_user(request, "Le rôle 'Bibliothécaire' n'existe pas sur le modèle.")
    make_librarian.short_description = "Définir le rôle sur Bibliothécaire"

    def set_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(request, f"{updated} compte(s) définis comme staff.")
    set_staff.short_description = "Attribuer is_staff=True"

    def unset_staff(self, request, queryset):
        updated = queryset.update(is_staff=False)
        self.message_user(request, f"{updated} compte(s) retirés du staff.")
    unset_staff.short_description = "Retirer is_staff"


admin.site.register(User, UserAdmin)


class RoleFilteredAdmin(admin.ModelAdmin):
    """Base admin to filter users by role and attach the correct inline and save behavior."""
    list_display = ("email", "first_name", "last_name", "role", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if hasattr(self, 'role_value'):
            return qs.filter(role=self.role_value)
        return qs

    def save_model(self, request, obj, form, change):
        # Ensure created/edited users keep the appropriate role
        if hasattr(self, 'role_value'):
            obj.role = self.role_value
        super().save_model(request, obj, form, change)


class StudentUserAdmin(RoleFilteredAdmin):
    role_value = User.STUDENT
    inlines = [StudentProfileInline]


class TeacherUserAdmin(RoleFilteredAdmin):
    role_value = User.TEACHER
    inlines = [TeacherProfileInline]


class LibrarianUserAdmin(RoleFilteredAdmin):
    role_value = User.LIBRARIAN if hasattr(User, 'LIBRARIAN') else 'librarian'
    inlines = [AdminProfileInline]


admin.site.register(StudentUser, StudentUserAdmin)
admin.site.register(TeacherUser, TeacherUserAdmin)
admin.site.register(LibrarianUser, LibrarianUserAdmin)
