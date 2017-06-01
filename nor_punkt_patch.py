"""
Patch for Norwegian sentence tokenizer

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
   

Then returns a list of sentences that match gold.
"""

def sent_patch(sentences):
    delims = ['.', '?', '!']
    retrn = []
    nonalpha = 0
    interposed_sent = ""
    
    for i in range(len(sentences)):
        current_sent = sentences[i]
        
        if nonalpha != 0:
            current_sent = nonalpha + ' ' + current_sent
            nonalpha = 0
        elif current_sent[0].islower():
            current_sent = interposed_sent + ' ' + current_sent
            if len(retrn) != 0:
                del retrn[-1]

        alpha = 0
        for char in current_sent:
            if char.isalpha():
                alpha = 1
                break
                
        if alpha != 1:
            nonalpha = current_sent
            
        else:
            current_sent = [current_sent]
            sent_build = ""
            current_pop = current_sent.pop()
            
            for j in range(len(current_pop)):
                sent_build += current_pop[j]

                if sent_build[-1] == ':':
                    if j+1 < len(current_pop) and  current_pop[j+1].isspace():
                        current_sent.append(sent_build)
                        sent_build = ""

                elif len(sent_build) > 1 and sent_build[-1] == '»':
                    if j > 0 and j+2 < len(current_pop):
                        if current_pop[j+1].isspace() and current_pop[j-1] in delims \
                        and current_pop[j+2].isupper():
                            current_sent.append(sent_build)
                            sent_build = ""

                elif len(sent_build) > 3 and sent_build[-1] in delims \
                and sent_build[-2] in delims and sent_build[-3] in delims:
                    if j+2 < len(current_pop):
                        if current_pop[j+1].isspace() and current_pop[j+2].isupper():
                            current_sent.append(sent_build)
                            sent_build = ""
                            
            if len(sent_build) != 0:
                current_sent.append(sent_build)

        if nonalpha == 0:
            for sent in current_sent:
                retrn.append(sent)
                
        interposed_sent = current_sent[-1]
        
    return retrn
