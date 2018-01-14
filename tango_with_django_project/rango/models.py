from datetime import datetime, timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Category(models.Model):
    name    = models.CharField(max_length=128, unique=True)
    views   = models.PositiveIntegerField(default=0)
    likes   = models.PositiveIntegerField(default=0)
    slug    = models.SlugField()

    def save(self, *args, **kwargs):
        # Uncomment if slug must remain the same regardless of the category's name
        # if self.id is None:
        #   self.slug = slugify(self.name)
        self.slug = slugify(self.name)

        if self.likes < 0:
            self.likes = 0

        if self.views < 0:
            self.views = 0

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
    first_visit = models.DateTimeField(null=True, blank=True)
    last_visit  = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Enforce some sanity in the page model whereby
        visits cannot be in the future and last visit
        cannot be before the first visit
        """
        time_now = timezone.now()

        if self.first_visit is not None:
            if (time_now - self.first_visit).seconds < 0:
                # first visit is in the future! no no
                self.first_visit = time_now

            # Do not allow changing the first visit once set
            try:
                this = Page.objects.get(id=self.id)
                if this.first_visit is not None:
                    self.first_visit = this.first_visit
            except:
                pass

        if self.last_visit is not None:
            if (time_now - self.last_visit).seconds < 0:
                # last visit in the future, no no
                self.last_visit = time_now

            # Check if first_visit is already set, if not set it now
            if self.first_visit is None:
               self.first_visit = self.last_visit

        # last visit is before the first visit, use last visit data
        if self.last_visit is not None and self.first_visit is not None and self.last_visit < self.first_visit:
            self.first_visit = self.last_visit

        super(Page, self).save(*args, **kwargs)

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
