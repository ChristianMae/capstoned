from django import forms
from portal.models import LearningMaterials


class LearningMaterialsForm(forms.ModelForm):
    tags = forms.CharField(label=("Tags"), widget=forms.TextInput(attrs={'data-role':('tagsinput')}))
    
    class Meta:
        model = LearningMaterials
        fields = ['title','author', 'tags', 'category', 'original_file']

