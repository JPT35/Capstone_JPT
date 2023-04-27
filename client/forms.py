from django import forms 


from . models import Client, Comment, ClientFile

class AddClientForm(forms.ModelForm):  #using modelForm so django will create this for us based on information in the clas meta
    class Meta:
        model = Client
        fields = ('name','org_name','email','address','description', 'customer_type', 'monthly_order', 'sales_rep')  #which fields I want to show in the form

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class AddFileForm(forms.ModelForm):
    class Meta:
        model = ClientFile
        fields = ('file',)