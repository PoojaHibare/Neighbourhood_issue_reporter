from django.db import models

CATEGORY_CHOICES = [
    ('Pothole', 'Pothole'),
    ('Streetlight', 'Streetlight'),
    ('Water Leakage', 'Water Leakage'),
    ('Garbage', 'Garbage'),
    ('Other', 'Other'),
]

STATUS_CHOICES = [
    ('Reported', 'Reported'),
    ('Verified', 'Verified'),
    ('Assigned', 'Assigned'),
    ('In Progress', 'In Progress'),
    ('Resolved', 'Resolved'),
    ('Closed', 'Closed'),
    ('Rejected', 'Rejected'),
]

PRIORITY_CHOICES = [
    ('Low', 'Low'),
    ('Medium', 'Medium'),
    ('High', 'High'),
]

class Issue(models.Model):
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    location_name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='issue_images/', blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Reported')
    assigned_department = models.CharField(max_length=120, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='Medium')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.category} at {self.location_name} ({self.status})'
