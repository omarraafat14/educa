from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):

    def __init__(self, for_fields=None, *args, **kwargs):
        """
        `for_fields` parameter, which allows you to indicate the fields
        used to order the data.
        """
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """
        pre_save() method which is executed before saving the field to the database.

        """
        """
        check whether a value already exists for this field in the model_instance.
        self.attname which is the attribute name given to the field in the model.
        """
        if getattr(model_instance, self.attname) is None:
            # no current value
            try:
                # retrieve the model class the field belongs to by accessing self.model.
                qs = self.model.objects.all()
                if self.for_fields:
                    # filter by objects with the same field values
                    # for the fields in "for_fields"
                    query = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }
                    qs = qs.filter(**query)
                # get the order of the last item
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)
