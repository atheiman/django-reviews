"""Test Review and Reviewable with a web store use case."""

from decimal import *
import time

from django.test import TestCase
from django.contrib.auth.models import User

from .models import *



class ModelsTestCase(TestCase):
    def setUp(self):
        """Create users, products, and reviews."""
        u_1 = User.objects.create_user(username='joetest')
        u_2 = User.objects.create_user(username='atheiman')
        u_3 = User.objects.create_user(username='willie')
        p_1 = Product.objects.create(name='22-inch TV')
        p_2 = Product.objects.create(name='8-inch Tablet')
        p_3 = Product.objects.create(name='Kitchen Table')
        r_1 = Review.objects.create(
            reviewed_object = p_1,
            user = u_1,
            score = 3,
            comment = "I like this tv a lot, I would buy it again.",
        )
        r_2 = Review.objects.create(
            reviewed_object = p_1,
            user = u_2,
            score = 4,
            comment = "This is an outstanding television!",
        )
        r_3 = Review.objects.create(
            reviewed_object = p_2,
            user = u_2,
            score = 3,
            comment = "My food doesn't taste any better off this table...",
        )

    def test_relationships(self):
        """Test accessing objects across relationships."""
        u_1 = User.objects.get(username='joetest')
        u_2 = User.objects.get(username='atheiman')
        u_3 = User.objects.get(username='willie')
        p_1 = Product.objects.get(name='22-inch TV')
        p_2 = Product.objects.get(name='8-inch Tablet')
        p_3 = Product.objects.get(name='Kitchen Table')
        r_1 = Review.objects.get(reviewed_object = p_1, user = u_1)
        r_2 = Review.objects.get(reviewed_object = p_1, user = u_2)
        r_3 = Review.objects.get(reviewed_object = p_2, user = u_2)

        # product -> reviews
        self.assertIn(r_1, p_1.reviews.all())
        # product -> user
        self.assertEqual(u_2.username, p_2.reviews.get(user=u_2).user.username)
        # user -> reviews
        self.assertIn(r_3, u_2.reviews.all())
        # user -> product
        self.assertEqual(p_1.name, u_2.reviews.get(reviewed_object=p_1).reviewed_object.name)
        # reviews -> user
        self.assertEqual(u_1.reviews.all(), Review.objects.filter(user__username=u_1.username))
        self.assertEqual([], Review.objects.filter(user=u_3))
        # reviews -> product
        self.assertEqual(p_2.reviews.all(), Review.objects.filter(reviewed_object__name=p_2.name))
        self.assertEqual([], Review.objects.filter(reviewed_object=p_3))

    def test_reviewable(self):
        """Test functionality of subclass of reviews.models.Reviewable."""
        p_1 = Product.objects.get(name='22-inch TV')
        p_2 = Product.objects.get(name='8-inch Tablet')
        p_3 = Product.objects.get(name='Kitchen Table')

        self.assertEqual(p_1.avg_review_score(), Decimal(3.5))
        self.assertEqual(p_2.avg_review_score(), Decimal(3.0))
        self.assertEqual(p_3.avg_review_score(), None)

    def test_review(self):
        """Test functionality of reviews.models.Review class."""
        r_1 = Review.objects.get(reviewed_object = p_1, user = u_1)
        r_2 = Review.objects.get(reviewed_object = p_1, user = u_2)
        r_3 = Review.objects.get(reviewed_object = p_2, user = u_2)

        self.assertFalse(r_1.is_updated())

        print 'sleeping to check Review.is_updated() time difference...'
        time.sleep(UPDATED_COMPARISON_SECONDS + 1)
        self.assertIs(type(r_1.is_updated()), datetime.timedelta)
