class FacebookUser:
    id = ''
    name = ''
    weight = 0

    def __init__(self, id, name, weight = 0):
        self.id = id
        self.name = name
        self.weight = weight

    def change_weight(self, diff):
        self.weight += diff

    def __hash__(self):
        return hash((self.id, self.name))

    def __eq__(self, other):
        return (self.id, self.name) == (other.id, other.name)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)


class Edge:
    id = ''
    source = FacebookUser('', '')
    target = FacebookUser('', '')
    name = ''
    weight = 0

    def __init__(self, id, source, target, name, weight = 0):
        self.id = id
        self.source = source
        self.target = target
        self.name = name
        self.weight = weight

    def change_weight(self, diff):
        self.weight += diff