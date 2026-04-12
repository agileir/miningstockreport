from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("verdict", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="needs_research",
            field=models.BooleanField(
                default=False,
                help_text="Flag for the AI agent to research and generate a verdict scorecard.",
            ),
        ),
    ]
