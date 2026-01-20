# profiles/admin.py

from django.contrib import admin
from .models import StudentProfile, TeacherProfile, AdminProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "student_id", "level", "group")
    search_fields = ("user__email", "student_id")


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "specialization", "rank", "office")
    search_fields = ("user__email", "specialization")


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "position", "department")
    search_fields = ("user__email", "position")
