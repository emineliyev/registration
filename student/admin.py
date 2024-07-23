from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Student,
    Year,
    StudentClass,
    Group,
    Subject,
    Exam,
    ClassNumber,
    Position,
    Proximity,
    TuitionFee,
    TuitionFeeSplit,
)
from .resources import (
    StudentResource, YearResource, GroupResource, SubjectResource, ExamResource, ClassNumberResource, ProximityResource,
    TuitionFeeResource, TuitionFeeSplitResource, StudentClassResource, PositionResource
)


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'first_name', 'last_name')
    search_fields = ('id', 'first_name', 'last_name')
    resource_class = StudentResource


@admin.register(Year)
class YearAdmin(ImportExportModelAdmin):
    list_display = ('id', 'year')
    resource_class = YearResource


@admin.register(Group)
class GroupAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name')
    resource_class = GroupResource


@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('id', 'name')
    resource_class = SubjectResource


@admin.register(Exam)
class ExamAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('id', 'name')
    resource_class = ExamResource


@admin.register(ClassNumber)
class ClassNumberAdmin(ImportExportModelAdmin):
    list_display = ('id', 'number')
    search_fields = ('id', 'number')
    resource_class = ClassNumberResource


@admin.register(Position)
class PositionAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    resource_class = PositionResource


@admin.register(Proximity)
class ProximityAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('id', 'name')
    resource_class = ProximityResource


@admin.register(TuitionFee)
class TuitionFeeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'student', 'annual_fee', 'start_date', 'number_of_months')
    search_fields = ('id', 'student')
    resource_class = TuitionFeeResource


@admin.register(TuitionFeeSplit)
class TuitionFeeSplitAdmin(ImportExportModelAdmin):
    list_display = ('id', 'student', 'installment_date', 'installment_amount', 'payment_date', 'payment_amount')
    search_fields = ('id', 'student')
    resource_class = TuitionFeeSplitResource


@admin.register(StudentClass)
class StudentClassAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('id', 'name', 'price')
    resource_class = StudentClassResource
