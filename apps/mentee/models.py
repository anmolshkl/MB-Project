from django.db import models
from django.contrib.auth.models import User


class Credits(models.Model):
    """Stores employment details of the user"""

    parent = models.OneToOneField(User, related_name="credits", primary_key=True)
    balance = models.FloatField(blank=True, default=5.0)

    def __unicode__(self):
        return u'{}'.format(self.parent.get_full_name())
        # return u'{2} in {1} of {0} from {3} to {4}'.format(self.organization,
        # self.department, self.designation, self.from_date, "present" if not self.to_date else self.to_date)

    class Meta:
        verbose_name = verbose_name_plural = "Credits"
