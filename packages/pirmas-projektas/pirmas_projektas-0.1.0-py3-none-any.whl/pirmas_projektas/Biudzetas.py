class Biudzetas:
    def __init__(self):
        self.pajamos = []
        self.islaidos = []

    def ivesti_pajamas(self, pajamu_suma):
        self.pajamos.append({"suma": pajamu_suma})

    def ivesti_islaidas(self, islaidu_suma):
        self.islaidos.append({"suma": islaidu_suma})

    def parodyti_biudzeta(self):
        print("Pajamos:")
        for i, pajama in enumerate(self.pajamos, 1):
            print(f"{i}. {pajama['suma']:.2f}")
        print("Išlaidos:")
        for i, islaida in enumerate(self.islaidos, 1):
            print(f"{i}. {islaida['suma']:.2f}")

    def parodyti_balansa(self):
        pajamu_suma = sum(pajama["suma"] for pajama in self.pajamos)
        islaidu_suma = sum(islaida["suma"] for islaida in self.islaidos)
        balansas = pajamu_suma - islaidu_suma
        print(f"Pajamų suma: {pajamu_suma:.2f}")
        print(f"Išlaidų suma: {islaidu_suma:.2f}")
        print(f"Balansas: {balansas:.2f}")