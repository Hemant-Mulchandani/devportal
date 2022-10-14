Write search queries with OpenSearch® and Python
================================================

Learn how to write and run search queries on your OpenSearch cluster using a `Python OpenSearch client <https://github.com/opensearch-project/opensearch-py>`_. 


For our data, we use a food recipe dataset `from Kaggle <https://www.kaggle.com/hugodarwood/epirecipes?select=full_format_recipes.json>`_. After injecting this data into our cluster, we will write search queries to find different food recipes.

Pre-requisites
''''''''''''''

GitHub repository
------------------

The full code used here can be found `in a GitHub repository <https://github.com/aiven/demo-opensearch-python>`_. The files are organized according to their functions:

- `config.py <https://github.com/aiven/demo-opensearch-python/blob/main/config.py>`_, information to connect to the cluster
- `index.py <https://github.com/aiven/demo-opensearch-python/blob/main/index.py>`_, methods that manipulate the index
- `search.py <https://github.com/aiven/demo-opensearch-python/blob/main/search.py>`_, customized search query methods
- `helpers.py <https://github.com/aiven/demo-opensearch-python/blob/main/helpers.py>`_, response handler of search requests

We use ``Typer`` Python `library <ttps://typer.tiangolo.com/>`_ to create CLI commands to run from the terminal. Follow the instructions to get the code on your machine and try the commands:

1. Clone the repository and install the dependencies

::

    git clone https://github.com/aiven/demo-opensearch-python
    pip install -r requirements.txt

2. Download the dataset from Kaggle's `recipe dataset <https://www.kaggle.com/hugodarwood/epirecipes?select=full_format_recipes.json>`_, and save the ``full_format_recipes.json`` in the current folder of the `demo repository <https://github.com/aiven/demo-opensearch-python>`_.

Connect to the OpenSearch cluster with Python
---------------------------------------------

Make sure to update the ``SERVICE_URI`` to your cluster ``SERVICE_URI`` in the ``.env`` `file <https://github.com/aiven/demo-opensearch-python/blob/main/.env>`_ as explained in the `README <https://github.com/aiven/demo-opensearch-python>`_.
Once the environment variables are set, create an OpenSearch Python client to connect to your OpenSearch cluster using the :doc:`connection instructions <connect-with-python>`. You can see find the whole code sample in the `config.py <https://github.com/aiven/demo-opensearch-python/blob/main/config.py>`_:

.. code-block:: python

    import os

    from dotenv import load_dotenv
    from opensearchpy import OpenSearch


    load_dotenv()
    INDEX_NAME = "epicurious-recipes"
    SERVICE_URI = os.getenv("SERVICE_URI")
    client = OpenSearch(SERVICE_URI, use_ssl=True)

.. tip::

    The ``SERVICE_URI`` value can be found in the Aiven Console dashboard.

After creating a client with a valid ``SERVICE_URI``, you're set to interact with your cluster.

Upload data to OpenSearch using Python
--------------------------------------

Once you're connected, the next step should be to :ref:`inject data into our cluster <load-data-with-python>`. This is done in our demo with the `load_data function <https://github.com/aiven/demo-opensearch-python/blob/main/index.py>`__.

You can inject the data to your cluster by running::

  python index.py load-data

Once the data is loaded, we can :ref:`retrieve the data mapping <get-mapping-with-python>` to explore the structure of the data, with their respective fields and types. You can find the code implementation in the `get_mapping function <https://github.com/aiven/demo-opensearch-python/blob/main/index.py>`__.

Check the structure of your data by running::

  python index.py get-mapping

You should be able to see the fields' output:

.. code-block:: bash

    [
      'calories',
      'categories',
      'date',
      'desc',
      'directions',
      'fat',
      'ingredients',
      'protein',
      'rating',
      'sodium',
      'title'
    ]

And the mapping with the fields and their respective types.

.. code-block:: bash

        {'calories': {'type': 'float'},
         'categories': {'fields': {'keyword': {'ignore_above': 256, 'type': 'keyword'}},
                        'type': 'text'},
         'date': {'type': 'date'},
         'desc': {'fields': {'keyword': {'ignore_above': 256, 'type': 'keyword'}},
                  'type': 'text'},
         'directions': {'fields': {'keyword': {'ignore_above': 256, 'type': 'keyword'}},
                        'type': 'text'},
         'fat': {'type': 'float'},
         'ingredients': {'fields': {'keyword': {'ignore_above': 256,
                                                'type': 'keyword'}},
                         'type': 'text'},
         'protein': {'type': 'float'},
         'rating': {'type': 'float'},
         'sodium': {'type': 'float'},
         'title': {'fields': {'keyword': {'ignore_above': 256, 'type': 'keyword'}},
                   'type': 'text'}}
        
    
All set to start writing your search queries.

Query the data
''''''''''''''

Use the ``search()`` method
---------------------------

You have an OpenSearch client and data injected in your cluster, so you can start writing search queries. Python OpenSearch client has a handy method called ``search()``, which we'll use to run our queries.

We can check the method signature to understand the function and which parameters we'll use.  As you can see, all the parameters are optional in the ``search()`` method. Find below the method signature::

  client.search: (body=None, index=None, doc_type=None, params=None, headers=None)


To run the search queries, we'll use two of these parameters - ``index`` and ``body``:

* ``index``, parameter refers to the name of the index we used to load the data. Therefore, it does not change. 
* ``body``, parameter refers to the search query specifications. We'll modify it according to our query purpose.

Lucene query and query DSL
--------------------------

OpenSearch supports the **Lucene query syntax** to perform searches by using the ``q`` parameter. The ``q`` parameter expects a string with your query specifications, for example:

.. code-block:: python

    client.search({
        index: 'recipes',
        q: 'ingredients:broccoli AND calories:(>=100 AND <200)'
    })

For users, who prefer to work with nested objects and familiar structures like JSON (equivalent to Python dictionaries), OpenSearch supports the `query domain-specific language (DSL) <https://opensearch.org/docs/latest/opensearch/query-dsl/index/>`_.

For the **Query DSL**, the field ``body`` expects a dictionary object which can facilitate the construction of more complex queries depending on your use case, for example:

.. code-block:: python

     query_body = {
                    "query": {
                      "multi_match": {
                        "query": "Garlic-Lemon",
                        "fields": [
                          "title",
                          "ingredients"
                        ]
                      }
                    }
                  }

In this example, we are searching for "Garlic-Lemon" across ``title`` and ``ingredients`` fields. Try out yourself using our demo::
  
  python search.py multi-match title ingredients Garlic-Lemon

Check what comes out from this interesting combination 🧄 🍋 :

.. code-block:: shell
  
      [
        'Garlic-Lemon Potatoes ',
        'Lemon Garlic Mayonnaise ',
        'Lemon Garlic Mayonnaise ',
        'Garlic-Lemon Croutons ',
        'Lemon-Garlic Vinaigrette ',
        'Lemon-Garlic Lamb Chops ',
        'Lemon Pepper Garlic Vinaigrette ',
        'Lemon-Garlic Baked Shrimp ',
        'Lemon-Herb Turkey with Lemon-Garlic Gravy ',
        'Garlic, Oregano, and Lemon Vinaigrette '
      ]

For this tutorial, we focus on the query DSL syntax to construct queries modifying the ``body`` parameter. In the method ``search()``, one of the optional fields is the ``size`` field, which is defined as the number of results returned in the search. 

.. note::
  The default value of the ``size`` field is 10, and we're using the default value in this tutorial.
  

Write common queries
''''''''''''''''''''

In the next section, we cover some of the more common queries. Time to start querying 🔎 

.. _match-query:

Create ``match`` query
----------------------

The ``match`` query helps you to find the best matches with multiple search words. It is the default option for a `full-text search <https://opensearch.org/docs/latest/opensearch/query-dsl/full-text/>`_. 

You can build your match query based on a ``field`` and the ``query`` that you are searching for. The DSL defaults to the "or" ``operator``.

.. code-block:: python

  query_body = {
                  "query": {
                    "match": {
                      field: {
                        "query": query,
                        "operator": operator
                      }
                    }
                  }
                }

Thinking about how the match query works, if we run this query, it will return matches. This could be confusing because in our cluster the field ``fat`` corresponds to a value ``float``, not a ``string``.

.. code-block:: python

  query_body = {
                  "query": {
                    "match": {
                      "fat": {
                        "query": "0"
                      }
                    }
                  }
                }

This is possible because `full-text queries <https://opensearch.org/docs/latest/opensearch/query-dsl/full-text/>`_, such as the match query, use an analyzer to make the data optimized for search. As we have not specified an analyzer when we searched, the default standard analyzer is used:

.. code-block:: python

  query_body = {
                  "query": {
                    "match": {
                      "fat": {
                        "query": "0",
                        "analyzer": "standard",
                      }
                    }
                  }
                }

The default standard analyzer drops most punctuation, breaks up text into individual words, and lower cases them to optimize the search. If you want to choose a different analyzer, check out the available ones in the `OpenSearch documentation <https://opensearch.org/docs/latest/opensearch/query-dsl/full-text/#match>`__. 

You can find out how a customized match query can be written with your Python OpenSearch client in the `search_match() <https://github.com/aiven/demo-opensearch-python/blob/main/search.py>`__ function. You can run yourself the code to explore the ``match`` function. For example, if you want to find out recipes with the name "Spring" on them:

.. code-block:: shell

  python search.py match title Spring

As a result of the "Spring" search recipes, you'll find:

.. code-block:: shell

  [
    'Spring Fever ',
    'Spring Rolls ',
    'Spring Feeling ',
    'Spring Fever ',
    'Spring Rolls ',
    'Spring Feeling ',
    'Spring Vegetable Sauté ',
    'Spring-Onion Cocktail ',
    'Braised Spring Legumes ',
    'Asian Spring Rolls '
  ]

.. seealso::
  
  Find out more about `match queries <https://opensearch.org/docs/latest/opensearch/query-dsl/full-text/#match>`_.

Use a ``multi_match`` query
---------------------------
One useful query when you want to align the ``match`` query properties but expand it to search in more fields is the ``multi_match`` query. You can add several fields in the ``fields`` property, to search for the ``query`` string across all those fields included in the list.

.. code-block:: python

     query_body = {
                    "query": {
                      "multi_match": {
                        "query": query,
                        "fields": [field1, field2 ...]
                      }
                    }
                  }

In our demo, we have a function called `search_multi_match() <https://github.com/aiven/demo-opensearch-python/blob/main/search.py>`__ that build customized multi match queries in Python. You can use our demo with ``multi-match`` keyword followed by the ``fields`` and the ``query`` to explore this type of query.

Suppose you are looking for citrus recipes 🍋. For example, recipes with ingredients and lemon in the title, you can run your query from our `demo <https://github.com/aiven/demo-opensearch-python/>`_ as:

::

  python search.py multi-match title ingredients lemon

.. _match-phrase-query:

Match with phrases
------------------

This query can be used to match **exact phrases** in a field. Where the ``query`` is the phrase that is being searched in a certain ``field``:

.. code-block:: python

     query_body = {
                    "query": {
                      "match_phrase": {
                        field: {
                          "query": query
                        }
                      }
                    }
                  }
  
If you know exactly which phrases you're looking for, you can try out our ``match-phrase`` `search_match_phrase() <https://github.com/aiven/demo-opensearch-python/blob/main/search.py>`__. 

.. note::
  
  If you misspell the searched word, the query will not return any results as the purpose is to look for **exact phrases**. The lowercase and uppercase can bring your results according to the relevance 

For example, try searching for ``pannacotta with lemon marmalade`` in the title:

::

  python search.py match-phrase title "Pannacotta with lemon marmalade"

If you just have a rough idea of the phrase you're looking for, you can make your match phrase query more flexible with the ``slop`` parameter as explained in the section :ref:`match phrase with slop query <match-phrase-slop>` section.

.. _match-phrase-slop:

Match phrases and add some ``slop``
-----------------------------------

You can use the ``slop`` parameter to create more flexible searches. Suppose you're searching for ``pannacotta marmalade`` with the ``match_phrase`` query, and no results are found. This happens because you are looking for exact phrases, as discussed in :ref:`match phrase query <match-phrase-query>` section.
You can expand your searches by configuring the ``slop`` parameter. The default value for the ``slop`` parameter is 0. 

The ``slop`` parameter allows to control the degree of disorder in your search as explained in the `OpenSearch documentation for the slop feature <https://opensearch.org/docs/latest/opensearch/query-dsl/full-text/#match>`_: 

      ``slop`` is the number of other words allowed between words in the query phrase. For example, to switch the order of two words requires two moves (the first move places the words atop one another), so to permit re-orderings of phrases, the slop must be at least two. A value of zero requires an exact match.

You can construct a query and add some ``slop`` like this:

.. code-block:: python

     query_body = {
                    "query": {
                      "match_phrase": {
                        field: {
                          "query": query
                          "slop": slop # integer or float
                        }
                      }
                    }
                  }

In the demo, you can find the `search_slop() <https://github.com/aiven/demo-opensearch-python/blob/main/search.py>`__ function where this query is used. Suppose you're looking for ``pannacotta marmalade`` phrase. To find more results rather than exact phrases, you should allow a certain degree. You can configure the ``slop`` to 2 , so it can find matches skipping **two words** between the searched ones. 

This is how you can run this query yourself:

.. code-block:: shell

  python search.py slop "title" "pannacotta marmalade" 2

Your result should look like this:

.. code-block:: python

    ['Lemon Pannacotta with Lemon Marmalade ']

So with ``slop`` parameter adjusted, you're may be able to find results even with other words in between the ones you searched.

.. seealso::

  Read more about ``slop`` parameter on the `OpenSearch project specifications <https://opensearch.org/docs/latest/opensearch/query-dsl/full-text#other-optional-query-fields>`_.


Use a ``term`` query
--------------------

If you want results with a precise value in a ``field``, the `term query <https://opensearch.org/docs/latest/opensearch/query-dsl/term/#term>`_ is the right choice. The term query can be used to find documents according to a precise value such as a price or product ID, for example.

This query can be constructed as:

.. code-block:: python

     query_body = {
                    "query": {
                      "term": {
                        field: value
                      }
                    }
                  }


In this query, the term is matched as it is, which means that no analyzer is applied to the search term. If you are searching for text field values, it is recommended to use :ref:`match query <match-query>` instead.

You can look the `search_term() <https://github.com/aiven/demo-opensearch-python/blob/main/search.py>`__ function, which uses this query to build customized term queries. 


Run the search query yourself to find recipes with zero sodium on it, for example:

::

  python search.py term sodium 0



Search with a ``range`` query
-----------------------------

This query helps to find documents that the field is within a provided range. This can be handy if you're dealing with **numerical values** and are interested **in ranges** instead of specific values. The queries can be constructed as:

.. code-block:: python

     query_body = {
                    "query": {
                      "range": {
                        field: {
                          "gte": gte,
                          "lte": lte
                        }
                      }
                    }
                  }

You can construct range queries with combinations of inclusive and exclusive parameters as can be seen in the table:

.. list-table::
  :header-rows: 1
  :stub-columns: 1
  :align: left

  * - Parameter
    - Behavior
  * - ``gte``
    - Greater than or equal to
  * - ``gt``
    - Greater than
  * - ``lt``
    - Less than
  * - ``lte``
    - Less than or equal to


Try to find recipes in a certain range of sodium, for example:

::

    python search.py range sodium 0 10

.. seealso::

  See more about the range query in the `OpenSearch documentation <https://opensearch.org/docs/latest/opensearch/query-dsl/term/#range-query>`_.

.. _fuzzy-query:

Write fuzzy queries
-------------------

This query looks for documents that have **similar term** to the searched term. This similarity is calculated by the ``Levenshtein`` `edit distance <https://en.wikipedia.org/wiki/Levenshtein_distance>`_. This distance refers to the minimum number of single-character edits between two words. Some of those changes:

* Change of a character: ``post`` → ``lost``
* Removal of a character: ``eggs`` → ``ggs``
* Insertion of a character:  ``edi`` → ``edit``
* Transposition of two adjacent characters: ``act`` → ``cat``


The queries can be constructed as:

.. code-block:: python

     query_body = {
                    "query": {
                        "fuzzy": {
                            field: {
                                "value": value
                                "fuzziness": fuzziness,
                            }
                        }
                    }
                  } 

We can try out looking for a misspelled word and allowing some ``fuzziness``. Writing a fuzzy query with a **misspelled word**, such as ``pinapple`` and setting ``fuzziness`` to zero. Running it, will bring no results:

.. code-block:: python

    python search.py fuzzy "title" "pinapple" 0


To correct ``pinapple`` → ``Pineapple`` word, we only need to change one letter. So we can try again to search this word setting the ``fuzziness`` to one and run the search again.

.. code-block:: python
  
  python search.py fuzzy "title" "pinapple" 1

As you can see, this search returns results 🍍:

.. code-block:: python

  [
    'Pineapple "Lasagna" ',
    'Pineapple Bowl ',
    'Pineapple Paletas ',
    'Pineapple "Salsa" ',
    'Pineapple Sangria ',
    'Pineapple Tart ',
    'Pineapple Split ',
    'Roasted Pineapple with Star Anise Pineapple Sorbet ',
    'Pineapple-Apricot Salsa ',
    'Pineapple Papaya Relish '
  ]

It is your turn, try out more combinations to better understand the fuzzy query.

Read more
'''''''''

Want to try out OpenSearch with other clients? You can learn how to write search queries with NodeJS client, see :doc:`our tutorial <opensearch-and-nodejs>`. We created an OpenSearch cluster, connected to it, and tried out different types of search queries. Now, you can explore more resources to help you to learn other features of OpenSearch and its Python client.

* `Demo repository <https://github.com/aiven/demo-opensearch-python>`_, contains all code from this tutorial
* `OpenSearch Python client  <https://opensearch.org/docs/latest/clients/python/>`_
* :doc:`How to use OpenSearch with curl <opensearch-with-curl>`
* `Official OpenSearch documentation <https://opensearch.org>`_