#!/usr/bin/env python
# coding: utf-8

# In[1]:


import wikipedia_helpers

# In[ ]:


# In[2]:


# path to save wikipedia texts to or load from if file already existing
path = "data/komponisten_texte.json"

# create dictionary with composers as keys and \
# for each key a dictionary with the texts of the wikipedia articles \
# in the languages german, arabic, english, italian, french and spanish
data_dict = wikipedia_helpers.extract_composers_texts(path)

"""
# In[3]:


df = pd.read_json(path)
# transpose index and columns of df
df = df.transpose()
df


# In[329]:


df.shape


# In[371]:


#df.de_title


# In[ ]:


####################################################################################################################################
####################################################################################################################################
# Methods to get Word Embeddings


# In[451]:


####################################################################################################################################
# Using Word2Vec
# preprocessing the texts necessary
de_texts_processed = df.de_text.apply(gensim.utils.simple_preprocess)
en_texts_processed = df.en_text.apply(gensim.utils.simple_preprocess)
ar_texts_processed = df.ar_text.apply(gensim.utils.simple_preprocess)
fr_texts_processed = df.fr_text.apply(gensim.utils.simple_preprocess)
es_texts_processed = df.es_text.apply(gensim.utils.simple_preprocess)
it_texts_processed = df.it_text.apply(gensim.utils.simple_preprocess)

multilingual_texts_processed = []
for lang in [de_texts_processed, en_texts_processed, ar_texts_processed, fr_texts_processed, es_texts_processed, it_texts_processed]:
    for sentences in lang:
        for words in sentences:
            multilingual_texts_processed.append(words)
multilingual_texts_processed


# In[431]:


model = gensim.models.Word2Vec(
    window=10,
    min_count=2,
    workers=4
)
# experiment with parameters, e.g. window=5


# In[432]:


model.build_vocab(multilingual_texts_processed, progress_per=10)


# In[433]:


model.epochs


# In[434]:


model.train(multilingual_texts_processed, total_examples=model.corpus_count, epochs=model.epochs)


# In[452]:


#model.save("word2vec_multilingual.model")
model = gensim.models.Word2Vec.load("word2vec_multilingual.model")


# In[1]:


#variant 2: save model with keyed vectors
word_vectors = model.wv
#word_vectors.save('vectors.kv')
reloaded_word_vectors = KeyedVectors.load('vectors.kv')
word2vec.get_word_in_static_embbedings(word_vectors, multilingual_texts_processed, save_path="word2vec_kv_models/word2vec_kv_model")


# In[445]:


# find words used in similar context
model.wv.most_similar("jewish")


# In[424]:


model.wv.similarity(w1="jude", w2="jew") 
#model.wv.distance("violinist", "pianist")


# In[426]:


model.wv.similarity(w1="composer", w2="musician") 


# In[416]:


model.wv.doesnt_match(['pianist', 'violinist', 'nazi'])


# In[428]:


model.wv.most_similar(positive=["komponist", "jude"], negative=["schönberg"])


# In[ ]:





# In[ ]:





# In[ ]:





# In[364]:


####################################################################################################################################
####################################################################################################################################
# Topic Modeling
# merge texts together for each language
de_documents = df.de_text.values.tolist()
en_documents = df.en_text.values.tolist()
ar_documents = df.ar_text.values.tolist()
fr_documents = df.fr_text.values.tolist()
es_documents = df.es_text.values.tolist()
it_documents = df.it_text.values.tolist()


# create list of documents of all languages
multilingual_documents = []
for language_documents in [de_documents, en_documents, ar_documents, fr_documents, es_documents, it_documents]:
    for document in language_documents:
        if document == "":
            continue
        multilingual_documents.append(document)


# In[386]:


# Getting sentences from text
multilingual_all_sentences = []
for document in multilingual_documents:
    sentences = nltk.sent_tokenize(document)
    for sentence in sentences:
        multilingual_all_sentences.append(sentence)


# In[394]:


####################################################################################################################################
# Using Top2Vec 
# distiluse-base-multilingual-cased pre-trained sentence transformer recommended for multilingual datasets
# TODO: further cleaning/ preprocessing of text might be needed!?
# embedding_model='distiluse-base-multilingual-cased' is sentence transformer model!
# no specified will use doc2vec method -> not multilingual
top2vec_model = Top2Vec(multilingual_documents, verbose=True, ngram_vocab=True, embedding_model='distiluse-base-multilingual-cased')
top2vec_model.save("Top2Vec_model")


# In[395]:


#top2vec_model = Top2Vec.load("Top2Vec_model")
top2vec_model.get_num_topics()


# In[396]:


topic_sizes, topic_nums = top2vec_model.get_topic_sizes()
print(topic_nums)
print(topic_sizes)


# In[397]:


words, word_scores = top2vec_model.similar_words(keywords=["emigrierte"], keywords_neg=[], num_words=20)
for word, score in zip(words, word_scores):
    print(f"{word} {score}")


# In[398]:


for topic in range(top2vec_model.get_num_topics()):
    print(top2vec_model.generate_topic_wordcloud(topic))


# In[366]:


####################################################################################################################################
# Using BERTopic
# Train model on documents with mixed languages
stop_words = stopwords.words('german') + stopwords.words('english') + stopwords.words('arabic') + stopwords.words('french') + stopwords.words('italian') + stopwords.words('spanish')
vectorizer_model = CountVectorizer(stop_words=stop_words)
topic_model = BERTopic(verbose=True, language="multilingual", vectorizer_model=vectorizer_model)
topics, probs = topic_model.fit_transform(multilingual_documents)
topic_model.save("BERTopic_model_multilingual")


# In[339]:


topic_model = BERTopic.load("BERTopic_model_multilingual")


# In[340]:


topic_model.get_topic_info()


# In[341]:


topic_model.visualize_topics()


# In[401]:


topic_model.transform("Er ist ein jüdischer Komponist.")


# In[342]:


# Update topic representation by increasing n-gram range and removing stopwords
cv = CountVectorizer(ngram_range=(1, 3), stop_words=stop_words)
topic_model.update_topics(multilingual_documents, topics, vectorizer_model=cv)


# In[343]:


topic_model.get_topic_info()


# In[403]:


for i in range(len(topic_model.get_topic_info())):
    print(f"Thema {i-1}")
    list = topic_model.get_topic(i-1)
    for elem in list:
        print(elem)
    print()


# In[344]:


topic_model.visualize_topics()


# In[ ]:





# In[ ]:
"""



