# This is where the wordlists can be created.
# It can be helpful to save as a guide to wordlists that have been created.

import Database2Lister as dl

# Now I will add a few lists for examples
# This is one way to add words sequentially
add_list = True

if add_list:
    DeregBingo_wow24 = dl.search_subgram('DEREGULATIONS', 7, 8, lexicon = 'wow24')
    DeregNine_wow24 = dl.search_subgram('DEREGULATIONS', 9, 9, lexicon = 'wow24')
    HighFive_wow24 = dl.search_list(['length = 5', 'score > 10'], lexicon = 'wow24')
    dl.save_entries(DeregBingo_wow24, 'DeregBingo', lexicon = 'wow24')
    dl.save_entries(DeregNine_wow24, 'DeregNine', lexicon = 'wow24')
    dl.save_entries(HighFive_wow24, 'HighFive', lexicon = 'wow24')
    conn.commit()

# I like starting with 2-4 letter words (in order of length) and
# ... deregulations bingos. XJZQ words and vowel dumps are also useful
    
