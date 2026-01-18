# resume/views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Profile, Skill, Certificate, Project

def home(request):
    """Главная страница с профилем и навыками"""
    profile = Profile.objects.filter(is_active=True).first()
    skills = Skill.objects.filter(profile=profile).order_by('category', 'order') if profile else []
    
    # Группируем навыки по категориям
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    context = {
        'profile': profile,  # ← профиль уже есть
        'skills_by_category': skills_by_category,
        'featured_certificates': Certificate.objects.filter(is_featured=True)[:3],
        'featured_projects': Project.objects.filter(is_featured=True)[:3],
    }
    return render(request, 'resume/home.html', context)

def profile_detail(request):
    """Детальная страница профиля"""
    profile = Profile.objects.filter(is_active=True).first()
    
    if not profile:
        # Если профиля нет, показываем сообщение
        return render(request, 'resume/no_profile.html')
    
    skills = Skill.objects.filter(profile=profile).order_by('category', 'order')
    
    # Группируем навыки по категориям
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    context = {
        'profile': profile,  # ← профиль уже есть
        'skills_by_category': skills_by_category,
    }
    return render(request, 'resume/profile_detail.html', context)

def certificate_list(request):
    """Список всех сертификатов"""
    profile = Profile.objects.filter(is_active=True).first()  # ← Добавить
    certificates = Certificate.objects.all().order_by('-issue_date')
    
    # Пагинация
    paginator = Paginator(certificates, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'profile': profile,  # ← Добавить профиль в контекст
        'page_obj': page_obj,
        'certificates': page_obj.object_list,
    }
    return render(request, 'resume/certificate_list.html', context)

def certificate_detail(request, pk):
    """Детальная страница сертификата"""
    profile = Profile.objects.filter(is_active=True).first()  # ← Добавить
    certificate = get_object_or_404(Certificate, pk=pk)
    context = {
        'profile': profile,  # ← Добавить профиль в контекст
        'certificate': certificate,
    }
    return render(request, 'resume/certificate_detail.html', context)

def project_list(request):
    """Список всех проектов"""
    profile = Profile.objects.filter(is_active=True).first()  # ← Добавить
    projects = Project.objects.all()
    
    # Фильтрация по технологии
    technology = request.GET.get('tech')
    if technology:
        projects = projects.filter(technologies__icontains=technology)
    
    # Пагинация
    paginator = Paginator(projects, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Получаем все уникальные технологии для фильтра
    all_technologies = set()
    for project in Project.objects.all():
        all_technologies.update(project.get_technologies_list())
    
    context = {
        'profile': profile,  # ← Добавить профиль в контекст
        'page_obj': page_obj,
        'projects': page_obj.object_list,
        'technologies': sorted(all_technologies),
        'current_tech': technology,
    }
    return render(request, 'resume/project_list.html', context)

def project_detail(request, pk):
    """Детальная страница проекта"""
    profile = Profile.objects.filter(is_active=True).first()  # ← Добавить
    project = get_object_or_404(Project, pk=pk)
    context = {
        'profile': profile,  # ← Добавить профиль в контекст
        'project': project,
    }
    return render(request, 'resume/project_detail.html', context)