from collective.contentrules.telegram import _
from OFS.SimpleItem import SimpleItem
from plone import api
from plone.app.contentrules.actions import ActionAddForm
from plone.app.contentrules.actions import ActionEditForm
from plone.app.contentrules.browser.formhelper import ContentRuleFormWrapper
from plone.contentrules.rule.interfaces import IExecutable
from plone.contentrules.rule.interfaces import IRuleElementData
from plone.stringinterp.interfaces import IStringInterpolator
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface

import telegram


class ITelegramAction(Interface):
    """Definition of the configuration of the action"""

    message = schema.Text(
        title=_(
            "Message to be sent",
        ),
        description=_(
            "",
        ),
        default="",
        required=True,
        readonly=False,
    )

    recipient = schema.TextLine(
        title=_(
            "Message recipient",
        ),
        description=_(
            "",
        ),
        default="",
        required=True,
        readonly=False,
    )

    token = schema.TextLine(
        title=_(
            "Telegram Bot Token",
        ),
        description=_(
            "Enter the token provided by the Telegram bot you need to create before configuring this rule. You can ignore this setting if you are using the same site-wide Telegram bot, which need to be configured in the global control panel available in the site settings",
        ),
        default="",
        required=False,
        readonly=False,
    )


@implementer(ITelegramAction, IRuleElementData)
class TelegramAction(SimpleItem):
    """The implementation of the action"""

    message = ""
    recipient = ""
    token = ""

    element = "collective.contentrules.telegram.action.TelegramAction"

    @property
    def summary(self):
        return _("Send a message to Telegram")


@implementer(IExecutable)
@adapter(Interface, ITelegramAction, Interface)
class TelegramActionExecutor:
    """The executor of the action"""

    def __init__(self, context, element, event):
        self.context = context
        self.element = element
        self.event = event

    def _get_token(self):
        """get the Telegram Token
        we have 2 options:
            - Either it is set explicitly in this action
            - It is a global setting

        """
        if hasattr(self.element, 'token') and self.element.token:
            return self.element.token

        return api.portal.get_registry_record(
            "collective.contentrules.telegram.telegram_bot_configuration_control_panel.token"
        )

    def __call__(self):
        """execute the action"""
        interpolator = IStringInterpolator(self.event.object)
        recipient = interpolator(self.element.recipient)
        message = interpolator(self.element.message)
        bot = telegram.Bot(token=self._get_token())
        bot.send_message(recipient, message)
        return True


class TelegramActionAddForm(ActionAddForm):
    """
    An add form for the mail action
    """

    schema = ITelegramAction
    label = _("Add Telegram Action")
    description = _("A telegram action to send messages to telegram chat channels.")
    form_name = _("Configure element")
    Type = TelegramAction
    # custom template will allow us to add help text
    template = ViewPageTemplateFile("telegram.pt")


class TelegramActionAddFormView(ContentRuleFormWrapper):
    """the view"""

    form = TelegramActionAddForm


class TelegramActionEditForm(ActionEditForm):
    """
    An edit form for the mail action
    """

    schema = ITelegramAction
    label = _("Edit Telegram Action")
    description = _("A telegram action to send messages to telegram chat channels.")
    form_name = _("Configure element")

    # custom template will allow us to add help text
    template = ViewPageTemplateFile("telegram.pt")


class TelegramActionEditFormView(ContentRuleFormWrapper):
    """Edit view"""

    form = TelegramActionEditForm
