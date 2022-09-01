# bachelor-thesis
Code for my bachelor's thesis.

Performs an NLP analysis over wikipedia pages of persecuted composers in the period of National Socialism in germany.


# How-to's

### setup
``` shell
conda env create --file environment.yml && \
conda activate thesis && \
python -m ipykernel install --user --name thesis --display-name "thesis kernel"

```

### update dependencies
``` shell
conda env update
```

### clean
``` shell
conda deactivate && \
conda env remove --name thesis
```

### download pretrained word vectors
We use the Glove vectors trained on Wikipedia 2014 and Gigaword 5.\
[Get them from here](https://nlp.stanford.edu/projects/glove/) and place under data/models/word_vectors.


