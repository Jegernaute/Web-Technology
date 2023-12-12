from django.forms import ModelForm
from .models import Subscription


class SubscriptionCreateForm(ModelForm):
    class Meta:
        model = Subscription
        fields = ["training_type", "subscription_purchase_date"]