from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Ad(models.Model):
    title = models.CharField(_("title"), max_length=255)
    price = models.DecimalField(_("price"), max_digits=10, decimal_places=2)
    description = models.TextField(_("description"))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads')
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("ad")
        verbose_name_plural = _("ads")


class Comment(models.Model):
    text = models.TextField(_("text"))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("created_at"), auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")
