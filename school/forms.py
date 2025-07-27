from django import forms

from school.models import Grade, Student, Subject


class GradesForm(forms.ModelForm):

    class Meta:
        model = Grade
        fields = ['grade', 'student', 'subject']

    #modifying fomr so that teacher can only add grades from his subjects
    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher',None)
        super().__init__(*args, **kwargs)
        if teacher:
            self.fields['subject'].queryset = teacher.subject.all()

class AddSubjectForm(forms.ModelForm):

    class Meta:
        model = Subject
        fields = ['subject']