
from Pages import LoginPage
from Pages import HomePage
def login(username, password):
    login=LoginPage()
    login.usernameElement(username)
    login.passwordElement(password)
    login.submit()