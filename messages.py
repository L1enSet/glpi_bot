def registration(user, status=None):
    try:
        text = "Профиль создан\n{} {}".format(user['name'], user['surname'])
    except KeyError as exc:
        if status == 400:
            text = "Ошибка. Сообщение администратору отправлено."
        else:
            text = "0"
    return text

def error_message(data):
    if data['error'] == 'not_found':
        text = "Пользователь не найден."
    else:
        text = "Неизвестная ошибка."
    return text

def try_reg(username, user_id, tg_user, status):
    text = "Попытка регистрации:\n{}\n{}\n@{}\nresult - {}".format(username, user_id, tg_user, status)
    return text