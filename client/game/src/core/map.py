class Map:
    def __init__(self, name, width, height, data):
        self.name = name
        self.width = width
        self.height = height
        self.data = data

    def __str__(self):
        return self.name + '\t' + str(self.width) + 'x' + str(self.height) + '\n' + str('\n'.join(self.data))