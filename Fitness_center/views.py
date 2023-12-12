import datetime

from django.core.checks import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Subscription, TrainingType
from .forms import SubscriptionCreateForm


@login_required
def subscription_create(request):
    if request.method == "POST":
        # отримуємо форму з запиту
        form = SubscriptionCreateForm(request.POST)

        # перевіряємо форму
        if form.is_valid():
            # отримуємо дані з форми
            training_type = form.cleaned_data["training_type"]
            subscription_purchase_date = form.cleaned_data["subscription_purchase_date"]

            # перевіряємо тип тренування
            try:
                training_type_obj = TrainingType.objects.get(name=training_type)
            except TrainingType.DoesNotExist:
                messages.error(request, "Неправильний тип тренування")
                return render(request, "subscription_create.html", {"form": form})

            # перевіряємо дату покупки
            if subscription_purchase_date < datetime.date.today():
                messages.error(request, "Дата покупки не може бути в минулому")
                return render(request, "subscription_create.html", {"form": form})

            # перевіряємо дату закінчення підписки
            subscription_end_date = subscription_purchase_date + datetime.timedelta(days=30)
            if subscription_end_date < datetime.date.today():
                messages.error(request, "Дата закінчення підписки має бути не менше сьогоднішньої дати")
                return render(request, "subscription_create.html", {"form": form})

            # створюємо модель Subscription
            subscription = Subscription(
                user=request.user,
                training_type=training_type_obj,
                subscription_purchase_date=subscription_purchase_date,
            )

            # зберігаємо модель
            subscription.save()

            # перенаправляємо користувача на головну сторінку
            return redirect("/")
        else:
            # форму не пройшла перевірку
            # формуємо контекст для шаблону
            context = {
                "form": form,
            }

            return render(request, "subscription_create.html", context)

    else:
        # отримуємо всі типи тренувань
        training_types = TrainingType.objects.all()

        # створюємо порожню форму
        form = SubscriptionCreateForm()

        # формуємо контекст для шаблону
        context = {
            "form": form,
        }

        return render(request, "subscription_create.html", context)
