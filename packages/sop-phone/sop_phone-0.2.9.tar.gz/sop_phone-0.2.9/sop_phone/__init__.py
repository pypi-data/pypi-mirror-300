from netbox.plugins import PluginConfig


class SopPhoneConfig(PluginConfig):
    name = "sop_phone"
    verbose_name = "SOP Phone"
    description = "Manage phone informations of each site."
    version='0.2.9'
    author = "Leorevoir"
    author_email = "leoquinzler@epitech.eu"
    base_url = "sop-phone"

config = SopPhoneConfig
