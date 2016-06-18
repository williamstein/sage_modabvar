"""
`L`-series of modular abelian varieties

At the moment very little functionality is implemented -- this is mostly a
placeholder for future planned work.

AUTHOR:

- William Stein (2007-03)

TESTS::
    sage: from sage_modabvar import J0
    sage: L = J0(37)[0].padic_lseries(5)
    sage: loads(dumps(L)) == L
    True
    sage: L = J0(37)[0].lseries()
    sage: loads(dumps(L)) == L
    True
"""

###########################################################################
#       Copyright (C) 2007 William Stein <wstein@gmail.com>               #
#  Distributed under the terms of the GNU General Public License (GPL)    #
#                  http://www.gnu.org/licenses/                           #
###########################################################################

from sage.structure.sage_object import SageObject
from sage.rings.all import Integer, infinity, ZZ, QQ
from sage.modules.free_module import span
from sage.modular.modform.constructor import Newform, CuspForms
from sage.modular.arithgroup.congroup_gamma0 import is_Gamma0
from sage.misc.misc_c import prod

class Lseries(SageObject):
    """
    Base class for `L`-series attached to modular abelian varieties.
    """
    def __init__(self, abvar):
        """
        Called when creating an L-series.

        INPUT:

        - ``abvar`` -- a modular abelian variety

        EXAMPLES::
            sage: from sage_modabvar import J0
            sage: J0(11).lseries()
            Complex L-series attached to Abelian variety J0(11) of dimension 1
            sage: J0(11).padic_lseries(7)
            7-adic L-series attached to Abelian variety J0(11) of dimension 1
        """
        self.__abvar = abvar

    def abelian_variety(self):
        """
        Return the abelian variety that this `L`-series is attached to.

        OUTPUT:
            a modular abelian variety

        EXAMPLES::
            sage: from sage_modabvar import J0
            sage: J0(11).padic_lseries(7).abelian_variety()
            Abelian variety J0(11) of dimension 1
        """
        return self.__abvar

class Lseries_complex(Lseries):
    """
    A complex `L`-series attached to a modular abelian variety.

    EXAMPLES::
        sage: from sage_modabvar import J0
        sage: A = J0(37)
        sage: A.lseries()
        Complex L-series attached to Abelian variety J0(37) of dimension 2
    """
    def __call__(self, s):
        """
        Evaluate this complex `L`-series at `s`.

        INPUT:

        - ``s`` -- complex number

        OUTPUT:
            a complex number L(A, s).

        EXAMPLES::

            sage: from sage_modabvar import J0
            sage: L = J0(23).lseries()
            sage: L(1)
            0.248431866590600

            sage: from sage_modabvar import J1
            sage: L = J1(29)[0].lseries()
            sage: L(1)
            0.291521565699153

            sage: from sage_modabvar import JH
            sage: L = JH(17,[2]).lseries()
            sage: L(1)
            0.386769938387780
        """
        abelian_variety = self.abelian_variety()
        # Check for easy J0 case
        if is_Gamma0(abelian_variety.group()) and abelian_variety.is_ambient():
            S = CuspForms(abelian_variety.level())
            newforms = S.newforms('a')
        else:
            simples = abelian_variety.decomposition()
            newforms = [Newform(simple.newform_label(),'a')
                    for simple in simples]

        factors = [newform.lseries(embedding=i)
                for newform in newforms
                for i in range(newform.base_ring().degree())]
        return prod(L(s) for L in factors)

    def __cmp__(self, other):
        """
        Compare this complex `L`-series to another one.

        INPUT:

        - ``other`` -- object

        OUTPUT:
           -1, 0, or 1

        EXAMPLES::
            sage: from sage_modabvar import J0
            sage: L = J0(37)[0].lseries(); M = J0(37)[1].lseries()
            sage: cmp(L,M)
            -1
            sage: cmp(L,L)
            0
            sage: cmp(M,L)
            1
        """
        if not isinstance(other, Lseries_complex):
            return cmp(type(self), type(other))
        return cmp(self.abelian_variety(), other.abelian_variety())


    def _repr_(self):
        """
        String representation of `L`-series.

        OUTPUT:
            a string

        EXAMPLES::
            sage: from sage_modabvar import J0
            sage: L = J0(37).lseries()
            sage: L._repr_()
            'Complex L-series attached to Abelian variety J0(37) of dimension 2'
        """
        return "Complex L-series attached to %s"%self.abelian_variety()

    def rational_part(self):
        """
        Return the rational part of this `L`-function at the central critical
        value 1.

        OUTPUT:
            a rational number

        EXAMPLES::
            sage: from sage_modabvar import J0
            sage: A, B = J0(43).decomposition()
            sage: A.lseries().rational_part()
            0
            sage: B.lseries().rational_part()
            2/7
        """
        abelian_variety = self.abelian_variety()
        modular_symbols = abelian_variety.modular_symbols()
        Phi = modular_symbols.rational_period_mapping()
        ambient_module = modular_symbols.ambient_module()

        e = ambient_module([0,infinity])
        if Phi(e).is_zero():
            return QQ(0)
        else:
            s = ambient_module.sturm_bound()
            I = ambient_module.hecke_images(0, range(1,s+1))
            PhiTe = span([Phi(ambient_module(I[n]))
                for n in range(I.nrows())], ZZ)

        ambient_plus = ambient_module.sign_submodule(1)
        ambient_plus_cusp = ambient_plus.cuspidal_submodule()
        PhiH1plus = span([Phi(x) for
            x in ambient_plus_cusp.integral_basis()], ZZ)

        return PhiTe.index_in(PhiH1plus)

class Lseries_padic(Lseries):
    """
    A `p`-adic `L`-series attached to a modular abelian variety.
    """
    def __init__(self, abvar, p):
        """
        Create a `p`-adic `L`-series.

        EXAMPLES::
            sage: from sage_modabvar import J0
            sage: J0(37)[0].padic_lseries(389)
            389-adic L-series attached to Simple abelian subvariety 37a(1,37) of dimension 1 of J0(37)
        """
        Lseries.__init__(self, abvar)
        p = Integer(p)
        if not p.is_prime():
            raise ValueError("p (=%s) must be prime"%p)
        self.__p = p

    def __cmp__(self, other):
        """
        Compare this `p`-adic `L`-series to another one.

        First the abelian varieties are compared; if they are the same,
        then the primes are compared.

        INPUT:
            other -- object

        OUTPUT:
            -1, 0, or 1

        EXAMPLES::
            sage: from sage_modabvar import J0
            sage: L = J0(37)[0].padic_lseries(5); M = J0(37)[1].padic_lseries(5)
            sage: K = J0(37)[0].padic_lseries(3)
            sage: cmp(L,K)
            1
            sage: cmp(K,L)
            -1
            sage: K < L
            True
            sage: cmp(L,M)
            -1
            sage: cmp(M,L)
            1
            sage: cmp(L,L)
            0
        """
        if not isinstance(other, Lseries_padic):
            return cmp(type(self), type(other))
        return cmp((self.abelian_variety(), self.__p),
                   (other.abelian_variety(), other.__p))

    def prime(self):
        """
        Return the prime `p` of this `p`-adic `L`-series.

        EXAMPLES::
            sage: from sage_modabvar import J0
            sage: J0(11).padic_lseries(7).prime()
            7
        """
        return self.__p

    def power_series(self, n=2, prec=5):
        """
        Return the `n`-th approximation to this `p`-adic `L`-series as
        a power series in `T`.  Each coefficient is a `p`-adic number
        whose precision is provably correct.

        NOTE: This is not yet implemented.

        EXAMPLES::
            sage: from sage_modabvar import J0
            sage: L = J0(37)[0].padic_lseries(5)
            sage: L.power_series()
            Traceback (most recent call last):
            ...
            NotImplementedError
            sage: L.power_series(3,7)
            Traceback (most recent call last):
            ...
            NotImplementedError
        """
        raise NotImplementedError

    def _repr_(self):
        """
        String representation of this `p`-adic `L`-series.

        EXAMPLES::
            sage: from sage_modabvar import J0
            sage: L = J0(37)[0].padic_lseries(5)
            sage: L._repr_()
            '5-adic L-series attached to Simple abelian subvariety 37a(1,37) of dimension 1 of J0(37)'
        """
        return "%s-adic L-series attached to %s"%(self.__p, self.abelian_variety())

