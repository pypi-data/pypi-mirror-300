import uuid
import threading
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

USER = get_user_model()

thread_local = threading.local()


def get_current_user():
    return  getattr(thread_local, 'user', None)


class BaseModel(models.Model):
    """
    Base model for other models
    """
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        primary_key=True,
        verbose_name=_('uuid')
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at?')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated at?')
    )

    created_by = models.ForeignKey(
        to=USER,
        verbose_name=_('Created by'),
        null=True,
        blank=True,
        related_name='%(class)s_created',
        on_delete=models.PROTECT
    )

    updated_by = models.ForeignKey(
        to=USER,
        verbose_name=_('Updated by'),
        null=True,
        blank=True,
        related_name='%(class)s_updated',
        on_delete=models.PROTECT
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is active?')
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Override the save method to set created_by and updated_by fields.
        """
        user = get_current_user()
        if user:
            if not self.created_by:  # Set created_by only on creation
                self.created_by = user

            self.updated_by = user  # Always set updated_by
        super(BaseModel, self).save(*args, **kwargs)

    @classmethod
    def get_all_default_model_fields_name(cls):
        """
        Return list of all fields of this model
        """
        field_name = []
        for field in cls._meta.fields:
            field_name.append(field.name)
        return field_name

    @classmethod
    def active(cls):
        """
        Get list of active objects
        @return: Filtered queryset
        """
        return cls.objects.filter(is_active=True)

    @classmethod
    def inactive(cls):
        """
        Get list of inactive objects
        @return: Filtered queryset
        """
        return cls.objects.filter(is_active=False)
