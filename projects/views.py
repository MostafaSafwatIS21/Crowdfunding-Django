from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.utils import timezone
from .models import Project, Fund
from .forms import ProjectForm, FundForm

def home_view(request):
    recent_projects = Project.objects.all().order_by('-created_at')[:6]
    return render(request, 'projects/home.html', {'recent_projects': recent_projects})

def project_list_view(request):
    projects = Project.objects.all().order_by('-created_at')
    
    # Handle search by date
    search_date = request.GET.get('date')
    if search_date:
        # A simple filter to find projects active on the specific date
        projects = projects.filter(
            start_time__date__lte=search_date,
            end_time__date__gte=search_date
        )
        
    context = {
        'projects': projects,
        'search_date': search_date,
    }
    return render(request, 'projects/project_list.html', context)

@login_required
def project_create_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, 'Campaign created successfully!')
            return redirect('projects:list')
    else:
        form = ProjectForm()
    
    return render(request, 'projects/project_form.html', {'form': form, 'title': 'Create Campaign'})

@login_required
def project_edit_view(request, id):
    project = get_object_or_404(Project, id=id)
    
    # Authorization check
    if project.owner != request.user:
        messages.error(request, 'You do not have permission to edit this project.')
        return redirect('projects:list')
        
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Campaign updated successfully!')
            return redirect('projects:list')
    else:
        form = ProjectForm(instance=project)
        
    return render(request, 'projects/project_form.html', {'form': form, 'project': project, 'title': 'Edit Campaign'})

@login_required
def project_delete_view(request, id):
    project = get_object_or_404(Project, id=id)
    
    # Authorization check
    if project.owner != request.user:
        messages.error(request, 'You do not have permission to delete this project.')
        return redirect('projects:list')
        
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Campaign deleted successfully!')
        return redirect('projects:list')
        
    # GET request could render a confirmation page, but typically delete is POST only via a button.
    # However, to be safe, if a GET request reaches here, redirect to list.
    return redirect('projects:list')

def project_detail_view(request, id):
    project = get_object_or_404(Project, id=id)
    total_raised = project.funds.aggregate(total=Sum('amount'))['total'] or 0
    
    progress_percentage = 0
    if project.total_target > 0:
        progress_percentage = min(int((total_raised / project.total_target) * 100), 100)

    form = FundForm()
    
    return render(request, 'projects/project_detail.html', {
        'project': project,
        'total_raised': total_raised,
        'progress_percentage': progress_percentage,
        'form': form
    })

@login_required
def fund_project(request, id):
    project = get_object_or_404(Project, id=id)
    
    if request.method == 'POST':
        if project.owner == request.user:
            messages.error(request, "You cannot fund your own campaign.")
            return redirect('projects:detail', id=project.id)
            
        if timezone.now() > project.end_time:
            messages.error(request, "This campaign has already ended.")
            return redirect('projects:detail', id=project.id)
            
        form = FundForm(request.POST)
        if form.is_valid():
            fund = form.save(commit=False)
            if fund.amount <= 0:
                messages.error(request, "Funding amount must be positive.")
            else:
                fund.backer = request.user
                fund.project = project
                fund.save()
                messages.success(request, f"Thank you for funding {fund.amount} EGP!")
            return redirect('projects:detail', id=project.id)
        else:
            messages.error(request, "Invalid funding amount.")
            return redirect('projects:detail', id=project.id)
            
    return redirect('projects:detail', id=project.id)
