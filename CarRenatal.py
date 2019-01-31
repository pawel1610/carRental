import pymysql


class Menu:

    def __init__(self):
        try:
            self.conn = pymysql.connect("localhost", "root", "root", "carrental")
            print("Witaj w wypożyczalni samochodów")
            self.menuWelcome()
        except:
            print("bledne dane logowania do serwera")

    def menuWelcome(self):
        dec = input("Wybierz:\n1-Logowanie\n2-Rejestracja")
        if dec == "1":
            self.log()
        else:
            Users.newUser(self)

    def log(self):
        login = input("podaj login")
        passw = input("podaj haslo")
        self.c = self.conn.cursor()
        self.c.execute("SELECT * from users WHERE login= %s and passw= %s", (login, passw))
        logResult = self.c.fetchall()


        if len(logResult) == 1:
            print("Witaj " + logResult[0][1] + " " + logResult[0][2])
            if logResult[0][7] == "admin":
                self.menuAdmin()
            else:
                self.menuCustomer()
        else:
            print("Błędne hasło lub login")
            self.log()

    def menuAdmin(self):
        dec = input("Jesteś w menu admina\n1 - zamowienia\n2 - klienci\n3 - produkty")

    def menuCustomer(self):
        dec = input("Jesteś w menu klienta:\n1 - Złóż zamówienie\n2 - Twoje zamówienia\n3 - Anuluj zamówienie\n4 - Twoje dane\n5 - Edytuj Twoje dane\n6 - Usuń konto")

Menu = Menu()