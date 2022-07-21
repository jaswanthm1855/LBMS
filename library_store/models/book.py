from django.contrib.auth import get_user_model
from django.db import models

from library_store.constants.enums import BookAvailabilityStatusEnum
from library_store.utils.models_ids import get_book_id

User = get_user_model()


class Book(models.Model):
    book_id = models.CharField(max_length=128, default=get_book_id, primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    author = models.CharField(max_length=50)
    availability_status = models.CharField(
        max_length=50, choices=BookAvailabilityStatusEnum.choices(),
        default=BookAvailabilityStatusEnum.available.value)
    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_removed = models.BooleanField(default=False)


class UserBookBorrowDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey("library_store.Book", on_delete=models.CASCADE)
    borrowed_date_time = models.DateTimeField(auto_now=True)
    is_returned = models.BooleanField(default=False)
    returned_date_time = models.DateTimeField(null=True, blank=True)
