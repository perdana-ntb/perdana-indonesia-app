from django.contrib.auth.models import Group
from django.db import models

from core.models import DescriptableModel


class MenuCategory(DescriptableModel):
    published = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AppMenu(DescriptableModel):
    app_module = models.CharField(max_length=255, null=True, blank=True)
    app_icon = models.ImageField(upload_to="menu_icon_dir/", null=True, blank=True)
    allowed_roles = models.ManyToManyField(Group, related_name="app_menus")
    published = models.BooleanField(default=True)
    category = models.ForeignKey(MenuCategory, on_delete=models.SET_NULL,
                                 null=True, blank=True, related_name="app_menus")

    def __str__(self):
        return self.name
