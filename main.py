word_length = 5

def load_words():
    words_txt = './words_alpha.txt'
    with open(words_txt) as word_file:
        valid_words = list(word_file.read().split())
    return valid_words

english_words = load_words()

print(f"{len(english_words)} words in total")

fl_words = []

for w in english_words:
    if len(w) == word_length:
        fl_words.append(w)

print(f"{len(fl_words)} words have {word_length} letters")


word_sets = []

unique_fl_words = []
for w in fl_words:
    unique_letters = set(w)
    if len(unique_letters) == word_length:
        if unique_letters not in word_sets:
            word_sets.append(unique_letters)
            unique_fl_words.append(w)

number_of_words = len(unique_fl_words)

print(f"{number_of_words} words have a unique set of {word_length} letters")

def build_graph(words):
    # Step 1: Preprocess words into sets of letters for efficient comparison
    word_sets = {word: set(word) for word in words}

    # Step 2: Initialize the graph as an adjacency list
    graph = {word: [] for word in words}

    # Step 3: Add edges between words with no common letters
    for word1 in words:
        for word2 in words:
            if word1 != word2 and word_sets[word1].isdisjoint(word_sets[word2]):
                graph[word1].append(word2)

    return graph

def filter_vertices_by_edge_count(graph, edge_count):
    # Filter vertices by the number of edges
    return {vertex: neighbors for vertex, neighbors in graph.items() if len(neighbors) == edge_count}


# Example usage
words = ["cat", "dog", "fish", "bird", "apple"]
graph = build_graph(words)
# graph = build_graph(unique_fl_words)

desired_edge_count = 2
filtered_graph = filter_vertices_by_edge_count(graph, desired_edge_count)

# Display the graph
for vertex, neighbors in filtered_graph.items():
    print(f"{vertex} ({len(neighbors)} edges): {neighbors}")