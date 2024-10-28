# Generated by Django 5.0.6 on 2024-06-29 06:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Paymentmethod",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("method", models.CharField(max_length=255)),
            ],
            options={
                "ordering": ("method",),
            },
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("subs", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name_plural": "Subscriptions",
                "ordering": ("subs",),
            },
        ),
        migrations.CreateModel(
            name="GymMembers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(blank=True, max_length=200, null=True)),
                ("phone_number", models.CharField(max_length=10)),
                ("address", models.CharField(max_length=500)),
                ("city", models.CharField(max_length=100)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user_profile_image",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gym_memberships",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "pay_method",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gym_memberships",
                        to="members.paymentmethod",
                    ),
                ),
                (
                    "sub_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gym_memberships",
                        to="members.subscription",
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
            },
        ),
    ]