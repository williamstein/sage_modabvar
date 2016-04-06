How to install locally:

    sage setup.py develop --user

How to test:

    sage -t --force-lib sage_modabvar

WARNING: We must go through *all* doctests and ensure that they import the
functions being tested directly from sage_modabvar, so that the code here
is being tested, not the code in the Sage library.


