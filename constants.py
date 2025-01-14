categories_plural = ["(nom.)", "(art.)"]
categories_verb = ["(vrb.)"]

# Color management
available_colors = "blue, green, orange, red, violet, grey, rainbow, primary".split(
    ", "
)

color_word_simple = "violet"
color_etimology = "green"

assert color_word_simple in available_colors
assert color_etimology in available_colors

color_word_complex = "#8b0000"