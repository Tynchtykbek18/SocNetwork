from django.contrib import admin

from apps.timetable.models import Course, Department, Lesson


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id", "department", "course")
    list_display_links = ("id", "department", "course")
    list_filter = ("department",)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ("id", "course", "day", "name")
    list_display_links = ("id", "course", "day", "name")
    search_fields = ("day", "name")
    list_filter = ("day",)
