import os
import errno
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import IntegrityError
from portal.forms import LearningMaterialsForm
from django.views.generic import TemplateView
from portal.mixin import ExtractMixin, DetectLanguageMixin, TranslationMixin
from portal.models import LearningMaterials
from django.contrib.auth.mixins import LoginRequiredMixin
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.core.files import File
from django.http import HttpResponseRedirect
from users.forms import LoginForm
from django.contrib.auth import login
from users.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class AddLearningView(LoginRequiredMixin, TemplateView, ExtractMixin, DetectLanguageMixin):
    template_name = "portal/contribute.html"
    login_url = '/login/'


    def get(self, request, *args, **kwargs):
        form = LearningMaterialsForm()
        return render(self.request, self.template_name, {'form': form})


    def post(self, request, *args, **kwargs):
        import pdb; pdb.set_trace();
        form = LearningMaterialsForm(self.request.POST, self.request.FILES)
     

        if form.is_valid():
            try:
                learning = form.save(commit= False)
                learning.user = self.request.user
                learning_path = self.request.FILES['original_file'].temporary_file_path()
                file_type = learning_path.split('.')[-1]
                file_type = file_type.lower()
                form.save()
                learningmaterial = LearningMaterials.objects.get(id=learning.id)
  
  
                if file_type == 'pdf':
                    content = self.extract_pdf(learningmaterial)
                    content = str(content)
                    source_lang = self.detect_lang(content)
                    if source_lang == 'ceb':
                        learningmaterial.source_language =  source_lang
                        learningmaterial.save()
                        return redirect(reverse('edit_learning', args=[learningmaterial.id]))
                    elif source_lang == 'en':
                        learningmaterial.source_language =  source_lang
                        learningmaterial.save()
                        return redirect(reverse('edit_learning', args=[learningmaterial.id]))
                    elif source_lang == 'ConnectionError':
                        learningmaterial.delete()
                        context = {
                            'form': form,
                            'error_messages': 'Something went wrong please try again.'
                        }
                        return render(self.request, self.template_name, context)
                    else: 
                        learningmaterial.delete()
                        context = {
                            'form': form,
                            'error_messages': 'Source Language must be in Cebuano or English.'
                        }
                        return render(self.request, self.template_name, context)

                elif file_type == 'docx':
                    content = self.extract_docx(learningmaterial)
                    content = str(content)
                    source_lang = self.detect_lang(content)
                    if source_lang == 'ceb':
                        learningmaterial.source_language =  source_lang
                        learningmaterial.save()
                        return redirect(reverse('edit_learning', args=[learningmaterial.id]))
                    elif source_lang == 'en':
                        learningmaterial.source_language =  source_lang
                        learningmaterial.save()
                        return redirect(reverse('edit_learning', args=[learningmaterial.id]))
                    elif source_lang == 'ConnectionError':
                        learningmaterial.delete()
                        context = {
                            'form': form,
                            'error_messages': 'Something went wrong please try again.'
                        }
                        return render(self.request, self.template_name, context)
                    else: 
                        learningmaterial.delete()
                        context = {
                        'form': form,
                         'error_messages': 'Source Language must be in Cebuano or English.'
                        }
                        return render(self.request, self.template_name, context)
                else: 
                    learningmaterial.delete()
                    context = {
                        'form': form,
                        'error_messages': 'Learning materials must be .docx, or .pdf'
                    }
                    return render(self.request, self.template_name, context)

            except IntegrityError as e:
                context ={
                    'error_messages' : 'Something went wrong please try again.',
                }
                return render(self.request, self.template_name, context)
        return render(self.request, self.template_name, {'form': form, 'error_messages': 'Something went wrong.'}) 


class EditLearningMaterialView(LoginRequiredMixin, TemplateView, ExtractMixin, TranslationMixin):
    template_name = 'portal/edit-material.html'
    login_url = '/login/'
    

    def get(self, request, *args, **kwargs):
        learningmaterial = LearningMaterials.objects.get(id=kwargs.get('id'))
        learning_language = learningmaterial.source_language

        if learning_language == 'en':
            file_type = learningmaterial.original_file.name.split('.')[-1]
            file_type = file_type.lower()
            if file_type == 'pdf':
                original_content = self.extract_pdf(learningmaterial)
                translated_content = self.translate(original_content)
                if translated_content == 'ConnectionError':
                    context = {
                        'error_messages': 'Something went wrong please try again.'
                    }
                    return render(self.request, self.template_name, context)
                else:
                    context = {
                        'translated_content': translated_content,
                        'learning': learningmaterial,
                        'content': original_content,
                    }
                    return render(self.request, self.template_name, context)
            elif file_type == 'docx':
                original_content = self.extract_docx(learningmaterial)
                translated_content = self.translate(original_content)
                if translated_content == 'ConnectionError':
                    context = {
                        'error_messages': 'Something went wrong please try again.'
                    }
                    return render(self.request, self.template_name, context)
                else:
                    context = {
                        'translated_content': translated_content,
                        'learning': learningmaterial,
                        'content': original_content,
                    }
                    return render(self.request, self.template_name, context)
            else:
                context = {
                    'form': form,
                    'error_messages': 'Learning materials must be .docx, or .pdf'
                }
                return render(self.request, self.template_name, context)
        elif learning_language == 'ceb':
            file_type =learningmaterial.original_file.name.split('.')[-1]
            file_type = file_type.lower()
            if file_type == 'pdf':
                translated_content = self.extract_pdf(learningmaterial)
                if translated_content == 'ConnectionError':
                    context = {
                            'form': form,
                            'error_messages': 'Something went wrong please try again.'
                        }
                    return render(self.request, self.template_name, context)
                else:
                    context = {
                        'translated_content': translated_content,
                        'learning': learningmaterial,
                        'content':'Source Language is already in Cebuano.',
                    }
                    return render(self.request, self.template_name, context)
            elif file_type == 'docx':
                translated_content = self.extract_docx(learningmaterial)
                if translated_content == 'ConnectionError':
                    context = {
                        'form': form,
                        'error_messages': 'Something went wrong please try again.'
                    }
                    return render(self.request, self.template_name, context)
                else:
                    context = {
                        'translated_content': translated_content,
                        'learning': learningmaterial,
                        'content':'Source Language is already in Cebuano.', 
                    }
                    return render(self.request, self.template_name, context)
            else:
                context = {
                    'form': form,
                    'error_messages': 'Learning materials must be .docx, or .pdf'
                }
                return render(self.request, self.template_name, context)
        else:
            return render(self.request, self.template_name, {'error_messages': 'Something went wrong.'}) 

    def post(self, *args, **kwargs):
        learning = LearningMaterials.objects.get(id=kwargs.get('id'))
        contribution_instance = self.request.POST['contribution']
        filename = '{}_translated.pdf'.format(learning.title) 
        file_path ='media_cdn/generated/{}'.format(filename)
       
        # text = contribution_instance.encode('utf-8')
        
        for word in contribution_instance:
            converted_text = contribution_instance.replace('  ', '\x0a\x0a').replace('\r\n', '<br />')

        
        #response = HttpResponse(content_type='application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

        doc = SimpleDocTemplate(file_path, pagesize=letter,
                                rightMargin = 50, leftMargin = 50,
                                topMargin = 50, bottomMargin = 50
            )

        Story = []
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
        ptext = '<font size=12>' + converted_text + '</font>'
        Story.append(Paragraph(ptext, styles["Justify"]))
        doc.build(Story)
        
        f = open(file_path,'rb')
        learning.translated_file.save(filename, File(f))
        learning.is_translated = True
        learning.is_cebuano = True
        learning.save()
        
        return redirect('contribution', learning.id)
  


class resutlView(LoginRequiredMixin, TemplateView):
    template_name = 'portal/result.html'
    login_url = '/login/'

    def get(self, request, *args, **kwargs):
        learning_table = LearningMaterials.objects.get(id=kwargs.get('id'), is_translated=True)
        return render(self.request, self.template_name, {'learning_table': learning_table, 'tags': learning_table.tags.split(',')})


class indexView(TemplateView):
    template_name = 'portal/index.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            materials = LearningMaterials.objects.filter(is_translated=True).order_by('-date_uploaded')
            
            page = self.request.GET.get('page')
            paginator = Paginator(materials, 6)
            
            try:
                items = paginator.page(page)
            except PageNotAnInteger:
                items = paginator.page(1)
            except EmptyPage:
                items = paginator.page(paginator.num_pages)


            return render(self.request, self.template_name,{'items': items})
        else:
            form = LoginForm()
            return render(self.request, self.template_name, {'form':form})


    def post(self, *args, **kwargs):
        form = LoginForm(self.request.POST)
        if self.request.user.is_authenticated:
            search_input = self.request.POST['search_input']
            search_result = LearningMaterials.objects.filter(title__contains=search_input,is_translated=True)
            return render(self.request, self.template_name, {'materials': search_result})
        else:
            if form.is_valid():
                login(self.request,form.user_cache)
            # return HttpResponseRedirect(reverse('index'))
            return render(self.request, self.template_name, {'form':form})

class profileView(TemplateView, LoginRequiredMixin):
    template_name = 'account/profile.html'


    def get(self, *args, **kwargs):
        materials = LearningMaterials.objects.filter(is_translated=True, user=self.request.user).order_by('-date_uploaded')
        user = User.objects.get(id=self.request.user.id)

        page = self.request.GET.get('page')
        paginator = Paginator(materials, 3)

        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)

        return render(self.request, self.template_name,{'materials': materials, 'user':user, 'items': items})


    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            search_input = self.request.POST['search_input']
            user = User.objects.get(id=self.request.user.id)
            search_result = LearningMaterials.objects.filter(title__contains=search_input,is_translated=True)
            return render(self.request, self.template_name, {'materials': search_result, 'user':user})