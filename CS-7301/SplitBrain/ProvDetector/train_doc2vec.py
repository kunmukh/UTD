
from tqdm import tqdm
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

NUM_WORKERS=4

# Create model
# Build volcabulary
# Train model

def train_doc2vec_from_docs(documents, vector_size, epochs):
    model = Doc2Vec(documents,
                vector_size=vector_size,
                min_count=1,
                workers=NUM_WORKERS,
                epochs=epochs,
                dm=1)
    return model

def train_doc2vec(data, vector_size, epochs):
    documents = [TaggedDocument(item, tags=str(i)) for i, item in enumerate(data)]

    return train_doc2vec_from_docs(documents, vector_size, epochs)


def train_doc2vec2(data, vector_size, alpha, epochs):
    documents = [TaggedDocument(words=item, tags=str(i)) for i, item in enumerate(data)]

    model = Doc2Vec(vector_size=vector_size,
                alpha=alpha,
                min_alpha=0.00025,
                min_count=1,
                workers=NUM_WORKERS,
                dm=1)

    model.build_vocab(documents)

    for epoch in tqdm(range(epochs)):
        model.train(documents, total_examples=model.corpus_count, epochs=model.epochs)
        model.alpha -= 0.0002
        model.min_alpha = model.alpha

    return model 

