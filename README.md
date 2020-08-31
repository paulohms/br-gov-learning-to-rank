# Abstract

With the growth in the amount of information, according to the governmental transparency available in recent years due to legislative requirements, access to information becomes increasingly difficult. Traditional search engines like Google, Yahoo and Bing return as desired information ordered by searching the document before the informed query. The area whose objective is to return relevant documents to the user is known as Information Retrieval which can be aided by machine learning algorithms to improve the ordering of documents, called in this context as Learning to Rank. There are several algorithms in the literature to solve Learning to Rank problems which each one seeks to solve the ranking problem in the best possible way. In the context of government documents, there is a possibility of identifying which are the main entities present in the most relevant documents relevant to a given query. This work aims to verify a way of obtaining an ordering of the documents available on the Brazilian Government Data Portal using Learning to Rank and extracting information from entities from unstructured, semi-structured and tabular databases, which are common among the sources available on the Portal. To achieve this goal, we will use state-of-the-art techniques to recognize named entities and convex optimization models to model the learning to rank.

# Data collection and indexing

For the Learning to Rank techniques, a corpus was elaborated with the information present in the [Data Portal](https://wwww.dados.gov.br). The first step to achieve this goal was retrieve information from the [Data Portal](https://wwww.dados.gov.br) through a crawler. For retrieve this data, the CKAN APIs were used, which is the largest open source data portal platform in the world. The datasets data retrieved by the crawler were grouped in different directories along with all of their attached documents to facilitate indexing. At the end of the crawlling process, we reached a total of 138 gigabytes of data collected.

The second step was to perform an analysis using the open source [Apache Tika](https://github.com/apache/tika) project. The project makes it possible to extract metadata and content from different types of files, such as, XLS, PDF and PPT.

The parsed data was indexed in an inverted index using the open source [Elasticsearch](https://github.com/elastic/elasticsearch) project. For building the training set, it was necessary to build before an application to perform searches in the created corpus. Once the application was built and its architecture was prepared to store the queries and related results, a next step was perform the queries on the indexed data sets. At total, 69 queries were random selected, related to the various subjects present in the [Data Portal](https://wwww.dados.gov.br). Each query performed was saved with the results linked in its order of execution.

With the history of the query and the related results, the Learning to Rank dataset was built with the pairwise approach. The query and document pair is represented by the features vector that contains 752 dimensions. The first 11 dimensions are part of the first group of features, which represents the information about the documents. The following nine dimensions represent the link between the query and the document. Finally, the last 732 are the entities present in the datasets. The third group of features represents the central part of the proposal of this work, as it aims to represent the entities that are present in the datasets and consequently prioritize the documents that have a greater number of entities. The following table contains a feature mapping for the group one and two.


| Dimension ID |             Feature description             |
|:------------:|:-------------------------------------------:|
|       1      |                  Title size                 |
|       2      |                Abstract size                |
|       3      |                Number of tags               |
|       4      |               Number of groups              |
|       5      |           Organization title size           |
|       6      |                 Author size                 |
|       7      |   Size of the responsible for the dataset   |
|       8      |          Minor Term Frequency (TF)          |
|       9      |          Major Term Frequency (TF)          |
|      10      |          Sum of Term Frequency (TF)         |
|      11      |        Average of Term Frequency (TF)       |
|      12      |    Minor Inverse Document Frequency (IDF)   |
|      13      |    Major Inverse Document Frequency (IDF)   |
|      14      |   Sum of Inverse Document Frequency (IDF)   |
|      15      | Average of Inverse Document Frequency (IDF) |
|      16      |                 Minor TF-IDF                |
|      17      |                 Major TF-IDF                |
|      18      |                Sum of TF-IDF                |
|      19      |              Average of TF-IDF              |
|      20      |                     BM25                    |


The third feature group was built using Named Entity Recognition techniques. Named Entity is a sequence of words that refers to some real world entity. The Named Entities Recognition task aims to process a free writing corpus and to identify entities such as people, locations and organizations. In order to extract the entities from the data sets, the open source tool [Spacy](https://github.com/explosion/spaCy) was used, written in the python language and which supports more than 33 languages. The library supports several Natural Language Processing techniques and in the context of this work, only the Named Entity Recognition (NER) module was used. The NER module recognizes 18 different types of entities, and the types, people and organizations were used to build the third features group.
