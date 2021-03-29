from os import get_inheritable
from telegram import ParseMode, update
from telegram.ext import CommandHandler, Updater
import logging
import os
import random

def conversione() -> str:
    bases = (2, 8, 10, 16)
    bases_fun = {2: bin, 8: oct, 10: int, 16: hex}
    n = random.randint(1, 64_500)
    b1 = random.choice(bases)
    b2 = random.choice(list(filter(lambda b: b != b1, bases)))
    n_str = str(bases_fun[b1](n))
    if b1 != 10:
        n_str = n_str[2:]
    return f'Convertire il numerale ({n_str}){b1} in base {b2}.' 

def complemento_2() -> str:
    n = random.randint(2, 1250)
    return f'Convertire i numerali (-{n})10 e ({n})10 in base 2 secondo la rappresentazione a complemento a 2. Qual è il minor numero di bit necessario?'

def gen_rappresentazione() -> str:
    fun_rappresentazioni = [
        conversione,
        complemento_2
    ]
    return random.choice(fun_rappresentazioni)()
    

_INFO = """`Hello, World!` Io sono *Heimer*, un bot dispensatore di esercizi per il corso di Fondamenti di Informatica.
Allo stato attuale, sono capace di generare casualmente esercizi su alcune parti del corso, senza però fornirne le soluzioni 🤪.
I comandi che attualmente comprendo sono i seguenti:

- */heimer rappresentazione* (esercizio casuale su conversione e rappresentazione complemento a 2)"""
COMMAND_NOT_RECOGNIZED = 'OPS! Questo comando non corrisponde a nessuna mia feature 🤔. Prova a chiamarmi con /heimer!'
COMMANDS = {
    'info': {
        'text': _INFO
    },
    'rappresentazione': {
        'generate': gen_rappresentazione
    }
}


def heimer(update, context) -> None:
    if len(context.args) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text=COMMANDS['info']['text'], parse_mode=ParseMode.MARKDOWN)
        return
    
    command = context.args[0]
    if command in COMMANDS:
        context.bot.send_message(chat_id=update.effective_chat.id, text=COMMANDS[command]['generate']())
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=COMMAND_NOT_RECOGNIZED)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    updater = Updater(token=os.environ['TELEGRAM_BOT_TOKEN'], use_context=True)
    dispatcher = updater.dispatcher

    general_handler = CommandHandler('heimer', heimer)
    dispatcher.add_handler(general_handler)

    updater.start_polling()

    updater.idle()
