from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError

# Custom User Model
class User(AbstractUser):
    def __str__(self):
        return self.username  # Using username for clarity

# User Profile to Define Roles
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Faculty', 'Faculty'),
        ('Parent', 'Parent'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Student')  # Default to student

    def __str__(self):
        return f"{self.user.username} | Role: {self.role}"

# Student Model
class Student(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    year_of_study = models.IntegerField()

    def clean(self):
        """ Ensure only students can have a Student profile """
        if self.user_profile.role != 'Student':
            raise ValidationError("User must have role 'Student' to be assigned a Student profile.")

    def __str__(self):
        return f"{self.user_profile.user.username} (Roll No: {self.roll_number})"

# Faculty Model
class Faculty(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)

    def clean(self):
        """ Ensure only faculty can have a Faculty profile """
        if self.user_profile.role != 'Faculty':
            raise ValidationError("User must have role 'Faculty' to be assigned a Faculty profile.")

    def __str__(self):
        return f"{self.user_profile.user.username} (Faculty: {self.subject})"

# Parent Model Using username for clarity

class Parent(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=100, default="Unknown Parent")
    relation_to_student = models.CharField(
        max_length=20,
        choices=[
            ('Father', 'Father'),
            ('Mother', 'Mother'),
            ('Guardian', 'Guardian'),
            ('Other', 'Other'),
        ],
        default='Father'
    )
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def clean(self):
        """ Ensure only parents can have a Parent profile """
        if self.user_profile.role != 'Parent':
            raise ValidationError("User must have role 'Parent' to be assigned a Parent profile.")

    def __str__(self):
        return f"{self.parent_name} ({self.relation_to_student}) - Parent of {self.student.user_profile.user.username}"

# Outpass Model
class Outpass(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    reason = models.TextField()
    destination = models.CharField(max_length=255)
    departure_time = models.DateTimeField(default=now)
    return_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """ Ensure return time is after departure time """
        if self.return_time <= self.departure_time:
            raise ValidationError("Return time must be after departure time.")

    def __str__(self):
        return f"Outpass for {self.student.user_profile.user.username} - {self.status}"

# Approval Model
class Approval(models.Model):
    outpass = models.OneToOneField('Outpass', on_delete=models.CASCADE, related_name='approval')
    approved_by = models.ForeignKey('Faculty', on_delete=models.SET_NULL, null=True, blank=True)
    approved_at = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Approval for {self.outpass.student.user_profile.user.username} by {self.approved_by.user_profile.user.username if self.approved_by else 'N/A'}"
