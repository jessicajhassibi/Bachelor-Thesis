# bachelor-thesis

Code for my bachelor's thesis. 

Performs NLP analysis and binary classification over the wikipedia articles of two wikipedia lists. \
The code is generic! \
You can suit it to your problem by changing the groups.ini file and placing your lists urls and the wiki categories you are looking for there. 

My two lists/ classes are:
- [Gottbegnateden-Liste](https://de.wikipedia.org/wiki/Gottbegnadeten-Liste)
- [Liste der vom NS-Regime oder seinen Verbündeten verfolgten Komponisten](https://de.wikipedia.org/wiki/Liste_der_vom_NS-Regime_oder_seinen_Verb%C3%BCndeten_verfolgten_Komponisten)

## Background

In the period of National Socialism in Germany the Nazis basically classified composers into two groups:
- "Gifted" Composers which they admired and supported 
- "Degenerated" Composers which were persecuted or killed by them

<b>Can we train a Machine Learning model that is able to correctly classify a composer by his biography on wikipedia?</b>

## How-to's

### setup
``` shell
conda env create --file environment.yml && \
conda activate thesis && \
python -m ipykernel install --user --name thesis --display-name "thesis kernel"

```

#### required for spacy:
``` shell
python -m spacy download 'xx_ent_wiki_sm'
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
[Get them here](https://nlp.stanford.edu/projects/glove/) and place to models/word_vectors.


