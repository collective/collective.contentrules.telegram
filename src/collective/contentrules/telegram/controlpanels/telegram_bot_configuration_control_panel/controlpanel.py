# -*- coding: utf-8 -*-
from collective.contentrules.telegram import _
from collective.contentrules.telegram.interfaces import ICollectiveContentrulesTelegramLayer
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.restapi.controlpanels import RegistryConfigletPanel
from plone.z3cform import layout
from zope.component import adapter
from zope.interface import Interface
from zope import schema

class ITelegramBotConfigurationControlPanel(Interface):
    myfield_name = schema.TextLine(
        title=_(
            "This is an example field for this control panel",
        ),
        description=_(
            "",
        ),
        default="",
        required=False,
        readonly=False,
    )


class TelegramBotConfigurationControlPanel(RegistryEditForm):
    schema = ITelegramBotConfigurationControlPanel
    schema_prefix = "collective.contentrules.telegram.telegram_bot_configuration_control_panel"
    label = _("Telegram Bot Configuration Control Panel")


TelegramBotConfigurationControlPanelView = layout.wrap_form(
    TelegramBotConfigurationControlPanel, ControlPanelFormWrapper
)



@adapter(Interface, ICollectiveContentrulesTelegramLayer)
class TelegramBotConfigurationControlPanelConfigletPanel(RegistryConfigletPanel):
    """Control Panel endpoint"""

    schema = ITelegramBotConfigurationControlPanel
    configlet_id = "telegram_bot_configuration_control_panel-controlpanel"
    configlet_category_id = "Products"
    title = _("Telegram Bot Configuration Control Panel")
    group = ""
    schema_prefix = "collective.contentrules.telegram.telegram_bot_configuration_control_panel"
