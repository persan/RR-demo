#
import GPS


def on_project_loaded():
    # GPS.Console().write("rr_demo.ide loaded")
    pass


try:  # Only load once
    dummy = GPS.rr_demo_plugin_loaded
except:
    on_project_loaded()
    GPS.rr_demo_plugin_loaded = True
