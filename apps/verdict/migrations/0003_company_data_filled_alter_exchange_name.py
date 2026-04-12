from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("verdict", "0002_company_needs_research"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="data_filled",
            field=models.BooleanField(
                default=False,
                help_text="Set automatically when the AI agent fills in company details from the ticker.",
            ),
        ),
        migrations.AlterField(
            model_name="company",
            name="name",
            field=models.CharField(blank=True, help_text="Leave blank — AI agent will fill this in from the ticker.", max_length=200),
        ),
    ]
