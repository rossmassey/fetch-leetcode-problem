cookies.txt
-----------
``cookies.txt`` is needed for synced user code.

Export a Netscape HTTP Cookie File for ``leetcode.com`` (refer to browser extensions).

Alternatively, create a file with the text ``LEETCODE_SESSION``, a tab (``\t``),
and your session token. This can be found in the Network tab in developer tools,
under Request Cookies, for requests to ``leetcode.com``.

Save as ``cookies.txt`` in the ``src/fetch_leetcode_problem/`` directory, or supply
the ``load_cookie`` function with its relative location.

.. code-block:: python

      import fetch_leetcode_problem as lc

      lc.load_cookies('/path/to/cookies.txt')
      info = lc.get_problem(1)
      print(info)


Copy cookies.txt to site packages
=================================
Run these commands from the location of ``cookies.txt`` for it to remain available:

.. code-block:: bash

    package_location=$(pip show rossmassey.fetch-leetcode-problem | grep Location)
    package_path=$(echo $package_location | cut -d ' ' -f2)
    cp cookies.txt $package_path/fetch_leetcode_problem/

It takes a while to expire