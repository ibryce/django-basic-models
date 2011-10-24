# Copyright 2011 Concentric Sky, Inc.·
#·
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#·
#   http://www.apache.org/licenses/LICENSE-2.0
#·
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from django import forms
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from cachemodel import models as cachemodels
import re

from basic_models.managers import HasActiveManager, IsActiveManager, SlugModelManager, IsActiveSlugModelManager
from basic_models.utils import u_slugify


class ActiveModel(cachemodels.CacheModel):
    is_active = models.BooleanField(default=True, db_index=True)
    objects = HasActiveManager()
    active_objects = IsActiveManager()

    class Meta:
        abstract = True


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserModel(models.Model):
    created_by = models.ForeignKey(User, related_name='%(class)s_created', default=1, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='%(class)s_updated', default=1, null=True, blank=True)

    class Meta:
        abstract = True


class DefaultModel(UserModel, TimestampedModel, ActiveModel):
    class Meta:
        abstract = True


class SlugModel(DefaultModel):
    name = models.CharField(max_length=1024)
    slug = models.SlugField(max_length=1024, unique=True)

    objects = SlugModelManager()
    active_objects = IsActiveSlugModelManager()

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name


class UnicodeSlugModel(DefaultModel):
    name = models.CharField(max_length=1024)
    slug = models.CharField(max_length=1024, unique=True, blank=True, db_index=True)

    objects = SlugModelManager()
    active_objects = IsActiveSlugModelManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = u_slugify(self.name)
        super(UnicodeSlugModel, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name
