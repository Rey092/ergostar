"""Unfold core app models."""

from django.db import models


class SubscriptionPlansUnfold(models.Model):
    """Subscription plans table."""

    id = models.UUIDField(primary_key=True, verbose_name="ID")
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    subtitle = models.CharField(max_length=255, verbose_name="Подзаголовок")
    monthly_price = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Ежемесячная цена, USD",
    )
    annual_price = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Годовая цена, USD",
    )
    monthly_requests_limit = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Лимит ежемесячных запросов",
    )
    rate_limit = models.IntegerField(
        blank=True,
        null=True,
        verbose_name="Лимит скорости",
    )
    rate_period = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Период скорости",
    )
    is_public = models.BooleanField(verbose_name="Публичный")
    created_at = models.DateTimeField(verbose_name="Дата создания")
    updated_at = models.DateTimeField(verbose_name="Дата обновления")

    class Meta:
        """Meta class."""

        managed = False
        db_table = "subscription_plans"

    def __str__(self):
        """Return string representation."""
        return self.title
