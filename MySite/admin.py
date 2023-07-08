from django.contrib import admin

from MySite.models import CourseAllocation, Lecturer, Course, Department


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name',)


class LecturerAdmin(admin.ModelAdmin):
    list_display = ('user', 'last_name', 'first_name', 'email', 'staff_id', 'department')


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'unit', 'department')


class CourseAllocationAdmin(admin.ModelAdmin):
    list_display = ('course', 'lecturer')


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Lecturer, LecturerAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseAllocation, CourseAllocationAdmin)
