from django import forms

from school.models import Grade, Subject, GradeObject, Klass, Subject


class GradesForm(forms.ModelForm):

    class Meta:
        model = Grade
        fields = ['grade', 'student', 'topic']

    # #modifying fomr so that teacher can only add grades from his subjects
    # def __init__(self, *args, **kwargs):
    #     teacher = kwargs.pop('teacher',None)
    #     super().__init__(*args, **kwargs)
    #     if teacher:
    #         self.fields['subject'].queryset = teacher.subject.all()

class AddSubjectToTeacherForm(forms.Form):


    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Subject',)

    def __init__(self, *args, **kwargs):
        teacher = kwargs.pop('teacher')
        super().__init__(*args, **kwargs)

        if teacher:
            self.fields['subject'].initial = Subject.objects.filter(teacher=teacher)


class AddGradeObjectForm(forms.ModelForm):
    class Meta:
        model = GradeObject
        fields = ['name', 'weight', 'subject']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if user.is_authenticated:
            self.fields['subject'].queryset = Subject.objects.filter(teacher=user)

class CreateClassForm(forms.ModelForm):
    class Meta:
        model = Klass
        fields = ['class_name']

class AddSubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'teacher', 'klass']

class EditStudentClassForm(forms.Form):
    classes = forms.ModelMultipleChoiceField(
        queryset=Klass.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='classes', )

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student')
        super().__init__(*args, **kwargs)
        self.fields['classes'].initial = Klass.objects.filter(student=student)

class SelectSubjectAndClassForm(forms.Form):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
    )
    Klass = forms.ModelChoiceField(
        queryset=Klass.objects.all(),
        required=False,
    )