from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import (
    ClassForm,
    YearForm,
    GroupForm, SubjectForm, ExamForm, ClassNumberForm, PositionForm, ProximityForm
)
from .models import (
    ClassNumber,
    StudentClass,
    Year,
    Group, Subject, Exam, Position, Proximity
)


# CLASS *******
class ClassListView(LoginRequiredMixin, ListView):
    model = StudentClass
    context_object_name = 'class_lists'
    template_name = 'student/parameters/class_list/class_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class ClassListCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentClass
    form_class = ClassForm
    template_name = 'student/parameters/class_list/add_class.html'
    success_url = reverse_lazy('student:class_list')
    success_message = 'Sinif uğurla əlavə edildi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class ClassListUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentClass
    form_class = ClassForm
    template_name = 'student/parameters/class_list/update_class.html'
    success_url = reverse_lazy('student:class_list')
    success_message = 'Sinif uğurla yeniləndi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class DeleteClassListView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = StudentClass
    template_name = 'student/parameters/class_list/delete_confirm_class.html'
    success_url = reverse_lazy('student:class_list')
    success_message = 'Sinif uğurla silindi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


# YEAR *******
class YearListView(LoginRequiredMixin, ListView):
    model = Year
    template_name = 'student/parameters/year/year_list.html'
    context_object_name = 'years'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class YearCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Year
    form_class = YearForm
    template_name = 'student/parameters/year/add_year.html'
    success_url = reverse_lazy('student:year_list')
    success_message = 'Tədris ili uğurla əlavə edildi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class YearUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Year
    form_class = YearForm
    template_name = 'student/parameters/year/update_year.html'
    success_url = reverse_lazy('student:year_list')
    success_message = 'Tədris ili uğurla yeniləndi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class DeleteYearListView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Year
    template_name = 'student/parameters/year/delete_confirm_year.html'
    success_url = reverse_lazy('student:year_list')
    success_message = 'Tədris ili uğurla silindi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


@csrf_exempt
def reorder_years(request):
    if request.method == 'POST':
        order = request.POST.getlist('order[]')
        for index, year_id in enumerate(order):
            year = Year.objects.get(id=year_id)
            year.order = index  # Предположим, что у вас есть поле order в модели Year для хранения порядка
            year.save()
            messages.success(request, message='Məlumatlar yeniləndi!')
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'fail'})


# GROUP *******

class GroupListView(LoginRequiredMixin, ListView):
    model = Group
    context_object_name = 'groups'
    template_name = 'student/parameters/group/group_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class GroupCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'student/parameters/group/add_group.html'
    success_url = reverse_lazy('student:group_list')
    success_message = 'Qrup uğurla əlavə edildi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class GroupUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Group
    form_class = ClassForm
    template_name = 'student/parameters/group/update_group.html'
    success_url = reverse_lazy('student:group_list')
    success_message = 'Qrup uğurla yeniləndi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class GroupDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Group
    template_name = 'student/parameters/group/delete_confirm_group.html'
    success_url = reverse_lazy('student:group_list')
    success_message = 'Qrup uğurla silindi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


# SUBJECT *******
class SubjectListView(LoginRequiredMixin, ListView):
    model = Subject
    context_object_name = 'subjects'
    template_name = 'student/parameters/subject/subject_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class SubjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'student/parameters/subject/add_subject.html'
    success_url = reverse_lazy('student:subject_list')
    success_message = 'Fənn uğurla əlavə edildi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class SubjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Subject
    form_class = SubjectForm
    template_name = 'student/parameters/subject/update_subject.html'
    success_url = reverse_lazy('student:subject_list')
    success_message = 'Fənn uğurla yeniləndi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class SubjectDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Exam
    template_name = 'student/parameters/subject/delete_confirm_subject.html'
    success_url = reverse_lazy('student:subject_list')
    success_message = 'İmatahn uğurla silindi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


# EXAM *******
class ExamListView(LoginRequiredMixin, ListView):
    model = Exam
    context_object_name = 'exams'
    template_name = 'student/parameters/exam/exam_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class ExamCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Exam
    form_class = ExamForm
    template_name = 'student/parameters/exam/add_exam.html'
    success_url = reverse_lazy('student:exam_list')
    success_message = 'İmtahan uğurla əlavə edildi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class ExamUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Exam
    form_class = ExamForm
    template_name = 'student/parameters/exam/update_exam.html'
    success_url = reverse_lazy('student:exam_list')
    success_message = 'İmtahan uğurla yeniləndi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class ExamDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Exam
    template_name = 'student/parameters/exam/delete_confirm_exam.html'
    success_url = reverse_lazy('student:exam_list')
    success_message = 'İmtahan uğurla silindi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


# CLASS-NUMBER *******
class ClassNumberListView(LoginRequiredMixin, ListView):
    model = ClassNumber
    context_object_name = 'class_numbers'
    template_name = 'student/parameters/class_number/class_number_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class ClassNumberCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ClassNumber
    form_class = ClassNumberForm
    template_name = 'student/parameters/class_number/add_class_number.html'
    success_url = reverse_lazy('student:class_number_list')
    success_message = 'Sinif kodu uğurla əlavə edildi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class ClassNumberUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ClassNumber
    form_class = ClassNumberForm
    template_name = 'student/parameters/class_number/update_class_number.html'
    success_url = reverse_lazy('student:class_number_list')
    success_message = 'Sinif kodu uğurla yeniləndi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class ClassNumberDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = ClassNumber
    template_name = 'student/parameters/class_number/delete_confirm_class_number.html'
    success_url = reverse_lazy('student:class_number_list')
    success_message = 'Sinif kodu uğurla silindi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


# POSITION *******
class PositionListView(LoginRequiredMixin, ListView):
    model = Position
    context_object_name = 'positions'
    template_name = 'student/parameters/positions/positions_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class PositionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Position
    form_class = PositionForm
    template_name = 'student/parameters/positions/add_positions.html'
    success_url = reverse_lazy('student:positions_list')
    success_message = 'Vəzifə uğurla əlavə edildi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class PositionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Position
    form_class = PositionForm
    template_name = 'student/parameters/positions/update_positions.html'
    success_url = reverse_lazy('student:positions_list')
    success_message = 'Vəzifə uğurla yeniləndi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class PositionDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Position
    template_name = 'student/parameters/positions/delete_confirm_positions.html'
    success_url = reverse_lazy('student:positions_list')
    success_message = 'Vəzifə uğurla silindi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


# PROXİMİTY *******
class ProximityListView(LoginRequiredMixin, ListView):
    model = Proximity
    context_object_name = 'proximity'
    template_name = 'student/parameters/proximity/proximity_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class ProximityCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Proximity
    form_class = ProximityForm
    template_name = 'student/parameters/proximity/add_proximity.html'
    success_url = reverse_lazy('student:proximity_list')
    success_message = 'Yaxınlıq uğurla əlavə edildi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class ProximityUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Proximity
    form_class = ProximityForm
    template_name = 'student/parameters/proximity/update_proximity.html'
    success_url = reverse_lazy('student:proximity_list')
    success_message = 'Yaxınlıq uğurla yeniləndi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class ProximityDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Proximity
    template_name = 'student/parameters/proximity/delete_confirm_proximity.html'
    success_url = reverse_lazy('student:proximity_list')
    success_message = 'Yaxınlıq uğurla silindi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context
