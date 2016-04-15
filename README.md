How to install locally:

    sage-develop setup.py develop --user
    
NOTE: By `sage-develop` we simply mean a recent version of Sage, e.g., at least version 7.1.  On SageMathCloud this is provided on the command line as `sage-develop`.

How to test:

    sage-develop -t --force-lib sage_modabvar

WARNING: We must go through *all* doctests and ensure that they import the
functions being tested directly from sage_modabvar, so that the code here
is being tested, not the code in the Sage library.


Always use:

    sage-develop 


