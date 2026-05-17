import validators


def validate_url(url):
    if len(url) > 255:
        return "Превышена допустимая длина ссылки"
    if not validators.url(url):
        return "Некорректный URL"
