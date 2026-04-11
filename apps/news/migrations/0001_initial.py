from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="NewsCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(unique=True)),
                ("icon_class", models.CharField(blank=True, help_text="Bootstrap icon class, e.g. bi-gem", max_length=50)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["sort_order", "name"],
                "verbose_name_plural": "news categories",
            },
        ),
        migrations.CreateModel(
            name="NewsLink",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("headline", models.CharField(max_length=300)),
                ("url", models.URLField(max_length=500)),
                ("url_hash", models.CharField(db_index=True, editable=False, max_length=64, unique=True)),
                ("source_name", models.CharField(max_length=100)),
                ("snippet", models.CharField(blank=True, max_length=300)),
                ("is_featured", models.BooleanField(db_index=True, default=False)),
                ("is_breaking", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(db_index=True, default=True)),
                ("added_by", models.CharField(choices=[("agent", "Agent"), ("manual", "Manual")], default="manual", max_length=10)),
                ("position", models.PositiveIntegerField(default=0)),
                ("published_at", models.DateTimeField(auto_now_add=True)),
                ("expires_at", models.DateTimeField(blank=True, null=True)),
                ("click_count", models.PositiveIntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="news.newscategory")),
            ],
            options={
                "ordering": ["-is_featured", "position", "-published_at"],
                "indexes": [
                    models.Index(fields=["is_active", "category", "-published_at"], name="news_newsl_is_acti_cat_pub"),
                    models.Index(fields=["is_active", "is_featured", "-published_at"], name="news_newsl_is_acti_feat_pub"),
                ],
            },
        ),
    ]
