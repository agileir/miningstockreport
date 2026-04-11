from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CommodityPrice",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("symbol", models.CharField(help_text="Yahoo Finance symbol, e.g. GC=F", max_length=20, unique=True)),
                ("name", models.CharField(help_text="Display name, e.g. Gold", max_length=50)),
                ("price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("change_pct", models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ("unit", models.CharField(default="/oz", help_text="Unit label, e.g. /oz, /lb", max_length=20)),
                ("fetched_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
    ]
