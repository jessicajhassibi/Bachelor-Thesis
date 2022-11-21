from gensim.models import Word2Vec, FastText
from data import get_fasttext_models_path, get_word2vec_models_path, get_languages, \
    get_fasttext_pretrained_aligned_models_path, get_fasttext_aligned_models_path
from gensim import models


def get_embedding_model(train_data, text_type="cleaned_texts", method="Word2Vec", training_type="from_scratch"):
    model, wv = None, None
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
            model = Word2Vec(sentences=train_data, vector_size=100, window=5, min_count=2) # TODO: try different params
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
            wv = model.wv
        except FileNotFoundError as err:
            print("fastText model not found.")
            print(f"Training new model on {len(train_data)} documents.")
            model = FastText(sentences=train_data, vector_size=300, window=5, min_count=2)
            print("Saving new model.")
            model.save(f"{fasttext_models_path}.bin")
            # save model as KeyedVectors
            wv = model.wv
            wv.save_word2vec_format(f"{fasttext_models_path}.vec")
        print("Model: ", fasttext_models_path, " loaded")

    elif method == "muse":
        if training_type == "pretrained_aligned":
            fasttext_models_path = get_fasttext_pretrained_aligned_models_path().joinpath(f"wiki.multi.{languages_string}.txt")
            try:
                # load model as KeyedVectors
                wv = models.KeyedVectors.load_word2vec_format(fasttext_models_path, binary=False)
            except FileNotFoundError as err:
                print("fastText model not found.")
                if len(get_languages()) == 1:
                    print("Please download a pretrained model before using this method.")
                else:
                    print("Concatenating monolingual aligned word embeddings to receive multilingual aligned word embeddings.")
                    with open(fasttext_models_path, 'w', errors='ignore', encoding="utf8") as multiling_out:
                        emb_dim = 300
                        count = 0
                        lines = list()
                        for lang in get_languages():
                            fasttext_lang_path = get_fasttext_pretrained_aligned_models_path().joinpath(f"wiki.multi.{lang}.txt")
                            with open(fasttext_lang_path, errors='ignore', encoding="utf8") as monoling_in:
                                first_line = monoling_in.readline()
                                count += int(first_line.split()[0])
                                for line in monoling_in:
                                    lines.append(line)
                            lines.append("\n")
                        multiling_out.write(f"{count} {emb_dim}\n")
                        multiling_out.writelines(lines[:-1])
                    # load model as KeyedVectors
                    wv = models.KeyedVectors.load_word2vec_format(fasttext_models_path, binary=False)
        else:
            muse_models_path = get_fasttext_aligned_models_path().joinpath(f"{training_type}/{languages_string}_{text_type}.txt")
            try:
                model = None
                # load model as KeyedVectors
                wv = models.KeyedVectors.load_word2vec_format(muse_models_path, binary=False)
            except FileNotFoundError as err:
                print("muse model not found.")
                print(f"Training new model on {len(train_data)} documents.")
                # takes from_scratch trained and then aligned fastText embeddings
                # placed under /models/classification/FastText/aligned_embeddings/{text_type}
                # and writes them in one file resulting in bilingual embeddings
                muse_src_embeddings_path = get_fasttext_aligned_models_path().joinpath(f"{text_type}/{languages_string}/vectors-en.txt")
                muse_tgt_embeddings_path = get_fasttext_aligned_models_path().joinpath(f"{text_type}/{languages_string}/vectors-de.txt")
                filenames = [muse_src_embeddings_path, muse_tgt_embeddings_path]
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
