class LocalizationError(Exception):
    """Custom exception raised when a localization is not found."""
    pass


class Lingopy:
    """Class to create localized messages.

    :param lang_func: A callable that returns the current language code.
    :param fallback_lang: A fallback language code if the current language is not found.
    """
    def __init__(
        self, lang_func: callable, fallback_lang: str | None = None
    ) -> None:
        self.lang_func = lang_func
        self.fallback_lang = fallback_lang

    def localized(self, **localizations: dict[str, str]) -> 'Localized':
        """Create a Localized object with the provided localizations.

        :param localizations: Key-value pairs where keys are language codes
                              and values are the localized messages.
        :return: A Localized object with the provided localizations.
        """
        return Localized(
            lang_func=self.lang_func,
            fallback_lang=self.fallback_lang,
            **localizations
        )


class Localized:
    """Class representing a localized message.

    :param lang_func: A callable that returns the current language code.
    :param fallback_lang: A fallback language code if the current language is not found.
    :param localizations: Key-value pairs where keys are language codes and values are the localized messages.
    """
    def __init__(
        self,
        lang_func: callable,
        fallback_lang: str | None = None,
        **localizations: dict[str, str]
    ) -> None:
        self.lang_func = lang_func
        self.fallback_lang = fallback_lang
        self.localizations = localizations

    @property
    def text(self) -> str:
        """Return the localized message as a string.

        :raises LocalizationError: If no localization is found for the current or fallback language.
        """
        return self.__str__()

    def __str__(self) -> str:
        """Return the localized message as a string.

        This method looks up the message based on the current language.
        
        :raises LocalizationError: If the localization is not found in either the current or fallback language.
        :return: The localized message.
        """
        current_lang = self.lang_func()
        localized_message = self.localizations.get(current_lang)

        if localized_message is None:
            if self.fallback_lang is None:
                raise LocalizationError(
                    "Tried to access a message that is not localized, and no fallback language was defined."
                )

            localized_message = self.localizations.get(self.fallback_lang)

            if localized_message is None:
                raise LocalizationError(
                    f'Tried to access a message that is not localized. Fallback language "{self.fallback_lang}" is also not localized.'
                )

        return localized_message

    def __call__(self, *args, **kwargs) -> str:
        """Return the localized message when the object is called.

        :return: The localized message as a string.
        """
        return self.text

    def __add__(self, other: str) -> str:
        """Concatenate the localized message with another string.

        :param other: The string to concatenate.
        :return: The concatenated result.
        """
        return self.__str__() + str(other)

    def __mul__(self, other: int) -> str:
        """Repeat the localized message a given number of times.

        :param other: The number of times to repeat the message.
        :return: The repeated localized message.
        """
        return self.__str__() * other

    def __repr__(self) -> str:
        """Return a string representation of the Localized object.

        :return: A string representation of the Localized object.
        """
        return f"Localized(lang_func={self.lang_func}, fallback_lang={self.fallback_lang}, localizations={self.localizations})"
