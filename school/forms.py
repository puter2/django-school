from django import forms

from school.models import Grade, Student, Subject, Teacher


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

class AddSubjectToTeacherForm(forms.Form):
    teacher = forms.ModelChoiceField(
        queryset=Teacher.objects.all(),
        label="Teacher",)

    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Subject',)