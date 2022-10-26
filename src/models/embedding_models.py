from gensim.models import Word2Vec, FastText
from data import get_fasttext_models_path, get_word2vec_models_path, get_languages
from gensim import models


def get_embedding_model(train_data, text_type, method= "Word2Vec"):
    languages_string = "_".join(get_languages())
    if method == "Word2Vec":
        word2vec_models_path = get_word2vec_models_path().joinpath(f"Word2Vec_{languages_string}_{text_type}")
        try:
            model = Word2Vec.load(f"{word2vec_models_path}.model")
            # load model as KeyedVectors
            wv = models.KeyedVectors.load(f"{word2vec_models_path}.wordvectors")
        except FileNotFoundError as err:
            print("Word2Vec model not found.")
            print(f"Training new model on {len(train_data)} documents.")
            model = Word2Vec(sentences=train_data, vector_size= 100, window=5, min_count=2) # TODO: try different params
            print("Saving new model.")
            model.save(f"{word2vec_models_path}.bin")
            # save model as KeyedVectors
            wv = model.wv
            wv.save(f"{word2vec_models_path}.vec")
        print("Model: ", word2vec_models_path, " loaded")

    elif method == "fastText":
        fasttext_models_path = get_fasttext_models_path().joinpath(f"FastText_{languages_string}_{text_type}")
        try:
            model = FastText.load(f"{fasttext_models_path}.bin")
            # load model as KeyedVectors
            wv = models.KeyedVectors.load(f"{fasttext_models_path}.vec")
        except FileNotFoundError as err:
            print("fastText model not found.")
            print(f"Training new model on {len(train_data)} documents.")
            model = FastText(sentences=train_data, vector_size=300, window=5, min_count=2) # TODO: try different params
            print("Saving new model.")
            model.save(f"{fasttext_models_path}.bin")
            # save model as KeyedVectors
            wv = model.wv
            wv.save_word2vec_format(f"{fasttext_models_path}.vec")
        print("Model: ", fasttext_models_path, " loaded")

    elif method == "muse":
        # takes pretrained aligned fastText empeddings placed under /models/classification/FastText/aligned_embeddings
        # and writes them in one file resulting in bilingual embeddings
        muse_src_embeddings_path = get_fasttext_models_path().joinpath(f"aligned_embeddings/{text_type}/vectors-en.txt")
        muse_tgt_embeddings_path = get_fasttext_models_path().joinpath(f"aligned_embeddings/{text_type}/vectors-de.txt")
        filenames = [muse_src_embeddings_path, muse_tgt_embeddings_path]
        muse_models_path = get_fasttext_models_path().joinpath(f"multilingual_embeddings/{languages_string}_{text_type}.txt")
        with open(muse_models_path, 'w') as outfile:
            emb_dim = 300
            count = 0
            lines = list()
            for fname in filenames:
                with open(fname, errors='ignore', encoding="utf8") as infile:
                    first_line = infile.readline()
                    count += int(first_line.split()[0])
                    for line in infile:
                        lines.append(line)
                lines.append("\n")
            outfile.write(f"{count} {emb_dim}\n")
            outfile.writelines(lines)
        model = None
        wv = models.KeyedVectors.load_word2vec_format(muse_models_path, binary=False)
    return model, wv
