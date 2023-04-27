import csv

from django.contrib import messages 
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View

from .forms import AddCommentForm, AddFileForm
from .models import Lead

from client.models import Client, Comment as ClientComment
from team.models import Team

@login_required
def leads_export(request):
    leads = Lead.objects.filter(created_by=request.user)

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attatchment; filename="leads.csv"'}
    )

    writer = csv.writer(response)
    writer.writerow(['Org Name','Contact', 'email','Phone Number','Address', 'priority', 'status', 'Created at', 'Created by'])
    
    for lead in leads:   #looping through all the clients and adding them to the file:
        writer.writerow([lead.org_name, lead.name, lead.email, lead.phone_number, lead.address, lead.priority, lead.status, lead.created_at, lead.created_by])

    return response

class LeadListView(LoginRequiredMixin, ListView):
    model = Lead

    def get_queryset(self):
        queryset = super(LeadListView, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user, converted_to_client=False)

        return queryset
#getting the number of new leads and high priority leads for active team
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        active_team = self.request.user.userprofile.active_team
        context['uncontacted_leads_count'] = Lead.objects.filter(team=active_team, status='new').count()
        context['high_priority_leads_count'] = Lead.objects.filter(team=active_team, priority='high').count()
        
        return context

class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddCommentForm()
        context['fileform'] = AddFileForm()

        return context

    def get_queryset(self):
        queryset = super(LeadDetailView, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))
        return queryset

class LeadDeleteView(LoginRequiredMixin, DeleteView):
    model = Lead
    success_url = reverse_lazy('leads:list')

    def get_queryset(self):
        queryset = super(LeadDeleteView, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

        return queryset

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    fields = ('name','org_name','phone_number', 'email', 'address', 'description', 'priority', 'status',)
    success_url = reverse_lazy('leads:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit lead'

        return context

    def get_queryset(self):
        queryset = super(LeadUpdateView, self).get_queryset()
        queryset = queryset.filter(created_by=self.request.user, pk=self.kwargs.get('pk'))

        return queryset

   

class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    fields = ('name','org_name','phone_number','email','address', 'description', 'priority', 'status',)
    success_url = reverse_lazy('leads:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = self.request.user.userprofile.active_team
        context['team'] = team
        context['title'] = 'Add lead'

        return context


    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.team = self.request.user.userprofile.active_team
        self.object.save()

        return redirect(self.get_success_url())

class AddFileView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
    
            file = form.save(commit=False)
            file.team = self.request.user.userprofile.active_team
            file.lead_id = pk
            file.created_by = request.user
            file.save()

            return redirect('leads:detail', pk=pk)


class AddCommentView(View):
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')

        form = AddCommentForm(request.POST)

        if form.is_valid():
       
            comment = form.save(commit=False)
            comment.team = self.request.user.userprofile.active_team
            comment.created_by = request.user
            comment.lead_id = pk 
            comment.save()

        return redirect('leads:detail', pk=pk)

class ConvertToClientView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')

        lead = get_object_or_404(Lead, created_by=request.user, pk=pk)
        team = self.request.user.userprofile.active_team

        client = Client.objects.create(
            name=lead.name,
            email=lead.email,
            description=lead.description,
            created_by=request.user,
            team = team,
        )

        lead.converted_to_client = True
        lead.save()

        team.converted_leads += 1
        team.save()

        #converting lead commments to client comments

        comments = lead.comments.all()

        for comment in comments:
            ClientComment.objects.create(
                client = client,
                content = comment.content,
                created_by = comment.created_by,
                team = team

            )

        #show message and redirect

        messages.success(request, 'Lead has been converted to client.')

        return redirect('leads:list')
