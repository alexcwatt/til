# Term Frequency–Inverse Document Frequency (TF–IDF)

In search, a word that occurs infrequently in the corpus of documents but occurs frequently in a particular document is a sign that this word has a high correlation with the document; if someone were to search for that word, the document is likely very relevant.

This is the intuition behind term frequency–inverse document frequency.

**Term frequency:** How often a term occurs within a particular document
**Document frequency:** How often a term occurs within any document in the collection
**Inverse document frequency:** As expected, the inverse of the document frequency

The product of the term frequency and the inverse document frequency is TF–IDF and can be used in ranking search results.
