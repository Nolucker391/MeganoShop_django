from django.db import models


def category_image_directory_path(instance: "CategoryImage", filename) -> str:
    '''
    Функция для сохранения пути фотографии, в директории.
    :param instance:
    :param filename:
    :return:
    '''
    if instance.category.parent:
        return (f"categories/"
                f"category_{instance.category.parent.pk}/"
                f"subcategory_{instance.category.pk}/"
                f"{filename}")
    else:
        return (f"categories/"
                f"category_{instance.category.pk}/"
                f"{filename}")


def product_images_directory_path(instance: 'ProductImage', filename: str) -> str:
    '''
    Функция для сохранения пути фотографии, в директории.
    :param instance:
    :param filename:
    :return:
    '''
    return (f'products/'
            f'product_{instance.product.pk}/'
            f'{filename}')


class CategoryProduct(models.Model):
    """
    Класс модель категории продукта.
    """
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['pk', 'title']

    title = models.CharField(max_length=40, db_index=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
    )
    favourite = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.title!r}"


class CategoryImage(models.Model):
    '''
    Класс модель фотографии категории.
    '''
    class Meta:
        verbose_name = 'Category image'
        verbose_name_plural = 'Category images'
        ordering = ['pk', ]

    category = models.OneToOneField(
        CategoryProduct,
        on_delete=models.CASCADE,
        related_name='image',
        blank=True,
        null=True,
    )
    src = models.ImageField(
        upload_to=category_image_directory_path,
    )

    def alt(self):
        return self.category.title

    def __str__(self):
        return f'{self.src}'


class Product(models.Model):
    """
    Класс описывающий модель продукта
    """
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = 'Products'
        ordering = ['pk', 'title']

    def __str__(self):
        return self.title

    title = models.CharField(max_length=200, null=False, blank=True) # название
    description = models.CharField(max_length=200, null=False, blank=True) # описание
    price = models.DecimalField(default=1, max_digits=8, decimal_places=2, null=False) # цена
    count = models.IntegerField(default=1, null=False) # количество
    rating = models.DecimalField(default=0, max_digits=5, decimal_places=2, null=False) # рейтинг продукта
    date = models.DateTimeField(auto_now_add=True, null=False) # дата создания
    archived = models.BooleanField(default=False) # архив
    freeDelivery = models.BooleanField(default=True) # бесплатная доставка
    limited_edition = models.BooleanField(default=False) # ограниченое количество
    fullDescription = models.TextField(null=False,blank=True) # полное описание
    sale_status = models.BooleanField(default=False)
    category = models.ForeignKey(
        CategoryProduct,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
    )

    # sale1 = models.ForeignKey(
    #     Sale,
    #     default=False,
    #     null=True,
    #     related_name='sales',
    # )
    def get_curr_price(self):
        if self.sale_status:
            return Sale.objects.filter(product=self)[0].salePrice
        else:
            return self.price


class ProductImage(models.Model):
    '''
    Класс модель фотографии продукта.
    '''
    class Meta:
        verbose_name = 'Product image'
        verbose_name_plural = 'Product images'
        ordering = ['pk', ]

    name = models.CharField(
        max_length=100,
        null=False,
        blank=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='product',
    )
    image = models.ImageField(
        upload_to=product_images_directory_path,
    )

    def src(self):
        return self.image

    def __str__(self):
        return f'{self.image}'

class Tag(models.Model):
    """Модель тэга продукта"""

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['pk', 'name']

    name = models.CharField(
        max_length=20,
        null=False,
        blank=True,
    )
    tags = models.ManyToManyField(
        Product,
        related_name='tags',
    )

    def __str__(self) -> str:
        return f'{self.name!r}'

class ProductSpecification(models.Model):
    """Модель характеристики продукта"""

    class Meta:
        verbose_name = 'Product specification'
        verbose_name_plural = 'Product specifications'

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='specifications',
    )

    name = models.CharField(
        max_length=200,
        default="",
    )
    value = models.CharField(
        max_length=200,
        default="",
    )


class Review(models.Model):
    """Модель отзыва на продукт"""

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'
        ordering = ['pk', 'rate']

    author = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    text = models.TextField()
    rate = models.PositiveSmallIntegerField(
        default=3,
        blank=False,
    )
    date = models.DateTimeField(
        auto_now_add=True,
        null=False,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='reviews'
    )

    def __str__(self) -> str:
        return f"{self.author!r}: {self.product.title!r}"


class Sale(models.Model):
    """Модель акции на продукт"""

    class Meta:
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'
        ordering = ['pk']

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='sales'
    )
    salePrice = models.DecimalField(
        default=1,
        max_digits=8,
        decimal_places=2,
        null=False,
    )
    dateFrom = models.DateField(default='')
    dateTo = models.DateField(
        blank=True,
        null=False,
    )

    def price(self):
        return self.product.price

    def title(self):
        return self.product.title

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.product.sale_status = True

        super().save(*args, **kwargs)