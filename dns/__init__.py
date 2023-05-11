from extras.plugins import PluginConfig

class DNSPluginConfig(PluginConfig):
    name = "dns"
    verbose_name = "DNS"
    description = "DNS"
    min_version = "3.5.0"
    version = "0.1.0"
    author = "Daniel Isaksen"
    author_email = "code@duniel.no"
    required_settings = []
    default_settings = {}

config = DNSPluginConfig
