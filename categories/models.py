from django.db import models
from decimal import Decimal
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import ugettext_lazy as _



# Create your models here.

class Category(MPTTModel):
    name = models.CharField(max_length=100, blank=False, unique=True)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'),
                                 verbose_name="Estimated budget", blank=True, null=True)

    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    # objects = models.Manager()

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        # ordering = ['name']
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):  # __unicode__ on Python 2
        return self.name

    def save(self, *args, **kwargs):
        if not self.is_root_node():
            super(Category, self).save(*args, **kwargs)  # Call the "real" save() method.
            ancestors = self.get_ancestors(True)
            level_amount = 0
            for sibling in self.get_siblings(True):
                level_amount = level_amount + sibling.amount
            for ancestor in ancestors:
                ancestor.amount = level_amount
                ancestor.save()
                for sibling in ancestor.get_siblings():
                    level_amount = level_amount + sibling.amount
        super(Category, self).save(*args, **kwargs)  # Call the "real" save() method.

    def create_tags(self, tags):
        tags = tags.strip()
        tag_list = tags.split(' ')
        for tag in tag_list:
            if tag:
                t, created = Tag.objects.get_or_create(tag=tag.lower(),
                                                       category=self)
    def get_tags(self):
        return Tag.objects.filter(category=self)


class Tag(models.Model):
    tag = models.CharField(max_length=50, unique=True)
    is_new_tag = models.BooleanField(default=True)
    will_be_used_as_tag = models.BooleanField(default=True)
    category = models.ForeignKey(Category, null=True, blank=True)

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        #unique_together = (('tag', 'category'),)
        #index_together = [['tag', 'category'], ]

    def __str__(self):
        return self.tag

    #Not tested !!!!
    @staticmethod
    def get_popular_tags():
        tags = Tag.objects.all()
        count = {}
        for tag in tags:
            #if tag.categry.status == Article.PUBLISHED:
                if tag.tag in count:
                    count[tag.tag] = count[tag.tag] + 1
                else:
                    count[tag.tag] = 1
        sorted_count = sorted(count.items(), key=lambda t: t[1], reverse=True)
        return sorted_count[:20]