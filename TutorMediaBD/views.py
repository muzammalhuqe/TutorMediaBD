from django.shortcuts import render
from tuitions.models import Tution
from tuitions.models import TutionDetails

def home(request, book_slug = None):

    data = TutionDetails.objects.all()
    if book_slug is not None:
        cat = Tution.objects.get(slug = book_slug)
        data = TutionDetails.objects.filter(tuition = cat)
    categories = Tution.objects.all()
    return render(request, 'home.html', {'data' : data, 'categories' : categories})