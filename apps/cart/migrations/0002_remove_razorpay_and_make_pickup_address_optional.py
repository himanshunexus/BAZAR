from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="UPDATE cart_order SET status = 'ready_for_pickup' WHERE status = 'shipped';",
            reverse_sql="UPDATE cart_order SET status = 'shipped' WHERE status = 'ready_for_pickup';",
        ),
        migrations.RunSQL(
            sql="UPDATE cart_order SET status = 'completed' WHERE status = 'delivered';",
            reverse_sql="UPDATE cart_order SET status = 'delivered' WHERE status = 'completed';",
        ),
        migrations.RunSQL(
            sql="UPDATE cart_order SET payment_method = 'pay_at_shop' WHERE payment_method = 'cod';",
            reverse_sql="UPDATE cart_order SET payment_method = 'cod' WHERE payment_method = 'pay_at_shop';",
        ),
        migrations.RemoveField(model_name='order', name='razorpay_order_id'),
        migrations.RemoveField(model_name='order', name='razorpay_payment_id'),
        migrations.AlterField(
            model_name='order', name='customer_address', field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='order', name='status',
            field=models.CharField(
                choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'),
                         ('processing', 'Processing'), ('ready_for_pickup', 'Ready for pickup'),
                         ('completed', 'Completed'), ('cancelled', 'Cancelled')],
                default='pending', max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='order', name='payment_method',
            field=models.CharField(choices=[('pay_at_shop', 'Pay at shop')],
                                  default='pay_at_shop', max_length=20),
        ),
    ]
