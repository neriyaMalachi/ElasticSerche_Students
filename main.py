from sklearn.datasets import fetch_20newsgroups
from elasticsearch import Elasticsearch

cats = ['alt.atheism', 'sci.space']
newsgroups_train = fetch_20newsgroups(categories=cats)


documents = newsgroups_train.data
labels = newsgroups_train.target
categories = newsgroups_train.target_names

es = Elasticsearch('http://localhost:9200')

index_name = "newsgroups"
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)

for i, doc in enumerate(documents):
    document = {
        "text": doc,
        "category": categories[labels[i]]
    }

    es.index(index=index_name, id=i, body=document)
    if i % 100 == 0:
        print(f"Indexed {i} documents.")
print("khhkhj")


query = {
    "query": {
        "match": {
            "text": "computer"
        }
    }
}

results = es.search(index=index_name, body=query)

print(f"Found {results['hits']['total']['value']} results.")
for hit in results['hits']['hits']:
    print(f"ID: {hit['_id']} - Category: {hit['_source']['category']}")
    print(f"Text: {hit['_source']['text'][:200]}...\n")  # Print first 200 characters