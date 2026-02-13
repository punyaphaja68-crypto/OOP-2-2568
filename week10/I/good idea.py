from abc import abstractmethod

class Printer:
    @abstractmethod
    def print(self, document):
        pass

class Scanner:
    @abstractmethod
    def scan(self, document):
        pass

class Fax:
    @abstractmethod
    def fax(self, document):
        pass

class MultiFunctionPrinter(Printer, Scanner, Fax):
    def print(self, docment):
        print("Printing doucment")
    def scan(self, document):
        print("Scanning doucment")
    def fax(self, document):
        print("Faxing doucment")