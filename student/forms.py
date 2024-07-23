from django import forms

from .models import (
    Student,
    StudentClass,
    Year,
    Group, Subject, Exam, ClassNumber, Position, Proximity
)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name',
            'last_name',
            'gender',
            'shift',
            'note',
            'student_class',
            'group',
            'section',
            'score',
            'registration_status',
            'class_number',
            'subject',
            'exam',
            'school',
            'city',
            'address',
            'father_first_name',
            'father_last_name',
            'father_workplace',
            'father_position',
            'father_phone_1',
            'father_phone_2',
            'mather_first_name',
            'mather_last_name',
            'mather_workplace',
            'mather_position',
            'mather_phone_1',
            'mather_phone_2',
            'responsible_first_name',
            'responsible_last_name',
            'responsible_sur_name',
            'responsible_address',
            'responsible_passport_number',
            'responsible_fin',
            'responsible_workplace',
            'responsible_position',
            'proximity',
            'responsible_phone_1',
            'responsible_phone_2',
            'concession_1',
            'concession_1_price',
            'concession_2',
            'concession_2_price',
            'concession_3',
            'concession_3_price',
            'concession_1_percent',
            'concession_2_percent',
            'concession_3_percent',
            'total_concession',
            'annual_fee',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'shift': forms.Select(attrs={'class': 'form-control'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'student_class': forms.Select(attrs={'class': 'form-control', 'id': 'id_student_class'}),
            'group': forms.Select(attrs={'class': 'form-control', 'id': 'id_group'}),
            'registration_status': forms.Select(attrs={'class': 'form-control'}),
            'section': forms.Select(attrs={'class': 'form-control'}),
            'score': forms.NumberInput(attrs={'class': 'form-control'}),
            'class_number': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.SelectMultiple(
                attrs={'class': 'form-control', 'multiple': 'multiple', 'id': 'id_subject'}),
            'exam': forms.SelectMultiple(attrs={'class': 'form-control', 'multiple': 'multiple', 'id': 'id_exam'}),
            'school': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),

            'father_first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_workplace': forms.TextInput(attrs={'class': 'form-control'}),
            'father_position': forms.Select(attrs={'class': 'form-control'}),
            'father_phone_1': forms.TextInput(attrs={'class': 'form-control phone-input', 'type': 'tel', 'maxlength': '16', 'placeholder': '(055) 555 55 55'}),
            'father_phone_2': forms.TextInput(attrs={'class': 'form-control phone-input', 'type': 'tel', 'maxlength': '16', 'placeholder': '(055) 555 55 55'}),

            'mather_first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mather_last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mather_workplace': forms.TextInput(attrs={'class': 'form-control'}),
            'mather_position': forms.Select(attrs={'class': 'form-control'}),
            'mather_phone_1': forms.TextInput(attrs={'class': 'form-control phone-input', 'type': 'tel', 'maxlength': '16', 'placeholder': '(055) 555 55 55'}),
            'mather_phone_2': forms.TextInput(attrs={'class': 'form-control phone-input', 'type': 'tel', 'maxlength': '16', 'placeholder': '(055) 555 55 55'}),

            'responsible_first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'responsible_last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'responsible_sur_name': forms.TextInput(attrs={'class': 'form-control'}),
            'responsible_passport_number': forms.TextInput(attrs={'class': 'form-control limited-input-11', 'placeholder': 'AA / AZE'}),
            'responsible_fin': forms.TextInput(attrs={'class': 'form-control limited-input', 'maxlength': '7'}),
            'responsible_address': forms.TextInput(attrs={'class': 'form-control'}),
            'responsible_workplace': forms.TextInput(attrs={'class': 'form-control'}),
            'responsible_position': forms.Select(attrs={'class': 'form-control'}),
            'proximity': forms.Select(attrs={'class': 'form-control'}),
            'responsible_phone_1': forms.TextInput(attrs={'class': 'form-control phone-input', 'type': 'tel', 'maxlength': '16', 'placeholder': '(055) 555 55 55'}),
            'responsible_phone_2': forms.TextInput(attrs={'class': 'form-control phone-input', 'type': 'tel', 'maxlength': '16', 'placeholder': '(055) 555 55 55'}),

            'concession_1': forms.TextInput(attrs={'class': 'form-control'}),
            'concession_1_price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_concession_1_price'}),
            'concession_2': forms.TextInput(attrs={'class': 'form-control'}),
            'concession_2_price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_concession_2_price'}),
            'concession_3': forms.TextInput(attrs={'class': 'form-control'}),
            'concession_3_price': forms.NumberInput(attrs={'class': 'form-control', 'id': 'id_concession_3_price'}),

            'total_concession': forms.NumberInput(attrs={'class': 'form-control', 'id': 'total_concession'}),

            'concession_1_percent': forms.NumberInput(attrs={'class': 'form-control', 'id': 'concession_1_percent'}),
            'concession_2_percent': forms.NumberInput(attrs={'class': 'form-control', 'id': 'concession_2_percent'}),
            'concession_3_percent': forms.NumberInput(attrs={'class': 'form-control', 'id': 'concession_3_percent'}),
            'annual_fee': forms.NumberInput(
                attrs={'class': 'form-control', 'id': 'id_annual_fee'}),
        }


class StudentSearchForm(forms.Form):
    first_name = forms.CharField(required=False, label='Ad')
    last_name = forms.CharField(required=False, label='Soyad')
    work_number = forms.CharField(required=False, label='İş nömrəsi')


class SplitTuitionFeeForm(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
                                 label="Start Date")
    number_of_months = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}), min_value=1,
                                          label="Number of Months")


class ClassForm(forms.ModelForm):
    class Meta:
        model = StudentClass
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = ['year', 'order']
        widgets = {
            'year': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ClassNumberForm(forms.ModelForm):
    class Meta:
        model = ClassNumber
        fields = ['number']
        widgets = {
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProximityForm(forms.ModelForm):
    class Meta:
        model = Proximity
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
