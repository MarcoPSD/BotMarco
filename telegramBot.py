#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO, Q1, Q2, Q3, Q4, END, MYSCRIPT = range(10)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Maschio", "Femmina", "Altro"]]

    await update.message.reply_text(
        "Ciao! Sono il bot di Marco. Ora inizieremo una conversazione, dove potrai chiedermi di più sul mio Creatore.\n\n"
        "Quando ti chiederò di scegliere, al lato dell'input dei messaggi apparirà un quadrato con dei pallini, clicca e scegli!\n\n "
        "Scrivi /cancel se non vuoi più parlare con me.\n\n"
        "Ora creeremo il tuo profilo utente nella nostra piattaforma\n\n"
        "Come ti identifichi? Scegli tra le opzioni",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Come ti identifichi?"
        ),
    )

    return GENDER


async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Mandami una tua foto, così la setto come immagine profilo!\n\n"
        "Specifico che noi non abbiamo accesso ai vostri dati.\n\nOppure scrivi /skip se vuoi inserirla più tardi.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO 


async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive("user_photo.jpg")
    logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    await update.message.reply_text(
        "Grande! ora mandami la tua posizione!, così possiamo direzionarti verso il server più vicino.\n\nOppure scrivi /skip per settarla più avanti(potrebbe causare rallentamenti)."
    )

    return LOCATION


async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    await update.message.reply_text(
        "Hai paura per caso? Non ho accesso a ciò che invii.\n\nOra, mandami la tua posizione,\n\nOppure scrivi /skip per settarla in seguito."
    )

    return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    await update.message.reply_text(
        "Verrò a trovarti un giorno!\n\nSe solo Marco riuscisse a trasferirmi in un corpo umano.\n\nBene, ora parlami un pò di te, scrivi ciò che vuoi!"
    )

    return BIO


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    await update.message.reply_text(
            "Come sei paranoico, tanto so già dove abiti.\n\n Allora parlami un pò di te, scrivi ciò che vuoi!"
    )

    return BIO


async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    reply_keyboard = [["Chi è Marco?"]]
    user = update.message.from_user
    logger.info("bio of %s: %s", user.first_name, update.message.text)

    await update.message.reply_text("Figo, ora che ci conosciamo meglio, puoi farmi delle domande sul mio creatore.\n\n Seleziona la domanda disponibile!",
    reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Scegli la domanda"),
    )
    return Q1

async def question1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Perchè dovrei scegliere Marco?"]]
    user = update.message.from_user
    logger.info("First question of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Marco è un ragazzo di 21 anni, intraprendente e determinato, che ha sempre sognato di studiare Coding ma non ha mai trovato la forza per abbandonare tutto e cambiare vita.\n\n"
        "Ha dimostrato che, se si ha sufficiente determinazione e passione, è possibile realizzare i propri sogni e trasformare le proprie ambizioni in realtà.\n\n"
        "Scrivi /cancel per smettere di parlare con me.\n\n"
        "Seleziona la prossima domanda!",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Scegli la domanda"),
    )

    return Q2

async def question2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Perchè Marco vuole diventare RED?"]]
    user = update.message.from_user
    logger.info("Third question of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Lui crede fermamente nel lavoro di squadra, sostiene che lavorare in team sia essenziale per ottenere il massimo risultato e che possa portare a soluzioni creative e innovative.\n\n"
        "Sa lavorare in modo efficiente e collaborativo con i colleghi, ed è alla continua ricerca di imparare nuovi linguaggi di programmazione e applicarli in modo innovativo. (So che attualmente ha in programma di studiare C++, Kotlin e Swift)\n\n"
        "Il fatto che ha lasciato tutto per inseguire il suo sogno dimostra la sua passione per la sua carriera. Questa passione unita alla sua formazione e alla sua motivazione lo rendono un candidato ideale per diventare RED.\n\n"
        "Se cercate altre motivazioni...leggete le lettere dei suoi compagni, sicuramente hanno scritto belle parole che condivide :)\n\n"
        "Scrivi /cancel per smettere di parlare con me.\n\n"
        "Seleziona la prossima domanda!",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Scegli la domanda"),
    )

    return Q3


async def question3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Cosa vorrebbe fare Marco in Futuro?"]]
    user = update.message.from_user
    logger.info("Second question of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Marco a volte si confida con me, mi raccontava l'altro giorno, che non lo sa nemmeno lui il perchè.\n\n"
        "No scherzo\n\n"
        "Marco crede che diventare RED sia l’opportunità giusta per affinare tutto ciò che ha imparato negli scorsi mesi, mettere mano a progetti nuovi e stimolanti.\n\n"
        " Una grandissima opportunità per  continuare a lavorare con alcuni membri della classe, e  per entrare a far parte del mondo del lavoro pur rimanendo nel contesto di BIGROCK e BIGWAVE, che ti permette di trovare persone veramente straordinarie con cui lavorare\n\n"
        "Srivi /cancel per smettere di parlare con me.\n\n"
        "Seleziona la prossima domanda!",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Scegli la domanda"),
    )

    return Q4

async def question4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Voglio sapere come sei stato Scritto"]]
    user = update.message.from_user
    logger.info("4 question of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Bella domanda…\n\n"
        "Marco non mi ha mai parlato del suo futuro, forse perchè ne ha paura, o forse perchè non ha ancora ben chiaro cosa aspettarsi da quest’ultimo.\n\n"
        "Spesso mi parla di voler andare all’estero, America, Olanda, Svezia, e di quanto sarebbe figo lavorare nelle Big Tech come Google o Apple.\n\n"
        "Magari il periodo RED potrà indicargli la strada giusta.\n\n"
        "Una cosa è certa…Marco è un sognatore e glielo avete insegnato voi ad esserlo no?\n\n"
        "Per aspera ad Astra.\n\n"
        "PS. Challenger 9, SEMPRE\n\n"
        "Seleziona come continuare",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Scegli la domanda"),
    )

    return MYSCRIPT

async def myscript(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Fine"]]
    user = update.message.from_user
    logger.info("script question of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
            "Puoi trovare lo script Python che mi controlla in questa repository Github: \n\n"
        "https://github.com/MarcoPSD/BotMarco\n\n"
        "Scrivi: 'Fine' , per finire la conversazione",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Scegli la domanda"),
    )

    return END

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    user = update.message.from_user
    logger.info("end question of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Grazie per aver parlato con me...\n\n"
        "Un'ultima cosa...salviamo tutti i dati inseriti, sicuramente li venderemo ;)\n\n"
        "Ci vediamo presto!",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Ciao, spero di rivederti presto!", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("MyToken").read_timeout(20).get_updates_read_timeout(42).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            GENDER: [MessageHandler(filters.Regex("^(Maschio|Femmina|Altro)$"), gender)],
            PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("skip", skip_photo)],
            LOCATION: [
                MessageHandler(filters.LOCATION, location),
                CommandHandler("skip", skip_location),
            ],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
            Q1: [MessageHandler(filters.Text("^(Chi è Marco?)$"), question1)],
            Q2: [MessageHandler(filters.Text("^(Perchè dovrei scegliere Marco?)$"), question2)],
            Q3: [MessageHandler(filters.Text("^(Perchè Marco vuole diventare RED?)$"), question3)],
            Q4: [MessageHandler(filters.Text("^(Cosa vorrebbe fare Marco in Futuro?)$"), question4)],
            END: [MessageHandler(filters.Text("^((Fine)$"), end)],
            MYSCRIPT: [MessageHandler(filters.Text("^((Voglio sapere come sei stato Scritto)$"), myscript)]

        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
