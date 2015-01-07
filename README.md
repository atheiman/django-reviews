# django-reviews

Simple abstract base classes to make implementing a review system easy.



## Basic Usage

1.  Install django-reviews from GitHub using pip:

    `pip install git+ssh://git@github.com/atheiman/django-reviews.git@master`

1.  In your app's `models.py` import the base classes and create your reviewable model and review model:

    ```python
    from reviews.models import Reviewable, Review
    from django.db import models
    from django.contrib.auth.models import User

    class Product(Reviewable):
        name = models.CharField(max_length=40)
        # ...
        reviews = models.ManyToManyField(
            'User',                                           # Reviews are tied to a User instance
            through='ProductReview',                          # Subclass of reviews.models.Review
            related_name='%(app_label)s_%(class)s_reviews',   # related_name available from User instance
        )
        # ...

    class ProductReview(Review):
        product = models.ForeignKey('Product')

        def __unicode__(self):
            return "product: {p}, score: {s}, user: {u}" % (
                     p=self.product, s=self.score, u=self.user.username)

        class Meta:
            unique_together = ("product", "user")   # only allow one review per product per user
    ```

1.  Utilize the functionality of the models:

    ```python
    >>> from my_app.models import Product, ProductReview, User
    >>> product = Product(name="22-inch television")
    >>> product.save()
    >>> user = User.objects.create_user(username="joetest")
    >>> product_review = ProductReview(
    ...   product = product,
    ...   user = user,
    ...   score = 4,          # score is by default an int greater than 0 but less than 6
    ...   comment = "This is a nice tv, I would buy it again.",
    ... )
    >>> product_review.save()
    >>> user.reviews.all()
    #####################
    >>> user.avg_review_score()
    #####################
    ```



## More Info

These base classes are not that complex currently. To see all available fields, simply [browse the code](https://github.com/atheiman/django-reviews/blob/master/reviews/models.py)



## Features to be Added

- [X] prevent user submitting multiple reviews
- [ ] Review.updated() return False or update DateTime
