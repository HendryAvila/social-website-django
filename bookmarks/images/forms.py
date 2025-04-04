from django import forms
from  .models import Image

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        
        widget = {
            'url': forms.HiddenInput,
        }
        
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extentions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.',1)[1].lower()
        if extension not in valid_extentions:
            raise forms.ValidationError('La URL proporcionada no coincide con una imagen valida.')