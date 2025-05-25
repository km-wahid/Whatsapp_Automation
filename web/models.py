from django.db import models

class CSVFile(models.Model):
    file = models.FileField(upload_to='csv_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.file)


class WhatsAppNumber(models.Model):
    number = models.CharField(max_length=20, unique=True)
    used = models.BooleanField(default=False)  # Marked as sent/not sent
    csv_file = models.ForeignKey(CSVFile, on_delete=models.CASCADE, related_name="numbers")  # Link to CSV file

    def __str__(self):
        return self.number 


class Template(models.Model):
    name = models.CharField(max_length=255)
    message = models.TextField()
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)  # Optional Image
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.db import models

class UserSession(models.Model):
    user_name = models.CharField(max_length=255, unique=True)  # User identifier
    profile_path = models.CharField(max_length=500, unique=True)  # Chrome profile path
    session_created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name

class MessageHistory(models.Model):
    user = models.ForeignKey(UserSession, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.CASCADE)
    sent_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user_name} - {self.template.name} - {self.sent_time}"
    
    
class SenderID(models.Model):
    user_session = models.OneToOneField(UserSession, on_delete=models.CASCADE, related_name='sender_id')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sender ID: {self.user_session.user_name}"
