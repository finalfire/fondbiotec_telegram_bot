import enum
from os import get_inheritable
from telegram import ParseMode, update
from telegram.ext import CommandHandler, Updater
import logging
import os
import random
import re

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


def wff() -> str:
    symbols = ('¬', '→', '∧', '∨', '↔︎')
    variables = ('p', 'q', 'r', 's')
    max_depth = 5

    def generate_formula(d):
        if random.random() < 0.35 or d > max_depth:
            return random.choice(variables)

        symbol = random.choice(symbols)
        
        if symbol == symbols[0]:
            return f'{symbol}({generate_formula(d+1)})'
        return f'({generate_formula(d+1)} {symbol} {generate_formula(d+1)})'
    
    single_not_pattern = re.compile(r'¬\(([qrs])\)')
    formula = re.sub(single_not_pattern, '¬\1', generate_formula(0))

    # disrupt formula
    if random.random() > 0.5:
        k = int(len(formula) * 0.25)
        ignore = [random.randint(0, len(formula)) for _ in k]
        formula = ''.join([x for i, x in enumerate(formula) if i not in ignore])
    
    return f'Determinare se la formula seguente è una formula ben formata (fbf): `{formula}`'


def generate(mode) -> str:
    modes = {
        'rappresentazione': [conversione, complemento_2],
        'logica': [wff]
    }
    
    return random.choice(modes[mode])()
    

_INFO = """`Hello, World!` Io sono *Heimer*, un bot dispensatore di esercizi per il corso di Fondamenti di Informatica.
Allo stato attuale, sono capace di generare casualmente esercizi su alcune parti del corso, senza però fornirne le soluzioni 🤪.
I comandi che attualmente comprendo sono i seguenti:

- */heimer rappresentazione* (esercizio casuale su conversione e rappresentazione complemento a 2)
- */heimer logica* (esercizio casuale sul determinare se una formula è una fbf)"""
COMMAND_NOT_RECOGNIZED = 'OPS! Questo comando non corrisponde a nessuna mia feature 🤔. Prova a chiamarmi con /heimer!'
COMMANDS = {
    'info': {
        'text': _INFO
    }
}


def heimer(update, context) -> None:
    if len(context.args) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id, text=COMMANDS['info']['text'], parse_mode=ParseMode.MARKDOWN)
        return
    
    command = context.args[0]
    if command in COMMANDS:
        context.bot.send_message(chat_id=update.effective_chat.id, text=generate(command))
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
