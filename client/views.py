import csv
import matplotlib.pyplot as plt

from django.contrib import messages 

from django.db.models import Sum

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import AddClientForm, AddCommentForm, AddFileForm
from .models import Client

from team.models import Team

@login_required
def clients_export(request):
    clients = Client.objects.filter(created_by=request.user)  #user created clients

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attatchment; filename="clients.csv"'}
    )

    writer = csv.writer(response)
    writer.writerow(['Org Name','Contact', 'Address', 'Created at', 'Created by', 'Customer Type', 'Monthly Order', 'Total Order Value', 'Sales Rep'])
    
    for client in clients:   #looping through all the clients and adding them to the file:
        writer.writerow([client.org_name ,client.name, client.address, client.created_at, client.created_by, client.customer_type, client.monthly_order, client.total_order_value, client.sales_rep])

    return response

@login_required
def clients_list(request):
    clients = Client.objects.filter(created_by=request.user) #user create clients
    total_order_value = clients.aggregate(Sum('total_order_value'))['total_order_value__sum'] or 0
    total_monthly_order = sum(client.monthly_order for client in clients)

    return render(request, 'client/clients_list.html',{
        'clients': clients,
        'total_monthly_order':total_monthly_order,
        'total_order_value': total_order_value
    })

@login_required
def clients_add_file(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            file = form.save(commit=False)
            file.team = request.user.userprofile.active_team
            file.created_by = request.user
            file.client_id = pk 
            file.save()

            return redirect('clients:detail', pk=pk)
    return redirect('clients:detail', pk=pk)

@login_required
def clients_detail(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    if request.method == 'POST':
        form = AddCommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.team = request.user.userprofile.active_team
            comment.created_by = request.user
            comment.client = client
            comment.save()

            return redirect('clients:detail', pk=pk)
    else:
        form = AddCommentForm()

    return render(request, 'client/clients_detail.html', {
        'client': client,
        'form':form,
        'fileform': AddFileForm(),
    })

@login_required
def clients_add(request):
    team = request.user.userprofile.active_team

    if request.method == 'POST':
        form = AddClientForm(request.POST)

        if form.is_valid():
            client = form.save(commit=False)  #set commit=False to prevent saving in the database
            client.created_by = request.user
            client.team = team
            client.save()

            messages.success(request, 'New client created')

            return redirect('clients:list')
    else:  #If not a post request, return an empty form
        form = AddClientForm()

    return render(request, 'client/clients_add.html', {
        'form' : form,
        'team': team,
    })

@login_required
def clients_delete(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)
    client.delete()

    messages.success(request, 'Client has been deleted.')

    return redirect('clients:list')   # redirect user back to the clients_list page

@login_required
def clients_edit(request, pk):
    client = get_object_or_404(Client, created_by=request.user, pk=pk)

    if request.method == 'POST':  # check if user has submitted
        form = AddClientForm(request.POST, instance=client)  # if user has submitted, create new form  instance=client is passing information for update

        if form.is_valid():
            form.save()

            messages.success(request, 'Changes to client saved') 

            return redirect('clients:list') 
    else:
        form = AddClientForm(instance=client)
    
    return render(request, 'client/clients_edit.html', {
        'form' : form 
    })

@login_required
def clients_report(request):
    data = Client.objects.all()
    context = {
        'data':data,
    }

    return render(request, 'client/clients_report.html', context)