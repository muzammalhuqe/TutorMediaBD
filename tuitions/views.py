from django.views.generic import DetailView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import TutionDetails, TuitionApplication
from django.shortcuts import render, get_object_or_404
from .forms import CommentForm, ContactForm
from .models import Comment, ContactUs
from . import forms
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string


def send_apply_email(user, subject, template):
        message = render_to_string(template, {
            'user' : user,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()



class DetailTuitionView(DetailView):
    model = TutionDetails
    template_name = 'tuition_details.html'
    pk_url_kwarg = 'id'
    context_object_name = 'tuition_details'

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data = self.request.POST)
        car  = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit = False)
            new_comment.car = car
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        car = self.object
        comments = car.comments.all()

        
        comment_form = forms.CommentForm()

        context ['comments'] = comments
        context ['comment_form'] = comment_form
        return context
    


class ApplyTutionView(LoginRequiredMixin, View):
    def get(self, request, id):
        tuition_detail = get_object_or_404(TutionDetails, pk=id)

        if tuition_detail.is_available:
            # Check if the user has already applied for this tuition
            existing_application = TuitionApplication.objects.filter(
                applicant=request.user,
                tuition=tuition_detail,
            ).first()

            if not existing_application:
                # Create a new application
                application = TuitionApplication(
                    applicant=request.user,
                    tuition=tuition_detail,
                    status='pending',
                )
                application.save()
                send_apply_email(self.request.user, "Apply Message", "apply_email.html")

                messages.success(request, 'Application submitted successfully.')
            else:
                messages.warning(request, 'You have already applied for this tuition.')

        else:
            messages.warning(request, 'This tuition is not available.')

        return redirect('apply_tuition')


def apply_tuition(request):
    return render(request, 'applyed_tuition.html')


class Review(DetailView):
    model = TutionDetails
    template_name = "review_form.html"
    pk_url_kwarg = 'id'
    context_object_name = 'review'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data = self.request.POST)
        car  = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit = False)
            new_comment.car = car
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        car = self.object
        comments = car.comments.all()
        comment_form = CommentForm()
        context ['comments'] = comments
        context ['comment_form'] = comment_form
        return context



class ContactUsView(View):
    template_name = 'contact_page.html'
    success_url = reverse_lazy('contact_us')

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_us')
        
        return render(request, self.template_name, {'form': form})
    




def view_comments(request, book_id):
    book = get_object_or_404(TutionDetails, pk=book_id)
    comments = Comment.objects.filter(car=book)

    if request.method == 'POST' and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.car = book
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'comments.html', {'comment_form': comment_form, 'comments': comments, 'user': request.user})

