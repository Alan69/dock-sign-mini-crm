from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

STATUS = (
    ('подписан', 'подписан'),
    ('не подписан', 'не подписан'),
)

class Document(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='не подписан', choices=STATUS)
    count = models.IntegerField(blank=True, null=True, default=0)

    def __str__(self):
        return self.name

class DockSignGroup(models.Model):
    users = models.ManyToManyField(User, related_name='docksign_groups')
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    signed_by = models.ManyToManyField(User, related_name='signed_documents', blank=True)
    created_by = models.ForeignKey(User, related_name='created_docksign_groups', on_delete=models.CASCADE)

    def __str__(self):
        return f"DockSignGroup for {self.document.name}"

    def add_user(self, current_user, new_user):
        """Method to allow a user to add another user to the group."""
        if current_user in self.users.all() or current_user == self.created_by:
            self.users.add(new_user)
            self.save()
            return True
        return False

    def sign_document(self, user):
        """Method to add a user's signature to the document."""
        if user in self.users.all() and user not in self.signed_by.all():
            self.signed_by.add(user)
            self.save()

    def is_document_signed(self):
        """Method to check if more than 50% of users have signed the document."""
        total_users = self.users.count()
        signed_users = self.signed_by.count()
        return signed_users > total_users / 2