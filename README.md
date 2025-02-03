# Five Letter Words
This code is my attempt at writing an efficient program to find all the sets of five five-letter words with twenty-five unique letters, inspired by Matt Parker’s [video](https://youtu.be/_-AfhLQfb6w?feature=shared) on the subject.

His attempt was written in Python and took 32 days of computing time. Shortly after speaking about his attempt on his podcast, a viewer created a python program to complete the same task in about 15 minutes.

Going into this I gave myself one rule: not to look at any of the other viewer’s submissions. The only assistance I had was the knowledge that the first person to beat Matt’s attempt used graph theory.
## My Approach
Knowing that graph theory could provide an efficient method for solving this problem, my approch works using the following steps:
* Prune word list down to all unique 5-letter words
* Convert the words to bitmasks for efficient comparison
* Create an adjacency list representation of all the words by having them connected to eachother if and only if they have no letters in common
* Each word in the adjacency list is stored as a key in a dictionary which points to a set object containing all its neighbours
* For each word, consider its neighbours candidates and expand the clique
* If each word in the current clique is in the candidate's neighbours set, we add that candidate to the current clique
* We continue until we have a clique of size 5, at which point we return the clique and remove those words from consideration

## Attempt History
### Attempt 1
My first functional attempt was run on a very old (2013-era) Lenovo laptop overnight and had the following results:

[‘ambry', 'pungs', 'vejoz', 'fldxt', 'whick'],
['ampyx', 'fjeld', 'chivw', 'gunks', 'bortz'],
['ampyx', 'crwth', 'glink', 'fdubs', 'vejoz'], 
['ampyx', 'hdqrs', 'bejig', 'fconv', 'klutz'], 
['ampyx', 'hdqrs', 'twick', 'flung', 'vejoz'], 
['avick', 'grosz', 'whump', 'benjy', 'fldxt'], 
['bawke', 'gconv', 'fultz', 'jimpy', 'hdqrs'], 
['becky', 'voraz', 'jumps', 'whing', 'fldxt'], 
['becks', 'vingt', 'japyx', 'frowl', 'zhmud'], 
['becks', 'whang', 'jumpy', 'vizor', 'fldxt'], 
['bizen', 'gucks', 'jarvy', 'whomp', 'fldxt'], 
['blitz', 'mawks', 'gryph', 'judex', 'fconv'], 
['block', 'windz', 'vughs', 'fremt', 'japyx'], 
['bovld', 'freck', 'whigs', 'muntz', 'japyx'], 
['bumph', 'wiver', 'jacks', 'zygon', 'fldxt'], 
['bumph', 'gravy', 'winze', 'jocks', 'fldxt'], 
['bumph', 'zincy', 'javer', 'gowks', 'fldxt'], 
['bumph', 'vower', 'zings', 'jacky', 'fldxt'], 
['chang', 'jowpy', 'mirvs', 'uzbek', 'fldxt'], 
['chimb', 'expwy', 'vangs', 'fjord', 'klutz'], 
['chomp', 'zingy', 'quawk', 'verbs', 'fldxt'], 
['evang', 'qophs', 'wrick', 'jumby', 'fldxt'], 
['expdt', 'furzy', 'jambs', 'whilk', 'gconv'], 
['expdt', 'furzy', 'jambs', 'klong', 'chivw'], 
['fcomp', 'vibex', 'waltz', 'junky', 'hdqrs'], 
['fcomp', 'vibex', 'waltz', 'gunky', 'hdqrs'], 
['johns', 'wramp', 'vicky', 'uzbeg', 'fldxt']

27 Answers
Execution time: 50443.78 s =14.01 hrs

First thing to note here is that in my first attempt I forgot to have the program discard words that I had used in a solution from subsequent solutions causing it to return far more solutions than expected, most of which are the same but with a single word changed.

Not great but better than Matt’s first attempt. My next ideas to improve speed are:
* Use bitmasks to represent the words for faster comparisons
* Use sets for faster inclusion checking

### Attempt 2:
Result:
['ambry', 'vejoz', 'fldxt', 'pucks', 'whing']
['ampyx', 'bortz', 'chivw', 'fjeld', 'gunks']
['bawke', 'fultz', 'gconv', 'jimpy', 'hdqrs']
['becks', 'frowl', 'japyx', 'zhmud', 'vingt']
['blitz', 'gryph', 'fconv', 'mawks', 'judex']
['chimb', 'fjord', 'vangs', 'klutz', 'expwy']
['dwarf', 'vibex', 'glyph', 'jocks', 'muntz']

7 Answers
Execution time: 94446.11 s = 26.24 hrs

Ok so now we are getting the expected amount of answers but clearly the amount of time this took to run is not optimal!

### Attempt 3:
Result: 
['whing', 'vejoz', 'bryum', 'packs', 'fldxt']
['klutz', 'gawby', 'fcomp', 'hdqrs', 'vixen']
['fritz', 'japyx', 'gconv', 'dumbs', 'whelk']
['nymph', 'waltz', 'gucks', 'fjord', 'vibex']
['gryph', 'mawks', 'blitz', 'fconv', 'judex']
['gunks', 'ampyx', 'bortz', 'chivw', 'fjeld']
['jarvy', 'flong', 'zhmud', 'twick', 'pbxes']

7 Answers
Execution time: 6307.44 s = 1.75 hrs

For this attempt I noticed some places where the comparisons could be done with sets which take constant time O(1) to access (and thus check inclusion). This seemed to improve speed by a large margin but obviously there is a long way to go. I’m still a bit dissapointed that I’m not yet at the speed of the first person to beat Matt’s time but oh well, I will persist.

