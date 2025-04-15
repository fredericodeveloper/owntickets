import os
import yaml

def list():
    languages = []
    for filename in os.listdir('./lang'):
        if filename.endswith('.yml'):
            langname = filename[:-4]
            languages.append(langname)
    return languages

def is_valid(lang):
    return lang in list()

def get_content(lang, key):
    if not is_valid(lang):
        raise ValueError(f"Invalid language: {lang}")

    filename = f"{lang}.yml"
    filepath = os.path.join('./lang', filename)

    with open(filepath, 'r') as file:
        data = yaml.safe_load(file)
        if key in data: # if key exists return it
            content = data[key]
        else: # if this key does not yet exist in the requested language, return in english
            en_file = "en.yml"
            en_filepath = os.path.join('./lang', en_file)
            with open(en_filepath, 'r') as en_file:
                en_data = yaml.safe_load(en_file)
                content = en_data.get(key, key)
        return content
