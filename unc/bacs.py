from unc.models import *


def initialize_data():
    Course.objects.get_or_create()

def

'''
name = models.CharField(max_length=20)
title = models.CharField(max_length=200)
author = models.CharField(null=True, max_length=100)
teacher = models.CharField(null=True, max_length=100)
description = models.TextField(null=True)
'''