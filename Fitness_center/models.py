from datetime import datetime


from django.db import models


class Client(models.Model):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(max_length=100, blank=False, null=False)
    phone = models.CharField(max_length=15, blank=False, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TrainingType(models.Model):
    name = models.CharField(max_length=100,blank=False, null=False, choices=[
        ('Хатха-йога', 'Хатха-йога'),
        ('Аштанга-йога', 'Аштанга-йога'),
        ('Інь-йога', 'Інь-йога'),
        ('Тренування в залі (індивідуально)', 'Тренування в залі (індивідуально)'),
        ('Тренування в залі (з тренером)', 'Тренування в залі (з тренером)'),
    ])
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, null=False)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user_id = models.ForeignKey(Client, on_delete=models.CASCADE, blank=False, null=False)
    subscription_purchase_date = models.DateField(blank=False, null=False)
    subscription_end_date = models.DateField(blank=False, null=False)

    # статус підписки
    status = models.CharField(max_length=50,blank=False, null=False, choices=[
        ('Активна', 'Активна'),
        ('Неактивна', 'Неактивна'),
        ('Припинена', 'Припинена'),
    ])

    # стать або гендер
    gender = models.CharField(max_length=10, blank=False, null=False, choices=[
        ('Чоловіча', 'Чоловіча'),
        ('Жіноча', 'Жіноча'),
    ])

    # тип тренування
    training_type = models.ForeignKey(TrainingType, on_delete=models.CASCADE, blank=False, null=False)

    # період підписки
    subscription_period = models.IntegerField(default=30, blank=False, null=False)

    def __str__(self):
        return f"Підписка для {self.user_id} - {self.subscription_purchase_date}"

    # обробник події pre_save для поля training_type
    def pre_save(self, **kwargs):
        # перевіряємо, чи було змінено поле training_type
        if self.training_type != self._old_training_type:
            # зберігаємо поточне значення поля subscription_period
            self._old_subscription_period = self.subscription_period
            # встановлюємо значення поля price відповідно до значення поля training_type
            self.price = self.training_type.price
        return

    # обробник події post_save для поля subscription_period
    def post_save(self, **kwargs):
        # обчислюємо дату закінчення підписки
        self.subscription_end_date = self.subscription_purchase_date + datetime.timedelta(days=self.subscription_period)

