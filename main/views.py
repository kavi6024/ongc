from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CompanyRegistrationForm, RequestForm, QueryForm
from .models import Company, Request, Query
from django.http import HttpResponseForbidden

def register(request):
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Company.objects.create(user=user)
            messages.success(request, 'Registration successful. Please wait for admin approval.')
            return redirect('login')
    else:
        form = CompanyRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def dashboard(request):
    if request.user.is_admin:
        companies = Company.objects.all()
        requests = Request.objects.all()
        queries = Query.objects.all()
        return render(request, 'main/admin_dashboard.html', {
            'companies': companies,
            'requests': requests,
            'queries': queries
        })
    elif request.user.is_company:
        company = request.user.company
        if not company.approved:
            return render(request, 'main/pending_approval.html')
        
        requests = Request.objects.filter(company=company)
        queries = Query.objects.filter(company=company)
        return render(request, 'main/company_dashboard.html', {
            'requests': requests,
            'queries': queries
        })
    return redirect('login')

@login_required
def create_request(request):
    if not request.user.is_company or not request.user.company.approved:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request = form.save(commit=False)
            new_request.company = request.user.company
            new_request.save()
            messages.success(request, 'Request created successfully.')
            return redirect('dashboard')
    else:
        form = RequestForm()
    return render(request, 'main/create_request.html', {'form': form})

@login_required
def create_query(request):
    if not request.user.is_company or not request.user.company.approved:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = QueryForm(request.POST, request.FILES)
        if form.is_valid():
            new_query = form.save(commit=False)
            new_query.company = request.user.company
            new_query.save()
            messages.success(request, 'Query created successfully.')
            return redirect('dashboard')
    else:
        form = QueryForm()
    return render(request, 'main/create_query.html', {'form': form})

@login_required
def approve_company(request, company_id):
    if not request.user.is_admin:
        return HttpResponseForbidden()
    
    company = get_object_or_404(Company, id=company_id)
    company.approved = True
    company.save()
    messages.success(request, f'Company {company.user.email} has been approved.')
    return redirect('dashboard')

@login_required
def complete_request(request, request_id):
    if not request.user.is_admin:
        return HttpResponseForbidden()
    
    req = get_object_or_404(Request, id=request_id)
    req.request_done = True
    req.save()
    messages.success(request, f'Request {req.id} has been marked as complete.')
    return redirect('dashboard')

@login_required
def resolve_query(request, query_id):
    if not request.user.is_admin:
        return HttpResponseForbidden()
    
    query = get_object_or_404(Query, id=query_id)
    query.solved = True
    query.save()
    messages.success(request, f'Query {query.id} has been marked as resolved.')
    return redirect('dashboard')
