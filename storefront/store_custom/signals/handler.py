from django.dispatch import receiver
from store.signals import order_created

@receiver(order_created)
def create_order_notif(sender,**kwargs):
    print(kwargs['order'])