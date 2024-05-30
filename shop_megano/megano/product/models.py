from django.db import models

class Product(models.Model):
    """
    Класс описывающий модель продукта
    """
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = 'Products'
        ordering = ['pk', 'name']

    def __str__(self):
        return self.name

    name = models.CharField(max_length=200, null=False, blank=True) # название
    description = models.CharField(max_length=200, null=False, blank=True) # описание
    price = models.DecimalField(default=1, max_digits=8, decimal_places=2, null=False) # цена
    count = models.IntegerField(default=1, null=False) # количество
    count_reviews = models.IntegerField(default=0, null=False) # количество отзывов
    rating = models.DecimalField(default=0, max_digits=5, decimal_places=2, null=False) # рейтинг продукта
    created_date = models.DateTimeField(auto_now_add=True, null=False) # дата создания
    archived = models.BooleanField(default=False) # архив
    freeDelivery = models.BooleanField(default=True) # бесплатная доставка
    # категория, теги, изображения

