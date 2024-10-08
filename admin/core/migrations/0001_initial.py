# Generated by Django 5.0.7 on 2024-08-11 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="SubscriptionPlansUnfold",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Заголовок")),
                (
                    "subtitle",
                    models.CharField(max_length=255, verbose_name="Подзаголовок"),
                ),
                (
                    "monthly_price",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Ежемесячная цена, USD"
                    ),
                ),
                (
                    "annual_price",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Годовая цена, USD"
                    ),
                ),
                (
                    "monthly_requests_limit",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Лимит ежемесячных запросов"
                    ),
                ),
                (
                    "rate_limit",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Лимит скорости"
                    ),
                ),
                (
                    "rate_period",
                    models.CharField(
                        blank=True, max_length=255, verbose_name="Период скорости"
                    ),
                ),
                ("is_public", models.BooleanField(verbose_name="Публичный")),
                ("created_at", models.DateTimeField(verbose_name="Дата создания")),
                ("updated_at", models.DateTimeField(verbose_name="Дата обновления")),
            ],
            options={
                "db_table": "subscription_plans",
                "managed": False,
            },
        ),
    ]
