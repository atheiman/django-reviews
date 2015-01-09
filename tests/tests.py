"""Test Review and Reviewable with a web store use case."""

from decimal import *
import time
import datetime

from django.test import TestCase
from django.conf import settings

from .models import Product
from reviews.models import Review
from django.contrib.auth.models import User

from .factories import UserFactory, ProductFactory, ReviewFactory




class ModelsTestCase(TestCase):
    def test_relationships(self):
        """Test accessing objects across relationships."""
        u_1 = UserFactory()
        u_2 = UserFactory()
        u_3 = UserFactory()
        p_1 = ProductFactory()
        p_2 = ProductFactory()
        p_3 = ProductFactory()
        r_1 = ReviewFactory(reviewed_object=p_1, user=u_1)
        r_2 = ReviewFactory(reviewed_object=p_1, user=u_2)
        r_3 = ReviewFactory(reviewed_object=p_2, user=u_2)

        # product -> reviews
        self.assertIn(r_1, p_1.reviews.all())
        # product -> user
        self.assertEqual(u_2.username, p_2.reviews.get(user=u_2).user.username)
        # user -> reviews
        self.assertIn(r_3, u_2.reviews.all())
        # user -> product
        self.assertEqual(p_1.name, u_2.reviews.get(product=p_1).reviewed_object.name)
        # reviews -> user
        self.assertIn(u_1.reviews.all()[0], Review.objects.filter(user__username=u_1.username))
        self.assertFalse(Review.objects.filter(user=u_3).exists())
        # reviews -> product
        self.assertIn(p_2.reviews.all()[0], Review.objects.filter(product__name=p_2.name))
        self.assertFalse(Review.objects.filter(product=p_3).exists())

    def test_reviewable(self):
        """Test reviews.models.Reviewable.avg_review_score()."""
        p_1 = ProductFactory()
        p_2 = ProductFactory()
        p_3 = ProductFactory()
        u_1 = UserFactory()
        u_2 = UserFactory()
        r_1 = ReviewFactory(
            user = u_1,
            reviewed_object = p_1,
            score = 3,
        )
        r_2 = ReviewFactory(
            user = u_1,
            reviewed_object = p_2,
            score = 3,
        )
        r_3 = ReviewFactory(
            user = u_2,
            reviewed_object = p_1,
            score = 4,
        )

        self.assertEqual(p_1.avg_review_score(), Decimal(3.5))
        self.assertEqual(p_2.avg_review_score(), Decimal(3.0))
        self.assertEqual(p_3.avg_review_score(), None)

    def test_review_avg_review_score(self):
        """Test reviews.models.Review.is_updated()."""
        u_1 = UserFactory()
        p_1 = ProductFactory()
        r_1 = ReviewFactory(reviewed_object = p_1, user = u_1)

        self.assertFalse(r_1.is_updated())

        time.sleep(
            settings.DJANGO_REVIEWS.get('UPDATED_COMPARISON_SECONDS') + 1
        )

        r_1.score += 1
        r_1.save()

        self.assertIsInstance(r_1.is_updated(), datetime.datetime)

    def test_review_is_publishable(self):
        u_1 = UserFactory()
        p_1 = ProductFactory()
        r_1 = ReviewFactory(reviewed_object = p_1, user = u_1)

        self.assertFalse(r_1.is_publishable())
        r_1.approved = True
        self.assertTrue(r_1.is_publishable())
