from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link = 'plugins:port_history_plugin:history',  # A reverse compatible link to follow.
        link_text = 'MAC and IP on switches ports',  # Text to display to user.
    ),
)