class Name:
    def __init__(self, first, last):
        self.first = first
        self.last = last

    def fullname(self):
        return f"{self.first} {self.last}"

if __name__ == "__main__":
    first = "raju"
    last = "baludu"
    name = Name(first, last)
    print(name.fullname())
