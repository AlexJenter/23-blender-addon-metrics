import csv


def generate_material_enum_items(csv_path):
    # https://www.scheideanstalt.de/metallglossar/metallglossar/
    with open(csv_path, newline='') as csvfile:
        table_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        mat_items = []
        for row in list(table_reader)[1:]:

            name, short_name, density, melting_point, comment = row

            mat_items.append((density,
                              name,
                              f"[{short_name:<2}] {name}\nDichte: {density:>7}kg/m³\n\n{comment}"))

    return mat_items
