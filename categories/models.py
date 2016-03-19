from django.db import models
from decimal import Decimal
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

class Category(MPTTModel):
    name = models.CharField(max_length=100, blank=False, unique=True)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name="Estimated budget", blank=True, null=True)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        ordering = ['name']
        verbose_name = u'Catégorie'
        verbose_name_plural = u'Catégories'

    def __str__(self):              # __unicode__ on Python 2
        return self.name

    def save(self, *args, **kwargs):
        if not self.is_root_node():
            super(Category, self).save(*args, **kwargs) # Call the "real" save() method.
            ancestors = self.get_ancestors(True)
            level_amount=0
            for sibling in self.get_siblings(True):
                level_amount = level_amount+sibling.amount
            for ancestor in ancestors:
                ancestor.amount=level_amount
                ancestor.save()
                for sibling in ancestor.get_siblings():
                    level_amount = level_amount+sibling.amount
        super(Category, self).save(*args, **kwargs) # Call the "real" save() method.

