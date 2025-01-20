import time
from tqdm import tqdm
word_length = 5
set_length = 5

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
        adj_list[words[i]] = []

    # Add edges
    for i in tqdm(range(n),"Adjacency Construction"):
        for j in range(n):

            if set(words[i]).isdisjoint(words[j]):
                adj_list[words[i]].append(words[j])

    return adj_list



def find_cliques(adj_list, clique_size):
    def backtrack(current_clique, candidates):

        # If the current clique size is n, we found a complete subgraph
        if len(current_clique) == clique_size:
            result.append(list(current_clique))
            print("New result: ")
            print(current_clique)

            # No longer want to consider these words in next searches
            for word in current_clique:
                # Cut off all its edges
                adj_list[word] = []
            return

        # Iterate over vertices starting from 'start'
        for word in list(candidates):
            new_candidates = candidates & set(adj_list[word])
            current_clique.append(word)
            backtrack(current_clique, new_candidates)
            current_clique.pop()


    result = list()

    for word in tqdm(adj_list,"Search Progress"):
        backtrack([word], set(adj_list[word]))
    return result

def words_to_bitmasks(words):
    # Convert a word to a 26-bit integer representing its letters

    bitwords = []
    for word in words:
        bitmask = 0
        for char in word:
            bitmask |= 1 << (ord(char) - ord('a'))
        bitwords.append(bitmask)

    return bitwords

start = time.time()

# Load words as a list
words = load_words()
words = extract_n_letter_words(words, word_length)
words = unique_words(words, word_length)

adj_list = create_adj_list(words)

result = find_cliques(adj_list, set_length)
print("Result: " + str(result))

end = time.time()
print(f"Execution time: {end-start} seconds")