class Calculator:
    def __init__(self):
        self.symbol = input("Pasirinkite veiksmą: -,+,/,* : ")
        self.number1 = int(input("Įrašykite pirmą skaičių: "))
        self.number2 = int(input("Įrašykite antrą skaičių: "))
    
    def add(self):
        return self.number1 + self.number2
    
    def sub(self):
        return self.number1 - self.number2
    
    def div(self):
        if self.number2 == 0:
            raise ValueError("Dalyba iš nulio negalima")
        return self.number1 / self.number2  
    
    def mul(self):      
        return self.number1 * self.number2   
        
    def calculate(self):        
        if self.symbol == '+':
            return self.add()
        elif self.symbol == '-':
            return self.sub()
        elif self.symbol == '/':
            return self.div()
        elif self.symbol == '*':
            return self.mul()
        else :
            raise ValueError("Netinkamas simbolis")
    def __str__(self):
        return f"Skaičiuojama: {self.number1} {self.symbol} {self.number2}"
            
rezultatas = Calculator()
print(rezultatas.calculate())
