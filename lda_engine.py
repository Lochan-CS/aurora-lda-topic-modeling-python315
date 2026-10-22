"""Dependency-free collapsed Gibbs sampler for Latent Dirichlet Allocation."""
import math
import random
import re
from collections import Counter

STOPWORDS = set('a an the and or but if in on at to of for from by with as is are was were be been being this that these those it its into through using use uses can will about after before under over than then their our your we you they he she his her them who which what where when how do does did have has had not no so such also more most each all one two three four five some many very new'.split())
TOKEN_PATTERN = re.compile(r"[a-zA-Z][a-zA-Z'-]{2,}")


def tokenize(text):
    return [w for w in TOKEN_PATTERN.findall(text.lower()) if w not in STOPWORDS]


def fit_lda(documents, n_topics=4, n_words=5, iterations=160, seed=42):
    if not isinstance(documents, list) or not 3 <= len(documents) <= 150:
        raise ValueError('Provide between 3 and 150 documents (one per line).')
    if not isinstance(n_topics, int) or not 2 <= n_topics <= min(10, len(documents)):
        raise ValueError('Topic count must be between 2 and min(10, document count).')
    if any(not isinstance(doc, str) or len(doc) > 3000 for doc in documents):
        raise ValueError('Each document must be text no longer than 3000 characters.')
    tokens = [tokenize(doc) for doc in documents]
    if any(len(row) < 2 for row in tokens):
        raise ValueError('Every document needs at least two meaningful words.')
    vocabulary = sorted({word for row in tokens for word in row})
    if len(vocabulary) < n_topics:
        raise ValueError('Not enough unique words for the selected number of topics.')
    vocab_index = {word: i for i, word in enumerate(vocabulary)}
    corpus = [[vocab_index[w] for w in row] for row in tokens]
    d_count, v_count, k_count = len(corpus), len(vocabulary), n_topics
    alpha, beta = 0.15, 0.08
    rng = random.Random(seed)
    doc_topic = [[0] * k_count for _ in range(d_count)]
    topic_word = [[0] * v_count for _ in range(k_count)]
    topic_totals = [0] * k_count
    assignments = []
    for d, row in enumerate(corpus):
        current = []
        for word in row:
            topic = rng.randrange(k_count)
            current.append(topic)
            doc_topic[d][topic] += 1
            topic_word[topic][word] += 1
            topic_totals[topic] += 1
        assignments.append(current)
    for _ in range(iterations):
        for d, row in enumerate(corpus):
            for i, word in enumerate(row):
                old = assignments[d][i]
                doc_topic[d][old] -= 1
                topic_word[old][word] -= 1
                topic_totals[old] -= 1
                probs = [(doc_topic[d][k] + alpha) * (topic_word[k][word] + beta) / (topic_totals[k] + v_count * beta) for k in range(k_count)]
                target = rng.random() * sum(probs)
                running, new = 0.0, k_count - 1
                for k, probability in enumerate(probs):
                    running += probability
                    if target <= running:
                        new = k
                        break
                assignments[d][i] = new
                doc_topic[d][new] += 1
                topic_word[new][word] += 1
                topic_totals[new] += 1
    topics = []
    for k in range(k_count):
        denom = topic_totals[k] + v_count * beta
        ranked = sorted(range(v_count), key=lambda v: (-topic_word[k][v], vocabulary[v]))[:n_words]
        words = [{'word': vocabulary[v], 'probability': round((topic_word[k][v] + beta) / denom, 5)} for v in ranked]
        topics.append({'id': k + 1, 'words': words, 'token_count': topic_totals[k]})
    classifications = []
    for d, row in enumerate(corpus):
        denom = len(row) + k_count * alpha
        distribution = [(doc_topic[d][k] + alpha) / denom for k in range(k_count)]
        best = max(range(k_count), key=lambda k: distribution[k])
        classifications.append({'document': documents[d], 'topic': best + 1, 'probability': round(distribution[best], 5), 'distribution': [round(p, 5) for p in distribution]})
    return {'documents': d_count, 'vocabulary': v_count, 'tokens': sum(map(len, corpus)), 'topics': topics, 'classifications': classifications, 'iterations': iterations, 'algorithm': 'Collapsed Gibbs Sampling LDA'}
