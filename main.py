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

            # Check if they have no letters in common
            if (words[i] & words[j]) == 0:
                adj_list[words[i]].append(words[j])

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
    def backtrack(current_clique, candidates):

        # If the current clique size is n, we found a complete subgraph
        if len(current_clique) == clique_size:
            result.append(list(current_clique))
            print("New result: ")
            print(bitmasks_to_words(current_clique, bitlist, wordlist))

            # No longer want to consider these words in next searches
            for word in current_clique:
                # Cut off all its edges
                adj_list.pop(word)
            return 1

        # Iterate over vertices starting from 'start'
        for word in list(candidates):
            if word in adj_list.keys():
                new_candidates = candidates & set(adj_list[word]) # O(n) n = adjacency size
                current_clique.append(word)
                if backtrack(current_clique, new_candidates) :
                    return 1
                current_clique.pop()


    result = list()
    adj_list_cp = adj_list.copy()
    for word in tqdm(adj_list_cp,"Search Progress"):
        if word in adj_list.keys():
            backtrack([word], set(adj_list[word]))
    return result



start = time.time()

# Load words as a list
words = load_words()
words = extract_n_letter_words(words, word_length)
words = unique_words(words, word_length)

valid_words = ["vibex", "glyph", "muntz", "dwarf","jocks","hello"]
# words = valid_words
bitwords = words_to_bitmasks(words)


# Build the graph as an adjacency list
adj_list = create_adj_list(bitwords)

# adj_list = {7: [3, 5],3: [2, 1, 4, 5],5: [3, 7], 1: [2,4,3], 2: [1, 4, 3]}

result = find_cliques(adj_list, set_length, bitwords, words)
print("Result: ")
for i in range(len(result)):
    print(bitmasks_to_words(result[i], bitwords, words))

end = time.time()
# Print how much time (in seconds) the code took
print(f"Execution time: {end-start} seconds")