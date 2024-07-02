import abc

import telegram as tg
import telegram.ext as tg_ext

from . import messages


class BaseHandler(abc.ABC):

    def __init__(self) -> None:
        self.user: tp.Optional[tg.User] = None

    def __call__(
            self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE
            ):
        self.user = update.effective_user
        self.messages = messages.get_messages(self.user)
        return self.handle(update, context)

    @abc.abstractmethod
    def handle(
        self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE
    ):
        raise NotImplemented


class StartHandler(BaseHandler):
    def handle(
        self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE
    ):
        return update.message.reply_text(self.messages.start())


class HelpHandler(BaseHandler):
    def handle(
        self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE
    ):
        return update.message.reply_text(self.messages.help())


class WeatherHandler(BaseHandler):
    def handle(
        self, update: tg.Update, context: tg_ext.ContextTypes.DEFAULT_TYPE
    ):
        return update.message.reply_text(
            self.messages.weather(update.message.text)
        )


def setup_handlers(application: tg_ext.Application) -> None:
    application.add_handler(tg_ext.CommandHandler('start', StartHandler()))
    application.add_handler(tg_ext.CommandHandler('help', HelpHandler()))

    application.add_handler(
        tg_ext.MessageHandler(
            tg_ext.filters.TEXT & ~tg_ext.filters.COMMAND, WeatherHandler()
        )
    )
