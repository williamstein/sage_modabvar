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

New test cases:

    sage: from sage_modabvar import J0
    sage: J = J0(11); B= J.degeneracy_map(33,1).codomain()
    sage: type(B)
    # problem is that this is "getting out of the space"

New one:

    sage: A = ModularSymbols(33).cuspidal_submodule().abelian_variety()
    # need to replace by some function.


New one:

    sage: sage.modular.abvar.abvar.ModularAbelianVariety_modsym_abstract._modular_symbols(A)

