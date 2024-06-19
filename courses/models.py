from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField


# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title


class Course(models.Model):
    owner = models.ForeignKey(
        User,
        related_name="courses_created",
        on_delete=models.CASCADE,
    )
    subject = models.ForeignKey(
        Subject,
        related_name="courses",
        on_delete=models.CASCADE,
    )
    students = models.ManyToManyField(
        User,
        related_name="courses_joined",
        blank=True,
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return self.title


class Module(models.Model):
    course = models.ForeignKey(
        Course,
        related_name="modules",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=["course"])

    class Meta:
        ordering = ["order"]

    def __str__(self) -> str:
        return f"{self.order}. {self.title}"


class Content(models.Model):
    module = models.ForeignKey(
        Module,
        related_name="contents",
        on_delete=models.CASCADE,
    )
    # set up a generic relation
    # A ForeignKey field to the ContentType model.
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "model__in": (
                "text",
                "video",
                "image",
                "file",
            )
        },
    )
    # A PositiveIntegerField to store the primary key of the related object.
    object_id = models.PositiveIntegerField()
    # A GenericForeignKey field to the related object combining the two previous fields.
    item = GenericForeignKey("content_type", "object_id")
    order = OrderField(blank=True, for_fields=["module"])

    class Meta:
        ordering = ["order"]

    """
    Only the content_type and object_id fields have a corresponding column in the database table of
    this model. The item field allows you to retrieve or set the related object directly, and its functionality
    is built on top of the other two fields.
    """


class ItemBase(models.Model):
    owner = models.ForeignKey(
        User, related_name="%(class)s_related", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to="files")


class Image(ItemBase):
    file = models.FileField(upload_to="images")


class Video(ItemBase):
    url = models.URLField()
