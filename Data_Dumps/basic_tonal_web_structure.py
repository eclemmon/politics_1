# Not really basic, but rather basic as fuck.
basic_major_tonal_web = {
    # CMaj
    (0, 4, 7): [(0, 4, 7, 11), (2, 5, 9), (2, 5, 9, 0), (5, 9, 0), (5, 9, 0, 4), (9, 0, 4), (9, 0, 4, 7), (7, 11, 2),
                (7, 11, 2, 5), (11, 2, 5), (11, 2, 5, 6)],
    # CMaj7
    (0, 4, 7, 11): [(0, 4, 7), (2, 5, 9), (2, 5, 9, 0), (5, 9, 0), (5, 9, 0, 4), (9, 0, 4), (9, 0, 4, 7), (7, 11, 2),
                    (7, 11, 2, 5), (11, 2, 5), (11, 2, 5, 6)],
    # dmin
    (2, 5, 9): [(2, 5, 9, 0), (5, 9, 0), (5, 9, 0, 4), (7, 11, 2), (7, 11, 2, 5), (11, 2, 5), (11, 2, 5, 6)],
    # Ddmin7
    (2, 5, 9, 0): [(2, 5, 9), (5, 9, 0), (5, 9, 0, 4), (7, 11, 2), (7, 11, 2, 5), (11, 2, 5), (11, 2, 5, 6)],
    # FMaj
    (5, 9, 0): [(0, 4, 7), (0, 4, 7, 11), (2, 5, 9), (2, 5, 9, 0), (5, 9, 0, 4), (9, 0, 4), (9, 0, 4, 7), (7, 11, 2),
                (7, 11, 2, 5)],
    # FMaj7
    (5, 9, 0, 4): [(0, 4, 7), (0, 4, 7, 11), (2, 5, 9), (2, 5, 9, 0), (5, 9, 0), (9, 0, 4), (9, 0, 4, 7), (7, 11, 2),
                   (7, 11, 2, 5)],
    # GMaj
    (7, 11, 2): [(0, 4, 7), (0, 4, 7, 11), (9, 0, 4), (9, 0, 4, 7), (7, 11, 2, 5)],
    # G7
    (7, 11, 2, 5): [(0, 4, 7), (0, 4, 7, 11), (9, 0, 4), (9, 0, 4, 7)],
    # amin
    (9, 0, 4): [(0, 4, 7, 11), (2, 5, 9), (2, 5, 9, 0), (5, 9, 0), (5, 9, 0, 4), (9, 0, 4, 7), (7, 11, 2),
                (7, 11, 2, 5), (11, 2, 5), (11, 2, 5, 6)],
    # amin7
    (9, 0, 4, 7): [(0, 4, 7, 11), (2, 5, 9), (2, 5, 9, 0), (5, 9, 0), (5, 9, 0, 4), (9, 0, 4), (7, 11, 2),
                   (7, 11, 2, 5), (11, 2, 5), (11, 2, 5, 6)],
    # bº
    (11, 2, 5): [(0, 4, 7), (0, 4, 7, 11), (9, 0, 4), (9, 0, 4, 7)],
    # b/º7
    (11, 2, 5, 6): [(0, 4, 7), (0, 4, 7, 11), (9, 0, 4), (9, 0, 4, 7)]
}

if __name__ == "__main__":
    print(basic_major_tonal_web[(11, 2, 5, 6)])
