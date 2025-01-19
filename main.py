from tqdm import tqdm
word_length = 5
set_length = 5

def load_words():
    words_txt = './words_alpha.txt'
    with open(words_txt) as word_file:
        read_words = set(word_file.read().split())

    print(f"{len(read_words)} words loaded")
    return read_words

def extract_n_letter_words(words, n):
    temp = set()
    for w in words:
        if len(w) == n:
            temp.add(w)
    return temp

def unique_words(words):
    temp = set()
    anagram_dict = {}
    # for w in words:
    #     sorted_word = ''.join(sorted(w))
    #     if sorted_word not in anagram_dict:
    #         anagram_dict[sorted_word] = set()
    #     anagram_dict[sorted_word].add(w)

    for w in words:
        unique_letters = set(w)
        sorted_word = ''.join(sorted(w))
        if len(unique_letters) == word_length:
            if unique_letters not in temp and sorted_word not in anagram_dict:
                temp.add(w)
                anagram_dict[sorted_word]= w
    return temp

def create_adjacency_matrix(words):
    # Convert words to a list (for indexing) and precompute letter sets
    letter_sets = [set(word) for word in words]
    n = len(words)

    # Initialize the adjacency matrix with zeros
    adj_matrix = [[0] * n for _ in range(n)]

    # Fill the adjacency matrix
    for i in range(n):
        for j in range(n):
            if i != j and letter_sets[i].isdisjoint(letter_sets[j]):
                adj_matrix[i][j] = 1

    return adj_matrix

def bron_kerbosch_fixed_size(R, P, X, adj_matrix, cliques, target_size):
    # If R has reached the target size, check if it's a valid clique
    if len(R) == target_size:
        if not P and not X:  # No more vertices to add or exclude
            cliques.append(R)
        return

    # Stop recursion if R exceeds the target size
    if len(R) > target_size:
        return

    for v in list(P):
        # Neighbors of v
        neighbors = {u for u in range(len(adj_matrix)) if adj_matrix[v][u] == 1}

        bron_kerbosch_fixed_size(
            R | {v},                  # Add v to current clique
            P & neighbors,            # Restrict to neighbors of v
            X & neighbors,            # Exclude neighbors of v
            adj_matrix,
            cliques,
            target_size               # Keep target size constraint
        )

        P.remove(v)
        X.add(v)

def find_cliques(adj_matrix, target_size):
    cliques = []
    n = len(adj_matrix)

    # Call the modified Bron–Kerbosch algorithm
    bron_kerbosch_fixed_size(set(), set(range(n)), set(), adj_matrix, cliques, target_size)
    return cliques


words = load_words()
words = extract_n_letter_words(words, word_length)
print(f"{len(words)} words have {word_length} letters")

words = unique_words(words)
words = list(words)
words = words[:2000]
print(f"{len(words)} words have a unique set of {word_length} letters")

adj_matrix = create_adjacency_matrix(words)

cliques = find_cliques(adj_matrix, 3)
print(cliques[0])
matches = []
for match in cliques[0]:
    matches.append(words[match])
print(matches)

