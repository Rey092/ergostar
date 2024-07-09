# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class DdlVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        app_label = "__main__"
        managed = False
        db_table = 'ddl_version'


class LandingHomePage(models.Model):
    id = models.BigAutoField(primary_key=True)
    subtitle_1 = models.CharField(max_length=255)
    subtitle_2 = models.CharField(max_length=255)
    description = models.TextField()
    you_get_label = models.CharField(max_length=255)
    you_get_title = models.CharField(max_length=255)
    you_get_subtitle = models.CharField(max_length=255)
    you_get_block_1_title = models.CharField(max_length=255)
    you_get_block_1_description = models.TextField()
    you_get_block_1_feather_icon = models.CharField(max_length=40)
    you_get_block_2_title = models.CharField(max_length=255)
    you_get_block_2_description = models.TextField()
    you_get_block_2_feather_icon = models.CharField(max_length=40)
    you_get_block_3_title = models.CharField(max_length=255)
    you_get_block_3_description = models.TextField()
    you_get_block_3_feather_icon = models.CharField(max_length=40)
    you_get_block_4_title = models.CharField(max_length=255)
    you_get_block_4_description = models.TextField()
    you_get_block_4_feather_icon = models.CharField(max_length=40)
    get_started_label = models.CharField(max_length=255)
    get_started_title = models.CharField(max_length=255)
    get_started_array = models.CharField(max_length=255)
    get_started_description = models.TextField()
    get_started_lower_title = models.CharField(max_length=255)
    get_started_button_text = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        app_label = "__main__"
        managed = False
        db_table = 'landing__home_page'


class LandingSettings(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    footer_description = models.TextField(blank=True, null=True)
    footer_rights = models.TextField()
    url_login = models.CharField(max_length=255)
    url_api_docs = models.CharField(max_length=255)
    url_register = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        app_label = "__main__"
        managed = False
        db_table = 'landing__settings'


class LandingSnippet(models.Model):
    id = models.BigAutoField(primary_key=True)
    tab = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField()
    code = models.TextField()
    code_language = models.CharField(max_length=20)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    feather_icon = models.CharField(max_length=40)

    class Meta:
        app_label = "__main__"
        managed = False
        db_table = 'landing__snippet'


class LandingSolution(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    title_carousel = models.CharField(max_length=255)
    description = models.TextField()
    is_top_active = models.BooleanField()
    is_carousel_active = models.BooleanField()
    docs_url = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    file = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        app_label = "__main__"
        managed = False
        db_table = 'landing__solution'


class SubscriptionsPlans(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    monthly_price = models.IntegerField(blank=True, null=True)
    monthly_requests_limit = models.IntegerField(blank=True, null=True)
    rate_limit = models.IntegerField(blank=True, null=True)
    rate_period = models.CharField(max_length=255, blank=True, null=True)
    annual_price = models.IntegerField(blank=True, null=True)
    is_public = models.BooleanField()

    class Meta:
        app_label = "__main__"
        managed = False
        db_table = 'subscriptions__plans'
