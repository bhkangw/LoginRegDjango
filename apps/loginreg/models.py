from __future__ import unicode_literals
import re
import bcrypt
from django.db import models

NAME_REGEX = re.compile(r'^[a-zA-Z]\w+$')
EMAIL_REGEX = re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)')

class UserManager(models.Manager):
    def registation_validator(self, postData):
        errors = {}
        # check length of name fields
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors['name'] = "Name fields must be at least 2 characters"
        # check length of password
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        # check name fields for only letter characters
        if not re.match(NAME_REGEX, postData['first_name']) or not re.match(NAME_REGEX, postData['last_name']):
            errors['namenum'] = "Name field but must be letters only"
        # check emailiness of email
        if not re.match(EMAIL_REGEX, postData['email']):
            errors['email'] = "Invalid email"
        # check uniqueness of email
        if len(User.objects.filter(email=postData['email'])) > 0:
            errors['dupemail'] = "Email already in use"
        # check password = pwconfirm
        if postData['password'] != postData['pwconfirm']:
            errors['pwconfirm'] = "Passwords do not match"
            
        if not errors:  # make our new user
            hashed = bcrypt.hashpw((postData['password'].encode()), bcrypt.gensalt(5))
            new_user = self.create(
                first_name=postData['first_name'],
                last_name=postData['last_name'],
                email=postData['email'],
                password=hashed
            )
            return new_user
        return errors

    def login_validator(self, postData):
        errors = {}
        # check DB for postData['email']
        if len(self.filter(email=postData['email'])) > 0:
            # check this user's password
            user = self.filter(email=postData['email'])[0]
            if not bcrypt.checkpw(postData['password'].encode(),user.password.encode()):
                errors['loginpw'] = "Emai/password incorrect"
        else:
            errors['login'] = "Email/password incorrect"
        if errors:
            return errors
        return user


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()
    def __str__(self):
        return self.email