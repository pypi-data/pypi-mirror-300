class Biudzetas:
    def __init__(self):
        self.balansas = 0

    def prideti_pajamas(self, suma):
        self.balansas += suma
        print(f"Pridėta {suma} EUR pajamų. Dabartinis balansas: {self.balansas} EUR")

    def prideti_islaidas(self, suma):
        if suma > self.balansas:
            print("Nepakanka lėšų šioms išlaidoms!")
        else:
            self.balansas -= suma
            print(f"Pridėta {suma} EUR išlaidų. Dabartinis balansas: {self.balansas} EUR")

    def parodyti_biudzeta(self):
        print(f"Dabartinis biudžeto balansas: {self.balansas} EUR")