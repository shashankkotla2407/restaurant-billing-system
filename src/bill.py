class Bill:
    def __init__(self, tax_rate=0.05):
        self.tax_rate = tax_rate

    def calculate_tax(self, amount):
        return round(amount * self.tax_rate, 2)

    def calculate_total(self, amount):
        tax = self.calculate_tax(amount)
        return round(amount + tax, 2)