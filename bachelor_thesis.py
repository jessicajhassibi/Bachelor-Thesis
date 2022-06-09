#!/usr/bin/env python
# coding: utf-8

# In[50]:


import wikipedia_helpers
import pandas as pd
import gensim.utils


# In[51]:


# path to save wikipedia texts to or load from if file already existing
path = "data/komponisten_texte.json"

# create dictionary with composers as keys and \
# for each key a dictionary with the texts of the wikipedia articles \
# in the languages german, arabic, english, italian, french and spanish
data_dict = wikipedia_helpers.extract_composers_texts(path)


# In[52]:


df = pd.read_json(path)
# transpose index and columns of df
df = df.transpose()
df.head()


# In[53]:


df.shape


# In[54]:


df.de_title


# In[146]:


de_texts_processed = df.de_text.apply(gensim.utils.simple_preprocess)
en_texts_processed = df.en_text.apply(gensim.utils.simple_preprocess)
ar_texts_processed = df.ar_text.apply(gensim.utils.simple_preprocess)
fr_texts_processed = df.fr_text.apply(gensim.utils.simple_preprocess)
es_texts_processed = df.es_text.apply(gensim.utils.simple_preprocess)
it_texts_processed = df.it_text.apply(gensim.utils.simple_preprocess)


# In[151]:


model = gensim.models.Word2Vec(
    window=10,
    min_count=2,
    workers=4
)
# experiment with parameters, e.g. window=5


# In[152]:


model.build_vocab(de_texts_processed, progress_per=10)


# In[153]:


model.epochs


# In[154]:


model.train(de_texts_processed, total_examples=model.corpus_count, epochs=model.epochs)


# In[155]:


model.save("word2vec_de.model")


# In[156]:


# find words used in similar surrounding 
model.wv.most_similar("jüdisch")


# In[158]:


model.wv.similarity(w1="pianist", w2="violinist") # Ohje...


# In[159]:


model.wv.doesnt_match(['pianist', 'violinist', 'nazi'])


# In[164]:





# In[ ]:




