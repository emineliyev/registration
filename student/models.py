import os
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
from django.utils import timezone
from student.utils import generate_contract
from pathlib import Path
from django.conf import settings


class Year(models.Model):
    year = models.CharField(max_length=20, verbose_name='Tədris ili')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Əlavə tarixi')
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.year}"

    class Meta:
        verbose_name = 'Tədris ili'
        verbose_name_plural = 'Tədris ili'
        ordering = ['order']


class StudentClass(models.Model):
    name = models.CharField(max_length=100, verbose_name='Sinif')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Qiymət', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Əlavə tarixi')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Sinif'
        verbose_name_plural = 'Sinif'
        ordering = ['name']


class Group(models.Model):
    name = models.CharField(max_length=100, verbose_name='Qrup')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Qiymət', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Əlavə tarixi')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Qrup'
        verbose_name_plural = 'Qrup'
        ordering = ['name']


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name='Fənn')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Qiymət', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'Fənn'
        verbose_name_plural = 'Fənn'
        ordering = ['name']


class Exam(models.Model):
    name = models.CharField(max_length=100, verbose_name='İmtahan')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Qiymət', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Əlavə tarixi')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = 'İmtahan'
        verbose_name_plural = 'İmtahan'
        ordering = ['-created_at']


class ClassNumber(models.Model):
    number = models.IntegerField(verbose_name="Sinif kodu")

    def __str__(self):
        return f"{self.number}"

    class Meta:
        verbose_name = "Sinif kodu"
        verbose_name_plural = "Sinif kodu"
        ordering = ['number']


class Position(models.Model):
    name = models.CharField(max_length=100, verbose_name="Vəzifə")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Vəzifə"
        verbose_name_plural = "Vəzifə"
        ordering = ['name']


class Proximity(models.Model):
    name = models.CharField(max_length=100, verbose_name='Yaxınlığı')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Yaxınlığı"
        verbose_name_plural = "Yaxınlığı"
        ordering = ['name']


class Student(models.Model):
    SECTION_CHOICES = [
        ('Azerbaijan', 'Azərbaycan'),
        ('Russian', 'Rus'),
    ]
    REGISTRATION_STATUS = [
        ('Registered', 'Qeydiyyatdadır'),
        ('Out', 'Çıxıb'),
    ]
    REGISTRATION_TYPE = [
        ('New', 'Yeni qeydiyyat'),
        ('Again', 'Təkrar qeydiyyat')
    ]
    GENDER = [
        ('Man', 'Kişi'),
        ('Woman', 'Qadın')
    ]
    SHIFT = [
        ('Morning', 'Səhər'),
        ('Afternoon', 'Günorta')
    ]
    year = models.ForeignKey(Year, on_delete=models.CASCADE, verbose_name='Tədris ili')
    work_number = models.IntegerField(verbose_name='İş nömrəsi', unique=True)

    registration_status = models.CharField(max_length=14, choices=REGISTRATION_STATUS, default='Registered',
                                           verbose_name='Qeydiyyat statusu')
    registration_type = models.CharField(max_length=16, choices=REGISTRATION_TYPE, default='New',
                                         verbose_name='Qeydiyyat növü')

    first_name = models.CharField(max_length=100, verbose_name="Ad")
    last_name = models.CharField(max_length=100, verbose_name="Soyad")
    gender = models.CharField(max_length=16, choices=GENDER, default='Man', verbose_name='Cinsiyyət')
    shift = models.CharField(max_length=10, verbose_name='Növbə', choices=SHIFT, default='Morning')
    note = models.TextField(verbose_name='Qeydiyyat', blank=True, null=True)
    student_class = models.ForeignKey(StudentClass, verbose_name="Sinif", on_delete=models.CASCADE,
                                      related_name='class_student')
    group = models.ForeignKey(Group, verbose_name="Qrup", on_delete=models.CASCADE, related_name='group_student', )
    section = models.CharField(max_length=10, choices=SECTION_CHOICES, verbose_name='Bölmə')
    score = models.IntegerField(verbose_name='Qəbul balı')
    class_number = models.ForeignKey(ClassNumber, verbose_name="Sinif kodu", on_delete=models.CASCADE,
                                     related_name='class_number')
    subject = models.ManyToManyField(Subject, verbose_name="Fənn", related_name='subject')
    exam = models.ManyToManyField(Exam, verbose_name="İmtahan", related_name='exam')
    school = models.CharField(max_length=100, verbose_name="Məktəb")
    city = models.CharField(max_length=100, verbose_name="Şəhər")
    address = models.CharField(max_length=250, verbose_name="Ünvan")
    concession_1 = models.CharField(max_length=250, verbose_name='Güzəşt-1 adı', blank=True, null=True)
    concession_1_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                             verbose_name='Güzəşt-1 məbləği', blank=True, null=True)
    concession_2 = models.CharField(max_length=250, verbose_name='Güzəşt-2 adı', blank=True, null=True)
    concession_2_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                             verbose_name='Güzəşt-2 məbləği', blank=True, null=True)
    concession_3 = models.CharField(max_length=250, verbose_name='Güzəşt-3 adı', blank=True, null=True)
    concession_3_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                             verbose_name='Güzəşt-3 məbləği', blank=True, null=True)
    concession_1_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                               verbose_name='Güzəşt-1 faiz', blank=True, null=True)
    concession_2_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                               verbose_name='Güzəşt-2 faiz', blank=True, null=True)
    concession_3_percent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                               verbose_name='Güzəşt-3 faiz', blank=True, null=True)
    total_concession = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                           verbose_name='Cəmi güzəşt məbləği', blank=True, null=True)

    # FATHER-INFORMATION
    father_first_name = models.CharField(max_length=100, verbose_name="Ata adı")
    father_last_name = models.CharField(max_length=100, verbose_name="Ata soyad")
    father_workplace = models.CharField(max_length=100, verbose_name='Ata iş yeri', blank=True, null=True)
    father_position = models.ForeignKey(Position, verbose_name="Vəzifə", on_delete=models.CASCADE,
                                        related_name='father_position')
    father_phone_1 = models.CharField(max_length=15, verbose_name="Ata telefon 1")
    father_phone_2 = models.CharField(max_length=15, verbose_name="Ata telefon 2", blank=True, null=True)

    # MOTHER-INFORMATION
    mather_first_name = models.CharField(max_length=100, verbose_name="Ana ad")
    mather_last_name = models.CharField(max_length=100, verbose_name="Ana soyad")
    mather_workplace = models.CharField(max_length=100, verbose_name='Ana iş yeri', blank=True, null=True)
    mather_position = models.ForeignKey(Position, verbose_name="Vəzifə", on_delete=models.CASCADE,
                                        related_name='mather_position')
    mather_phone_1 = models.CharField(max_length=15, verbose_name="Ana telefon 1")
    mather_phone_2 = models.CharField(max_length=15, verbose_name="Ana telefon 2", blank=True, null=True)

    # RESPONSIBLE-PERSON
    responsible_first_name = models.CharField(max_length=100, verbose_name="Məhsul şəxs adı")
    responsible_last_name = models.CharField(max_length=100, verbose_name="Məhsul şəxs soyad")
    responsible_sur_name = models.CharField(max_length=100, verbose_name="Məhsul şəxs ata adı")
    responsible_passport_number = models.CharField(max_length=100, verbose_name="Məhsul şəxs vəsiqə nömrəsi")
    responsible_fin = models.CharField(max_length=100, verbose_name="Məhsul şəxs vəsiqə FİN")
    responsible_workplace = models.CharField(max_length=100, verbose_name='Məhsul şəxs iş yeri', blank=True, null=True)
    responsible_address = models.CharField(max_length=250, verbose_name="Məhsul şəxs ünvan")
    responsible_position = models.ForeignKey(Position, verbose_name="Məhsul şəxs vəzifə", on_delete=models.CASCADE,
                                             related_name='responsible_position')
    proximity = models.ForeignKey(Proximity, on_delete=models.CASCADE, verbose_name='Yaxınlığı',
                                  related_name='proximity')
    responsible_phone_1 = models.CharField(max_length=15, verbose_name="Məsul şəxs telefon 1")
    responsible_phone_2 = models.CharField(max_length=15, verbose_name="Məsul şəxs telefon 2", blank=True, null=True)

    annual_fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Təhsil haqqı')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Qeydiyyat tarixi')
    update = models.DateTimeField(auto_now=True, verbose_name='Yenilənə tarixi')
    is_split_edited = models.BooleanField(default=False)
    is_debtor = models.BooleanField(default=False, verbose_name='Borc')

    def delete(self, *args, **kwargs):
        # Найти и удалить файлы документов, связанные со студентом
        contracts_dir = Path(settings.MEDIA_ROOT) / 'contracts'
        for contract_file in contracts_dir.glob(f'{self.work_number}_contract.docx'):
            if contract_file.exists():
                os.remove(contract_file)

        # Вызов стандартного метода delete
        super().delete(*args, **kwargs)

    def update_debtor_status(self):
        today = timezone.now().date()
        overdue_payments = self.tuitionfeesplit_set.filter(payment_date__isnull=True, installment_date__lt=today)
        self.is_debtor = overdue_payments.exists()
        self.save()

    def generate_work_number(self):
        while True:
            work_number = random.randint(2000000, 9999999)
            if not Student.objects.filter(work_number=work_number).exists():
                return work_number

    def save(self, *args, **kwargs):
        if not self.pk:  # только для новых записей
            self.year = Year.objects.latest('id')
            self.work_number = self.generate_work_number()
            super().save(*args, **kwargs)
            generate_contract(self)  # Генерация контракта после сохранения
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'Şagird'
        verbose_name_plural = 'Şagird'
        ordering = ['-created_at']


class TuitionFee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    annual_fee = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    number_of_months = models.IntegerField()

    def __str__(self):
        return f"{self.student} - {self.annual_fee} ₼"


class TuitionFeeSplit(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    installment_date = models.DateField()
    installment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Новое поле

    class Meta:
        ordering = ['installment_date']

    def __str__(self):
        return f"{self.student} - {self.installment_date}"


# @receiver(post_save, sender=TuitionFeeSplit)
# def add_income_record(sender, instance, created, **kwargs):
#     if instance.payment_date and instance.payment_amount:
#         income_category, _ = IncomeCategory.objects.get_or_create(name='Təhsil haqqı')
#         Income.objects.update_or_create(
#             split_payment=instance,
#             defaults={
#                 'name': f"Təhsil haqqı ödənişi: {instance.student.first_name} {instance.student.last_name}",
#                 'category': income_category,
#                 'description': f"{instance.installment_date} Aylıq ödəniş",
#                 'amount': instance.payment_amount,
#                 'create_at': instance.payment_date,
#             }
#         )


@receiver(post_save, sender=TuitionFeeSplit)
def update_student_debtor_status(sender, instance, **kwargs):
    instance.student.update_debtor_status()
