from io import open
import numpy as np

id2word = ["there", "year", "when"]
word2id = {word: id for id, word in enumerate(id2word)}

# INITIALIZE EMBEDDINGS TO RANDOM VALUES
embed_size = 50
vocab_size = len(id2word)
sd = 1/np.sqrt(embed_size)  # Standard deviation to use
weights = np.random.normal(0, scale=sd, size=[vocab_size, embed_size])
weights = weights.astype(np.float32)


file = "glove.6B.50d.txt"

# EXTRACT DESIRED GLOVE WORD VECTORS FROM TEXT FILE
with open(file, encoding="utf-8", mode="r") as textFile:
    for line in textFile:
        # Separate the values from the word
        line = line.split()
        word = line[0]

        # If word is in our vocab, then update the corresponding weights
        id = word2id.get(word, None)
        if id is not None:
            weights[id] = np.array(line[1:], dtype=np.float32)
print(weights)
