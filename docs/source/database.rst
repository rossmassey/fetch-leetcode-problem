Database and Queries
--------------------
.. _GraphQL API: https://leetcode.com/graphql
.. _all their problems: https://leetcode.com/api/problems/all/

Leetcode provides a `GraphQL API`_ and a listing of `all their problems`_

The GraphQL routes use a ``$titleSlug`` for querying problems, and a
``$questionId`` for the synced code (separate from the ``num`` aka
``questionFrontendId``).

Instead of searching that list every time problem information is needed,
a local database is created from ``update_problem_listing()`` that
stores a lookup table indexed to the problem number.

That is then used to quickly find the ``$titleSlug`` and ``$questionId``,
which can be inserted into the following queries

:Problem Info:

.. code-block:: graphql

    query questionCustom($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            questionFrontendId
            title
            titleSlug
            difficulty
            content
            codeSnippets {
                lang
                langSlug
                code
            }
        }
    }


:Synced Code:

.. code-block:: graphql

    query SyncedCode($questionId: Int!, $lang: Int!) {
      syncedCode(questionId: $questionId, lang: $lang) {
        code
      }
    }

The language ID can be found with this query:

.. code-block:: graphql

    query languageList {
      languageList {
        id
        name
      }
    }

Python 2 is ``2``, and Python 3 is ``11``. This package currently defaults
to Python 3.

Deleting database
=================

The database is located as a ``.db`` file in the ``src``

.. code-block:: bash

    package_location=$(pip show rossmassey.fetch-leetcode-problem | grep Location)
    package_path=$(echo $package_location | cut -d ' ' -f2)
    rm -f $package_path/fetch_leetcode_problem/problems.db
