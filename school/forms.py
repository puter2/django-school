from django import forms

from school.models import Grade, Student


class GradesForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), label="Select Student")

    class Meta:
        model = Grade
        fields = ['grade', 'student']
