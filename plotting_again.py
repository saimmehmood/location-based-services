#from gmplot import gmplot

API_KEY = 'AIzaSyCcFSRX4kExONVVB9cqQynjh7EXgZwcyaI'

#gmap = gmplot.GoogleMapPlotter(43.739829, -79.514102, 13, API_KEY)


found_comma = False
string_1 = ""
string_2 = ""

with open("points_check.txt") as f:
    for line in f:

        if not found_comma:
            split_line = line.split(",")

            if len(split_line) == 1:
                string_1 += split_line[0].replace("\n", "")

            else:
                found_comma = True
                string_1 += split_line[0].replace("\n", "")
                string_2 += split_line[1].replace("\n", "")

        else:
            string_2 += line.replace("\n", "")

    print(string_1)
    print(string_2)

#
# l1 = (str(line).replace("[","").replace("]","").replace(" ", "").replace("\n","").split(','))
#
# print(l1)
# gmap.marker(float(w), float(h), 'green')

# Draw
# gmap.draw("my_map.html")

