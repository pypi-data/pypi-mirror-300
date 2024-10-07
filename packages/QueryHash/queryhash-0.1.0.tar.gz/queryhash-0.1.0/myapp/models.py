from django.db import models

# Create your models here.
class HashRecord(models.Model):
    query = models.TextField(default='')
    query_hash = models.CharField(max_length=64, default='')
    response_hash = models.CharField(max_length=64, default='')
    count = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('query_hash', 'response_hash')

    def __str__(self):
        return f"Query Hash: {self.query_hash}, Response Hash: {self.response_hash}"