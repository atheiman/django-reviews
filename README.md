# django-reviews

Simple abstract base classes to make implementing a review system easy.



## Gettings Started

1.  Install django-reviews from GitHub using pip:

    `pip install git+ssh://git@github.com/atheiman/django-reviews.git@master#egg=reviews`

1.  Add django-reviews to your `INSTALLED_APPS`. Be sure the [contenttypes framework](https://docs.djangoproject.com/en/1.7/ref/contrib/contenttypes/#django.contrib.contenttypes.generic.GenericForeignKey) is there too (in a default django project creation, it should be there).

    ```python
    INSTALLED_APPS = (
        # ...
        'django.contrib.contenttypes',
        'reviews',
        # ...
    )
    ```

1.  In your app's `models.py` import the necessary classes and create your reviewable model:

    ```python
    from django.db import models
    from django.contrib.contenttypes.fields import GenericRelation
    from reviews.models import Review, Reviewable

    class Product(Reviewable):
        name = models.CharField(max_length=40)

        reviews = GenericRelation(Review, related_query_name="products")

        def __unicode__(self):
            return self.name
    ```



## Usage

Create reviews with `Review.objects.create()`. `user.reviews.add()` or `Reviewable.reviews.add()` will not work.

```python
>>> from reviews.models import Review
>>> from django.contrib.auth.models import User
>>> from simple_app.models import Product
>>>
>>> user = User.objects.create_user(username='joetest')
>>> product = Product.objects.create(name='22-inch TV')
>>> review = Review.objects.create(
...   reviewed_object = product,
...   user = user,
...   score = 3,
...   comment = "I like this tv a lot, I would buy it again.",
... )
```

Simple lookups across the relationships:

```python
>>> user.reviews.all()
[<Review: object: 22-inch TV, score: 3, user: joetest>]
>>> product.reviews.all()
[<Review: object: 22-inch TV, score: 3, user: joetest>]
```

Reverse lookups from the Review table as well:

```python
>>> Review.objects.filter(products__name__contains='tv')
[<Review: object: 22-inch TV, score: 3, user: joetest>]
>>> Review.objects.filter(user__username__contains='joe')
[<Review: object: 22-inch TV, score: 3, user: joetest>]
```

Extra functions built into Reviewable base model:

```python
>>> user_2 = User.objects.create_user(username='atheiman')
>>> review_2 = Review.objects.create(
...   reviewed_object = product,
...   user = user_2,
...   score = 4,
...   comment = "This is an outstanding television!",
... )
>>> product.avg_review_score()
Decimal('3.5')
```

Functionality available in Review:

```python
>>> review.is_updated()    # returns False if no updates
False
>>> review.score = 1
>>> review.comment = "After using the tv for more than 10 seconds, it broke."
>>> review.save()
>>> review.is_updated()    # returns updated datetime if updated
datetime.datetime(2015, 1, 7, 19, 20, 15, 723908, tzinfo=<UTC>)
```



## More Info

These models are not all that complex currently. To see all available fields, simply [browse the code](https://github.com/atheiman/django-reviews/blob/master/reviews/models.py)
