from django.db import models
from users.models import User


class LearningMaterials(models.Model):
    all_level = 'All Level'
    grade_level = 'Grade Level'
    kinder_level = 'Kinder Level'
    category_choice  = (
        ( all_level, 'All Level'),
        ( grade_level, 'Grade Level'),
        ( kinder_level, 'Kind Level'),
    )
    original_title = models.CharField(max_length = 250)
    translated_title = models.CharField(max_length = 250)
    tags = models.CharField(max_length=300, null=True, blank=True)
    is_translated = models.BooleanField(default=False)
    source_language = models.CharField(max_length = 4, default='None')
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE
    )   
    author = models.CharField(
        max_length= 200, 
        null=True, 
        blank=True
    )
    translated_file = models.FileField(
        blank=True, null=True, 
        upload_to='translated/'
        )
    original_file = models.FileField(
        upload_to ='original/'
        )
    date_uploaded = models.DateField(
        auto_now=True, 
        blank=False
    )
    category = models.CharField(
        max_length = 12, 
        choices = category_choice,
        default = all_level,
    )
   
