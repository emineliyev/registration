import django_filters
from .models import Student, StudentClass, Group


class StudentFilter(django_filters.FilterSet):
    created_at__gte = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', input_formats=['%Y-%m-%d'])
    created_at__lte = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', input_formats=['%Y-%m-%d'])
    student_class = django_filters.ModelMultipleChoiceFilter(queryset=StudentClass.objects.all(), conjoined=False)
    group = django_filters.ModelMultipleChoiceFilter(queryset=Group.objects.all(), conjoined=False)

    class Meta:
        model = Student
        fields = {
            'year': ['exact'],
            'work_number': ['exact', 'icontains'],
            'first_name': ['exact', 'icontains'],
            'last_name': ['exact', 'icontains'],
            'gender': ['exact'],
            'shift': ['exact'],
            'student_class': ['exact'],
            'group': ['exact'],
            'class_number': ['exact'],
            'section': ['exact'],
            'registration_status': ['exact'],
            'registration_type': ['exact'],
        }


