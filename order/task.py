from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def send_order_message(order_id):
    """
    Task to send messages after order created"
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order # {}'.format(order_id)
    message = 'Dear {} \n\nYou have successfully placed an order. \'' \
              'Your order number is {}.'.format(order.user_email, order_id)
    mail_send = send_mail(
        subject,
        message,
        'rudavinp@gmail.com',
        [order.user_email]
    )
    return mail_send
