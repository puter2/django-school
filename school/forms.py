from django import forms

from school.models import Grade, Student, Subject


class GradesForm(forms.ModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), label="Select Student")

    class Meta:
        model = Grade
        fields = ['grade', 'student']

class AddSubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = ['subject']