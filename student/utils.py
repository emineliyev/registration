from docx import Document
from django.conf import settings
import os

from django.utils import timezone

from pathlib import Path
from accounting.models import DocumentTemplate


def generate_contract(student):
    # Предположим, что `student_class` содержит уровень класса
    student_class_level = str(student.student_class)

    # Поиск соответствующего шаблона
    try:
        template = DocumentTemplate.objects.get(class_level=student_class_level)
    except DocumentTemplate.DoesNotExist:
        # Использование стандартного шаблона, если конкретный шаблон для уровня класса не найден
        template = DocumentTemplate.objects.get(class_level='standard')

    template_path = Path(settings.MEDIA_ROOT) / template.file.name

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found at {template_path}")

    document = Document(template_path)

    # Замена плейсхолдеров значениями
    for paragraph in document.paragraphs:
        if '{first_name}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{first_name}', student.first_name)
        if '{last_name}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{last_name}', student.last_name)
        if '{student_class}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{student_class}', str(student.student_class))
        if '{school}' in paragraph.text:
            paragraph.text = paragraph.text.replace('{school}', student.school)
        # Добавьте другие замены по необходимости

    # Сохранение документа
    file_path = Path(settings.MEDIA_ROOT) / 'contracts' / f'{student.work_number}_contract.docx'
    file_path.parent.mkdir(parents=True, exist_ok=True)
    document.save(file_path)

    return file_path

