from django.urls import path
from portal.views import (
    AddLearningView,
    EditLearningMaterialView,
    resutlView,
    indexView,
    profileView,
    )
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', indexView.as_view(), name='index'),
    path('add/', AddLearningView.as_view(), name='add_learning'),
    path('edit/<int:id>/', EditLearningMaterialView.as_view(), name='edit_learning'),
    path('result/<int:id>/', resutlView.as_view(), name='contribution'),
    path('<int:id>/', profileView.as_view(), name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)