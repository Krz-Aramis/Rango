from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Category(models.Model):
    name    = models.CharField(max_length=128, unique=True)
    views   = models.IntegerField(default=0)
    likes   = models.IntegerField(default=0)
    slug    = models.SlugField()

    def save(self, *args, **kwargs):
        # Uncomment if slug must remain the same regardless of the category's name
        # if self.id is None:
        #   self.slug = slugify(self.name)
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Page(models.Model):
    category    = models.ForeignKey(Category, on_delete=models.PROTECT)
    title       = models.CharField(max_length=128)
    url         = models.URLField()
    views       = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    # Associate this object with the standard User model
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Our additional attributes:
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
