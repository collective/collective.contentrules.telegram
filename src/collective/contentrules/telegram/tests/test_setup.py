"""Setup tests for this package."""

from collective.contentrules.telegram.testing import (  # noqa: E501
    COLLECTIVE_CONTENTRULES_TELEGRAM_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that collective.contentrules.telegram is properly installed."""

    layer = COLLECTIVE_CONTENTRULES_TELEGRAM_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if collective.contentrules.telegram is installed."""
        self.assertTrue(
            self.installer.is_product_installed("collective.contentrules.telegram")
        )

    def test_browserlayer(self):
        """Test that ICollectiveContentrulesTelegramLayer is registered."""
        from collective.contentrules.telegram.interfaces import (
            ICollectiveContentrulesTelegramLayer,
        )
        from plone.browserlayer import utils

        self.assertIn(ICollectiveContentrulesTelegramLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_CONTENTRULES_TELEGRAM_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        if get_installer:
            self.installer = get_installer(self.portal, self.layer["request"])
        else:
            self.installer = api.portal.get_tool("portal_quickinstaller")
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("collective.contentrules.telegram")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.contentrules.telegram is cleanly uninstalled."""
        self.assertFalse(
            self.installer.is_product_installed("collective.contentrules.telegram")
        )

    def test_browserlayer_removed(self):
        """Test that ICollectiveContentrulesTelegramLayer is removed."""
        from collective.contentrules.telegram.interfaces import (
            ICollectiveContentrulesTelegramLayer,
        )
        from plone.browserlayer import utils

        self.assertNotIn(
            ICollectiveContentrulesTelegramLayer, utils.registered_layers()
        )
