class Machine:
    def print(self, document):
        pass
    def scan(self, document):
        pass
    def fax(self, document):
        pass

class OldFashionedPrinter(Machine):
    def print(self, document):
        # Implementation of print
        print("Printing document...")
    
    def scan(self, document):
        raise NotImplementedError("This printer cannot scan.")
    
    def fax(self, document):
        raise NotImplementedError("This printer cannot fax.")