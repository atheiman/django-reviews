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



## Basic Usage

```python

```



## More Info

These classes are not that complex currently. To see all available fields, simply [browse the code](https://github.com/atheiman/django-reviews/blob/master/reviews/models.py)



## Features to be Added

- [ ] import settings dict from django settings
- [ ] prevent user submitting multiple reviews
- [x] Review.updated() return False or updated DateTime
- [ ] Reviewable.reviews = GenericRelation(Review, related_query_name='%(class)ss')
- [ ] get all reviews pointing to a specific class
- [ ] admin site
