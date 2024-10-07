from flask import Flask, request

from src.lingopy import Lingopy

app = Flask(__name__)


# Define the language function
def get_language():
    # Get the 'Accept-Language' header from the request
    lang = request.headers.get('Accept-Language')

    # Return None when header is not presented.
    if not lang:
        return None

    # Split the header values into a list
    languages = lang.split(',')

    # Remove duplicates while maintaining order
    unique_languages = []

    for language in languages:
        # Simplify the language code (e.g., 'pl-PL' => 'pl')
        simplified_language = language.split('-')[0]

        # Add to the list only if it's not already included
        if simplified_language not in unique_languages:
            unique_languages.append(simplified_language)

    # Return the first result or default to 'en'
    return unique_languages[0] if unique_languages else None


# Create an instance of Lingopy
lingopy = Lingopy(lang_func=get_language, fallback_lang="pl")


@app.route('/')
def home():
    # Localized messages
    welcome_msg = lingopy.localized(
        en="Welcome to the application!", pl="Witamy w aplikacji!"
    )

    return welcome_msg.text  # Returns the message in the user's language


if __name__ == "__main__":
    app.run(debug=True)
