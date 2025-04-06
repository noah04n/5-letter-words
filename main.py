import time
from tqdm import tqdm
word_length = 5
clique_size = 5

def load_words():
    words_txt = './words_alpha.txt'
    with open(words_txt) as word_file:
        read_words = list(word_file.read().split())

    print(f"{len(read_words)} words loaded")
    return read_words

def extract_n_letter_words(words, n):
    temp = list()
    for w in words:
        if len(w) == n:
            temp.append(w)
    print(f"{len(temp)} words have {n} letters")
    return temp

def unique_words(words, n):
    temp = list()
    anagram_dict = {}

    for w in words:
        unique_letters = set(w)
        sorted_word = ''.join(sorted(w))
        if len(unique_letters) == n:
            if unique_letters not in temp and sorted_word not in anagram_dict:
                temp.append(w)
                anagram_dict[sorted_word]= w
    print(f"{len(temp)} words have a unique set of {n} letters")
    return temp

def create_adj_list(words):
    n = len(words)

    # Initialize adjacency list
    adj_list = {}

    # Add vertices to the dictionary
    for i in range(n):
        adj_list[words[i]] = set()

    # Add edges
    for i in tqdm(range(n),"Adjacency Construction"):
        for j in range(n):

            # Check if they have no letters in common
            if (words[i] & words[j]) == 0:
                adj_list[words[i]].add(words[j])

    return adj_list

def words_to_bitmasks(words):
    bitwords = []
    for word in words:
        bitmask = 0
        for char in word:
            bitmask |= 1 << (ord(char) - ord('a'))
        bitwords.append(bitmask)

    return bitwords

def bitmasks_to_words(bitmasks, bitlist, wordlist):
    words = []
    for bitmask in bitmasks:
        words.append(wordlist[bitlist.index(bitmask)])
    return words

def find_cliques(adj_list, clique_size, bitlist, wordlist):
    result = []
    all_nodes = set(adj_list.keys())

    def backtrack(current_clique, candidates):
        # If the number of candidates if less than the required clique size
        # Stop immediately
        if len(current_clique) + len(candidates) < clique_size:
            return None

        # If the current clique size is n, we found a complete subgraph
        if len(current_clique) == clique_size:
            return current_clique

        # For each candidate, try to expand the clique
        for vertex in list(candidates):
            new_candidates = candidates.intersection(adj_list[vertex])
            clique_found = backtrack(current_clique | {vertex}, new_candidates)
            if clique_found is not None:
                return clique_found
            candidates.remove(vertex)
        return None

    # Iterate over the remaining nodes until none are left
    while all_nodes:
        node = all_nodes.pop()
        clique = backtrack({node}, set(adj_list[node]))
        if clique is not None:
            # A valid clique was found.
            result.append(list(clique))
            print("New result:")
            print(bitmasks_to_words(clique, bitlist, wordlist))

            # Remove each word of the answer from subsequent searches
            for v in clique:
                if v in all_nodes:
                    all_nodes.remove(v)
                if v in adj_list:
                    del adj_list[v]
            
            for key in list(adj_list.keys()):
                adj_list[key] = adj_list[key] - clique

    return result

start = time.time()

# Load words as a list
words = load_words()
words = extract_n_letter_words(words, word_length)
words = unique_words(words, word_length)

bitwords = words_to_bitmasks(words)

# Build the graph as an adjacency list
adj_list = create_adj_list(bitwords)

result = find_cliques(adj_list, clique_size, bitwords, words)
print("Result: ")
for i in range(len(result)):
    print(bitmasks_to_words(result[i], bitwords, words))

end = time.time()

# Print how much time (in seconds) the code took
print(f"Execution time: {end-start} seconds")