from lingopy.lingopy import Lingopy

lang_func = lambda: 'en'

lingopy = Lingopy(lang_func=lang_func, fallback_lang='pl')

BAD_EMAIL_MSG = lingopy.localized(
    en="You have entered the bad e-mail.",
    pl="Wpisałeś zły adres e-mail.",
)

BAD_PASSWORD_MSG = lingopy.localized(
    en="You have entered the bad password.", pl="Wpisałeś złe hasło."
)

print(BAD_EMAIL_MSG + BAD_PASSWORD_MSG)  # Both are Localized type.
print(BAD_EMAIL_MSG.text + BAD_PASSWORD_MSG.text)  # Both are str type.
print(BAD_EMAIL_MSG.text + "Added text")  # Both are str type.
print(BAD_EMAIL_MSG + "Added text")  # Localized type, str type.
# print("Added text" + BAD_EMAIL_MSG)  # str type, Localized type. That won't work, because str type cannot handle adding another type to it.

from lingopy.lingopy import Localized

BAD_EMAIL_MSG = Localized(
    lang_func=lambda: 'en',
    fallback_lang='pl',
    en="You have entered the bad e-mail.",
    pl="Wpisałeś zły adres e-mail.",
)

BAD_PASSWORD_MSG = Localized(
    lang_func=lambda: 'en',
    fallback_lang='pl',
    en="You have entered the bad password.",
    pl="Wpisałeś złe hasło."
)

print(BAD_EMAIL_MSG, BAD_PASSWORD_MSG)
