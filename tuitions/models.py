from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tution(models.Model):
    classes = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100, unique = True, blank=True, null=True)

    def __str__(self):
        return self.classes


class TutionDetails(models.Model):
    tuition = models.ForeignKey(Tution, on_delete = models.CASCADE, blank=True, null=True)
    teacher_name = models.CharField(max_length = 50)
    subject_name = models.CharField(max_length = 50)
    location = models.CharField(max_length = 200)
    tuition_days = models.CharField(max_length = 50,blank=True, null=True)
    salary = models.CharField(max_length = 50)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to = 'tuition_app/media/uploads/', blank=True, null=True)

    def __str__(self) :
        return f"Subject name: {self.subject_name}, Tuition : {self.tuition.classes}"



class TuitionApplication(models.Model):
    APPLICANT_STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    tuition = models.ForeignKey(TutionDetails, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=APPLICANT_STATUS, default='pending')

    def __str__(self):
        return f"{self.applicant.username} - {self.status}"


class ContactUs(models.Model):
    fullname = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    phone_no = models.CharField(max_length=13)
    comments = models.TextField()

    def __str__(self):
        return self.fullname




class Comment(models.Model):
    car = models.ForeignKey(TutionDetails, on_delete = models.CASCADE, related_name = 'comments')
    name = models.CharField(max_length = 30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"Comment by {self.name}"