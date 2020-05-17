from django.db.models import (CharField, ForeignKey, ManyToManyField,
                              OneToOneField, TextField)

# Register your models here.


class DefaultAdminMixin:
    """
    class mixin to setup default `raw_id_fields` and `search_fields`.
    """
    list_display = ()
    list_display_link = ()
    raw_id_fields = ()
    search_fields = ()

    def __init__(self, model, admin_site, *args, **kwargs):
        self.list_display = self.setup_list_display(model)
        self.list_display_links = self.setup_list_display_links(model)
        self.raw_id_fields = self.setup_raw_id_fields(model)
        self.search_fields = self.setup_search_fields(model)
        super().__init__(model, admin_site, *args, **kwargs)

    def setup_raw_id_fields(self, model):
        return tuple(
            f.name for f in model._meta.get_fields() if isinstance(f, (ForeignKey, OneToOneField))
        )

    def setup_search_fields(self, model):
        return tuple(
            f.name for f in model._meta.get_fields() if isinstance(f, (CharField, TextField))
        )

    def setup_list_display(self, model):
        return tuple(
            f.name for f in model._meta.get_fields() if not isinstance(f, ManyToManyField)
        )

    def setup_list_display_links(self, model, start=0, end=3):
        return tuple(
            f.name
            for f in model._meta.get_fields()
            if not isinstance(f, (ManyToManyField))
        )[start:end]
