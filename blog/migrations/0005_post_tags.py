# Generated by Django 5.0.2 on 2024-02-12 00:57

import taggit.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_comment_comment_blog_commen_created_4e025c_idx"),
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="tags",
            field=taggit.managers.TaggableManager(
                help_text="A comma-separated list of tags.",
                through="taggit.TaggedItem",
                to="taggit.Tag",
                verbose_name="Tags",
            ),
        ),
    ]
