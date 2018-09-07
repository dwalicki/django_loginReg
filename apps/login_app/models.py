# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
from django.db import models
import bcrypt
# Create your models here.



class UserManager(models.Manager):
    def loginVal(self, postData):
        results = {'status': True, 'errors':[], 'user': None}
        users = self.filter(email = postData['email'])

        if len(users) < 1:
            results['status'] = False
        else:
            if bcrypt.checkpw(postData['password'].encode(), users[0].password.encode()):
                results['user'] = users[0]
            else:
                results['status'] = False
        return results

    def creator(self, postData):
        user = self.create(first_name = postData['first_name'], last_name = postData['last_name'], email = postData['email'], \
        password = bcrypt.hashpw(postData(postData['password']).encode(), bcrypt.gensalt()))
        return user

    def validate(self, postData):
        results = {'status': True, 'errors':[]}
        if len(postData['first_name']) < 3:
            results['errors'].append('Your first name is too short.')
            results['status'] = False
        
        if len(postData['last_name']) < 1:
            results['errors'].append('Your last name is too short.')
            results['status'] = False

        if not re.match("[^@]+@[^@]+\.[^@]+", postData['email']):        
            results['errors'].append('Email is not valid.')
            results['status'] = False

        if postData['password'] != postData['confirm_password']:
            results['errors'].append('Passwords do not match')
            results['status'] = False

        if len(postData['password']) < 4:
            results['errors'].append('Password is too short, must be four characters minimum.')
            results['status'] = False            

        if len(self.filter(email = postData['email'])) > 0:
            results['errors'].append('Account already exists.')
            results['status'] = False 
        return results

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    objects = UserManager()