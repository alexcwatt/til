# Binary Embeddings

Embeddings are useful for semantic search: a document has an embedding representing its meaning, and so does a search query. A similarity measure such as cosine similarity can then be used to determine which embeddings are closest to each other.

There is a trick for making cosine similarity much less computationally expensive: binary embeddings. You can take an N-dimensional embedding vector—ordinarily a set of N floating-point numbers—and compress it so that each dimension is reduced to a single bit: `1` if the value is positive, and `0` if it is not.

This allows for a much faster initial pass when retrieving similar embeddings. You might miss some matches this way, but if the tradeoff is acceptable, you can save a significant amount of compute.
