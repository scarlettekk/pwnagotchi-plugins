from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import logging
import subprocess

class NetworkTimePlugin(plugins.Plugin):
    __author__ = "scarlettekk"
    __version__ = "1"
    __license__ = "GPL3"
    __description__ = "Display the time of day synced to the network"
    __name__ = "NetworkTime"
    __help__ = """
    A plugin that displays the current time on the display and syncs with NTP.
    Run `sudo dpkg-reconfigure tzdata` to configure your timezone.
    """

    def on_loaded(self):
        logging.info("[NetworkTime] plugin loaded.")

    def on_ui_setup(self, ui):
        with ui._lock:
            ui.add_element(
                "datetime",
                LabeledValue(
                    color=BLACK,
                    label="T",
                    value="00:00:00",
                    position=(ui.width() / 3 * 2, ui.height() / 3 * 2 - 12),
                    label_font=fonts.BoldSmall,
                    text_font=fonts.Small,
                ),
            )

    def on_ui_update(self, ui):
        dt = str(subprocess.check_output(['date', '+%H:%M:%S']))[2:-3]
        ui.set("datetime", dt)

    def on_internet_available(self, agent):
        subprocess.run(["timedatectl", "set-ntp", "off"])
        subprocess.run(["timedatectl", "set-ntp", "on"])

    def on_unload(self, ui):
        with ui._lock:
            logging.info("[NetworkTime] plugin unloaded")
            ui.remove_element("datetime")
