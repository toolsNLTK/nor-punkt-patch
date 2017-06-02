# nor-punkt-patch
Patch for NLTK's Norwegian sent punkt tokenizer

Takes a list of sentences and further tokenize the sentences;
 
Split at colon:

    Punkt: ∗ '[...] tre gaver som var gitt til paven personlig: En sjekk på [...]'
    Gold: '[...] tre gaver som var gitt til paven personlig:' | 'En sjekk på [...]'
    
Split after delimiter and guillemet:

    Punkt: ∗ '[...] regninger og sånn?» Det var liksom ikke [...]'
    Gold: '[...] regninger og sånn?»' | 'Det var liksom ikke [...]'
    
Split after multiple delimiters:

    Punkt: ∗ '[...] meg ned i bilen i går kveld ... Hvordan resten [...]'
    Gold: '[...] meg ned i bilen i går kveld ...' | 'Hvordan resten [...]'
    
Stitch interpose sentences:

    Punkt: ∗ 'Siden Hagen (intil videre?)' | 'fortsatt kommer til å [...]'
    Gold: 'Siden Hagen (intil videre?) fortsatt kommer til å [...]'
    
Stitch non-alphabetic sentences to a sentence:

    Punkt: ∗ '3.' | 'Alternativ til statskirkeordningen og [...]'
    Gold: '3. Alternativ til statskirkeordningen og [...]'

(Gold is Norwegian Dependency Treebank (NDT), 
 http://www.nb.no/sprakbanken/show?serial=sbr-10)
 
Then returns a list of sentences that match gold.
