from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

from openedx.core.djangoapps.plugins.constants import ProjectType, PluginSettings, SettingsType, PluginURLs


class EdxBlockExporterConfig(AppConfig):
    name = 'edx_block_exporter'
    verbose_name = _('Edx Block Exporter')

    # Class attribute that configures and enables this app as a Plugin App.
    plugin_app = {

        # Configuration setting for Plugin URLs for this app.
        PluginURLs.CONFIG: {

            # Configure the Plugin URLs for each project type, as needed.
            ProjectType.CMS: {

                # The namespace to provide to django's urls.include.
                PluginURLs.NAMESPACE: u'edx_block_exporter',

                # The application namespace to provide to django's urls.include.
                # Optional; Defaults to None.
                PluginURLs.APP_NAME: u'edx_block_exporter',

                # The regex to provide to django's urls.url.
                # Optional; Defaults to r''.
                PluginURLs.REGEX: r'^/edx_block_exporter/',
            }
        },

        # Configuration setting for Plugin Settings for this app.
        PluginSettings.CONFIG: {

            # Configure the Plugin Settings for each Project Type, as needed.
            ProjectType.CMS: {

                # Configure each Settings Type, as needed.
                SettingsType.AWS: {

                    # The python path (relative to this app) to the settings module for the relevant Project Type and Settings Type.
                    # Optional; Defaults to u'settings'.
                    PluginSettings.RELATIVE_PATH: u'settings.pod',
                },
                SettingsType.COMMON: {
                    PluginSettings.RELATIVE_PATH: u'settings.base',
                },
                SettingsType.DEVSTACK: {
                    PluginSettings.RELATIVE_PATH: u'settings.local',
                },
                SettingsType.TEST: {
                    PluginSettings.RELATIVE_PATH: u'settings.test',
                },
            }
        },
    }
