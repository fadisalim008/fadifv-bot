from app.buttons import blue_btn, red_btn
from app.config import DEV_USERNAME

from app.help1 import TEXT as HELP1
from app.help2 import TEXT as HELP2
from app.help3 import TEXT as HELP3
from app.help4 import TEXT as HELP4
from app.help5 import TEXT as HELP5
from app.help6 import TEXT as HELP6
from app.bank import TEXT as BANK

def help_menu():
    return {
        "inline_keyboard": [

            [
                blue_btn("• 1 •", callback_data="help1"),
                blue_btn("• 2 •", callback_data="help2")
            ],

            [
                blue_btn("• 3 •", callback_data="help3")
            ],

            [
                blue_btn("• 4 •", callback_data="help4"),
                blue_btn("• 5 •", callback_data="help5")
            ],

            [
                blue_btn("• 6 •", callback_data="help6")
            ],

            [
                blue_btn("البنك", callback_data="bank")
            ],

            [
                red_btn(
                    "SOURCE FADI",
                    url=f"https://t.me/{DEV_USERNAME}"
                )
            ]
        ]
    }


def get_help_text(code):

    data = {
        "help1": HELP1,
        "help2": HELP2,
        "help3": HELP3,
        "help4": HELP4,
        "help5": HELP5,
        "help6": HELP6,
        "bank": BANK
    }

    return data.get(code, "قائمة الاوامر")
