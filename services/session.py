sessions = {}


def create_session(username, password, uid):
    sessions[username] = {
        "password": password,
        "uid": uid,
        "theme": "light"
    }


def get_session(username):
    return sessions.get(username)


def update_session_theme(username, theme):
    if username in sessions:
        sessions[username]["theme"] = theme