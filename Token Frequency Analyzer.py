from dotenv import load_dotenv
load_dotenv()
from transformers import AutoTokenizer
from collections import Counter

document="""Greedy search is the simplest decoding method. At each step, it selects the word (token) with the highest probability and adds it to the sequence. This process continues until a stop condition is met, such as reaching an end token or a maximum sequence length.

Imagine you’re at a fruit market with a friend who has a quirky method for choosing fruits. Every time they choose, they pick the fruit they like most at that very moment without thinking about what they’ll want next. This method might not result in a varied fruit basket, but it’s quick and straightforward.

Now, let’s equate this to how a language model, using Greedy Search, might complete a sentence.

Given the sentence start: “My favorite fruit is ___.”

The model will predict the next word based on its training data. At each step, it picks the word with the highest probability without considering the broader context of the sentence.

1st Step: After “My”, the model might have high probabilities for “favorite”, “mother”, “dog”, etc. Since we’re using Greedy Search, it picks “favorite” as it has the highest probability.

2nd Step: For “My favorite”, the next word might be “fruit”, “color”, “thing”, etc. Again, it chooses the word with the highest probability, which is “fruit”.

3rd Step: Now, for “My favorite fruit”, the options might be “is”, “are”, “was”, etc. It selects “is”, having the highest probability.

4th Step: After “My favorite fruit is”, the options could be “apple”, “banana”, “grapes”, and so forth. If “apple” has the highest probability, it chooses that.

So, with Greedy Search, the completed sentence might be: “My favorite fruit is apple.”

Using Greedy Search is like how our friend at the fruit market selects fruits – always going for the most appealing option at the present moment without thinking ahead. While this method is simple and fast, it doesn’t always provide the best or most varied outcomes. In our sentence example, Greedy Search didn’t consider other possible, and maybe more interesting, continuations like “My favorite fruit is the exotic dragon fruit” because it was only focused on the highest immediate probability at each step.

The benefit of greedy search is its simplicity and computational efficiency. Because it only keeps track of the single most probable sequence, it requires less memory and computation compared to more complex decoding methods."""


tokenizer=AutoTokenizer.from_pretrained("bert-base-uncased")

def analyze(text):
    encoded=tokenizer.encode(text, add_special_tokens=True)
    token_count=Counter(encoded)
    
    decoded_counts = {
            tokenizer.decode([token_id]): count
            for token_id, count in token_count.items()
        }

    return decoded_counts

def analyze_raw(text):
    encode=tokenizer.encode(text,add_special_tokens=True)
    token_count=Counter(encode)

    return token_count


decoded_counts=analyze(document)
token_count=analyze_raw(document)
most_frq = max(decoded_counts.items(),key=lambda x:x[1])
least_freq = min(decoded_counts.items(), key=lambda x:x[1])

print(f"Most frequent token is: {most_frq}")
print(f"Least frequent token is: {least_freq}")