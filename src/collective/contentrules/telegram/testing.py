from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.contentrules.telegram


class CollectiveContentrulesTelegramLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity)
        import plone.restapi

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.contentrules.telegram)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.contentrules.telegram:default")


COLLECTIVE_CONTENTRULES_TELEGRAM_FIXTURE = CollectiveContentrulesTelegramLayer()


COLLECTIVE_CONTENTRULES_TELEGRAM_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_CONTENTRULES_TELEGRAM_FIXTURE,),
    name="CollectiveContentrulesTelegramLayer:IntegrationTesting",
)


COLLECTIVE_CONTENTRULES_TELEGRAM_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_CONTENTRULES_TELEGRAM_FIXTURE,),
    name="CollectiveContentrulesTelegramLayer:FunctionalTesting",
)


