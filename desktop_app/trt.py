lego_bricks = dict()  # cheia va fi id-ul, valoarea va fi [obiect, is_used]; lista va contine toate piesele initializate


class Brick:
    def __init__(self, length, width, height, color, space, studs, tubes):
        global lego_bricks
        self.brick_id = len(lego_bricks) + 1  # cheia dictionarului
        self.length = length
        self.width = width
        self.height = height
        self.color = color
        # self.weight = weight -> trebuie sau nu?

        # urmatoarele atribute vor avea cate o lista cu coordonatele lor pe un plan in care se afla doar piesa respectiva
        self.space = space
        self.studs = studs
        self.tubes = tubes

        # urmatoarele atribute sunt folosite atunci cand piesa este pusa in alta piesa
        self.start_coordinates = [-1, -1, -1]  # coordonatele de unde incepe (coltul din stanga sus <=> unde x, y minim)
        self.rotation = 0  # 0 -> in dreapta, 1 -> in jos, 2 -> in stanga, 3 -> in sus
        self.occupied_space = []  # lista de liste [x, y, z]
        self.stud_coordinates = []  # studs = spatiile de sus; flagurile vor fi id-ul pieselor inserate (0 daca nu e nicio piesa <=> e liber)
        self.tube_coordinates = []  # tubes = spatiile de jos; la fel ca sus

        lego_bricks[self.brick_id] = [self, False]

    # functia asta pune obiectul peste alte obiecte (in studs)
    # piesa va fi pusa de la x la x + width, y la y + length, z la z + height
    def place_in_studs(self, start_coordinates, brick_list):
        pass

    # functia asta pune obiectul in tuburile altui obiect
    def place_in_tubes(self, start_coordinates, brick_list):
        pass

    # flag-ul din dictionar se face fals, listele occupied_space, stud_coordinates, tube_coordinates primesc [] ca noua valoare
    # in functie de id-ul din stud_coordinates a piesei curente, se reseteaza flag-urile din tube_coordinates din piesele respective
    def remove_from_studs(self):
        pass

    # flag-ul din dictionar se face fals, listele occupied_space, stud_coordinates, tube_coordinates primesc [] ca noua valoare
    # in functie de id-ul din tube_coordinates a piesei curente, se reseteaza flag-urile din stud_coordinates din piesele respective
    def remove_from_tubes(self):
        pass

    # metoda care incearca sa puna piesa asta in studs/tubes la o lista de id-uri ale pieselor
    #   daca primeste parametru cu coordonate va incerca sa o faca de acolo, altfel backtracking
    # cum o va face -> face o lista din toate listele cu studs/tubes care au flag de neocupat


if __name__ == '__main__':
    test_brick = Brick(1, 1, 1, "White", [[0, 0, 0]], [[0, 0, 0]], [[0, 0, 0]])  # piesa generica de 1x1x1
    test_brick_2 = Brick(2, 2, 3, "White",
                         [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 0], [0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 1],
                          [0, 0, 2], [0, 1, 2], [1, 0, 2], [1, 1, 2]],
                         [[0, 0, 2], [0, 1, 2], [1, 0, 2], [1, 1, 2]],
                         [[0, 0, 0], [0, 1, 0], [1, 0, 0],
                          [1, 1, 0]])  # piesa generica de 2x2x3 (2x2 de inaltime "normala")
    print(lego_bricks)