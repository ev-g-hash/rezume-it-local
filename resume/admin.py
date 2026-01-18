# resume/admin.py
from django.contrib import admin
from .models import Profile, Skill, Certificate, Project, ProjectImage

class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1
    ordering = ('order',)

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    ordering = ('order',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'position', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('first_name', 'last_name', 'position')
    inlines = [SkillInline]

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'issue_date', 'is_featured')
    list_filter = ('is_featured', 'organization', 'issue_date')
    search_fields = ('title', 'organization')
    list_editable = ('is_featured',)
    ordering = ('-issue_date',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('title', 'description', 'technologies')
    inlines = [ProjectImageInline]
    prepopulated_fields = {'short_description': ('description',)}