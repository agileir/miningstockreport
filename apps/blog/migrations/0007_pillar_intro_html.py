from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0006_post_geo_target_post_post_type_post_ranked_items"),
    ]

    operations = [
        migrations.AddField(
            model_name="pillar",
            name="intro_html",
            field=models.TextField(
                blank=True,
                help_text=(
                    "Long-form on-page intro for the pillar landing page. "
                    "Rendered as HTML below the header and filter bar. "
                    "Aim for 300-400 unique words per pillar to avoid thin-content SEO flags."
                ),
            ),
        ),
    ]
