sessions = {}


def create_session(username, password, uid):
    sessions[username] = {
        "password": password,
        "uid": uid
    }


def get_session(username):
    return sessions.get(username)