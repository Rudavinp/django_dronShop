from django.db import models
from django.db.models import Max, F

from account.models import User
from product.models import Product

class SortedModel(models.Model):
    sort_order = models.PositiveIntegerField(editable=False, db_index=True)

    class Meta:
        abstract = True

    def get_ordering_queryset(self):
        raise NotImplementedError('Unknown queryset')

    def save(self, *args, **kwargs):
        if self.sort_order is None:
            qs = self.get_ordering_queryset()
            existing_max = qs.aggregate(Max('sort_order'))
            existing_max = existing_max.get('sort_order__max')
            self.sort_order = 0 if existing_max is None else existing_max + 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        qs = self.get_ordering_queryset()
        qs.filter(sort_order__gt=self.sort_order).update(
            sort_order=F('sort_order') - 1
        )
        super().delete(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comment',
                             on_delete=models.CASCADE)
    text = models.TextField(max_length=350)
    date_comment = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, related_name='comment',
                                on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return 'Comment id # {} to prod {}'.format(self.pk, self.product.name)
