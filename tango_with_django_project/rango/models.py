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
    # The default file is in the root of the 'media' directory
    picture = models.ImageField(upload_to='profile_images', blank=True, default='/default.jpg')

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        """
        Upon saving the model, this routine compares the old URL path with the new one.
        If it is different, we delete the old file from the disk.

        Note: when the routine executes the changes have been committed to the db yet.
        This is why we can compare the two paths.
        """

        try:
            # Thank you Stackoverflow
            this = UserProfile.objects.get(id=self.id)
            if this.picture.url != self.picture.url:
                this.picture.delete()
        except:
            pass

        super(UserProfile, self).save(*args, **kwargs)
