class ExportLatePaymentsExcelView(View):
    """
    Экспорт просроченных сумм
    """
    def get(self, request, *args, **kwargs):
        # Создание Excel файла
        workbook = openpyxl.Workbook()
        worksheet = workbook.active
        worksheet.title = "Late Payments"

        # Заголовки столбцов
        columns = [
            "İş nömrə", "Ad", "Soyad", "Sinif", "Qrup", "Sinif коду", "Bölmə",
            "Məhsul şəxsin telefonu", "Ümumi məbləğ", "Ödənən məbləğ", "Gecикən məbləğ", "Gecикən taksit sayı",
            "Gecикən taksit tarixləri"
        ]
        row_num = 1

        # Добавление заголовков в первую строку
        for col_num, column_title in enumerate(columns, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = column_title

        # Получение данных студентов
        students = Student.objects.filter(is_debtor=True).select_related('student_class', 'group', 'class_number')

        # Получение данных студентов
        queryset = Student.objects.filter(
            tuitionfeesplit__payment_date=payment_date
        ).distinct()

        year = request.GET.get('year')
        work_number = request.GET.get('work_number__icontains')
        first_name = request.GET.get('first_name__icontains')
        last_name = request.GET.get('last_name__icontains')
        student_class = request.GET.get('student_class')

        group = request.GET.get('group')
        class_number = request.GET.get('class_number')
        section = request.GET.get('section')

        overdue_date_gte = request.GET.get('overdue_date__gte')
        overdue_date_lte = request.GET.get('overdue_date__lte')

        if year:
            queryset = queryset.filter(year_id=year)
        if work_number:
            queryset = queryset.filter(work_number__icontains=work_number)
        if first_name:
            queryset = queryset.filter(first_name__icontains=first_name)
        if last_name:
            queryset = queryset.filter(last_name__icontains=last_name)
        if student_class:
            queryset = queryset.filter(student_class_id=student_class)

        if group:
            queryset = queryset.filter(group_id=group)
        if class_number:
            queryset = queryset.filter(class_number_id=class_number)
        if section:
            queryset = queryset.filter(section_id=section)

        if overdue_date_gte and overdue_date_lte:
            queryset = queryset.filter(
                tuitionfeesplit__payment_date__gte=overdue_date_gte,
                tuitionfeesplit__payment_date__lte=overdue_date_lte
            ).distinct()

        # Добавление данных студентов в таблицу
        for student in students:
            tuition_fee = TuitionFee.objects.filter(student=student).first()
            total_paid, debt_months, debt_amount, overdue_installment_dates = self.calculate_payments(student)

            row_num += 1
            row = [
                student.work_number, student.first_name, student.last_name,
                student.student_class.name, student.group.name, student.class_number.number,
                student.get_section_display(), student.responsible_phone_1,
                tuition_fee.annual_fee if tuition_fee else 0, total_paid, debt_amount, debt_months,
                overdue_installment_dates
            ]

            for col_num, cell_value in enumerate(row, 1):
                cell = worksheet.cell(row=row_num, column=col_num)
                cell.value = cell_value

        # Сохранение рабочей книги в память
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=geciken_odenisler.xlsx'
        workbook.save(response)
        return response

    def calculate_payments(self, student):
        # Получаем годовую оплату
        tuition_fee = TuitionFee.objects.filter(student=student).first()
        annual_fee = tuition_fee.annual_fee if tuition_fee else 0

        # Подсчет суммы, которую студент уже оплатил
        total_paid = TuitionFeeSplit.objects.filter(student=student, payment_date__isnull=False).aggregate(
            total=models.Sum('payment_amount'))['total'] or 0

        # Подсчет месяцев с задолженностью и суммы долга
        today = date.today()
        unpaid_installments = TuitionFeeSplit.objects.filter(student=student, payment_date__isnull=True,
                                                             installment_date__lt=today)
        debt_months = unpaid_installments.count()
        debt_amount = unpaid_installments.aggregate(total=models.Sum('installment_amount'))['total'] or 0

        overdue_installment_dates = ", ".join(
            [str(installment.installment_date) for installment in unpaid_installments])

        return total_paid, debt_months, debt_amount, overdue_installment_dates