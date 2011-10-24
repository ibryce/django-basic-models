# Copyright 2011 Concentric Sky, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.contrib.admin import ModelAdmin
import datetime

__all__ = ['DefaultModelAdmin', 'SlugModelAdmin']


class DefaultModelAdmin(ModelAdmin):
    """ModelAdmin subclass that will automatically update created_at or updated_at fields if they exist"""
    save_on_top = True

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        self._update_instance(instance, request.user)
        instance.save()
        return instance

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            self._update_instance(instance, request.user)
            instance.save()
        formset.save_m2m()

    @staticmethod
    def _update_instance(instance, user):
        if not instance.pk:
            if hasattr(instance, 'created_by'):
                instance.created_by = user
            if hasattr(instance, 'created_at'):
                instance.created_at = datetime.datetime.now()
        if hasattr(instance, 'updated_by'):
            instance.updated_by = user
        if hasattr(instance, 'updated_at'):
            instance.updated_at = datetime.datetime.now()


class SlugModelAdmin(DefaultModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('slug','name')

