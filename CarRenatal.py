import pymysql
import datetime
from datetime import date


class Menu:

    def __init__(self):
        try:
            self.conn = pymysql.connect("localhost", "root", "root", "carrental")
            print("Witaj w wypożyczalni samochodów")
            self.menuWelcome()
        except:
            print("Wprowadziłeś błędne dane, nastąpiło wylogowanie")

    def menuWelcome(self):
        dec = input("Wybierz:\n1-Logowanie\n2-Rejestracja")
        if dec == "1":
            self.log()
        else:
            User.newCustomer(self)
            print("Rejestracja przebiegła pomyślnie, zaloguj się.")
            self.log()

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
                self.menuCustomer(login)
        else:
            print("Błędne hasło lub login")
            self.log()

    def menuAdmin(self):
        dec = input("Jesteś w menu admin\n1 - wynajmy\n2 - użytkownicy\n3 - samochody\n4 - Wyloguj")
        if dec == "1":
            Rent.rentsMenu(self)
        elif dec == "2":
            User.usersMenu(self)
        elif dec == "3":
            Car.carsMenu(self)
        elif dec == "4":
            print("Do zobaczenia!")
            self.conn.close()
        else:
            print("Błędny wybór")
            self.menuAdmin()

    def menuCustomer(self,login):
        dec = input("Jesteś w menu klienta:\n1 - Zarezerwuj wynajem\n2 - Twoje wynajmy\n"
                    "3 - Anuluj wynajem\n4 - Twoje dane\n5 - Edytuj Twoje dane kontaktowe\n6 - Wyloguj")
        if dec == "1":
            Rent.newRent(self,login)
            self.menuCustomer(login)
        elif dec == "2":
            Rent.diplayUserRentDetails(self,login)
            self.menuCustomer(login)
        elif dec == "3":
            Rent.diplayUserRentDetails(self, login)
            Rent.delRentUser(self,login)
            self.menuCustomer(login)
        elif dec == "4":
            self.c.execute("SELECT * FROM users WHERE login = %s", (login))
            User.displayList(self)
            self.menuCustomer(login)
        elif dec == "5":
            User.editUserContact(self,login)
            self.menuCustomer(login)
        elif dec == "6":
            print("Do zobaczenia!")
            self.conn.close()
        else:
            print("Błędny wybór")
            self.menuCustomer(login)


class Rent:

    def rentsMenu(self):
        dec = input("Wynajmy:\n1 - lista wynajmów\n2 - lista wynajmów bieżących\n3 - lista wynajmów zakonczonych\n"
                    "4 - lista wynajmow uzytkownika\n5 - lista wynajmow po samochodzie\n6 - edytuj wynajem\n"
                    "7 - anuluj wynajem\n8 - menu głowne")
        if dec == "1":
            Rent.rentsList(self)
            Rent.rentsMenu(self)
        elif dec == "2":
            Rent.activeRents(self)
            Rent.rentsMenu(self)
        elif dec == "3":
            Rent.pastRents(self)
            Rent.rentsMenu(self)
        elif dec == "4":
            Rent.rentListByUser(self)
            Rent.rentsMenu(self)
        elif dec == "5":
            Rent.rentListByCar(self)
            Rent.rentsMenu(self)
        elif dec == "6":
            Rent.editRent(self)
            Rent.rentsMenu(self)
        elif dec == "7":
            Rent.delRent(self)
            Rent.rentsMenu(self)
        elif dec == "8":
            Menu.menuAdmin(self)
        else:
            print("Błędny wybór")
            Rent.rentsMenu(self)

    def rentsList(self):
        self.c.execute("SELECT rents.rent_id, users.name, users.surname, cars.brand, cars.model, cars.class, "
                       "rents.order_date,"
                       " rents.rent_start, rents.rent_end, cars.price"
                       " from rents, cars, users where users.user_id = rents.user_id and cars.car_id = rents.car_id")
        Rent.displayRents(self)

    def activeRents(self):
        self.c.execute("SELECT rents.rent_id, users.name, users.surname, cars.brand, cars.model, cars.class, rents.order_date,"
                       " rents.rent_start, rents.rent_end, cars.price"
                       " from rents, cars, users where users.user_id = rents.user_id and"
                       " cars.car_id = rents.car_id and rent_end >= CURDATE()")
        Rent.displayRents(self)

    def pastRents(self):
        self.c.execute("SELECT rents.rent_id, users.name, users.surname, cars.brand, cars.model, cars.class, rents.order_date,"
                       " rents.rent_start, rents.rent_end, cars.price"
                       " from rents, cars, users where users.user_id = rents.user_id and"
                       " cars.car_id = rents.car_id and rent_end < CURDATE()")
        Rent.displayRents(self)

    def rentListByUser(self):
        User.usersList(self)
        userId = input("podaj ID uzytkownika")
        dec = input("1 - wszystkie wynajmy\n2 - aktywne\n3 - zakończone")
        if dec == "1":
            self.c.execute("SELECT rents.rent_id, users.name, users.surname, cars.brand, cars.model, cars.class,"
                           " rents.order_date, rents.rent_start, rents.rent_end,cars.price from rents, cars,"
                           " users where users.user_id = rents.user_id and cars.car_id = rents.car_id and"
                           " users.user_id = %s",(userId))
            Rent.displayRents(self)
        elif dec == "2":
            self.c.execute("SELECT rents.rent_id, users.name, users.surname, cars.brand, cars.model,"
                           " cars.class, rents.order_date,"
                           " rents.rent_start, rents.rent_end, cars.price from"
                           " rents, cars, users where users.user_id = rents.user_id and cars.car_id = rents.car_id and"
                           " users.user_id = %s and rent_end >= CURDATE()", (userId))

            Rent.displayRents(self)
        elif dec == "3":
            self.c.execute("SELECT rents.rent_id, users.name, users.surname, cars.brand, cars.model,"
                           " cars.class, rents.order_date,"
                           " rents.rent_start, rents.rent_end, cars.price from"
                           " rents, cars, users where users.user_id = rents.user_id and cars.car_id = rents.car_id and"
                           " users.user_id = %s and rent_end < CURDATE()", (userId))
            Rent.displayRents(self)
        else:
            print("Błędny wybór")
            Rent.rentsMenu(self)

    def rentListByCar(self):
        Car.carsMenu(self)
        carId = input("podaj ID samochodu")
        dec = input("1 - wszystkie wynajmy\n2 - aktywne\n3 - zakończone")
        if dec == "1":
            self.c.execute("SELECT rents.rent_id, users.name, users.surname, cars.brand,"
                           " cars.model, cars.class, rents.order_date,"
                           " rents.rent_start, rents.rent_end, cars.price from"
                           " rents, cars, users where users.user_id = rents.user_id and cars.car_id = rents.car_id and"
                           " car.car_id = %s)", (carId))
            Rent.displayRents(self)
        elif dec == "2":
            self.c.execute("SELECT rents.rent_id, users.name, users.surname, cars.brand, cars.model,"
                           " cars.class, rents.order_date,"
                           " rents.rent_start, rents.rent_end, cars.price from"
                           " rents, cars, users where users.user_id = rents.user_id and cars.car_id = rents.car_id and"
                           " car.car_id = %s and rent_end >= CURDATE())", (carId))
            Rent.displayRents(self)
        elif dec == "3":
            self.c.execute("SELECT rents.rent_id, users.name, users.surname, cars.brand, cars.model, cars.class, "
                           "rents.order_date, rents.rent_start, rents.rent_end,"
                           " cars.price  from"
                           " rents, cars, users where users.user_id = rents.user_id and cars.car_id = rents.car_id and"
                           " car.car_id = %s and rent_end < CURDATE())", (carId))
            Rent.displayRents(self)
        else:
            print("Błędny wybór")
            Rent.rentsMenu(self)

    def editRent(self):
        Rent.rentsList(self)
        id = input("Podaj numer wynajmu, który chcesz edytować")
        print("Podaj nową datę wynajmu w formacie YYYY-MM-DD")
        year = int(input('podaj rok'))
        month = int(input('podaj miesiac'))
        day = int(input('podaj dzien'))
        newDate = datetime.date(year, month, day)
        year2 = int(input('podaj rok'))
        month2 = int(input('podaj miesiac'))
        day2 = int(input('podaj dzien'))
        newDate2 = datetime.date(year2, month2, day2)
        now = date.today()
        if newDate >= now and newDate2 >= now and newDate2 >= newDate:
            self.c.execute("UPDATE rents SET rent_start = %s WHERE rent_id=%s",(newDate,id))
            dec = input("czy na pewno chcesz datę rozpoczęcia T/N").upper()
            if dec == "T":
                self.conn.commit()
                print("zmieniono datę rozpoczęcia na " + str(newDate))
            else:
                self.conn.rollback()
                print("powrot do menu")
        else:
            print("Błędna data")
            Rent.editRent(self)

    def delRent(self):
        Rent.rentsList(self)
        id = input("podaj id wynajmu, który chcesz anulować")
        self.c.execute("SELECT rent_start FROM rents WHERE rent_id = %s",(id))
        startdate = self.c.fetchall()
        now = date.today()
        if startdate[0][0] <= now:
            print("Nie można anulować rozpoczętego wynajmu")
        else:
            self.c.execute("DELETE FROM rents WHERE rent_id = %s", (id))
            dec = input("czy na pewno chcesz anulowac wynajem T/N").upper()
            if dec == "T":
                self.conn.commit()
                print("anulowano wynajem")
            else:
                self.conn.rollback()
                print("powrot do menu")

    def delRentUser(self,login):
        id = input("Podaj id wynajmu, który chcesz anulować")
        self.c.execute("SELECT rent_start FROM rents,users WHERE rents.user_id = users.user_id and rent_id = %s"
                       " and login = %s", (id,login))
        print(login)
        result = self.c.fetchall()
        now = date.today()
        if len(result) == 1:
            if result[0][0] <= now:
                print("Nie można anulować rozpoczętego wynajmu")
            else:
                self.c.execute("DELETE FROM rents WHERE rent_id = %s", (id))
                dec = input("Czy na pewno chcesz anulowac wynajem T/N").upper()
                if dec == "T":
                    self.conn.commit()
                    print("Anulowano wynajem")
                else:
                    self.conn.rollback()
                    print("Powrot do menu")
        else:
            print("Nie masz uprawnień do anlucaji tego wynajmu")

    def displayRents(self):
        list = self.c.fetchall()
        if len(list) == 0:
            print("Brak wynajmów spełniających kryteria")
        else:
            for row in list:
                RentId      = 0
                Name        = 1
                Surname     = 2
                Brand       = 3
                Model       = 4
                Class       = 5
                DateOfOrder = 6
                StartDate   = 7
                EndDate     = 8
                Price       = 9

                print("numer wynajmu: %2s Imie: %-10s Nazwisko: %-10s Marka: %-8s Model: %-8s klasa: %-12s "
                      "Data rezerwacji %-12s Data rozpoczęcia: %-12s Data zakończenia: %-12s Koszt: %-8s"
                      % (row[RentId], row[Name], row[Surname], row[Brand], row[Model], row[Class],
                         row[DateOfOrder], row[StartDate], row[EndDate], (((row[EndDate]-row[StartDate]).days+1)*row[Price])))

    def diplayUserRentDetails(self, login):
        self.c.execute("SELECT rents.rent_id, users.name, users.surname, cars.brand, cars.model, cars.class,rents."
                       "order_date, rents.rent_start, rents.rent_end, cars.price from rents, cars,"
                       " users where users.user_id = rents.user_id and"
                       " cars.car_id = rents.car_id and users.login = %s", (login))
        Rent.displayRents(self)

    def calculatePrice(self,carId,startDate,endDate): #oblicz cene całego wynajmu

        self.c.execute("select price from cars where car_id = %s", (carId))
        getPrice = self.c.fetchall()
        days =endDate-startDate
        price = (days.days+1)*(getPrice[0][0])
        print("Cena wynajmu wynosi " + str(price) + " PLN")

    def newRent(self,login):
        print("Nasze samochody:")
        Car.carList(self)

        carId = input("Ktory samochód wybierasz?")
        print("Podaj datę rozpoczęcia wynajmu w formacie YYYY-MM-DD")
        startDate = datetime.date(int(input('Rok')), int(input('Miesiac')), int(input('Dzien')))
        print("podaj  datę zakończenia w formacie YYYY-MM-DD")
        endDate = datetime.date(int(input('podaj rok')), int(input('podaj miesiac')), int(input('podaj dzien')))

        Rent.isCarAvailable(self, carId, startDate, endDate,login)
        Rent.calculatePrice(self, carId, startDate, endDate)
        self.c.execute("select user_id from users where login = %s",(login))
        userId=self.c.fetchall()
        self.c.execute("INSERT INTO rents VALUES (0,%s,%s,CURDATE(),%s,%s)",((userId[0][0]),carId,startDate,endDate))
        dec = input("Czy poteirdzasz rezerwację? T/N").upper()
        if dec == "T":
            self.conn.commit()
            print("Zarezerwowałeś samochód")
        else:
            self.conn.rollback()
            print("powrot do menu")

    def isCarAvailable(self,carId,startDate,endDate,login): # sprawdza czy dane auto nie jest zarezerwowoane w terminie
        now = date.today()
        if startDate < now:
            print("Podałeś przeszłą datę wynajmu")
        elif startDate > endDate:
            print("Wynajem nie może zakończyć się przed jego rozpoczęciem")
        else:
            self.c.execute("SELECT rent_start, rent_end FROM rents WHERE rent_end >= CURDATE() and car_id = %s",(carId))
            result = self.c.fetchall()
            if len(result) == 0:
                print("Samochód jest dostępny")
            else:
                availableSum = 0
                for i in range(0, len(result)):
                    if startDate <= result[i][1] and endDate >= result[i][0]:
                        availableSum = availableSum
                    else:
                        availableSum += 1
                        i += 1
                if availableSum == len(result):
                    print("Samochód jest dostępny")
                else:
                    print("Samochód niedostępny w tym terminie")
                    self.menuCustomer(login)


class User:

    def usersMenu(self):
        dec = input("Użytkownicy:\n1 - lista użytkowników\n2 - lista adminów\n3 - lista klientów\n4 - nowy klient\n"
                    "5 - nowy admin\n6 - edytuj uzytkownika\n7 - menu głowne")
        if dec == "1":
            User.usersList(self)
            User.usersMenu(self)
        elif dec == "2":
            User.adminList(self)
            User.usersMenu(self)
        elif dec == "3":
            User.customerList(self)
            User.usersMenu(self)
        elif dec == "4":
            User.newCustomer(self)
            User.usersMenu(self)
        elif dec == "5":
            User.newAdmin(self)
            User.usersMenu(self)
        elif dec == "6":
            User.editUser(self)
            User.usersMenu(self)
        elif dec == "7":
            Menu.menuAdmin(self)
        else:
            print("Błędny wybór")
            User.usersMenu(self)

    def usersList(self):
        self.c.execute("SELECT * from users")
        User.displayList(self)

    def adminList(self):
        self.c.execute("SELECT * from users where type = 'admin'")
        User.displayList(self)

    def customerList(self):
        self.c.execute("SELECT * from users where type = 'customer'")
        User.displayList(self)

    def newCustomer(self):
        name = input("Podaj imie")
        surname = input("Podaj nazwisko")
        login = input("Podaj login")
        self.c.execute("select * from users Where login = %s", (login))
        result = self.c.fetchall()
        if len(result) == 1:
            print("Podany login już jest zajęty")
            User.newCustomer(self)
        else:
            passw = input("Podaj haslo")
            adress = input("Podaj adres")
            phone = input("Podaj numer telefonu")
            self.c.execute("INSERT INTO users values (0,%s,%s,%s,%s,%s,%s,%s)",
                           (name, surname, login, passw, adress, phone, "customer"))
            dec = input("czy na pewno chcesz dodac użytkownika T/N").upper()
            if dec == "T":
                self.conn.commit()
                print("dodano uzytkownika")
            else:
                self.conn.rollback()
                print("powrot do menu")

    def newAdmin(self):

        name = input("Podaj imie")
        surname = input("Podaj nazwisko")
        login = input("Podaj login")
        self.c.execute("select * from users Where login = %s", (login))
        result = self.c.fetchall()
        if len(result) == 1:
            print("Podany login już jest zajęty")
            User.newCustomer(self)
        else:
            passw = input("Podaj haslo")
            adress = input("Podaj adres")
            phone = input("Podaj numer telefonu")
            self.c.execute("INSERT INTO users values (0,%s,%s,%s,%s,%s,%s,%s)",
                           (name, surname, login, passw, adress, phone, "admin"))
            dec = input("czy na pewno chcesz dodac użytkownika T/N").upper()
            if dec == "T":
                self.conn.commit()
                print("dodano uzytkownika")
            else:
                self.conn.rollback()
                print("powrot do menu")

    def editUser(self):
        User.usersList(self)
        id = input("podaj id klienta, którego chcesz edytować")
        dec = input("edytuje:\n1 - imię\n2 - nazwisko\n3 - adres\n4 - telefon\n5 - typ")
        if dec == "1":
            new = input("podaj nowe imie")
            self.c.execute("UPDATE users SET name = %s WHERE user_id=%s", (new, id))
            dec = input("czy na pewno chcesz zmienic imie T/N").upper()
            if dec == "T":
                self.conn.commit()
                print("zmieniono imie na "+new)
            else:
                self.conn.rollback()
                print("powrot do menu")
        elif dec == "2":
            new = input("podaj nowe nazwisko")
            self.c.execute("UPDATE users SET surname = %s WHERE user_id=%s", (new, id))
            dec = input("czy na pewno chcesz zmienic nazwisko T/N").upper()
            if dec == "T":
                self.conn.commit()
                print("zmieniono nazwisko na "+new)
            else:
                self.conn.rollback()
                print("powrot do menu")
        elif dec == "3":
            new = input("podaj nowy adres")
            self.c.execute("UPDATE users SET adress = %s WHERE user_id=%s", (new, id))
            dec = input("czy na pewno chcesz zmienic adres T/N").upper()
            if dec == "T":
                self.conn.commit()
                print("zmieniono adres na "+new)
            else:
                self.conn.rollback()
                print("powrot do menu")
        elif dec == "4":
            new = input("podaj nowy numer telefonu")
            self.c.execute("UPDATE users SET phone = %s WHERE user_id=%s", (new, id))
            dec = input("czy na pewno chcesz zmienic numer telefonu T/N").upper()
            if dec == "T":
                self.conn.commit()
                print("zmieniono numer telefonu na "+new)
            else:
                self.conn.rollback()
                print("powrot do menu")
        elif dec == "5":
            new = input("podaj typ admin lub customer")
            self.c.execute("UPDATE users SET type = %s WHERE user_id=%s", (new, id))
            dec = input("czy na pewno chcesz zmienic typ uzytkownika T/N").upper()
            if dec == "T":
                self.conn.commit()
                print("zmieniono typ uzytkownika na "+new)
            else:
                self.conn.rollback()
                print("powrot do menu")
        else:
            User.editUser(self)

    def editUserContact(self,login):
        print(login)
        self.c.execute("SELECT * FROM users WHERE login = %s", (login))
        User.displayList(self)
        dec = input("Co chesz edytować? :\n1 - adres\n2 - telefon")
        if dec == "1":
            new = input("Podaj nowy adres")
            self.c.execute("UPDATE users SET adress = %s WHERE login=%s", (new, login))
            dec = input("Czy na pewno chcesz zmienic adres T/N").upper()
            if dec == "T":
                self.conn.commit()
                print("Zmieniono adres na " + new)
            else:
                self.conn.rollback()
                print("Powrot do menu")
        elif dec == "2":
            new = input("Podaj nowy numer telefonu")
            self.c.execute("UPDATE users SET phone = %s WHERE login=%s", (new, login))
            dec = input("Czy na pewno chcesz zmienic numer telefonu T/N").upper()
            if dec == "T":
                self.conn.commit()
                print("Zmieniono numer telefonu na " + new)
            else:
                self.conn.rollback()
                print("Powrot do menu")
        else:
            print("Błędny wybór")
            self.menuCustomer(login)

    def displayList(self):
        list = self.c.fetchall()
        for row in list:
            UserId   = 0
            Name     = 1
            Surname  = 2
            Login    = 3
            Password = 4
            Adress   = 5
            Phone    = 6
            Type     = 7
            print("%-2s %-10s %-15s %-12s %-12s %-35s %-10s %-10s "
                  %(row[UserId], row[Name], row[Surname], row[Login], row[Password], row[Adress], row[Phone], row[Type]))


class Car:

    def carsMenu(self):
        dec = input("Samochody:\n1 - lista samochodów\n2 - dodaj nowy samochód\n3-menu głowne")
        if dec == "1":
            Car.carList(self)
            Car.carsMenu(self)
        elif dec == "2":
            Car.addCar(self)
            Car.carsMenu(self)
        elif dec == "3":
            Menu.menuAdmin(self)
        else:
            print("Błędny wybór")
            Car.carsMenu(self)

    def carList(self):
        self.c.execute("SELECT * FROM cars")
        Car.displayCars(self)

    def addCar(self):
        brand = input("podaj markę")
        model = input("podaj model")
        cls = input("podaj klasę: 'mini' 'compact'  'medium'  'standard'  'premium'")
        year = input("podaj rocznik")
        regnbr = input("podaj Numer rejestracyjny")
        price = float(input("podaj cenę"))
        self.c.execute("INSERT INTO cars values(0,%s,%s,%s,%s,%s,%s)", (brand, model, cls, year, regnbr, price))
        dec = input("czy na pewno chcesz dodać nowy samochód T/N").upper()
        if dec == "T":
            self.conn.commit()
            print("Dodano nowy samochód " + brand + " " + model)
        else:
            self.conn.rollback()
            print("powrot do menu")

    def displayCars(self):
        list = self.c.fetchall()
        if len(list) == 0:
            print("Brak wynajmów spełniających kryteria")
        else:
            for row in list:
                CarId  = 0
                Brand  = 1
                Model  = 2
                Class  = 3
                Year   = 4
                RegNBR = 5
                Price  = 6

                print("numer samochodu: %2s Marka: %-10s Model: %-10s Klasa: %-8s Rocznik: %-8s Numer rejestracyjny:"
                      " %-12s Cena %-12s" % (row[CarId], row[Brand], row[Model], row[Class], row[Year], row[RegNBR],
                        row[Price]))


Menu = Menu()