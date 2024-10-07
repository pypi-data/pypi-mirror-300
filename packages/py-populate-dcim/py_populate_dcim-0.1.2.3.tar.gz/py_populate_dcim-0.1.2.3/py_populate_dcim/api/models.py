from django.db import models

class RefreshRequest(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    debug = models.BooleanField(default=False)
    refresh_synergy_frames = models.BooleanField(default=False)
    create_oneview_server_devices = models.BooleanField(default=False)
    create_oneview_server_modules = models.BooleanField(default=False)
    create_oneview_server_interfaces = models.BooleanField(default=False)
    import_nautobot_types = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
