import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from openpyxl import Workbook
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import logging
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from dateutil.relativedelta import relativedelta

from accounting.models import DocumentTemplate
from .filters import StudentFilter
from .forms import (
    StudentForm, SplitTuitionFeeForm, StudentSearchForm
)
from .models import (
    Student, TuitionFeeSplit, Year, StudentClass, Group, ClassNumber, Subject, Exam
)
from django.db import models

logger = logging.getLogger(__name__)


@login_required
def export_students(request):
    field_display_names = {
        'year': 'Tədris ili',
        'work_number': 'İş nömrəsi',
        'first_name': 'Ad',
        'last_name': 'Soyad',
        'gender': 'Cins',
        'shift': 'Növbə',
        'student_class': 'Sinif',
        'group': 'Qrup',
        'class_number': 'Sinif kodu',
        'section': 'Bölmə',
        'registration_status': 'Qeydiyyat statusu',
        'registration_type': 'Qeydiyyat növü',
        'score': 'Qəbul balı',
        'school': 'Məktəb',
        'city': 'Şəhər',
        'address': 'Ünvan',
        'father_first_name': 'Atanın adı',
        'father_last_name': 'Atanın soyadı',
        'father_sur_name': 'Atanın ata adı',
        'father_workplace': 'Atanın iş yeri',
        'father_position': 'Atanın vəzifəsi',
        'father_phone_1': 'Atanın telefonu 1',
        'father_phone_2': 'Atanın telefonu 2',
        'mather_first_name': 'Ananın adı',
        'mather_last_name': 'Ananın soyadı',
        'mather_sur_name': 'Ananın ata adı',
        'mather_workplace': 'Ananın iş yeri',
        'mather_position': 'Ananın vəzifəsi',
        'mather_phone_1': 'Ananın telefonu 1',
        'mather_phone_2': 'Ananın telefonu 2',
        'responsible_first_name': 'Məsul şəxs adı',
        'responsible_last_name': 'Məsul şəxs soyadı',
        'responsible_sur_name': 'Məsul şəxs ata adı',
        'responsible_passport_number': 'Məsul şəxs vəsiqə nömrəsi',
        'responsible_fin': 'Məsul şəxs vəsiqə FİN',
        'responsible_workplace': 'Məsul şəxs iş yeri',
        'responsible_position': 'Məsul şəxs vəzifəsi',
        'proximity': 'Məsul şəxs yaxınlığı',
        'responsible_phone_1': 'Məsul şəxs telefonu 1',
        'responsible_phone_2': 'Məsul şəxs telefonu 2',
        'annual_fee': 'İllik ödəniş',
        'created_at': 'Əlavə tarixi',
        'update': 'Yenilənə tarixi',
        'is_split_edited': 'Bölüşdürmə redaktəsi',
        'is_debtor': 'Borclu'
    }

    if request.method == 'POST':
        fields = request.POST.getlist('fields')
        filter_data = request.POST.dict()
        filter_data.pop('fields', None)
        filter_data.pop('csrfmiddlewaretoken', None)

        queryset = Student.objects.all()

        year = request.POST.get('year')
        work_number = request.POST.get('work_number__icontains')
        first_name = request.POST.get('first_name__icontains')
        last_name = request.POST.get('last_name__icontains')
        gender = request.POST.get('gender')
        shift = request.POST.get('shift')
        student_class = request.POST.get('student_class_hidden', '').split(',') if request.POST.get(
            'student_class_hidden') else []
        group = request.POST.get('group_hidden', '').split(',') if request.POST.get('group_hidden') else []
        class_number = request.POST.get('class_number')
        section = request.POST.get('section')
        registration_status = request.POST.get('registration_status')
        registration_type = request.POST.get('registration_type')
        created_at__gte = request.POST.get('created_at__gte')
        created_at__lte = request.POST.get('created_at__lte')

        # Применение фильтров к queryset
        if year:
            queryset = queryset.filter(year_id=year)
        if work_number:
            queryset = queryset.filter(work_number__icontains=work_number)
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if gender:
            queryset = queryset.filter(gender=gender)
        if shift:
            queryset = queryset.filter(shift=shift)
        if student_class:
            queryset = queryset.filter(student_class_id__in=student_class)
        if group:
            queryset = queryset.filter(group_id__in=group)
        if class_number:
            queryset = queryset.filter(class_number_id=class_number)
        if section:
            queryset = queryset.filter(section=section)
        if registration_status:
            queryset = queryset.filter(registration_status=registration_status)
        if registration_type:
            queryset = queryset.filter(registration_type=registration_type)
        if created_at__gte:
            queryset = queryset.filter(created_at__gte=created_at__gte)
        if created_at__lte:
            queryset = queryset.filter(created_at__lte=created_at__lte)

        students = queryset

        wb = Workbook()
        ws = wb.active
        ws.title = 'Students'

        headers = [field_display_names.get(field, field.replace('_', ' ').title()) for field in fields]
        ws.append(headers)

        for student in students:
            row = []
            for field in fields:
                value = getattr(student, field)
                if isinstance(value, models.Model):
                    value = str(value)
                elif isinstance(student._meta.get_field(field), models.ForeignKey):
                    related_object = getattr(student, field)
                    value = str(related_object)
                elif field in ['section', 'registration_status', 'registration_type']:
                    value = getattr(student, f'get_{field}_display')()
                elif isinstance(value, timezone.datetime):
                    value = value.replace(tzinfo=None)
                row.append(value)
            ws.append(row)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=sagirler.xlsx'
        wb.save(response)
        return response

    excluded_fields = {'id', 'update', 'is_split_edited', 'is_debtor'}
    fields = [(field.name, field_display_names.get(field.name, field.name.replace('_', ' ').title()))
              for field in Student._meta.fields if field.name not in excluded_fields]
    return render(request, 'export_students.html', {'fields': fields})


@require_POST
def calculate_fee(request):
    student_class_id = request.POST.get('student_class')
    group_id = request.POST.get('group')
    subject_ids = request.POST.getlist('subject[]')
    exam_ids = request.POST.getlist('exam[]')

    total_fee = 0

    if student_class_id:
        student_class = StudentClass.objects.get(id=student_class_id)
        total_fee += student_class.price or 0

    if group_id:
        group = Group.objects.get(id=group_id)
        total_fee += group.price or 0

    if subject_ids:
        subjects = Subject.objects.filter(id__in=subject_ids)
        total_fee += sum(subject.price for subject in subjects if subject.price)

    if exam_ids:
        exams = Exam.objects.filter(id__in=exam_ids)
        total_fee += sum(exam.price for exam in exams if exam.price)

    return JsonResponse({'total_fee': total_fee})


def download_contract(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    file_path = os.path.join(settings.MEDIA_ROOT, f'contracts/{student.work_number}_contract.docx')

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    else:
        return HttpResponse("Müqavilə tapılmadı!", status=404)


class BaseStudentListView(LoginRequiredMixin, ListView):
    model = Student
    context_object_name = 'students'
    paginate_by = 20

    def get_default_category(self):
        """
        Этот метод предназначен для получения и кэширования значения по умолчанию для категории.
        Это позволяет избежать повторных запросов к базе данных.
        :return:
        """
        if not hasattr(self, '_default_category'):
            self._default_category = Year.objects.values_list('id', flat=True).first()
        return self._default_category

    def get_years(self):
        if not hasattr(self, '_years'):
            self._years = list(Year.objects.all())
        return self._years

    def get_queryset(self):
        queryset = super().get_queryset().select_related('student_class', 'group', 'class_number').prefetch_related(
            'tuitionfeesplit_set')
        data = self.request.GET.copy()
        data.setdefault('year', self.get_default_category())
        self.filterset = StudentFilter(data, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        additional_context = self.get_additional_context_data()
        context.update(additional_context)
        context['student_count'] = self.filterset.qs.count()
        return context

    def get_additional_context_data(self):
        student_classes = StudentClass.objects.all()
        groups = Group.objects.all()
        class_numbers = ClassNumber.objects.all()

        return {
            'years': self.get_years(),
            'student_classes': student_classes,
            'groups': groups,
            'genders': Student.GENDER,
            'shifts': Student.SHIFT,
            'class_numbers': class_numbers,
            'sections': Student.SECTION_CHOICES,
            'registration_statuses': Student.REGISTRATION_STATUS,
            'registration_types': Student.REGISTRATION_TYPE,
            'filter': self.filterset,
            'fields': [(field.name, field.verbose_name) for field in Student._meta.fields if
                       field.name not in {'id', 'update', 'is_split_edited', 'is_debtor'}],
            'request_GET': self.request.GET,
        }


class StudentListView(BaseStudentListView):
    template_name = 'student/student_list.html'


class StudentDeleteConfirm(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'student/student_delete_confirm.html'
    model = Student
    success_url = reverse_lazy('student:student_list')
    success_message = 'Şagird uğurla silindi!.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/update_student.html'
    success_url = reverse_lazy('student:student_list')
    success_message = 'Şagird məlumatları uğurla yeniləndi!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context


class CreateStudentView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = 'student/add_student.html'
    success_url = reverse_lazy('student:student_list')
    success_message = 'Şagird uğurla əlavə edildi!'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context

    def form_valid(self, form):
        try:
            # Проверка наличия шаблона документа
            if not DocumentTemplate.objects.exists():
                raise DocumentTemplate.DoesNotExist

            return super().form_valid(form)
        except DocumentTemplate.DoesNotExist:
            messages.error(
                self.request,
                "Sinfə uyğun müqavilə tapılmadı! Zəhmət olmasa müqavilə yükləyin."
            )
            return self.form_invalid(form)
        except ObjectDoesNotExist:
            messages.error(
                self.request,
                "Şagird əlavə etməkdən öncə tədris ili yaradın"
            )
            return self.form_invalid(form)

        except FileNotFoundError:
            messages.error(
                self.request,
                "Müqavilə silinib. Şagird müqaviləsiz əlavə edildi!"
            )
            return self.form_invalid(form)


class RepeatRegistrationSearchView(LoginRequiredMixin, View):
    def get(self, request):
        form = StudentSearchForm(request.GET)
        students = []
        if form.is_valid():
            students = Student.objects.filter(
                first_name__icontains=form.cleaned_data['first_name'],
                last_name__icontains=form.cleaned_data['last_name'],
                work_number__icontains=form.cleaned_data['work_number']
            )
        return render(request, 'student/repeat_registration_search.html', {'form': form, 'students': students})


class RepeatRegistrationCreateView(LoginRequiredMixin, View):
    def get(self, request, student_id):
        original_student = get_object_or_404(Student, id=student_id)
        form = StudentForm(instance=original_student)
        form.initial['registration_type'] = 'Again'

        # Очистить поля, связанные со скидками
        for field in ['concession_1', 'concession_1_price', 'concession_2', 'concession_2_price',
                      'concession_3', 'concession_3_price', 'concession_1_percent',
                      'concession_2_percent', 'concession_3_percent', 'total_concession']:
            form.initial[field] = ''

        return render(request, 'student/add_student.html', {'form': form, 'is_repeat_registration': True})

    def post(self, request, student_id):
        original_student = get_object_or_404(Student, id=student_id)
        form = StudentForm(request.POST, instance=original_student)

        # Очистить поля, связанные со скидками
        for field in ['concession_1', 'concession_1_price', 'concession_2', 'concession_2_price',
                      'concession_3', 'concession_3_price', 'concession_1_percent',
                      'concession_2_percent', 'concession_3_percent', 'total_concession']:
            form.data = form.data.copy()  # Копируем данные формы, чтобы сделать их изменяемыми
            form.data[field] = ''

        if form.is_valid():
            new_student = form.save(commit=False)
            new_student.id = None
            new_student.registration_type = 'Again'
            new_student.save()
            return redirect('student:student_list')
        return render(request, 'student/add_student.html', {'form': form, 'is_repeat_registration': True})


class SplitTuitionFeeView(LoginRequiredMixin, View):
    template_name = 'student/split_tuition_fee.html'

    def get(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        form = SplitTuitionFeeForm()
        return render(request, self.template_name, {'student': student, 'form': form})

    def post(self, request, student_id):
        student = get_object_or_404(Student, pk=student_id)
        form = SplitTuitionFeeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            number_of_months = form.cleaned_data['number_of_months']
            monthly_fee = student.annual_fee // number_of_months
            remainder = student.annual_fee % number_of_months

            TuitionFeeSplit.objects.filter(student=student).delete()  # Удаляем предыдущие записи

            for i in range(number_of_months):
                installment_amount = monthly_fee
                if remainder > 0:
                    installment_amount += 1
                    remainder -= 1

                installment_date = start_date + relativedelta(months=i)
                TuitionFeeSplit.objects.create(
                    student=student,
                    installment_date=installment_date,
                    installment_amount=installment_amount
                )
            return redirect('student:tuition_fee_split_detail', student_id=student.pk)
        return render(request, self.template_name, {'student': student, 'form': form})


class TuitionFeeSplitDetailView(LoginRequiredMixin, DetailView):
    """
    Представление для отображения детальной информации о частичных платежах за обучение студента.

    Наследование:
    - LoginRequiredMixin: требует аутентификации пользователя для доступа к этому представлению.
    - DetailView: предоставляет базовый функционал для детализированных представлений.

    Атрибуты:
    - model: модель, используемая в представлении (Student).
    - template_name: путь к шаблону, который будет использоваться для отображения (student/tuition_fee_split_detail.html).
    - context_object_name: имя переменной контекста для объекта (student).
    - pk_url_kwarg: ключевое слово URL, используемое для получения первичного ключа объекта (student_id).
    """
    model = Student
    template_name = 'student/tuition_fee_split_detail.html'
    context_object_name = 'student'
    pk_url_kwarg = 'student_id'

    def get_context_data(self, **kwargs):
        """
        Получает контекстные данные для отображения в шаблоне.

        Дополняет контекст данными о частичных платежах студента, включая:
        - annual_fee: годовая плата за обучение.
        - total_paid: общая сумма оплаченных частичных платежей.
        - remaining_amount: оставшаяся сумма для оплаты за обучение.
        - next_payment_date: дата следующего частичного платежа.
        - next_payment_amount: сумма следующего частичного платежа.
        - today: текущая дата.
        - overdue_amount: общая сумма просроченных платежей.
        - tuition_fee_splits: список всех частичных платежей с атрибутом amount_due.

        Возвращает:
        dict: обновленный контекст для использования в шаблоне.
        """
        context = super().get_context_data(**kwargs)
        student = self.get_object()
        tuition_fee_splits = TuitionFeeSplit.objects.filter(student=student).order_by('installment_date')

        # Годовая плата
        context['annual_fee'] = student.annual_fee

        # Общая оплаченная сумма
        total_paid = sum(s.payment_amount for s in tuition_fee_splits if s.payment_date)
        context['total_paid'] = total_paid

        # Оставшаяся сумма
        remaining_amount = student.annual_fee - total_paid
        context['remaining_amount'] = remaining_amount

        # Следующая оплата
        next_payment = tuition_fee_splits.filter(payment_date__isnull=True).first()
        context['next_payment_date'] = next_payment.installment_date if next_payment else None
        context['next_payment_amount'] = next_payment.installment_amount if next_payment else None

        # Текущая дата
        context['today'] = timezone.localdate()

        # Просроченные платежи
        overdue_payments = tuition_fee_splits.filter(payment_date__isnull=True, installment_date__lt=context['today'])
        overdue_amount = sum(p.installment_amount for p in overdue_payments)
        context['overdue_amount'] = overdue_amount

        # Сумма к оплате
        for split in tuition_fee_splits:
            split.amount_due = split.installment_amount - (split.payment_amount or 0)

        context['tuition_fee_splits'] = tuition_fee_splits
        return context


class PaymentReceiptView(LoginRequiredMixin, DetailView):
    model = TuitionFeeSplit
    template_name = 'student/payment_receipt.html'
    context_object_name = 'split'
    pk_url_kwarg = 'split_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        split = self.get_object()
        student = split.student
        tuition_fee_splits = TuitionFeeSplit.objects.filter(student=student).order_by('installment_date')

        # Годовая плата
        context['annual_fee'] = student.annual_fee

        # Общая оплаченная сумма
        total_paid = sum(s.payment_amount for s in tuition_fee_splits if s.payment_date)
        context['total_paid'] = total_paid

        # Оставшаяся сумма
        remaining_amount = student.annual_fee - total_paid
        context['remaining_amount'] = remaining_amount

        # Следующая оплата
        next_payment = tuition_fee_splits.filter(payment_date__isnull=True).first()
        context['next_payment_date'] = next_payment.installment_date if next_payment else None
        context['next_payment_amount'] = next_payment.installment_amount if next_payment else None
        context['today'] = timezone.localdate()
        context['student'] = student
        return context


@login_required
def tuition_fee_schedule_view(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    tuition_fee_splits = TuitionFeeSplit.objects.filter(student=student).order_by('installment_date')
    today = timezone.localdate()

    context = {
        'student': student,
        'today': today,
        'tuition_fee_splits': tuition_fee_splits,
    }

    return render(request, 'student/payment_schedule.html', context)


@login_required
@require_POST
def make_payment(request, split_id):
    split = get_object_or_404(TuitionFeeSplit, id=split_id)
    if not split.payment_date:  # Проверяем, не была ли оплата уже проведена
        split.payment_date = timezone.now()
        split.payment_amount = split.installment_amount  # Оплачиваем полную сумму разделения
        split.save()
        messages.success(request,
                         'Ödəniş müvəffəqiyyətlə tamamlanmışdır!')  # Устанавливаем сообщение об успешной оплате

    return redirect('student:tuition_fee_split_detail', student_id=split.student.id)


@login_required
@require_POST
def save_splits(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    tuition_fee_splits = TuitionFeeSplit.objects.filter(student=student).order_by('installment_date')

    # Сохраняем существующие строки
    for split in tuition_fee_splits:
        installment_date = request.POST.get(f'installment_date_{split.id}')
        installment_amount = request.POST.get(f'installment_amount_{split.id}')

        if installment_date:
            split.installment_date = installment_date
        if installment_amount:
            split.installment_amount = installment_amount

        messages.success(request, 'Cədvəl yeniləndi!')

        split.save()

    # Добавляем новые строки
    new_splits = []
    for key, value in request.POST.items():
        if key.startswith('new_installment_date_'):
            index = key.split('_')[-1]
            new_date = value
            new_amount = request.POST.get(f'new_installment_amount_{index}')
            if new_date and new_amount:
                new_splits.append(TuitionFeeSplit(
                    student=student,
                    installment_date=new_date,
                    installment_amount=new_amount
                ))

    if new_splits:
        TuitionFeeSplit.objects.bulk_create(new_splits)

    # Удаляем удаленные строки
    deleted_splits = request.POST.get('deleted_splits')
    if deleted_splits:
        deleted_ids = deleted_splits.split(',')
        TuitionFeeSplit.objects.filter(id__in=deleted_ids).delete()

    return redirect('student:tuition_fee_split_detail', student_id=student.pk)


@login_required
@require_POST
def refund_payment(request, split_id):
    split = get_object_or_404(TuitionFeeSplit, id=split_id)
    student = split.student

    if split.payment_date:
        logger.info(f"Attempting to refund payment for split ID: {split_id}")

        # Удаляем запись из доходов, если она существует
        if hasattr(split, 'income_record'):
            logger.info(f"Deleting income record for split ID: {split_id}")
            split.income_record.delete()

        # Восстанавливаем следующую месячную оплату
        next_split = TuitionFeeSplit.objects.filter(student=student, installment_date__gt=split.installment_date,
                                                    payment_date__isnull=True).first()
        if next_split:
            next_split.installment_amount += split.payment_amount - split.installment_amount
            next_split.save()

        # Сбрасываем платежную информацию
        split.payment_date = None
        split.payment_amount = None
        split.save()
        messages.success(request,
                         'Ödəniş müvəffəqiyyətlə qaytarıldı!')  # Устанавливаем сообщение об успешной оплате

        logger.info(f"Refunded payment for split: {split.student} - {split.installment_date}")

    return redirect('student:tuition_fee_split_detail', student_id=student.id)
