import logging
import json
import llamadas
import global_vars
import configurations
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)


LOGIN, STORE, VOTINGS, VOTING, SAVE_VOTE  = range(5)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def login(update, context):
    user = update.message.from_user
    logger.info("%s  %s", user.first_name, update.message.text)
    update.message.reply_text("Indique su nombre de usuario y tu contraseña de la siguiente forma. \nUsername \nContraseña",
                              reply_markup=ReplyKeyboardRemove())
    return STORE


def store(update, context):
    credentials = {}
    next_state = ConversationHandler.END
    for index, i in enumerate(update.message.text.split("\n")):
        if index == 0:
            credentials["username"] = i
        else:
            credentials["password"] = i

    response = llamadas.get_token(credentials)
    if response.status_code == 200:
        global_vars.token = json.loads(response.text)["token"]
        username = credentials['username']
        update.message.reply_text("¡Ya has iniciado sesión, " + username + "!")
        user = update.message.from_user
        logger.info("Usuario  %s logged", user.first_name)
        reply_keyboard = [['Vote']]
        update.message.reply_text(update.message.text, reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True))
        next_state = VOTINGS
    else:
        update.message.reply_text(
            "Los credenciales son incorrectos, índicalos o escribe /cancel para salir")
        next_state = STORE

    return next_state