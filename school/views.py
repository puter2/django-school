from django.shortcuts import render
from django.views import View

from school.models import Grade


# Create your views here.
class GradesView(View):

    def get(self, request):
        grades = Grade.objects.all()
        return render(request, 'show_grades.html', {'grades': grades})