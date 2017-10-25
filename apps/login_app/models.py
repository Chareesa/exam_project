# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

# Model Manager.
class UserManager(models.Manager):
    def loginVal(self, postData):
        results = {
            'errors': [],
            'status': False,
            'user': None
        }
        email_matches = self.filter(email = postData['email'])
        if len(email_matches) == 0:
            results['errors'].append('Please check your email and password and try again.')
            results['status'] = True
        else:
            results['user'] = email_matches[0]
            if not bcrypt.checkpw(postData['password'].encode(), results['user'].password.encode()):
                results['errors'].append('Please check your email and password and try again.')
                results['status'] = True
        return results
        
    def createUser(self, postData):
        new_password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        self.create(name = postData['name'], alias = postData['alias'], email = postData['email'], password = new_password, birthday = postData['birthday'])

    def registerVal(self, postData):
        results = {
        	'errors': [],
            'status': False 
        }
        if len(postData['name']) < 2:
            results['status'] = True
            results['errors'].append('Name is too short.')

        if not postData['name'].isalpha():
            results['status'] = True 
            results['errors'].append("For name, please use alphabetic characters only")

        if not postData['alias'].isalnum():
            results['status'] = True 
            results['errors'].append("For alias, please use alphanumeric characters only")

        if len(postData['alias']) < 2:
            results['status'] = True
            results['errors'].append('Alias is too short.')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", postData['email']):
            results['status'] = True
            results['errors'].append('Email is not valid.')
        
        if len(postData['password']) < 3:
            results['status'] = True
            results['errors'].append('Password is too short.')

        if not postData['password'].isalnum():
            results['status'] = True 
            results['errors'].append("Please Enter a valid Password")

        if postData['password'] != postData['c_password']:
            results['status'] = True
            results['errors'].append('Passwords do not match.')


        # if not postData['birthday'].isalnum():
        #     results['status'] = True 
        #     results['errors'].append("For birthday, please use alphanumeric characters only")

        # if len(postData['birthday']) < 2:
        #     results['status'] = True
        #     results['errors'].append('Birthday is incorrect format.')


        user = self.filter(email= postData['email'])

        if len(user) > 0:
            results['status'] = True
            results['errors'].append('User already exists in database.')

        return results

#Model      
class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    birthday = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    friends = models.ManyToManyField('User', related_name="friended")
    objects = UserManager()
