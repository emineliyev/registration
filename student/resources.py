from import_export import resources
from student.models import Year, StudentClass, Group, Subject, Exam, ClassNumber, Proximity, Student, TuitionFee, \
    TuitionFeeSplit, Position


class YearResource(resources.ModelResource):
    class Meta:
        model = Year


class StudentClassResource(resources.ModelResource):
    class Meta:
        model = StudentClass


class GroupResource(resources.ModelResource):
    class Meta:
        model = Group


class PositionResource(resources.ModelResource):
    class Meta:
        model = Position


class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject


class ExamResource(resources.ModelResource):
    class Meta:
        model = Exam


class ClassNumberResource(resources.ModelResource):
    class Meta:
        model = ClassNumber


class ProximityResource(resources.ModelResource):
    class Meta:
        model = Proximity


class StudentResource(resources.ModelResource):
    class Meta:
        model = Student


class TuitionFeeResource(resources.ModelResource):
    class Meta:
        model = TuitionFee


class TuitionFeeSplitResource(resources.ModelResource):
    class Meta:
        model = TuitionFeeSplit
