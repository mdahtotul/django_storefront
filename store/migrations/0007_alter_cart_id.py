# Generated by Django 4.2.4 on 2023-08-09 14:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_cartitem_cart_alter_cartitem_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
