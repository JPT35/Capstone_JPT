from django import forms 

from . models import Lead, Comment, LeadFile

INPUT_CLASS = 'w-full py-4 px-6 rounded-xl bg-gray-100'

class AddLeadForm(forms.ModelForm):  #using modelForm so django will create this for us based on information in the clas meta
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Lead Name',
        'class': INPUT_CLASS}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder':'Email',
        'class': INPUT_CLASS}))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'class': INPUT_CLASS}))

    class Meta:
        model = Lead
        fields = ('name','email','org_name','phone_number','address', 'description', 'priority', 'status',)  #whihc fields I want to show in the form

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class AddFileForm(forms.ModelForm):
    class Meta:
        model = LeadFile
        fields = ('file',)