class CustomCross:
    def __init__(self, filename):
        self.filename = filename

    def parse_file(self):
        with open(self.filename, 'r') as file_custom_cross:
            data = file_custom_cross.read().splitlines(True)
        file_custom_cross.close()
        for row in data:
            print(data)
