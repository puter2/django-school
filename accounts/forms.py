from django import forms
from django.contrib.auth.models import User
from accounts.models import Role
from school.models import Teacher, Subject


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        data = super().clean()
        if data['password1'] != data['password2']:
            raise forms.ValidationError("The two password fields didn't match.")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name']

class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role']

class EditTeacherForm(forms.ModelForm):
    subject = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Subject',)

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        user = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if user.role.role != 'teacher':
            self.fields.pop('subject', None)
        else:
            try:
                teacher = Teacher.objects.get(user=user)
                self.fields['subject'].initial = teacher.subject.all()
            except Teacher.DoesNotExist:
                self.fields['subject'].initial = []
