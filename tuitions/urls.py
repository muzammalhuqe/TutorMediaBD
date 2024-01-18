from django.urls import path, include
from . views import DetailTuitionView,ApplyTutionView, view_comments, Review
urlpatterns = [
    path('tuition/<int:id>', DetailTuitionView.as_view(), name='tuition_details'),
    path('tuition_request/<int:id>/', ApplyTutionView.as_view(), name='tuition_request'),
    path('view/<int:id>', view_comments, name='view_details'),
    path('review/<int:id>', Review.as_view(), name='review'),
]