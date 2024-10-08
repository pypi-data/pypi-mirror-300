from django.test import TestCase

from plugin.manager import plugin_manager


class TestWhiteboxPluginGpsDisplay(TestCase):
    def setUp(self) -> None:
        self.plugin = [
            x
            for x in plugin_manager.plugins
            if x.__class__.__name__ == "WhiteboxPluginGpsDisplay"
        ][0]
        return super().setUp()

    def test_plugin_name(self):
        self.assertEqual(self.plugin.name, "GPS Display")

    def test_plugin_template(self):
        expected_template = (
            "whitebox_plugin_gps_display/whitebox_plugin_gps_display.html"
        )
        self.assertEqual(self.plugin.plugin_template, expected_template)

    def test_plugin_js(self):
        expected_js = [
            "/static/whitebox_plugin_gps_display/whitebox_plugin_gps_display.js"
        ]
        self.assertEqual(self.plugin.plugin_js, expected_js)

    def test_plugin_css(self):
        expected_css = [
            "/static/whitebox_plugin_gps_display/whitebox_plugin_gps_display.css"
        ]
        self.assertEqual(self.plugin.plugin_css, expected_css)
