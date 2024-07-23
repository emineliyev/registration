from django.urls import path
from .parameters_views import (
    ClassListView,
    ClassListCreateView,
    ClassListUpdateView,
    DeleteClassListView,
    YearListView,
    YearCreateView,
    YearUpdateView,
    DeleteYearListView,
    reorder_years,
    GroupDeleteView,
    GroupUpdateView,
    GroupCreateView,
    GroupListView, SubjectDeleteView, SubjectUpdateView, SubjectCreateView, SubjectListView, ExamListView,
    ExamCreateView, ExamUpdateView, ExamDeleteView, ClassNumberListView, ClassNumberCreateView, ClassNumberUpdateView,
    ClassNumberDeleteView, PositionListView, PositionCreateView, PositionUpdateView, PositionDeleteView,
    ProximityListView, ProximityCreateView, ProximityUpdateView, ProximityDeleteView
)
from .report_views import (
    LatePaymentListView, ExportLatePaymentsExcelView, DailyPayments, ExportDailyPaymentsExcelView,
    StudentReportListView, ExportStudentReportExcelView

)
from .views import (
    CreateStudentView,
    StudentListView,
    SplitTuitionFeeView,
    TuitionFeeSplitDetailView,
    refund_payment,
    PaymentReceiptView,
    save_splits,
    make_payment,
    export_students,
    RepeatRegistrationSearchView,
    RepeatRegistrationCreateView, calculate_fee, StudentUpdateView, download_contract, StudentDeleteConfirm,
    tuition_fee_schedule_view
)

app_name = 'student'
urlpatterns = [
    # STUDENT
    path('student_list/', StudentListView.as_view(), name='student_list'),
    path('add_student/', CreateStudentView.as_view(), name='add_student'),
    path('update_student/<int:pk>/', StudentUpdateView.as_view(), name='update_student'),
    path('repeat_registration_search/', RepeatRegistrationSearchView.as_view(),
         name='repeat_registration_search'),
    path('repeat_registration_create/<int:student_id>/', RepeatRegistrationCreateView.as_view(),
         name='repeat_registration_create'),
    path('export_students/', export_students, name='export_students'),
    path('calculate-fee/', calculate_fee, name='calculate_fee'),
    path('student/<int:student_id>/download_contract/', download_contract, name='download_contract'),
    path('student_delete_confirm/<int:pk>/', StudentDeleteConfirm.as_view(), name='student_delete_confirm'),

    # PAYMENT
    path('student/<int:student_id>/split/', SplitTuitionFeeView.as_view(), name='split_tuition_fee'),
    path('student/split/<int:student_id>/', TuitionFeeSplitDetailView.as_view(), name='tuition_fee_split_detail'),
    path('student/make_payment/<int:split_id>/', make_payment, name='make_payment'),

    path('student/refund_payment/<int:split_id>/', refund_payment, name='refund_payment'),
    path('student/payment_receipt/<int:split_id>/', PaymentReceiptView.as_view(), name='payment_receipt'),
    path('student/save_splits/<int:student_id>/', save_splits, name='save_splits'),
    path('students/<int:student_id>/tuition-fee-schedule/', tuition_fee_schedule_view, name='tuition_fee_schedule'),

    # PARAMETERS
    # ***CLASS-LIST***
    path('class_list/', ClassListView.as_view(), name='class_list'),
    path('add_class/', ClassListCreateView.as_view(), name='add_class'),
    path('update_class/<int:pk>/', ClassListUpdateView.as_view(), name='update_class'),
    path('delete_confirm_class/<int:pk>/', DeleteClassListView.as_view(), name='delete_confirm_class'),

    # ***YEAR-LIST***
    path('year_list/', YearListView.as_view(), name='year_list'),
    path('add_year/', YearCreateView.as_view(), name='add_year'),
    path('update_year/<int:pk>/', YearUpdateView.as_view(), name='update_year'),
    path('delete_year/<int:pk>/', DeleteYearListView.as_view(), name='delete_year'),
    path('reorder_years/', reorder_years, name='reorder_years'),

    # GROUP
    path('group_list/', GroupListView.as_view(), name='group_list'),
    path('add_group/', GroupCreateView.as_view(), name='add_group'),
    path('update_group/<int:pk>/', GroupUpdateView.as_view(), name='update_group'),
    path('delete_confirm_group/<int:pk>/', GroupDeleteView.as_view(), name='delete_confirm_group'),

    # FƏNN
    path('subject_list/', SubjectListView.as_view(), name='subject_list'),
    path('add_subject/', SubjectCreateView.as_view(), name='add_subject'),
    path('update_subject/<int:pk>/', SubjectUpdateView.as_view(), name='update_subject'),
    path('delete_confirm_subject/<int:pk>/', SubjectDeleteView.as_view(), name='delete_confirm_subject'),

    # EXAM
    path('exam_list/', ExamListView.as_view(), name='exam_list'),
    path('add_exam/', ExamCreateView.as_view(), name='add_exam'),
    path('update_exam/<int:pk>/', ExamUpdateView.as_view(), name='update_exam'),
    path('delete_confirm_exam/<int:pk>/', ExamDeleteView.as_view(), name='delete_confirm_exam'),

    # CLASS-NUMBER
    path('class_number_list/', ClassNumberListView.as_view(), name='class_number_list'),
    path('add_class_number/', ClassNumberCreateView.as_view(), name='add_class_number'),
    path('update_class_number/<int:pk>/', ClassNumberUpdateView.as_view(), name='update_class_number'),
    path('delete_confirm_class_number/<int:pk>/', ClassNumberDeleteView.as_view(), name='delete_confirm_class_number'),

    # POSITIONS
    path('positions_list/', PositionListView.as_view(), name='positions_list'),
    path('add_position/', PositionCreateView.as_view(), name='add_position'),
    path('update_position/<int:pk>/', PositionUpdateView.as_view(), name='update_position'),
    path('delete_confirm_position/<int:pk>/', PositionDeleteView.as_view(), name='delete_confirm_position'),

    # PROXIMITY
    path('proximity_list/', ProximityListView.as_view(), name='proximity_list'),
    path('add_proximity/', ProximityCreateView.as_view(), name='add_proximity'),
    path('update_proximity/<int:pk>/', ProximityUpdateView.as_view(), name='update_proximity'),
    path('delete_confirm_proximity/<int:pk>/', ProximityDeleteView.as_view(), name='delete_confirm_proximity'),

    # REPORT
    path('late_payments/', LatePaymentListView.as_view(), name='late_payments'),
    path('export_late_payments/', ExportLatePaymentsExcelView.as_view(), name='export_late_payments'),
    path('daly_payments/', DailyPayments.as_view(), name='daly_payments'),
    path('export_daily_payments/', ExportDailyPaymentsExcelView.as_view(), name='export_daily_payments'),
    path('student_report/', StudentReportListView.as_view(), name='student_report'),
    path('export_student_report/', ExportStudentReportExcelView.as_view(), name='export_student_report'),
]
