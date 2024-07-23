from django.db import models


class DocumentTemplate(models.Model):
    CLASS_CHOICES = [
        ('standard', 'Digər'),
        ('0', 'Məktəbəqədər'),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
    ]

    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='document_templates/')
    class_level = models.CharField(max_length=10, choices=CLASS_CHOICES, default='standard')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.uploaded_at}"

    def delete(self, *args, **kwargs):
        self.file.delete()
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = "Müqavilə"
        verbose_name_plural = "Müqavilə"
