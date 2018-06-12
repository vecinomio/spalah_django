import names
import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError

from blog.models import Post
from datetime import datetime

from random import randrange
from datetime import timedelta

def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

d1 = datetime.strptime('1/1/2000 1:30 PM', '%m/%d/%Y %I:%M %p')
d2 = datetime.strptime('1/1/2017 4:50 AM', '%m/%d/%Y %I:%M %p')


class Command(BaseCommand):
    help = 'Generates random data'
    # python manage.py create_test_data

    def handle(self, *args, **options):


        # clean DB data
        print(User.objects.filter(is_superuser=False).query)
        User.objects.filter(is_superuser=False).delete()
        Post.objects.all().delete()

        NUM = 100

        # create users
        for i in range(NUM):
            first_name = names.get_first_name()
            last_name = names.get_last_name()
            email = f"{first_name}_{last_name}@gmail.com".lower()
            is_staff = random.randint(1, 20) == 1

            try:
                User.objects.create(
                    username=email,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    is_staff=is_staff,
                )
            except IntegrityError:
                pass

        # get all users from DB
        users = list(User.objects.all())

        # create posts and link to random author
        for i in range(NUM * 5):
            author = random.choice(users)
            title = f"TITLE {i}"
            text = f"POSTTEXT {i} " * 100
            published_date = random_date(d1, d2)

            Post.objects.create(
                author=author,
                title=title,
                text=text,
                published_date=published_date,
)