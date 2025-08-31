from sklearn.datasets import fetch_20newsgroups
from elasticsearch import Elasticsearch

# Load the 20 Newsgroups dataset
cats = ['alt.atheism', 'sci.space']
newsgroups_train = fetch_20newsgroups(categories=cats)
#newsgroups_train = fetch_20newsgroups(subset='train', categories=cats)
documents = newsgroups_train.data
labels = newsgroups_train.target
categories = newsgroups_train.target_names

# Initialize Elasticsearch client
es = Elasticsearch('http://localhost:9200')

# Define the index name
index_name = "newsgroups"
# Create an index in Elasticsearch
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)

# Index each document
for i, doc in enumerate(documents):
    document = {
        "text": doc,
        "category": categories[labels[i]]
    }

    es.index(index=index_name, id=i, body=document)
    if i % 100 == 0:  # For large datasets, you can add progress updates
        print(f"Indexed {i} documents.")



# Search for documents containing the word "computer"
query = {
    "query": {
        "match": {
            "text": "computer"
        }
    }
}

# Execute the search
results = es.search(index=index_name, body=query)

# Print the results
print(f"Found {results['hits']['total']['value']} results.")
for hit in results['hits']['hits']:
    print(f"ID: {hit['_id']} - Category: {hit['_source']['category']}")
    print(f"Text: {hit['_source']['text'][:200]}...\n")  # Print first 200 characters