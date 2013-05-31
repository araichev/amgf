r"""
Let $F(x) = \sum_{\nu \in \NN^d} F_{\nu} x^\nu$ be a multivariate power series with complex coefficients that converges in a neighborhood of the origin. Assume that $F = G/H$ for some functions $G$ and $H$ holomorphic in a neighborhood of the origin.
Assume also that $H$ is a polynomial.

This Python module for use within `Sage <http://www.sagemath.org>`_ computes asymptotics for the coefficients $F_{r \alpha}$ as $r \to \infty$ with $r \alpha \in \NN^d$ for $\alpha$ in a permissible subset of $d$-tuples of positive reals. 
More specifically, it computes arbitrary terms of the asymptotic expansion for $F_{r \alpha}$ when the asymptotics are controlled by a strictly minimal multiple point of the alegbraic variety $H = 0$.

The algorithms and formulas implemented here come from [RaWi2008a]_
and [RaWi2012]_.

.. [AiYu1983] I.A. Aizenberg and A.P. Yuzhakov, "Integral representations and residues in multidimensional complex analysis", Translations of Mathematical Monographs, 58. American Mathematical Society, Providence, RI, 1983. x+283 pp. ISBN: 0-8218-4511-X.

.. [Raic2012] Alexander Raichev, "Leinartas's partial fraction decomposition", `<http://arxiv.org/abs/1206.4740>`_.

.. [RaWi2008a] Alexander Raichev and Mark C. Wilson, "Asymptotics of coefficients of multivariate generating functions: improvements for smooth points", Electronic Journal of Combinatorics, Vol. 15 (2008), R89, `<http://arxiv.org/pdf/0803.2914.pdf>`_.

.. [RaWi2012] Alexander Raichev and Mark C. Wilson, "Asymptotics of coefficients of multivariate generating functions: improvements for smooth points", To appear in 2012 in the Online Journal of Analytic Combinatorics, `<http://arxiv.org/pdf/1009.5715.pdf>`_.

AUTHORS:

- Alexander Raichev (2008-10-01): Initial version
- Alexander Raichev (2010-09-28): Corrected many functions
- Alexander Raichev (2010-12-15): Updated documentation
- Alexander Raichev (2011-03-09): Fixed a division by zero bug in relative_error()
- Alexander Raichev (2011-04-26): Rewrote in object-oriented style
- Alexander Raichev (2011-05-06): Fixed bug in cohomologous_integrand() and fixed _crit_cone_combo() to work in SR
- Alexander Raichev (2012-08-06): Major rewrite. Created class FFPD and moved functions around. 
- Alexander Raichev (2012-10-03): Fixed whitespace errors, added examples to those six functions missing them (which i overlooked), changed package name to a more descriptive title, made asymptotics methods work for univariate functions.

EXAMPLES::

    sage: from sage.combinat.asymptotics_multivariate_generating_functions import *

A univariate smooth point example::

    sage: R.<x> = PolynomialRing(QQ)
    sage: H = (x - 1/2)^3
    sage: Hfac = H.factor()
    sage: G = -1/(x + 3)/Hfac.unit()
    sage: F = FFPD(G, Hfac)
    sage: print F
    (-1/(x + 3), [(x - 1/2, 3)])
    sage: alpha = [1]
    sage: decomp = F.asymptotic_decomposition(alpha)
    sage: print decomp
    [(0, []), (-1/2*(x^2 + 6*x + 9)*r^2/(x^5 + 9*x^4 + 27*x^3 + 27*x^2) - 1/2*(5*x^2 + 24*x + 27)*r/(x^5 + 9*x^4 + 27*x^3 + 27*x^2) - 3*(x^2 + 3*x + 3)/(x^5 + 9*x^4 + 27*x^3 + 27*x^2), [(x - 1/2, 1)])]
    sage: F1 = decomp[1]
    sage: p = {x: 1/2}
    sage: asy = F1.asymptotics(p, alpha, 3)
    sage: print asy
    (8/343*(49*r^2 + 161*r + 114)*2^r, 2, 8/7*r^2 + 184/49*r + 912/343)
    sage: print F.relative_error(asy[0], alpha, [1, 2, 4, 8, 16], asy[1])
    Calculating errors table in the form
    exponent, scaled Maclaurin coefficient, scaled asymptotic values, relative errors...
    [((1,), 7.555555556, [7.556851312], [-0.0001714971672]), ((2,), 14.74074074, [14.74052478], [0.00001465051901]), ((4,), 35.96502058, [35.96501458], [1.667911934e-7]), ((8,), 105.8425656, [105.8425656], [4.399565380e-11]), ((16,), 355.3119534, [355.3119534], [0.0000000000])]
    
Another smooth point example (Example 5.4 of [RaWi2008a]_)::

    sage: R.<x,y> = PolynomialRing(QQ)
    sage: q = 1/2
    sage: qq = q.denominator()
    sage: H = 1 - q*x + q*x*y - x^2*y
    sage: Hfac = H.factor()
    sage: G = (1 - q*x)/Hfac.unit()
    sage: F = FFPD(G, Hfac)
    sage: alpha = list(qq*vector([2, 1 - q]))
    sage: print alpha
    [4, 1]
    sage: I = F.smooth_critical_ideal(alpha)
    sage: print I
    Ideal (y^2 - 2*y + 1, x + 1/4*y - 5/4) of Multivariate Polynomial Ring
    in x, y over Rational Field
    sage: s = solve(I.gens(), [SR(x) for x in R.gens()], solution_dict=true)
    sage: print s
    [{y: 1, x: 1}]
    sage: p = s[0]
    sage: asy = F.asymptotics(p, alpha, 1) # long time
    Creating auxiliary functions...
    Computing derivatives of auxiliary functions...
    Computing derivatives of more auxiliary functions...
    Computing second order differential operator actions...
    sage: print asy # long time
    (1/12*2^(2/3)*sqrt(3)*gamma(1/3)/(pi*r^(1/3)), 1,
    1/12*2^(2/3)*sqrt(3)*gamma(1/3)/(pi*r^(1/3)))
    sage: print F.relative_error(asy[0], alpha, [1, 2, 4, 8, 16], asy[1]) # long time
    Calculating errors table in the form
    exponent, scaled Maclaurin coefficient, scaled asymptotic values,
    relative errors...
    [((4, 1), 0.1875000000, [0.1953794675], [-0.04202382689]), ((8, 2),
    0.1523437500, [0.1550727862], [-0.01791367323]), ((16, 4), 0.1221771240,
    [0.1230813519], [-0.007400959228]), ((32, 8), 0.09739671811,
    [0.09768973377], [-0.003008475766]), ((64, 16), 0.07744253816,
    [0.07753639308], [-0.001211929722])]

A multiple point example (Example 6.5 of [RaWi2012]_)::

    sage: R.<x,y>= PolynomialRing(QQ)
    sage: H = (1 - 2*x - y)**2 * (1 - x - 2*y)**2
    sage: Hfac = H.factor()
    sage: G = 1/Hfac.unit()
    sage: F = FFPD(G, Hfac)
    sage: print F
    (1, [(x + 2*y - 1, 2), (2*x + y - 1, 2)])
    sage: I = F.singular_ideal()
    sage: print I
    Ideal (x - 1/3, y - 1/3) of Multivariate Polynomial Ring in x, y over
    Rational Field
    sage: p = {x: 1/3, y: 1/3}
    sage: print F.is_convenient_multiple_point(p)
    (True, 'convenient in variables [x, y]')
    sage: alpha = (var('a'), var('b'))
    sage: decomp =  F.asymptotic_decomposition(alpha); print decomp # long time
    [(0, []), (-1/9*(2*a^2*y^2 - 5*a*b*x*y + 2*b^2*x^2)*r^2/(x^2*y^2) +
    1/9*(5*(a + b)*x*y - 6*a*y^2 - 6*b*x^2)*r/(x^2*y^2) - 1/9*(4*x^2 - 5*x*y
    + 4*y^2)/(x^2*y^2), [(x + 2*y - 1, 1), (2*x + y - 1, 1)])]
    sage: F1 = decomp[1]
    sage: print F1.asymptotics(p, alpha, 2) # long time
    (-3*((2*a^2 - 5*a*b + 2*b^2)*r^2 + (a + b)*r +
    3)*((1/3)^(-b)*(1/3)^(-a))^r, (1/3)^(-b)*(1/3)^(-a), -3*(2*a^2 - 5*a*b +
    2*b^2)*r^2 - 3*(a + b)*r - 9)
    sage: alpha = [4, 3]
    sage: decomp =  F.asymptotic_decomposition(alpha)
    sage: F1 = decomp[1]
    sage: asy = F1.asymptotics(p, alpha, 2) # long time
    sage: print asy # long time
    (3*(10*r^2 - 7*r - 3)*2187^r, 2187, 30*r^2 - 21*r - 9)
    sage: print F.relative_error(asy[0], alpha, [1, 2, 4, 8], asy[1])   # long time
    Calculating errors table in the form
    exponent, scaled Maclaurin coefficient, scaled asymptotic values,
    relative errors...
    [((4, 3), 30.72702332, [0.0000000000], [1.000000000]), ((8, 6),
    111.9315678, [69.00000000], [0.3835519207]), ((16, 12), 442.7813138,
    [387.0000000], [0.1259793763]), ((32, 24), 1799.879232, [1743.000000],
    [0.03160169385])]
    
"""
#*****************************************************************************
#       Copyright (C) 2008 Alexander Raichev <tortoise.said@gmail.com>
#
#  Distributed under the terms of the GNU General Public License (GPL)
#                  http://www.gnu.org/licenses/
#*****************************************************************************

from functools import total_ordering

# Sage libraries
from sage.categories.unique_factorization_domains   import UniqueFactorizationDomains
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing
from sage.rings.polynomial.polynomial_ring  import is_PolynomialRing
from sage.rings.polynomial.multi_polynomial_ring_generic    import is_MPolynomialRing
from sage.symbolic.ring import SR
from sage.geometry.cone import Cone
from sage.calculus.functional   import diff
from sage.calculus.functions    import jacobian
from sage.calculus.var  import function, var
from sage.combinat.cartesian_product    import CartesianProduct
from sage.combinat.combinat     import stirling_number1
from sage.combinat.permutation  import Permutation
from sage.combinat.tuple    import UnorderedTuples
from sage.functions.log     import exp, log
from sage.functions.other   import factorial, gamma, sqrt
from sage.matrix.constructor    import matrix
from sage.misc.misc import add
from sage.misc.misc_c   import prod
from sage.misc.mrange   import cartesian_product_iterator, mrange
from sage.modules.free_module_element   import vector
from sage.rings.arith   import binomial, xgcd
from sage.rings.all import CC
from sage.rings.fraction_field  import FractionField
from sage.rings.integer import Integer
from sage.rings.integer_ring    import ZZ
from sage.rings.polynomial.polynomial_ring_constructor  import PolynomialRing
from sage.rings.rational_field  import QQ
from sage.sets.set  import Set
from sage.structure.sage_object import SageObject
from sage.symbolic.constants    import pi
from sage.symbolic.relation import solve

@total_ordering
class FFPD(object):
    r"""
    Represents a fraction with factored polynomial denominator (FFPD)
    $p/(q_1^{e_1} \cdots q_n^{e_n})$ by storing the parts $p$ and
    $[(q_1, e_1), \ldots, (q_n, e_n)]$.
    Here $q_1, \ldots, q_n$ are elements of a 0- or multi-variate factorial
    polynomial ring $R$ , $q_1, \ldots, q_n$ are distinct irreducible elements
    of $R$ , $e_1, \ldots, e_n$ are positive integers, and $p$ is a function
    of the indeterminates of $R$ (a Sage Symbolic Expression).
    An element $r$ with no polynomial denominator is represented as $[r, (,)]$.

    AUTHORS:

    - Alexander Raichev (2012-07-26)
    """

    def __init__(self, numerator=None, denominator_factored=None,
                 quotient=None, reduce_=True):
        r"""
        Create a FFPD instance.

        INPUT:

        - ``numerator`` - (Optional; default=None) An element $p$ of a
          0- or 1-variate factorial polynomial ring $R$.
        - ``denominator_factored`` - (Optional; default=None)
          A list of the form
          $[(q_1, e_1), \ldots, (q_n, e_n)]$ where the $q_1, \ldots, q_n$ are
          distinct irreducible elements of $R$ and the $e_i$ are positive
          integers.
        - ``quotient`` - (Optional; default=None) An element of a field of
          fractions of a factorial ring.
        - ``reduce_`` - (Optional; default=True) If True, then represent
          $p/(q_1^{e_1} \cdots q_n^{e_n})$ in lowest terms.
          If False, then won't attempt to divide $p$ by any of the $q_i$.

        OUTPUT:

        A FFPD instance representing the rational expression
        $p/(q_1^{e_1} \cdots q_n^{e_n})$.
        To get a non-None output, one of ``numerator`` or ``quotient`` must be
        non-None.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y> = PolynomialRing(QQ)
            sage: df = [x, 1], [y, 1], [x*y+1, 1]
            sage: f = FFPD(x, df)
            sage: print f
            (1, [(y, 1), (x*y + 1, 1)])
            sage: ff = FFPD(x, df, reduce_=False)
            sage: print ff
            (x, [(y, 1), (x, 1), (x*y + 1, 1)])

        ::

            sage: f = FFPD(x + y, [(x + y, 1)])
            sage: print f
            (1, [])

        ::

            sage: R.<x> = PolynomialRing(QQ)
            sage: f = 5*x^3 + 1/x + 1/(x-1) + 1/(3*x^2 + 1)
            sage: print FFPD(quotient=f)
            (5*x^7 - 5*x^6 + 5/3*x^5 - 5/3*x^4 + 2*x^3 - 2/3*x^2 + 1/3*x - 1/3,
            [(x - 1, 1), (x, 1), (x^2 + 1/3, 1)])

        ::

            sage: R.<x, y> = PolynomialRing(QQ)
            sage: f = 2*y/(5*(x^3 - 1)*(y + 1))
            sage: print FFPD(quotient=f)
            (2/5*y, [(y + 1, 1), (x - 1, 1), (x^2 + x + 1, 1)])

        ::

            sage: R.<x, y>= PolynomialRing(QQ)
            sage: p = 1/x^2
            sage: q = 3*x**2*y
            sage: qs = q.factor()
            sage: f = FFPD(p/qs.unit(), qs)
            sage: print f
            (1/(3*x^2), [(y, 1), (x, 2)])

        ::

            sage: R.<x, y> = PolynomialRing(QQ)
            sage: f = FFPD(cos(x)*x*y^2, [(x, 2), (y, 1)])
            sage: print f
            (x*y^2*cos(x), [(y, 1), (x, 2)])

        ::

            sage: R.<x, y> = PolynomialRing(QQ)
            sage: G = exp(x + y)
            sage: H = (1 - 2*x - y) * (1 - x - 2*y)
            sage: a = FFPD(quotient=G/H)
            sage: print a
            (e^(x + y)/(2*x^2 + 5*x*y + 2*y^2 - 3*x - 3*y + 1), [])
            sage: print a._ring
            None
            sage: b = FFPD(G, H.factor())
            sage: print b
            (e^(x + y), [(x + 2*y - 1, 1), (2*x + y - 1, 1)])
            sage: print b._ring
            Multivariate Polynomial Ring in x, y over Rational Field

        Singular throws a 'not implemented' error when trying to factor in
        a multivariate polynomial ring over an inexact field ::

            sage: R.<x, y>= PolynomialRing(CC)
            sage: f = (x + 1)/(x*y*(x*y + 1)^2)
            sage: FFPD(quotient=f)
            Traceback (most recent call last):
            ...
            TypeError: Singular error:
               ? not implemented
               ? error occurred in or before STDIN line 17:
               `def sage9=factorize(sage8);`

        """
        # Attributes are
        # self._numerator
        # self._denominator_factored
        # self._ring
        if quotient is not None:
            p = quotient.numerator()
            q = quotient.denominator()
            R = q.parent()
            self._numerator = quotient
            self._denominator_factored = []
            if is_PolynomialRing(R) or is_MPolynomialRing(R):
                self._ring = R
                if not R(q).is_unit():
                    # Factor q
                    try:
                        df = q.factor()
                    except NotImplementedError:
                        # Singular's factor() needs 'proof=False'.
                        df = q.factor(proof=False)
                    self._numerator = p/df.unit()
                    df = sorted([tuple(t) for t in df]) # Sort for consitency.
                    self._denominator_factored = df
            else:
                self._ring = None
            # Done. No reducing needed, as Sage reduced quotient beforehand.
            return

        self._numerator = numerator
        if denominator_factored:
            self._denominator_factored = sorted([tuple(t) for t in
                                             denominator_factored])
            self._ring = denominator_factored[0][0].parent()
        else:
            self._denominator_factored = []
            self._ring = None
        R = self._ring
        if R is not None and numerator in R and reduce_:
            # Reduce fraction if possible.
            numer = R(self._numerator)
            df = self._denominator_factored
            new_df = []
            for (q, e) in df:
                ee = e
                quo, rem = numer.quo_rem(q)
                while rem == 0 and ee > 0:
                    ee -= 1
                    numer = quo
                    quo, rem = numer.quo_rem(q)
                if ee > 0:
                    new_df.append((q, ee))
            self._numerator = numer
            self._denominator_factored = new_df

    def numerator(self):
        r"""
        Return the numerator of ``self``.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x,y>= PolynomialRing(QQ)
            sage: H = (1 - x - y - x*y)**2*(1-x)
            sage: Hfac = H.factor()
            sage: G = exp(y)/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: print F.numerator()
            -e^y
        """
        return self._numerator

    def denominator(self):
        r"""
        Return the denominator of ``self``.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x,y>= PolynomialRing(QQ)
            sage: H = (1 - x - y - x*y)**2*(1-x)
            sage: Hfac = H.factor()
            sage: G = exp(y)/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: print F.denominator()
            x^3*y^2 + 2*x^3*y + x^2*y^2 + x^3 - 2*x^2*y - x*y^2 - 3*x^2 - 2*x*y
            - y^2 + 3*x + 2*y - 1
        """
        return prod([q**e for q, e in self.denominator_factored()])

    def denominator_factored(self):
        r"""
        Return the factorization in ``self.ring()`` of the denominator of
        ``self`` but without the unit part.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x,y>= PolynomialRing(QQ)
            sage: H = (1 - x - y - x*y)**2*(1-x)
            sage: Hfac = H.factor()
            sage: G = exp(y)/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: print F.denominator_factored()
            [(x - 1, 1), (x*y + x + y - 1, 2)]
        """
        return self._denominator_factored

    def ring(self):
        r"""
        Return the ring of the denominator of ``self``, which is
        None in the case where ``self`` doesn't have a denominator.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x,y>= PolynomialRing(QQ)
            sage: H = (1 - x - y - x*y)**2*(1-x)
            sage: Hfac = H.factor()
            sage: G = exp(y)/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: print F.ring()
            Multivariate Polynomial Ring in x, y over Rational Field
            sage: F = FFPD(quotient=G/H)
            sage: print F
            (e^y/(x^3*y^2 + 2*x^3*y + x^2*y^2 + x^3 - 2*x^2*y - x*y^2 - 3*x^2 -
            2*x*y - y^2 + 3*x + 2*y - 1), [])
            sage: print F.ring()
            None
        """
        return self._ring

    def dimension(self):
        r"""
        Return the number of indeterminates of ``self.ring()``.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x,y>= PolynomialRing(QQ)
            sage: H = (1 - x - y - x*y)**2*(1-x)
            sage: Hfac = H.factor()
            sage: G = exp(y)/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: print F.dimension()
            2
        """
        R = self.ring()
        if is_PolynomialRing(R) or is_MPolynomialRing(R):
            return R.ngens()
        else:
            return None

    def list(self):
        r"""
        Convert ``self`` into a list for printing.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x,y>= PolynomialRing(QQ)
            sage: H = (1 - x - y - x*y)**2*(1-x)
            sage: Hfac = H.factor()
            sage: G = exp(y)/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: print F # indirect doctest
            (-e^y, [(x - 1, 1), (x*y + x + y - 1, 2)])
        """
        return (self.numerator(), self.denominator_factored())

    def quotient(self):
        r"""
        Convert ``self`` into a quotient.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x,y>= PolynomialRing(QQ)
            sage: H = (1 - x - y - x*y)**2*(1-x)
            sage: Hfac = H.factor()
            sage: G = exp(y)/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: print F
            (-e^y, [(x - 1, 1), (x*y + x + y - 1, 2)])
            sage: print F.quotient()
            -e^y/(x^3*y^2 + 2*x^3*y + x^2*y^2 + x^3 - 2*x^2*y - x*y^2 - 3*x^2 -
            2*x*y - y^2 + 3*x + 2*y - 1)
        """
        return self.numerator()/self.denominator()

    def __str__(self):
        r"""
        Returns a string representation of ``self``

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x,y> = PolynomialRing(QQ)
            sage: f = FFPD(x + y, [(y, 1), (x, 1)])
            sage: print f
            (x + y, [(y, 1), (x, 1)])
            
        """
        return str(self.list())

    def __eq__(self, other):
        r"""
        Two FFPD instances are equal iff they represent the same
        fraction.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y>= PolynomialRing(QQ)
            sage: df = [x, 1], [y, 1], [x*y+1, 1]
            sage: f = FFPD(x, df)
            sage: ff = FFPD(x, df, reduce_=False)
            sage: f == ff
            True
            sage: g = FFPD(y, df)
            sage: g == f
            False

        ::

            sage: R.<x, y> = PolynomialRing(QQ)
            sage: G = exp(x + y)
            sage: H = (1 - 2*x - y) * (1 - x - 2*y)
            sage: a = FFPD(quotient=G/H)
            sage: b = FFPD(G, H.factor())
            sage: bool(a == b)
            True
        """
        return self.quotient() == other.quotient()

    def __ne__(self, other):
        r"""
        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y>= PolynomialRing(QQ)
            sage: df = [x, 1], [y, 1], [x*y+1, 1]
            sage: f = FFPD(x, df)
            sage: ff = FFPD(x, df, reduce_=False)
            sage: f != ff
            False
            sage: g = FFPD(y, df)
            sage: g != f # indirect doctest
            True
        """
        return not (self == other)

    def __lt__(self, other):
        r"""
        FFPD A is less than FFPD B iff
        (the denominator factorization of A is shorter than that of B) or
        (the denominator factorization lengths are equal and
        the denominator of A is less than that of B in their ring) or
        (the denominator factorization lengths are equal and the
        denominators are equal and the numerator of A is less than that of B
        in their ring).

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y>= PolynomialRing(QQ)
            sage: df = [x, 1], [y, 1], [x*y+1, 1]
            sage: f = FFPD(x, df)
            sage: ff = FFPD(x, df, reduce_=False)
            sage: g = FFPD(y, df)
            sage: h = FFPD(exp(x), df)
            sage: i = FFPD(sin(x + 2), df)
            sage: print f, ff
            (1, [(y, 1), (x*y + 1, 1)]) (x, [(y, 1), (x, 1), (x*y + 1, 1)])
            sage: print f < ff
            True
            sage: print f < g
            True
            sage: print g < h
            True
            sage: print h < i
            False
        """
        sn = self.numerator()
        on = other.numerator()
        sdf = self.denominator_factored()
        odf = other.denominator_factored()
        sd = self.denominator()
        od = other.denominator()

        return bool(len(sdf) < len(odf) or\
          (len(sdf) == len(odf) and sd < od) or\
          (len(sdf) == len(odf) and sd == od and sn < on))

    def univariate_decomposition(self):
        r"""
        Return the usual univariate partial fraction decomposition
        of ``self`` as a FFPDSum instance.
        Assume that ``self`` lies in the field of fractions
        of a univariate factorial polynomial ring.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *

        One variable::

            sage: R.<x> = PolynomialRing(QQ)
            sage: f = 5*x^3 + 1/x + 1/(x-1) + 1/(3*x^2 + 1)
            sage: print f
            (15*x^7 - 15*x^6 + 5*x^5 - 5*x^4 + 6*x^3 - 2*x^2 + x - 1)/(3*x^4 -
            3*x^3 + x^2 - x)
            sage: decomp = FFPD(quotient=f).univariate_decomposition()
            sage: print decomp
            [(5*x^3, []), (1, [(x - 1, 1)]), (1, [(x, 1)]),
            (1/3, [(x^2 + 1/3, 1)])]
            sage: print decomp.sum().quotient() == f
            True

        One variable with numerator in symbolic ring::

            sage: R.<x> = PolynomialRing(QQ)
            sage: f = 5*x^3 + 1/x + 1/(x-1) + exp(x)/(3*x^2 + 1)
            sage: print f
            e^x/(3*x^2 + 1) + ((5*(x - 1)*x^3 + 2)*x - 1)/((x - 1)*x)
            sage: decomp = FFPD(quotient=f).univariate_decomposition()
            sage: print decomp
            [(e^x/(3*x^2 + 1) + ((5*(x - 1)*x^3 + 2)*x - 1)/((x - 1)*x), [])]

        One variable over a finite field::

            sage: R.<x> = PolynomialRing(GF(2))
            sage: f = 5*x^3 + 1/x + 1/(x-1) + 1/(3*x^2 + 1)
            sage: print f
            (x^6 + x^4 + 1)/(x^3 + x)
            sage: decomp = FFPD(quotient=f).univariate_decomposition()
            sage: print decomp
            [(x^3, []), (1, [(x, 1)]), (x, [(x + 1, 2)])]
            sage: print decomp.sum().quotient() == f
            True

        One variable over an inexact field::

            sage: R.<x> = PolynomialRing(CC)
            sage: f = 5*x^3 + 1/x + 1/(x-1) + 1/(3*x^2 + 1)
            sage: print f
            (15.0000000000000*x^7 - 15.0000000000000*x^6 + 5.00000000000000*x^5
            - 5.00000000000000*x^4 + 6.00000000000000*x^3 -
            2.00000000000000*x^2 + x - 1.00000000000000)/(3.00000000000000*x^4
            - 3.00000000000000*x^3 + x^2 - x)
            sage: decomp = FFPD(quotient=f).univariate_decomposition()
            sage: print decomp
            [(5.00000000000000*x^3, []), (1.00000000000000,
            [(x - 1.00000000000000, 1)]), (-0.288675134594813*I,
            [(x - 0.577350269189626*I, 1)]), (1.00000000000000, [(x, 1)]),
            (0.288675134594813*I, [(x + 0.577350269189626*I, 1)])]
            sage: print decomp.sum().quotient() == f # Rounding error coming
            False

        NOTE::

        Let $f = p/q$ be a rational expression where $p$ and $q$ lie in a
        univariate factorial polynomial ring $R$.
        Let $q_1^{e_1} \cdots q_n^{e_n}$ be the
        unique factorization of $q$ in $R$ into irreducible factors.
        Then $f$ can be written uniquely as

        (*)   $p_0 + \sum_{i=1}^{m} p_i/ q_i^{e_i}$,

        for some $p_j \in R$.
        I call (*) the *usual partial fraction decomposition* of f.

        AUTHORS:

        - Robert Bradshaw (2007-05-31)
        - Alexander Raichev (2012-06-25)
        """
        if self.dimension() is None or self.dimension() > 1:
            return FFPDSum([self])

        R = self.ring()
        p = self.numerator()
        q = self.denominator()
        if p in R:
            whole, p = p.quo_rem(q)
        else:
            whole = p
            p = R(1)
        df = self.denominator_factored()
        decomp = [FFPD(whole, [])]
        for (a, m) in df:
            numer = p * prod([b**n for (b, n) in df if b != a]).\
                    inverse_mod(a**m) % (a**m)
            # The inverse exists because the product and a**m
            # are relatively prime.
            decomp.append(FFPD(numer, [(a, m)]))
        return FFPDSum(decomp)

    def nullstellensatz_certificate(self):
        r"""
        Let $[(q_1, e_1), \ldots, (q_n, e_n)]$ be the denominator factorization
        of ``self``.
        Return a list of polynomials $h_1, \ldots, h_m$ in ``self.ring()``
        that satisfies $h_1 q_1 + \cdots + h_m q_n = 1$ if it exists.
        Otherwise return None.
        Only works for multivariate ``self``.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y> = PolynomialRing(QQ)
            sage: G = sin(x)
            sage: H = x^2 * (x*y + 1)
            sage: f = FFPD(G, H.factor())
            sage: L = f.nullstellensatz_certificate()
            sage: print L
            [y^2, -x*y + 1]
            sage: df = f.denominator_factored()
            sage: sum([L[i]*df[i][0]**df[i][1] for i in xrange(len(df))]) == 1
            True

        ::

            sage: f = 1/(x*y)
            sage: L = FFPD(quotient=f).nullstellensatz_certificate()
            sage: L is None
            True

        """

        R = self.ring()
        if R is None:
            return None

        df = self.denominator_factored()
        J = R.ideal([q**e for q, e in df])
        if R(1) in J:
            return R(1).lift(J)
        else:
            return None

    def nullstellensatz_decomposition(self):
        r"""
        Return a Nullstellensatz decomposition of ``self`` as a FFPDSum
        instance.

        Recursive.
        Only works for multivariate ``self``.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y> = PolynomialRing(QQ)
            sage: f = 1/(x*(x*y + 1))
            sage: decomp = FFPD(quotient=f).nullstellensatz_decomposition()
            sage: print decomp
            [(0, []), (1, [(x, 1)]), (-y, [(x*y + 1, 1)])]
            sage: decomp.sum().quotient() == f
            True
            sage: for r in decomp:
            ...       L = r.nullstellensatz_certificate()
            ...       L is None
            ...
            True
            True
            True

        ::

            sage: R.<x, y> = PolynomialRing(QQ)
            sage: G = sin(y)
            sage: H = x*(x*y + 1)
            sage: f = FFPD(G, H.factor())
            sage: decomp = f.nullstellensatz_decomposition()
            sage: print decomp
            [(0, []), (sin(y), [(x, 1)]), (-y*sin(y), [(x*y + 1, 1)])]
            sage: bool(decomp.sum().quotient() == G/H)
            True
            sage: for r in decomp:
            ...       L = r.nullstellensatz_certificate()
            ...       L is None
            ...
            True
            True
            True

        NOTE::

        Let $f = p/q$ where $q$ lies in a $d$ -variate polynomial ring $K[X]$ for some field $K$ and $d \ge 1$.
        Let $q_1^{e_1} \cdots q_n^{e_n}$ be the
        unique factorization of $q$ in $K[X]$ into irreducible factors and
        let $V_i$ be the algebraic variety $\{x \in L^d: q_i(x) = 0\}$ of
        $q_i$ over the algebraic closure $L$ of $K$.
        By [Raic2012]_, $f$ can be written as

        (*)   $\sum p_A/\prod_{i \in A} q_i^{e_i}$,

        where the $p_A$ are products of $p$ and elements in $K[X]$ and
        the sum is taken over all subsets
        $A \subseteq \{1, \ldots, m\}$ such that
        $\cap_{i\in A} T_i \neq \emptyset$.

        I call (*) a *Nullstellensatz decomposition* of $f$.
        Nullstellensatz decompositions are not unique.

        The algorithm used comes from [Raic2012]_.
        """
        L = self.nullstellensatz_certificate()
        if L is None:
            # No decomposing possible.
            return FFPDSum([self])

        # Otherwise decompose recursively.
        decomp = FFPDSum()
        p = self.numerator()
        df = self.denominator_factored()
        m = len(df)
        iteration1 = FFPDSum([FFPD(p*L[i],[df[j]
                              for j in xrange(m) if j != i])
                              for i in xrange(m) if L[i] != 0])

        # Now decompose each FFPD of iteration1.
        for r in iteration1:
            decomp.extend(r.nullstellensatz_decomposition())

        # Simplify and return result.
        return decomp.combine_like_terms().whole_and_parts()

    def algebraic_dependence_certificate(self):
        r"""
        Return the ideal $J$ of annihilating polynomials for the set
        of polynomials ``[q**e for (q, e) in self.denominator_factored()]``,
        which could be the zero ideal.
        The ideal $J$ lies in a polynomial ring over the field
        ``self.ring().base_ring()`` that has
        ``m = len(self.denominator_factored())`` indeterminates.
        Return None if ``self.ring()`` is None.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y> = PolynomialRing(QQ)
            sage: f = 1/(x^2 * (x*y + 1) * y^3)
            sage: ff = FFPD(quotient=f)
            sage: J = ff.algebraic_dependence_certificate()
            sage: print J
            Ideal (1 - 6*T2 + 15*T2^2 - 20*T2^3 + 15*T2^4 - T0^2*T1^3 -
            6*T2^5  + T2^6) of Multivariate Polynomial Ring in
            T0, T1, T2 over Rational Field
            sage: g = J.gens()[0]
            sage: df = ff.denominator_factored()
            sage: g(*(q**e for q, e in df)) == 0
            True

        ::

            sage: R.<x, y> = PolynomialRing(QQ)
            sage: G = exp(x + y)
            sage: H = x^2 * (x*y + 1) * y^3
            sage: ff = FFPD(G, H.factor())
            sage: J = ff.algebraic_dependence_certificate()
            sage: print J
            Ideal (1 - 6*T2 + 15*T2^2 - 20*T2^3 + 15*T2^4 - T0^2*T1^3 -
            6*T2^5 + T2^6) of Multivariate Polynomial Ring in
            T0, T1, T2 over Rational Field
            sage: g = J.gens()[0]
            sage: df = ff.denominator_factored()
            sage: g(*(q**e for q, e in df)) == 0
            True

        ::

            sage: f = 1/(x^3 * y^2)
            sage: J = FFPD(quotient=f).algebraic_dependence_certificate()
            sage: print J
            Ideal (0) of Multivariate Polynomial Ring in T0, T1 over
            Rational Field

        ::

            sage: f = sin(1)/(x^3 * y^2)
            sage: J = FFPD(quotient=f).algebraic_dependence_certificate()
            sage: print J
            None
        """
        R = self.ring()
        if R is None:
            return None

        df = self.denominator_factored()
        if not df:
            return R.ideal()    # The zero ideal.
        m = len(df)
        F = R.base_ring()
        Xs = list(R.gens())
        d = len(Xs)

        # Expand R by 2*m new variables.
        S = 'S'
        while S in [str(x) for x in Xs]:
            S = S + 'S'
        Ss = [S + str(i) for i in xrange(m)]
        T = 'T'
        while T in [str(x) for x in Xs]:
            T = T + 'T'
        Ts = [T + str(i) for i in xrange(m)]

        Vs = [str(x) for x in Xs] + Ss + Ts
        RR = PolynomialRing(F, Vs)
        Xs = RR.gens()[:d]
        Ss = RR.gens()[d: d + m]
        Ts = RR.gens()[d + m: d + 2 * m]

        # Compute the appropriate elimination ideal.
        J = RR.ideal([ Ss[j] - RR(df[j][0]) for j in xrange(m)] +\
                 [ Ss[j]**df[j][1] - Ts[j] for j in xrange(m)])
        J = J.elimination_ideal(Xs + Ss)

        # Coerce J into the polynomial ring in the indeteminates Ts[m:].
        # I choose the negdeglex order because i find it useful in my work.
        RRR = PolynomialRing(F, [str(t) for t in Ts], order ='negdeglex')
        return RRR.ideal(J)

    def algebraic_dependence_decomposition(self, whole_and_parts=True):
        r"""
        Return an algebraic dependence decomposition of ``self`` as a FFPDSum
        instance.

        Recursive.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y> = PolynomialRing(QQ)
            sage: f = 1/(x^2 * (x*y + 1) * y^3)
            sage: ff = FFPD(quotient=f)
            sage: decomp = ff.algebraic_dependence_decomposition()
            sage: print decomp
            [(0, []), (-x, [(x*y + 1, 1)]), (x^2*y^2 - x*y + 1,
            [(y, 3), (x, 2)])]
            sage: print decomp.sum().quotient() == f
            True
            sage: for r in decomp:
            ...       J = r.algebraic_dependence_certificate()
            ...       J is None or J == J.ring().ideal()  # The zero ideal
            ...
            True
            True
            True

        ::

            sage: R.<x, y> = PolynomialRing(QQ)
            sage: G = sin(x)
            sage: H = x^2 * (x*y + 1) * y^3
            sage: f = FFPD(G, H.factor())
            sage: decomp = f.algebraic_dependence_decomposition()
            sage: print decomp
            [(0, []), (x^4*y^3*sin(x), [(x*y + 1, 1)]),
            (-(x^5*y^5 - x^4*y^4 + x^3*y^3 - x^2*y^2 + x*y - 1)*sin(x),
            [(y, 3), (x, 2)])]
            sage: bool(decomp.sum().quotient() == G/H)
            True
            sage: for r in decomp:
            ...       J = r.algebraic_dependence_certificate()
            ...       J is None or J == J.ring().ideal()
            ...
            True
            True
            True

        NOTE::

        Let $f = p/q$ where $q$ lies in a $d$ -variate polynomial ring
        $K[X]$ for some field $K$.
        Let $q_1^{e_1} \cdots q_n^{e_n}$ be the
        unique factorization of $q$ in $K[X]$ into irreducible factors and
        let $V_i$ be the algebraic variety $\{x\in L^d: q_i(x) = 0\}$ of
        $q_i$ over the algebraic closure $L$ of $K$.
        By [Raic2012]_, $f$ can be written as

        (*)   $\sum p_A/\prod_{i \in A} q_i^{b_i}$,

        where the $b_i$ are positive integers, each $p_A$ is a products
        of $p$ and an element in $K[X]$,
        and the sum is taken over all subsets
        $A \subseteq \{1, \ldots, m\}$ such that $|A| \le d$ and
        $\{q_i : i\in A\}$ is algebraically independent.

        I call (*) an *algebraic dependence decomposition* of $f$.
        Algebraic dependence decompositions are not unique.

        The algorithm used comes from [Raic2012]_.
        """
        J = self.algebraic_dependence_certificate()
        if not J:
            # No decomposing possible.
            return FFPDSum([self])

        # Otherwise decompose recursively.
        decomp = FFPDSum()
        p = self.numerator()
        df = self.denominator_factored()
        m = len(df)
        g = J.gens()[0]     # An annihilating polynomial for df.
        new_vars = J.ring().gens()
        # Note that each new_vars[j] corresponds to df[j] such that
        # g([q**e for q, e in df]) = 0.
        # Assuming here that g.parent() has negdeglex term order
        # so that g.lt() is indeed the monomial we want below.
        # Use g to rewrite r into a sum of FFPDs,
        # each with < m distinct denominator factors.
        gg = (g.lt() - g)/(g.lc())
        numers = map(prod, zip(gg.coefficients(), gg.monomials()))
        e = list(g.lt().exponents())[0:m]
        denoms = [(new_vars[j], e[0][j] + 1) for j in xrange(m)]
        # Write r in terms of new_vars,
        # cancel factors in the denominator, and combine like terms.
        iteration1_temp = FFPDSum([FFPD(a, denoms) for a in numers]).\
                          combine_like_terms()
        # Substitute in df.
        qpowsub = dict([(new_vars[j], df[j][0]**df[j][1])
                        for j in xrange(m)])
        iteration1 = FFPDSum()
        for r in iteration1_temp:
            num1 = p*g.parent()(r.numerator()).subs(qpowsub)
            denoms1 = []
            for q, e in r.denominator_factored():
                j = new_vars.index(q)
                denoms1.append((df[j][0], df[j][1]*e))
            iteration1.append(FFPD(num1, denoms1))
        # Now decompose each FFPD of iteration1.
        for r in iteration1:
            decomp.extend(r.algebraic_dependence_decomposition())

        # Simplify and return result.
        return decomp.combine_like_terms().whole_and_parts()

    def leinartas_decomposition(self):
        r"""
        Return a Leinartas decomposition of ``self`` as a FFPDSum instance.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x> = PolynomialRing(QQ)
            sage: f = (x^2 + 1)/((x + 2)*(x - 1)*(x^2 + x + 1))
            sage: decomp = FFPD(quotient=f).leinartas_decomposition()
            sage: print decomp
            [(0, []), (2/9, [(x - 1, 1)]), (-5/9, [(x + 2, 1)]), (1/3*x, [(x^2 + x + 1, 1)])]
            sage: print decomp.sum().quotient() == f
            True
            
        ::
        
            sage: R.<x, y> = PolynomialRing(QQ)
            sage: f = 1/x + 1/y + 1/(x*y + 1)
            sage: decomp = FFPD(quotient=f).leinartas_decomposition()
            sage: print decomp
            [(0, []), (1, [(x*y + 1, 1)]), (x + y, [(y, 1), (x, 1)])]
            sage: print decomp.sum().quotient() == f
            True
            sage: for r in decomp:
            ...       L = r.nullstellensatz_certificate()
            ...       print L is None
            ...       J = r.algebraic_dependence_certificate()
            ...       print J is None or J == J.ring().ideal()
            ...
            True
            True
            True
            True
            True
            True

        ::

            sage: R.<x, y> = PolynomialRing(QQ)
            sage: f = sin(x)/x + 1/y + 1/(x*y + 1)
            sage: G = f.numerator()
            sage: H = R(f.denominator())
            sage: ff = FFPD(G, H.factor())
            sage: decomp = ff.leinartas_decomposition()
            sage: print decomp
            [(0, []), (-(x*y^2*sin(x) + x^2*y + x*y + y*sin(x) + x)*y,
            [(y, 1)]), ((x*y^2*sin(x) + x^2*y + x*y + y*sin(x) + x)*x*y,
            [(x*y + 1, 1)]), (x*y^2*sin(x) + x^2*y + x*y + y*sin(x) + x,
            [(y, 1), (x, 1)])]
            sage: bool(decomp.sum().quotient() == f)
            True
            sage: for r in decomp:
            ...       L = r.nullstellensatz_certificate()
            ...       print L is None
            ...       J = r.algebraic_dependence_certificate()
            ...       print J is None or J == J.ring().ideal()
            ...
            True
            True
            True
            True
            True
            True
            True
            True

        ::

            sage: R.<x, y, z>= PolynomialRing(GF(2, 'a'))
            sage: f = 1/(x * y * z * (x*y + z))
            sage: decomp = FFPD(quotient=f).leinartas_decomposition()
            sage: print decomp
            [(0, []), (1, [(z, 2), (x*y + z, 1)]),
            (1, [(z, 2), (y, 1), (x, 1)])]
            sage: print decomp.sum().quotient() == f
            True

        NOTE::

        Let $f = p/q$ where $q$ lies in a $d$ -variate polynomial ring $K[X]$
        for some field $K$.
        Let $q_1^{e_1} \cdots q_n^{e_n}$ be the
        unique factorization of $q$ in $K[X]$ into irreducible factors and
        let $V_i$ be the algebraic variety
        $\{x\in L^d: q_i(x) = 0\}$ of $q_i$ over the algebraic closure
        $L$ of $K$.
        By [Raic2012]_, $f$ can be written as

        (*)   $\sum p_A/\prod_{i \in A} q_i^{b_i}$,

        where the $b_i$ are positive integers, each $p_A$ is a product of $p$ and an element of $K[X]$, 
        and the sum is taken over all subsets $A \subseteq \{1, \ldots, m\}$ such that 
        (1) $|A| \le d$,
        (2) $\cap_{i\in A} T_i \neq \emptyset$, and
        (3) $\{q_i : i\in A\}$ is algebraically independent.

        In particular, any rational expression in $d$ variables
        can be represented as a sum of rational expressions
        whose denominators each contain at most $d$ distinct irreducible
        factors.

        I call (*) a *Leinartas decomposition* of $f$.
        Leinartas decompositions are not unique.

        The algorithm used comes from [Raic2012]_.
        """
        if self.dimension() == 1:
            # Sage's lift() function doesn't work in
            # univariate polynomial rings.
            # So nullstellensatz_decomposition() won't work.
            # Can use algebraic_dependence_decomposition(),
            # which is sufficient.
            # temp = FFPDSum([self])
            # Alternatively can use univariate_decomposition(), 
            # which is more efficient.
            return self.univariate_decomposition()
        temp = self.nullstellensatz_decomposition()
        decomp = FFPDSum()
        for r in temp:
            decomp.extend(r.algebraic_dependence_decomposition())

        # Simplify and return result.
        return decomp.combine_like_terms().whole_and_parts()

    def cohomology_decomposition(self):
        r"""
        Let $p/(q_1^{e_1} \cdots q_n^{e_n})$ be the fraction represented
        by ``self`` and let $K[x_1, \ldots, x_d]$ be the polynomial ring
        in which the $q_i$ lie.
        Assume that $n \le d$ and that the gradients of the $q_i$ are linearly
        independent at all points in the intersection
        $V_1 \cap \ldots \cap V_n$ of the algebraic varieties
        $V_i = \{x \in L^d: q_i(x) = 0 \}$, where $L$ is the algebraic closure
        of the field $K$.
        Return a FFPDSum $f$ such that the differential form
        $f dx_1 \wedge \cdots \wedge dx_d$ is de Rham cohomologous to the
        differential form
        $p/(q_1^{e_1} \cdots q_n^{e_n}) dx_1 \wedge \cdots \wedge dx_d$
        and such that the denominator of each summand of $f$ contains
        no repeated irreducible factors.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x> = PolynomialRing(QQ)
            sage: f = 1/(x^2 + x + 1)^3
            sage: decomp = FFPD(quotient=f).cohomology_decomposition()
            sage: print decomp
            [(0, []), (2/3, [(x^2 + x + 1, 1)])]
        
        ::    
            
            sage: R.<x, y>= PolynomialRing(QQ)
            sage: print FFPD(1, [(x, 1), (y, 2)]).cohomology_decomposition()
            [(0, [])]

        ::

            sage: R.<x, y>= PolynomialRing(QQ)
            sage: p = 1
            sage: qs = [(x*y - 1, 1), (x**2 + y**2 - 1, 2)]
            sage: f = FFPD(p, qs)
            sage: print f.cohomology_decomposition()
            [(0, []), (4/3*x*y + 4/3, [(x^2 + y^2 - 1, 1)]),
            (1/3, [(x*y - 1, 1), (x^2 + y^2 - 1, 1)])]

        NOTES:

        The algorithm used here comes from the proof of Theorem 17.4 of
        [AiYu1983]_.

        AUTHORS:

        - Alexander Raichev (2008-10-01, 2011-01-15, 2012-07-31)
        """
        R = self.ring()
        df = self.denominator_factored()
        n = len(df)
        if R is None or sum([e for (q, e) in df]) <= n:
            # No decomposing possible.
            return FFPDSum([self])

        # Otherwise decompose recursively.
        decomp = FFPDSum()
        p = self.numerator()
        qs = [q for (q, e) in df]
        X = sorted(R.gens())
        var_sets_n = Set(X).subsets(n)

        # Compute Jacobian determinants for qs.
        dets = []
        for v in var_sets_n:
            # Sort v according to the term order of R.
            x = sorted(v)
            jac = jacobian(qs, x)
            dets.append(R(jac.determinant()))

        # Get a Nullstellensatz certificate for qs and dets.
        if self.dimension() == 1:
            # Sage's lift() function doesn't work in
            # univariate polynomial rings.
            # So use xgcd(), which does the same thing in this case.
            # Note that by assumption qs and dets have length 1.
            L = xgcd(qs[0], dets[0])[1:]
        else:
            L = R(1).lift(R.ideal(qs + dets))

        # Do first iteration of decomposition.
        iteration1 = FFPDSum()
        # Contributions from qs.
        for i in xrange(n):
            if L[i] == 0:
                continue
            # Cancel one df[i] from denominator.
            new_df = [list(t) for t in df]
            if new_df[i][1] > 1:
                new_df[i][1] -= 1
            else:
                del(new_df[i])
            iteration1.append(FFPD(p*L[i], new_df))

        # Contributions from dets.
        # Compute each contribution's cohomologous form using
        # the least index j such that new_df[j][1] > 1.
        # Know such an index exists by first 'if' statement at
        # the top.
        for j in xrange(n):
            if df[j][1] > 1:
                J = j
                break
        new_df = [list(t) for t in df]
        new_df[J][1] -= 1
        for k in xrange(var_sets_n.cardinality()):
            if L[n + k] == 0:
                continue
            # Sort variables according to the term order of R.
            x = sorted(var_sets_n[k])
            # Compute Jacobian in the Symbolic Ring.
            jac = jacobian([SR(p*L[n + k])] +
                           [SR(qs[j]) for j in xrange(n) if j != J],
                           [SR(xx) for xx in x])
            det = jac.determinant()
            psign = FFPD.permutation_sign(x, X)
            iteration1.append(FFPD((-1)**J*det/\
                                   (psign*new_df[J][1]),
                                   new_df))

        # Now decompose each FFPD of iteration1.
        for r in iteration1:
            decomp.extend(r.cohomology_decomposition())

        # Simplify and return result.
        return decomp.combine_like_terms().whole_and_parts()

    @staticmethod
    def permutation_sign(s, u):
        r"""
        This function returns the sign of the permutation on
        ``1, ..., len(u)`` that is induced by the sublist
        ``s`` of ``u``.
        For internal use by cohomology_decomposition().

        INPUT:

        - ``s`` - A sublist of ``u``.
        - ``u`` - A list.

        OUTPUT:

        The sign of the permutation obtained by taking indices
        within ``u`` of the list ``s + sc``, where ``sc`` is ``u``
        with the elements of ``s`` removed.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: u = ['a','b','c','d','e']
            sage: s = ['b','d']
            sage: FFPD.permutation_sign(s, u)
            -1
            sage: s = ['d','b']
            sage: FFPD.permutation_sign(s, u)
            1

        AUTHORS:

        - Alexander Raichev (2008-10-01, 2012-07-31)
        """
        # Convert lists to lists of numbers in {1,..., len(u)}
        A = [i + 1  for i in xrange(len(u))]
        B = [u.index(x) + 1 for x in s]

        C = sorted(list(Set(A).difference(Set(B))))
        P = Permutation(B + C)
        return P.signature()

    def asymptotic_decomposition(self, alpha, asy_var=None):
        r"""
        Return a FFPDSum that has the same asymptotic expansion as ``self``
        in the direction ``alpha`` but each of whose FFPDs has a
        denominator factorization of the form $[(q_1, 1), \ldots, (q_n, 1)]$,
        where ``n`` is at most ``d = self.dimension()``.
        The output results from a Leinartas decomposition followed by a
        cohomology decomposition.

        INPUT:

        - ``alpha`` - A d-tuple of positive integers or symbolic variables.
        - ``asy_var`` - (Optional; default=None) A symbolic variable with
          respect to which to compute asymptotics.
          If None is given the set ``asy_var = var('r')``.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x> = PolynomialRing(QQ)
            sage: f = (x^2 + 1)/((x - 1)^3*(x + 2))
            sage: F = FFPD(quotient=f)
            sage: alpha = [var('a')]
            sage: print F.asymptotic_decomposition(alpha)
            [(0, []), (1/54*(5*a^2*x^2 + 2*a^2*x + 11*a^2)*r^2/x^2 - 1/54*(5*a*x^2 - 2*a*x - 33*a)*r/x^2 + 11/27/x^2, [(x - 1, 1)]), (-5/27, [(x + 2, 1)])]
            
        ::    
            
            sage: R.<x, y>= PolynomialRing(QQ)
            sage: H = (1 - 2*x -y)*(1 - x -2*y)**2
            sage: Hfac = H.factor()
            sage: G = 1/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: alpha = var('a, b')
            sage: print F.asymptotic_decomposition(alpha) # long time
            [(0, []), (-1/3*(a*y - 2*b*x)*r/(x*y) + 1/3*(2*x - y)/(x*y),
            [(x + 2*y - 1, 1), (2*x + y - 1, 1)])]

        AUTHORS:

        - Alexander Raichev (2012-08-01)
        """
        R = self.ring()
        if R is None:
            return None

        d = self.dimension()
        n = len(self.denominator_factored())
        X = [SR(x) for x in R.gens()]

        # Reduce number of distinct factors in denominator of self
        # down to at most d.
        decomp1 = FFPDSum([self])
        if n > d:
            decomp1 = decomp1[0].leinartas_decomposition()

        # Reduce to no repeated factors in denominator of each element
        # of decomp1.
        # Compute the cohomology decomposition for each
        # Cauchy differential form generated by each element of decomp.
        if asy_var is None:
            asy_var = var('r')
        cauchy_stuff = prod([X[j]**(-alpha[j]*asy_var - 1) for j in xrange(d)])
        decomp2 = FFPDSum()
        for f in decomp1:
            ff = FFPD(f.numerator()*cauchy_stuff,
                      f.denominator_factored())
            decomp2.extend(ff.cohomology_decomposition())
        decomp2 = decomp2.combine_like_terms()

        # Divide out cauchy_stuff from integrands.
        decomp3 = FFPDSum()
        for f in decomp2:
            ff = FFPD((f.numerator()/cauchy_stuff).\
                      simplify_full().collect(asy_var),
                      f.denominator_factored())
            decomp3.append(ff)

        return decomp3

    def asymptotics(self, p, alpha, N, asy_var=None, numerical=0):
        r"""
        Return the first $N$ terms (some of which could be zero)
        of the asymptotic expansion of the Maclaurin ray coefficients
        $F_{r\alpha}$ of the function $F$ represented by ``self``
        as $r\to\infty$, where $r$ = ``asy_var`` and ``alpha`` is a tuple of
        positive integers of length ``d = self.dimension()``.
        Assume that 
        
        - $F$ is holomorphic in a neighborhood of the origin;
        - the unique factorization of the denominator $H$ of $F$ in the local 
          algebraic ring at $p$ equals its unique factorization in the local 
          analytic ring at $p$;
        - the unique factorization of $H$ in the local algebraic ring at $p$
          has $<= d$ irreducible factors, none of which are repeated
          (one can reduce to this case via asymptotic_decomposition());
        - $p$ is a convenient strictly minimal smooth or multiple point
          with all nonzero coordinates that is critical and nondegenerate
          for ``alpha``.

        INPUT:

        - ``p`` - A dictionary with keys that can be coerced to equal
          ``self.ring().gens()``.
        - ``alpha`` - A tuple of length ``self.dimension()`` of
          positive integers or, if $p$ is a smooth point,
          possibly of symbolic variables.
        - ``N`` - A positive integer.
        - ``numerical`` - (Optional; default=0) A natural number.
          If numerical > 0, then return a numerical approximation
          of $F_{r \alpha}$ with ``numerical`` digits of precision.
          Otherwise return exact values.
        - ``asy_var`` - (Optional; default=None) A  symbolic variable.
          The variable of the asymptotic expansion.
          If none is given, ``var('r')`` will be assigned.

        OUTPUT:

        The tuple (asy, exp_scale, subexp_part).
        Here asy is the sum of the first $N$ terms (some of which might be 0)
        of the asymptotic expansion of $F_{r\alpha}$ as $r\to\infty$;
        exp_scale**r is the exponential factor of asy;
        subexp_part is the subexponential factor of asy.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *

        A smooth point example::

            sage: R.<x,y>= PolynomialRing(QQ)
            sage: H = (1 - x - y - x*y)**2
            sage: Hfac = H.factor()
            sage: G = 1/Hfac.unit()
            sage: F = FFPD(G, Hfac); print(F)
            (1, [(x*y + x + y - 1, 2)])
            sage: alpha = [4, 3]
            sage: decomp = F.asymptotic_decomposition(alpha); print decomp
            [(0, []), (-3/2*(y + 1)*r/y - 1/2*(y + 1)/y, [(x*y + x + y - 1, 1)])]
            sage: F1 = decomp[1]
            sage: p = {y: 1/3, x: 1/2}
            sage: asy = F1.asymptotics(p, alpha, 2)  # long time
            Creating auxiliary functions...
            Computing derivatives of auxiliary functions...
            Computing derivatives of more auxiliary functions...
            Computing second order differential operator actions...
            sage: print asy  # long time
            (1/6000*(3600*sqrt(2)*sqrt(3)*sqrt(5)*sqrt(r)/sqrt(pi) + 463*sqrt(2)*sqrt(3)*sqrt(5)/(sqrt(pi)*sqrt(r)))*432^r, 432, 3/5*sqrt(2)*sqrt(3)*sqrt(5)*sqrt(r)/sqrt(pi) + 463/6000*sqrt(2)*sqrt(3)*sqrt(5)/(sqrt(pi)*sqrt(r)))
            sage: print F.relative_error(asy[0], alpha, [1, 2, 4, 8, 16], asy[1]) # long time
            Calculating errors table in the form
            exponent, scaled Maclaurin coefficient, scaled asymptotic
            values, relative errors...
            [((4, 3), 2.083333333, [2.092576110], [-0.004436533009]),
            ((8, 6), 2.787374614, [2.790732875], [-0.001204811281]),
            ((16, 12), 3.826259447, [3.827462310], [-0.0003143703383]),
            ((32, 24), 5.328112821, [5.328540787], [-0.00008032229296]),
            ((64, 48), 7.475927885, [7.476079664], [-0.00002030233658])]

        A multiple point example::

            sage: R.<x,y,z>= PolynomialRing(QQ)
            sage: H = (4 - 2*x - y - z)**2*(4 - x - 2*y - z)
            sage: Hfac = H.factor()
            sage: G = 16/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: print F
            (-16, [(x + 2*y + z - 4, 1), (2*x + y + z - 4, 2)])
            sage: alpha = [3, 3, 2]
            sage: decomp = F.asymptotic_decomposition(alpha); print decomp
            [(0, []), (16*(4*y - 3*z)*r/(y*z) + 16*(2*y - z)/(y*z), [(x + 2*y + z - 4, 1), (2*x + y + z - 4, 1)])]
            sage: F1 = decomp[1]
            sage: p = {x: 1, y: 1, z: 1}
            sage: asy = F1.asymptotics(p, alpha, 2) 
            Creating auxiliary functions...
            Computing derivatives of auxiliary functions...
            Computing derivatives of more auxiliary functions...
            Computing second-order differential operator actions...
            sage: print asy 
            (4/3*sqrt(3)*sqrt(r)/sqrt(pi) + 47/216*sqrt(3)/(sqrt(pi)*sqrt(r)), 1, 4/3*sqrt(3)*sqrt(r)/sqrt(pi) + 47/216*sqrt(3)/(sqrt(pi)*sqrt(r)))
            sage: print F.relative_error(asy[0], alpha, [1, 2, 4, 8], asy[1]) 
            Calculating errors table in the form
            exponent, scaled Maclaurin coefficient, scaled asymptotic values,
            relative errors...
            [((3, 3, 2), 0.9812164307, [1.515572606], [-0.5445854340]),
            ((6, 6, 4),
            1.576181132, [1.992989399], [-0.2644418580]),
            ((12, 12, 8), 2.485286378,
            [2.712196351], [-0.09130133851]), ((24, 24, 16), 3.700576827,
            [3.760447895], [-0.01617884750])]

        NOTES:

        The algorithms used here come from [RaWi2008a]_ and [RaWi2012]_.

        AUTHORS:

        - Alexander Raichev (2008-10-01, 2010-09-28, 2011-04-27, 2012-08-03)
        """
        R = self.ring()
        if R is None:
            return None

        # Coerce keys of p into R.
        p = FFPD.coerce_point(R, p)

        if asy_var is None:
            asy_var = var('r')
        d = self.dimension()
        X = list(R.gens())
        alpha = list(alpha)
        df = self.denominator_factored()
        n = len(df)     # Number of smooth factors
        
        # Find greatest i such that X[i] is a convenient coordinate,
        # that is, such that for all (h, e) in df, we have
        # (X[i]*diff(h, X[i])).subs(p) != 0.
        # Assuming such an i exists.
        i = d - 1
        while 0 in [(X[i]*diff(h, X[i])).subs(p) for (h, e) in df]:
            i -= 1
        coordinate = i

        if n == 1:
            # Smooth point.
            return self.asymptotics_smooth(p, alpha, N, asy_var,
                                           coordinate, numerical)
        else:
            # Multiple point.
            return self.asymptotics_multiple(p, alpha, N, asy_var,
                                             coordinate, numerical)

    def asymptotics_smooth(self, p, alpha, N, asy_var, coordinate=None,
                           numerical=0):
        r"""
        Does what asymptotics() does but only in the case of a
        convenient smooth point.
        
        INPUT:

        - ``p`` - A dictionary with keys that can be coerced to equal
          ``self.ring().gens()``.
        - ``alpha`` - A tuple of length ``d = self.dimension()`` of
          positive integers or, if $p$ is a smooth point,
          possibly of symbolic variables.
        - ``N`` - A positive integer.
        - ``asy_var`` - (Optional; default=None) A symbolic variable.
          The variable of the asymptotic expansion.
          If none is given, ``var('r')`` will be assigned.
        - ``coordinate``- (Optional; default=None) An integer in
          {0, ..., d-1} indicating a convenient coordinate to base
          the asymptotic calculations on.
          If None is assigned, then choose ``coordinate=d-1``.
        - ``numerical`` - (Optional; default=0) A natural number.
          If numerical > 0, then return a numerical approximation of the
          Maclaurin ray coefficients of ``self`` with ``numerical`` digits
          of precision.
          Otherwise return exact values.

        NOTES:

        The formulas used for computing the asymptotic expansions are
        Theorems 3.2 and 3.3 [RaWi2008a]_ with the exponent of H equal to 1.
        Theorem 3.2 is a specialization of Theorem 3.4 of [RaWi2012]_
        with $n=1$.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x> = PolynomialRing(QQ)
            sage: H = 2 - 3*x 
            sage: Hfac = H.factor()
            sage: G = 1/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: print F
            (-1/3, [(x - 2/3, 1)])
            sage: alpha = [2]
            sage: p = {x: 2/3}
            sage: asy = F.asymptotics_smooth(p, alpha, 3, asy_var=var('r'))
            sage: print asy
            (1/2*(9/4)^r, 9/4, 1/2)
            
        ::
        
            sage: R.<x, y>= PolynomialRing(QQ)
            sage: H = 1-x-y-x*y
            sage: Hfac = H.factor()
            sage: G = 1/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: alpha = [3, 2]
            sage: p = {y: 1/2*sqrt(13) - 3/2, x: 1/3*sqrt(13) - 2/3}
            sage: print F.asymptotics_smooth(p, alpha, 2, var('r'), numerical=3) # long time
            Creating auxiliary functions...
            Computing derivatives of auxiliary functions...
            Computing derivatives of more auxiliary functions...
            Computing second order differential operator actions...
            ((0.369/sqrt(r) - 0.0186/r^(3/2))*71.2^r, 71.2,
            0.369/sqrt(r) - 0.0186/r^(3/2))

        ::

            sage: R.<x, y> = PolynomialRing(QQ)
            sage: q = 1/2
            sage: qq = q.denominator()
            sage: H = 1 - q*x + q*x*y - x^2*y
            sage: Hfac = H.factor()
            sage: G = (1 - q*x)/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: alpha = list(qq*vector([2, 1 - q]))
            sage: print alpha
            [4, 1]
            sage: p = {x: 1, y: 1}
            sage: print F.asymptotics_smooth(p, alpha, 5, var('r')) # long time
            Creating auxiliary functions...
            Computing derivatives of auxiliary functions...
            Computing derivatives of more auxiliary functions...
            Computing second order differential operator actions...
            (1/12*2^(2/3)*sqrt(3)*gamma(1/3)/(pi*r^(1/3)) -
            1/96*2^(1/3)*sqrt(3)*gamma(2/3)/(pi*r^(5/3)), 1,
            1/12*2^(2/3)*sqrt(3)*gamma(1/3)/(pi*r^(1/3)) -
            1/96*2^(1/3)*sqrt(3)*gamma(2/3)/(pi*r^(5/3)))

        AUTHORS:

        - Alexander Raichev (2008-10-01, 2010-09-28, 2012-08-01)
        """
        R = self.ring()
        if R is None:
            return None

        d = self.dimension()
        I = sqrt(-Integer(1))
        # Coerce everything into the Symbolic Ring.
        X = [SR(x) for x in R.gens()]
        G = SR(self.numerator())
        H = SR(self.denominator())
        p = dict([(SR(x), p[x]) for x in R.gens()])
        alpha = [SR(a) for a in alpha]

        # Put given convenient coordinate at end of variable list.
        if coordinate is not None:
            x = X.pop(coordinate)
            X.append(x)
            a = alpha.pop(coordinate)
            alpha.append(a)

        # Deal with the simple univariate case first.
        # Same as the multiple point case with n == d.
        # but with a negative sign.
        # I'll just past the code from the multiple point case.
        if d == 1:
            det = jacobian(H, X).subs(p).determinant().abs()
            exp_scale = prod([(p[X[i]]**(-alpha[i])).subs(p)
                              for i in xrange(d)] )
            subexp_part = -G.subs(p)/(det*prod(p.values()))
            if numerical:
                exp_scale = exp_scale.n(digits=numerical)
                subexp_part = subexp_part.n(digits=numerical)
            return (exp_scale**asy_var*subexp_part, exp_scale, subexp_part)
            
        # If p is a tuple of rationals, then compute with it directly.
        # Otherwise, compute symbolically and plug in p at the end.
        if vector(p.values()) in QQ**d:
            P = p
        else:
            sP = [var('p' + str(j)) for j in xrange(d)]
            P = dict( [(X[j], sP[j]) for j in xrange(d)] )
            p = dict( [(sP[j], p[X[j]]) for j in xrange(d)] )

        # Setup.
        print "Creating auxiliary functions..."
        # Implicit functions.
        h = function('h', *tuple(X[:d - 1]))
        U = function('U', *tuple(X))
        # All other functions are defined in terms of h, U, and
        # explicit functions.
        Gcheck = -G/U * (h/X[d - 1])
        A = Gcheck.subs({X[d - 1]: Integer(1)/h})/h
        t = 't'
        while t in [str(x) for x in X]:
            t = t + 't'
        T = [var(t + str(i)) for i in xrange(d - 1)]
        e = dict([(X[i], P[X[i]]*exp(I*T[i])) for i in xrange(d - 1)])
        ht = h.subs(e)
        Ht = H.subs(e).subs({X[d - 1]: Integer(1)/ht})
        At = A.subs(e)
        Phit = -log(P[X[d - 1]]*ht) + \
               I * add([alpha[i]/alpha[d - 1]*T[i] for i in xrange(d - 1)])
        Tstar = dict([(t, Integer(0)) for t in T])
        # Store h and U and all their derivatives evaluated at P.
        atP = P.copy()
        atP.update({h.subs(P): Integer(1)/P[X[d - 1]]})

        # Compute the derivatives of h up to order 2*N, evaluate at P,
        # and store in atP.
        # Keep a copy of unevaluated h derivatives for use in the case
        # d = 2 and v > 2 below.
        hderivs1 = {}   # First derivatives of h.
        for i in xrange(d - 1):
            s = solve( diff(H.subs({X[d - 1]: Integer(1)/h}), X[i]),
                      diff(h, X[i]))[0].rhs().simplify()
            hderivs1.update({diff(h, X[i]): s})
            atP.update({diff(h, X[i]).subs(P): s.subs(P).subs(atP)})
        hderivs = FFPD.diff_all(h, X[0: d - 1], 2*N, sub=hderivs1, rekey=h)
        for k in hderivs.keys():
            atP.update({k.subs(P):hderivs[k].subs(atP)})

        # Compute the derivatives of U up to order 2*N and evaluate at P.
        # To do this, differentiate H = U*Hcheck over and over, evaluate at P,
        # and solve for the derivatives of U at P.
        # Need the derivatives of H with short keys to pass on
        # to diff_prod later.
        Hderivs = FFPD.diff_all(H, X, 2*N, ending=[X[d - 1]], sub_final=P)
        print "Computing derivatives of auxiliary functions..."
        # For convenience in checking if all the nontrivial derivatives of U
        # at p are zero a few line below, store the value of U(p) in atP
        # instead of in Uderivs.
        Uderivs ={}
        atP.update({U.subs(P): diff(H, X[d - 1]).subs(P)})
        end = [X[d - 1]]
        Hcheck = X[d - 1] - Integer(1)/h
        k = H.polynomial(CC).degree() - 1
        if k == 0:
            # Then we can conclude that all higher derivatives of U are zero.
            for l in xrange(1, 2*N + 1):
                for s in UnorderedTuples(X, l):
                    Uderivs[diff(U, s).subs(P)] = Integer(0)
        elif k > 0 and k < 2*N:
            all_zero = True
            Uderivs =  FFPD.diff_prod(Hderivs, U, Hcheck, X,
                                     range(1, k + 1), end, Uderivs, atP)
            # Check for a nonzero U derivative.
            if Uderivs.values() != [Integer(0)  for i in xrange(len(Uderivs))]:
                all_zero = False
            if all_zero:
                # Then, using a proposition at the end of [RaWi2012], we can
                # conclude that all higher derivatives of U are zero.
                for l in xrange(k + 1, 2*N +1):
                    for s in UnorderedTuples(X, l):
                        Uderivs.update({diff(U, s).subs(P): Integer(0)})
            else:
                # Have to compute the rest of the derivatives.
                Uderivs = FFPD.diff_prod(Hderivs, U, Hcheck, X,
                                         range(k + 1, 2*N + 1), end, Uderivs,
                                         atP)
        else:
            Uderivs = FFPD.diff_prod(Hderivs, U, Hcheck, X,
                                     range(1, 2*N + 1), end, Uderivs, atP)
        atP.update(Uderivs)

        # In general, this algorithm is not designed to handle the case of a
        # singular Phit''(Tstar).
        # However, when d = 2 the algorithm can cope.
        if d == 2:
            # Compute v, the order of vanishing at Tstar of Phit.
            # It is at least 2.
            v = Integer(2)
            Phitderiv = diff(Phit, T[0], 2)
            splat = Phitderiv.subs(Tstar).subs(atP).subs(p).simplify()
            while splat == 0:
                v += 1
                if v > 2*N:
                    # Then need to compute more derivatives of h for atP.
                    hderivs.update({diff(h, X[0], v):
                                    diff(hderivs[diff(h, X[0], v - 1)],
                                    X[0]).subs(hderivs1)})
                    atP.update({diff(h, X[0], v).subs(P):
                                hderivs[diff(h, X[0], v)].subs(atP)})
                Phitderiv = diff(Phitderiv, T[0])
                splat = Phitderiv.subs(Tstar).subs(atP).subs(p).simplify()
        if d == 2 and v > 2:
            t = T[0]  # Simplify variable names.
            a = splat/factorial(v)
            Phitu = Phit - a*t**v

            # Compute all partial derivatives of At and Phitu
            # up to orders 2*(N - 1) and 2*(N - 1) + v, respectively,
            # in case v is even.
            # Otherwise, compute up to orders N - 1 and N - 1 + v,
            # respectively.
            # To speed up later computations,
            # create symbolic functions AA and BB
            # to stand in for the expressions At and Phitu, respectively.
            print "Computing derivatives of more auxiliary functions..."
            AA = function('AA', t)
            BB = function('BB', t)
            if v.mod(2) == 0:
                At_derivs = FFPD.diff_all(At, T, 2*N - 2,
                                          sub=hderivs1, sub_final=[Tstar, atP],
                                          rekey=AA)
                Phitu_derivs = FFPD.diff_all(Phitu, T, 2*N - 2 +v,
                                             sub=hderivs1,
                                             sub_final=[Tstar, atP],
                                             zero_order=v + 1, rekey=BB)
            else:
                At_derivs = FFPD.diff_all(At, T, N - 1, sub=hderivs1,
                                          sub_final=[Tstar, atP], rekey=AA)
                Phitu_derivs = FFPD.diff_all(Phitu, T, N - 1 + v,
                                             sub=hderivs1,
                                             sub_final=[Tstar, atP],
                                             zero_order=v + 1 , rekey=BB)
            AABB_derivs = At_derivs
            AABB_derivs.update(Phitu_derivs)
            AABB_derivs[AA] = At.subs(Tstar).subs(atP)
            AABB_derivs[BB] = Phitu.subs(Tstar).subs(atP)
            print "Computing second order differential operator actions..."
            DD = FFPD.diff_op_simple(AA, BB, AABB_derivs, t, v, a, N)

            # Plug above into asymptotic formula.
            L = []
            if v.mod(2) == 0:
                for k in xrange(N):
                    L.append(add([
                    (-1)**l * gamma((2*k + v*l + 1)/v)/\
                    (factorial(l) * factorial(2*k + v*l))*\
                    DD[(k, l)] for l in xrange(0, 2*k + 1) ]))
                chunk = a**(-1/v)/(pi*v)*add([
                        alpha[d - 1 ]**(-(2*k + 1)/v)*\
                        L[k]*asy_var**(-(2*k + 1)/v) for k in xrange(N) ])
            else:
                zeta = exp(I*pi/(2*v))
                for k in xrange(N):
                    L.append(add([
                    (-1)**l*gamma((k + v*l + 1)/v)/\
                    (factorial(l)*factorial(k + v*l))*\
                    (zeta**(k + v*l + 1) +\
                    (-1)**(k + v*l)*zeta**(-(k + v*l + 1)))*\
                    DD[(k, l)] for l in xrange(0, k + 1) ]))
                chunk = abs(a)**(-1/v)/(2*pi*v)*add([
                        alpha[d - 1]**(-(k + 1)/v)*\
                        L[k] *asy_var**(-(k + 1)/v) for k in xrange(N) ])

        # Asymptotics for d >= 2 case.
        # A singular Phit''(Tstar) will cause a crash in this case.
        else:
            Phit1 = jacobian(Phit, T).subs(hderivs1)
            a = jacobian(Phit1, T).subs(hderivs1).subs(Tstar).subs(atP)
            a_inv = a.inverse()
            Phitu = Phit - (Integer(1)/Integer(2))*matrix([T])*\
                    a*matrix([T]).transpose()
            Phitu = Phitu[0][0]
            # Compute all partial derivatives of At and Phitu up to
            # orders 2*N-2 and 2*N, respectively.
            # Take advantage of the fact that At and Phitu
            # are sufficiently differentiable functions so that mixed partials
            # are equal.  Thus only need to compute representative partials.
            # Choose nondecreasing sequences as representative differentiation-
            # order sequences.
            # To speed up later computations,
            # create symbolic functions AA and BB
            # to stand in for the expressions At and Phitu, respectively.
            print "Computing derivatives of more auxiliary functions..."
            AA = function('AA', *tuple(T))
            At_derivs = FFPD.diff_all(At, T, 2*N - 2, sub=hderivs1,
                                      sub_final =[Tstar, atP], rekey=AA)
            BB = function('BB', *tuple(T))
            Phitu_derivs = FFPD.diff_all(Phitu, T, 2*N, sub=hderivs1,
                                         sub_final =[Tstar, atP], rekey=BB,
                                         zero_order=3)
            AABB_derivs = At_derivs
            AABB_derivs.update(Phitu_derivs)
            AABB_derivs[AA] = At.subs(Tstar).subs(atP)
            AABB_derivs[BB] = Phitu.subs(Tstar).subs(atP)
            print "Computing second order differential operator actions..."
            DD = FFPD.diff_op(AA, BB, AABB_derivs, T, a_inv, 1 , N)

            # Plug above into asymptotic formula.
            L =[]
            for k in xrange(N):
                L.append(add([
                         DD[(0, k, l)]/((-1)**k*2**(l+k)*\
                         factorial(l)*factorial(l+k))
                         for l in xrange(0, 2*k + 1) ]))
            chunk = add([ (2*pi)**((1 - d)/Integer(2))*\
                    a.determinant()**(-Integer(1)/Integer(2))*\
                    alpha[d - 1]**((Integer(1) - d)/Integer(2) - k)*L[k]*\
                    asy_var**((Integer(1) - d)/Integer(2) - k)
                    for k in xrange(N) ])

        chunk = chunk.subs(p).simplify()
        coeffs = chunk.coefficients(asy_var)
        coeffs.reverse()
        coeffs = coeffs[:N]
        if numerical:
            subexp_part = add([co[0].subs(p).n(digits=numerical)*\
                          asy_var**co[1] for co in coeffs])
            exp_scale = prod([(P[X[i]]**(-alpha[i])).subs(p)
                              for i in xrange(d)]).n(digits=numerical)
        else:
            subexp_part = add([co[0].subs(p)*asy_var**co[1] for co in coeffs])
            exp_scale = prod([(P[X[i]]**(-alpha[i])).subs(p)
                             for i in xrange(d)])
        return (exp_scale**asy_var*subexp_part, exp_scale, subexp_part)

    def asymptotics_multiple(self, p, alpha, N, asy_var, coordinate=None,
                             numerical=0):
        r"""
        Does what asymptotics() does but only in the case of a
        convenient multiple point nondegenerate for alpha.
        Assume also that ``self.dimension >= 2`` and that the 
        ``p.values()`` are not symbolic variables.

        INPUT:

        - ``p`` - A dictionary with keys that can be coerced to equal
          ``self.ring().gens()``.
        - ``alpha`` - A tuple of length ``d = self.dimension()`` of
          positive integers or, if $p$ is a smooth point,
          possibly of symbolic variables.
        - ``N`` - A positive integer.
        - ``asy_var`` - (Optional; default=None) A symbolic variable.
          The variable of the asymptotic expansion.
          If none is given, ``var('r')`` will be assigned.
        - ``coordinate``- (Optional; default=None) An integer in
          {0, ..., d-1} indicating a convenient coordinate to base
          the asymptotic calculations on.
          If None is assigned, then choose ``coordinate=d-1``.
        - ``numerical`` - (Optional; default=0) A natural number.
          If numerical > 0, then return a numerical approximation of the
          Maclaurin ray coefficients of ``self`` with ``numerical`` digits
          of precision.
          Otherwise return exact values.

        NOTES:

        The formulas used for computing the asymptotic expansion are
        Theorem 3.4 and Theorem 3.7 of [RaWi2012]_.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y, z>= PolynomialRing(QQ)
            sage: H = (4 - 2*x - y - z)*(4 - x -2*y - z)
            sage: Hfac = H.factor()
            sage: G = 16/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: print F
            (16, [(x + 2*y + z - 4, 1), (2*x + y + z - 4, 1)])
            sage: p = {x: 1, y: 1, z: 1}
            sage: alpha = [3, 3, 2]
            sage: print F.asymptotics_multiple(p, alpha, 2, var('r')) # long time
            Creating auxiliary functions...
            Computing derivatives of auxiliary functions...
            Computing derivatives of more auxiliary functions...
            Computing second-order differential operator actions...
            (4/3*sqrt(3)/(sqrt(pi)*sqrt(r)) -
            25/216*sqrt(3)/(sqrt(pi)*r^(3/2)), 1,
            4/3*sqrt(3)/(sqrt(pi)*sqrt(r)) - 25/216*sqrt(3)/(sqrt(pi)*r^(3/2)))

        ::

            sage: R.<x, y, z>= PolynomialRing(QQ)
            sage: H = (1 - x*(1 + y))*(1 - z*x**2*(1 + 2*y))
            sage: Hfac = H.factor()
            sage: G = 1/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: print F
            (1, [(x*y + x - 1, 1), (2*x^2*y*z + x^2*z - 1, 1)])
            sage: p = {x: 1/2, z: 4/3, y: 1}
            sage: alpha = [8, 3, 3]
            sage: print F.asymptotics_multiple(p, alpha, 2, var('r'), coordinate=1) # long time
            Creating auxiliary functions...
            Computing derivatives of auxiliary functions...
            Computing derivatives of more auxiliary functions...
            Computing second-order differential operator actions...
            (1/172872*(24696*sqrt(3)*sqrt(7)/(sqrt(pi)*sqrt(r)) -
            1231*sqrt(3)*sqrt(7)/(sqrt(pi)*r^(3/2)))*108^r, 108,
            1/7*sqrt(3)*sqrt(7)/(sqrt(pi)*sqrt(r)) -
            1231/172872*sqrt(3)*sqrt(7)/(sqrt(pi)*r^(3/2)))

        ::

            sage: R.<x, y>= PolynomialRing(QQ)
            sage: H = (1 - 2*x - y) * (1 - x - 2*y)
            sage: Hfac = H.factor()
            sage: G = exp(x + y)/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: print F
            (e^(x + y), [(x + 2*y - 1, 1), (2*x + y - 1, 1)])
            sage: p = {x: 1/3, y: 1/3}
            sage: alpha = (var('a'), var('b'))
            sage: print F.asymptotics_multiple(p, alpha, 2, var('r')) # long time
            (3*((1/3)^(-b)*(1/3)^(-a))^r*e^(2/3), (1/3)^(-b)*(1/3)^(-a),
            3*e^(2/3))

        AUTHORS:

        - Alexander Raichev (2008-10-01, 2010-09-28, 2012-08-02)
        """
        from itertools import product

        R = self.ring()
        if R is None:
            return None

        # Coerce keys of p into R.
        p = FFPD.coerce_point(R, p)

        d = self.dimension()
        I = sqrt(-Integer(1))
        # Coerce everything into the Symbolic Ring.
        X = [SR(x) for x in R.gens()]
        G = SR(self.numerator())
        H = [SR(h) for (h, e) in self.denominator_factored()]
        Hprod = prod(H)
        n = len(H)
        P = dict([(SR(x), p[x]) for x in R.gens()])
        Sstar = self.crit_cone_combo(p, alpha, coordinate)

        # Put the given convenient variable at end of variable list.
        if coordinate is not None:
            x = X.pop(coordinate)
            X.append(x)
            a = alpha.pop(coordinate)
            alpha.append(a)


        # Case n = d.
        if n == d:
            det = jacobian(H, X).subs(P).determinant().abs()
            exp_scale = prod([(P[X[i]]**(-alpha[i])).subs(P)
                              for i in xrange(d)] )
            subexp_part = G.subs(P)/(det*prod(P.values()))
            if numerical:
                exp_scale = exp_scale.n(digits=numerical)
                subexp_part = subexp_part.n(digits=numerical)
            return (exp_scale**asy_var*subexp_part, exp_scale, subexp_part)

        # Case n < d.
        # If P is a tuple of rationals, then compute with it directly.
        # Otherwise, compute symbolically and plug in P at the end.
        if vector(P.values()) not in QQ**d:
            sP = [var('p' + str(j)) for j in xrange(d)]
            P = dict( [(X[j], sP[j]) for j in xrange(d)] )
            p = dict( [(sP[j], p[X[j]]) for j in xrange(d)] )

        # Setup.
        print "Creating auxiliary functions..."
        # Create T and S variables.
        t = 't'
        while t in [str(x) for x in X]:
            t = t + 't'
        T = [var(t + str(i)) for i in xrange(d - 1)]
        s = 's'
        while s in [str(x) for x in X]:
            s = s + 't'
        S = [var(s + str(i)) for i in xrange(n - 1)]
        Sstar = dict([(S[j], Sstar[j]) for j in xrange(n - 1)])
        thetastar = dict([(t, Integer(0)) for t in T])
        thetastar.update(Sstar)
        # Create implicit functions.
        h = [function('h' + str(j), *tuple(X[:d - 1])) for j in xrange(n)]
        U = function('U', *tuple(X))
        # All other functions are defined in terms of h, U, and
        # explicit functions.
        Hcheck =  prod([X[d - 1] - Integer(1)/h[j] for j in xrange(n)])
        Gcheck = -G/U * prod([-h[j]/X[d - 1] for j in xrange(n)])
        A = [(-1)**(n - 1)*X[d - 1]**(-n + j)*\
             diff(Gcheck.subs({X[d - 1]: Integer(1)/X[d - 1]}), X[d - 1], j)
             for j in xrange(n)]
        e = dict([(X[i], P[X[i]]*exp(I*T[i])) for i in xrange(d - 1)])
        ht = [hh.subs(e) for hh in h]
        Ht = [H[j].subs(e).subs({X[d - 1]: Integer(1)/ht[j]})
              for j in xrange(n)]
        hsumt = add([S[j]*ht[j] for j in xrange(n - 1)]) +\
                (Integer(1) - add(S))*ht[n - 1]
        At = [AA.subs(e).subs({X[d - 1]: hsumt}) for AA in A]
        Phit = -log(P[X[d - 1]]*hsumt) +\
               I*add([alpha[i]/alpha[d - 1]*T[i] for i in xrange(d - 1)])
        # atP Stores h and U and all their derivatives evaluated at C.
        atP = P.copy()
        atP.update(dict([(hh.subs(P), Integer(1)/P[X[d - 1]]) for hh in h]))

        # Compute the derivatives of h up to order 2*N and evaluate at P.
        hderivs1 = {}   # First derivatives of h.
        for (i, j) in mrange([d - 1, n]):
            s = solve(diff(H[j].subs({X[d - 1]: Integer(1)/h[j]}), X[i]),
                      diff(h[j], X[i]))[0].rhs().simplify()
            hderivs1.update({diff(h[j], X[i]): s})
            atP.update({diff(h[j], X[i]).subs(P): s.subs(P).subs(atP)})
        hderivs = FFPD.diff_all(h, X[0:d - 1], 2*N, sub=hderivs1, rekey=h)
        for k in hderivs.keys():
            atP.update({k.subs(P): hderivs[k].subs(atP)})

        # Compute the derivatives of U up to order 2*N - 2 + min{n, N} - 1 and
        # evaluate at P.
        # To do this, differentiate H = U*Hcheck over and over, evaluate at P,
        # and solve for the derivatives of U at P.
        # Need the derivatives of H with short keys to pass on to
        # diff_prod later.
        print "Computing derivatives of auxiliary functions..."
        m = min(n, N)
        end = [X[d-1] for j in xrange(n)]
        Hprodderivs = FFPD.diff_all(Hprod, X, 2*N - 2 + n, ending=end,
                                    sub_final=P)
        atP.update({U.subs(P): diff(Hprod, X[d - 1], n).subs(P)/factorial(n)})
        Uderivs ={}
        k = Hprod.polynomial(CC).degree() - n
        if k == 0:
            # Then we can conclude that all higher derivatives of U are zero.
            for l in xrange(1, 2*N - 2 + m):
                for s in UnorderedTuples(X, l):
                    Uderivs[diff(U, s).subs(P)] = Integer(0)
        elif k > 0 and k < 2*N - 2 + m - 1:
            all_zero = True
            Uderivs = FFPD.diff_prod(Hprodderivs, U, Hcheck, X,
                                     range(1, k + 1), end, Uderivs, atP)
            # Check for a nonzero U derivative.
            if Uderivs.values() != [Integer(0)  for i in xrange(len(Uderivs))]:
                all_zero = False
            if all_zero:
                # Then all higher derivatives of U are zero.
                for l in xrange(k + 1, 2*N - 2 + m):
                    for s in UnorderedTuples(X, l):
                        Uderivs.update({diff(U, s).subs(P): Integer(0)})
            else:
                # Have to compute the rest of the derivatives.
                Uderivs = FFPD.diff_prod(Hprodderivs, U, Hcheck, X,
                                         range(k + 1, 2*N - 2 + m), end,
                                         Uderivs, atP)
        else:
            Uderivs = FFPD.diff_prod(Hprodderivs, U, Hcheck, X,
                                     range(1, 2*N - 2 + m), end, Uderivs, atP)
        atP.update(Uderivs)
        Phit1 = jacobian(Phit, T + S).subs(hderivs1)
        a = jacobian(Phit1, T + S).subs(hderivs1).subs(thetastar).subs(atP)
        a_inv = a.inverse()
        Phitu = Phit - (Integer(1)/Integer(2))*matrix([T + S])*a*\
                matrix([T + S]).transpose()
        Phitu = Phitu[0][0]

        # Compute all partial derivatives of At and Phitu up to orders 2*N - 2
        # and 2*N, respectively.  Take advantage of the fact that At and Phitu
        # are sufficiently differentiable functions so that mixed partials
        # are equal.  Thus only need to compute representative partials.
        # Choose nondecreasing sequences as representative differentiation-
        # order sequences.
        # To speed up later computations, create symbolic functions AA and BB
        # to stand in for the expressions At and Phitu respectively.
        print "Computing derivatives of more auxiliary functions..."
        AA = [function('A' + str(j), *tuple(T + S)) for j in xrange(n)]
        At_derivs = FFPD.diff_all(At, T + S, 2*N - 2, sub=hderivs1,
                                  sub_final =[thetastar, atP], rekey=AA)
        BB = function('BB', *tuple(T + S))
        Phitu_derivs = FFPD.diff_all(Phitu, T + S, 2*N, sub=hderivs1,
                                     sub_final =[thetastar, atP], rekey=BB,
                                     zero_order=3)
        AABB_derivs = At_derivs
        AABB_derivs.update(Phitu_derivs)
        for j in xrange(n):
            AABB_derivs[AA[j]] = At[j].subs(thetastar).subs(atP)
        AABB_derivs[BB] = Phitu.subs(thetastar).subs(atP)

        print "Computing second-order differential operator actions..."
        DD = FFPD.diff_op(AA, BB, AABB_derivs, T + S, a_inv, n, N)
        L = {}
        for (j, k) in product(xrange(min(n, N)), xrange(max(0, N - 1 - n), N)):
            if j + k <= N - 1:
                L[(j, k)] = add([DD[(j, k, l)]/((-1)**k*2**(k + l)*\
                                 factorial(l)*factorial(k + l))
                                 for l in xrange(2*k + 1)])
        det = a.determinant()**(-Integer(1)/Integer(2))*\
              (2*pi)**((n - d)/Integer(2))
        chunk = det*add([
                (alpha[d - 1]*asy_var)**((n - d)/Integer(2) - q)*\
                add([L[(j, k)]*binomial(n - 1, j)*\
                     stirling_number1(n - j, n + k - q)*(-1)**(q - j - k)
                     for (j, k) in product(xrange(min(n - 1, q) + 1),               
                                           xrange(max(0, q - n), q + 1))
                     if j + k <= q])
                for q in xrange(N)])
        chunk = chunk.subs(P).simplify()
        coeffs = chunk.coefficients(asy_var)
        coeffs.reverse()
        coeffs = coeffs[:N]
        if numerical:
            subexp_part = add([co[0].subs(p).n(digits=numerical)*asy_var**co[1]
                               for co in coeffs])
            exp_scale = prod([(P[X[i]]**(-alpha[i])).subs(p)
                              for i in xrange(d)]).n(digits=numerical)
        else:
            subexp_part = add([co[0].subs(p)*asy_var**co[1] for co in coeffs])
            exp_scale = prod([(P[X[i]]**(-alpha[i])).subs(p)
                              for i in xrange(d)])
        return (exp_scale**asy_var*subexp_part, exp_scale, subexp_part)

    @staticmethod
    def subs_all(f, sub, simplify=False):
        r"""
        Return the items of $f$ substituted by the dictionaries
        of $sub$ in order of their appearance in $sub$.

        INPUT:

        - ``f`` - An individual or list of symbolic expressions or dictionaries
        - ``sub`` - An individual or list of dictionaries.
        - ``simplify`` - Boolean (default: False).

        OUTPUT:

        The items of $f$ substituted by the dictionaries of $sub$ in order of
        their appearance in $sub$.
        The subs() command is used.
        If simplify is True, then simplify() is used after substitution.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: var('x, y, z')
            (x, y, z)
            sage: a = {x:1}
            sage: b = {y:2}
            sage: c = {z:3}
            sage: FFPD.subs_all(x + y + z, a)
            y + z + 1
            sage: FFPD.subs_all(x + y + z, [c, a])
            y + 4
            sage: FFPD.subs_all([x + y + z, y^2], b)
            [x + z + 2, 4]
            sage: FFPD.subs_all([x + y + z, y^2], [b, c])
            [x + 5, 4]

        ::

            sage: var('x, y')
            (x, y)
            sage: a = {'foo': x**2 + y**2, 'bar': x - y}
            sage: b = {x: 1 , y: 2}
            sage: FFPD.subs_all(a, b)
            {'foo': 5, 'bar': -1}

        AUTHORS:

        - Alexander Raichev (2009-05-05)
        """
        singleton = False
        if not isinstance(f, list):
            f = [f]
            singleton = True
        if not isinstance(sub, list):
            sub = [sub]
        g = []
        for ff in f:
            for D in sub:
                if isinstance(ff, dict):
                    ff = dict( [(k, ff[k].subs(D)) for k in ff.keys()] )
                else:
                    ff = ff.subs(D)
            g.append(ff)
        if singleton and simplify:
            if isinstance(g[Integer(0) ], dict):
                return g[Integer(0) ]
            else:
                return g[Integer(0) ].simplify()
        elif singleton and not simplify:
            return g[Integer(0) ]
        elif not singleton and simplify:
            G = []
            for gg in g:
                if isinstance(gg, dict):
                    G.append(gg)
                else:
                    G.append(gg.simplify())
            return G
        else:
            return g

    @staticmethod
    def diff_all(f, V, n, ending=[], sub=None, sub_final=None,
                 zero_order=0, rekey=None):
        r"""
        Return a dictionary of representative mixed partial
        derivatives of $f$ from order 1 up to order $n$ with respect to the
        variables in $V$.
        The default is to key the dictionary by all nondecreasing sequences
        in $V$ of length 1 up to length $n$.
        For internal use.

        INPUT:

        - ``f`` - An individual or list of $\mathcal{C}^{n+1}$ functions.
        - ``V`` - A list of variables occurring in $f$.
        - ``n`` - A natural number.
        - ``ending`` - A list of variables in $V$.
        - ``sub`` - An individual or list of dictionaries.
        - ``sub_final`` - An individual or list of dictionaries.
        - ``rekey`` - A callable symbolic function in $V$ or list thereof.
        - ``zero_order`` - A natural number.

        OUTPUT:

        The dictionary ${s_1:deriv_1,..., s_r:deriv_r}$.
        Here $s_1,\ldots, s_r$ is a listing of
        all nondecreasing sequences of length 1 up to length $n$ over the
        alphabet $V$, where $w > v$ in $X$ iff $str(w) > str(v)$, and
        $deriv_j$ is the derivative of $f$ with respect to the derivative
        sequence $s_j$ and simplified with respect to the substitutions in
        $sub$ and evaluated at $sub_final$.
        Moreover, all derivatives with respect to sequences of length less than
        $zero_order$ (derivatives of order less than $zero_order$ )
        will be made zero.

        If $rekey$ is nonempty, then $s_1,\ldots, s_r$ will be replaced by the
        symbolic derivatives of the functions in $rekey$.

        If $ending$ is nonempty, then every derivative sequence $s_j$ will be
        suffixed by $ending$.

        EXAMPLES::

        I'd like to print the entire dictionaries, but that doesn't yield
        consistent output order for doctesting.
        Order of keys changes.::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: f = function('f', x)
            sage: dd = FFPD.diff_all(f, [x], 3)
            sage: dd[(x, x, x)]
            D[0, 0, 0](f)(x)

        ::

            sage: d1 = {diff(f, x): 4*x^3}
            sage: dd = FFPD.diff_all(f,[x], 3, sub=d1)
            sage: dd[(x, x, x)]
            24*x

        ::

            sage: dd = FFPD.diff_all(f,[x], 3, sub=d1, rekey=f)
            sage: dd[diff(f, x, 3)]
            24*x

        ::

            sage: a = {x:1}
            sage: dd = FFPD.diff_all(f,[x], 3, sub=d1, rekey=f, sub_final=a)
            sage: dd[diff(f, x, 3)]
            24

        ::

            sage: X = var('x, y, z')
            sage: f = function('f',*X)
            sage: dd = FFPD.diff_all(f, X, 2, ending=[y, y, y])
            sage: dd[(z, y, y, y)]
            D[1, 1, 1, 2](f)(x, y, z)

        ::

            sage: g = function('g',*X)
            sage: dd = FFPD.diff_all([f, g], X, 2)
            sage: dd[(0, y, z)]
            D[1, 2](f)(x, y, z)

        ::

            sage: dd[(1, z, z)]
            D[2, 2](g)(x, y, z)

        ::

            sage: f = exp(x*y*z)
            sage: ff = function('ff',*X)
            sage: dd = FFPD.diff_all(f, X, 2, rekey=ff)
            sage: dd[diff(ff, x, z)]
            x*y^2*z*e^(x*y*z) + y*e^(x*y*z)

        AUTHORS:

        - Alexander Raichev (2008-10-01, 2009-04-01, 2010-02-01)
        """
        singleton=False
        if not isinstance(f, list):
            f = [f]
            singleton=True

        # Build the dictionary of derivatives iteratively from a list
        # of nondecreasing derivative-order sequences.
        derivs = {}
        r = len(f)
        if ending:
            seeds = [ending]
            start = Integer(1)
        else:
            seeds = [[v] for v in V]
            start = Integer(2)
        if singleton:
            for s in seeds:
                derivs[tuple(s)] = FFPD.subs_all(diff(f[0], s), sub)
            for l in xrange(start, n + 1):
                for t in UnorderedTuples(V, l):
                    s = tuple(t + ending)
                    derivs[s] = FFPD.subs_all(diff(derivs[s[1:]], s[0]), sub)
        else:
            # Make the dictionary keys of the form (j, sequence of variables),
            # where j in range(r).
            for s in seeds:
                value = FFPD.subs_all([diff(f[j], s) for j in xrange(r)], sub)
                derivs.update(dict([(tuple([j]+s), value[j])
                                    for j in xrange(r)]))
            for l in xrange(start, n + 1):
                for t in UnorderedTuples(V, l):
                    s = tuple(t + ending)
                    value = FFPD.subs_all([diff(derivs[(j,) + s[1:]],
                                          s[0]) for j in xrange(r)], sub)
                    derivs.update(dict([((j,) + s, value[j])
                                        for j in xrange(r)]))
        if zero_order:
            # Zero out all the derivatives of order < zero_order
            if singleton:
                for k in derivs.keys():
                    if len(k) < zero_order:
                        derivs[k] = Integer(0)
            else:
                # Ignore the first of element of k, which is an index.
                for k in derivs.keys():
                    if len(k) - 1  < zero_order:
                        derivs[k] = Integer(0)
        if sub_final:
            # Substitute sub_final into the values of derivs.
            for k in derivs.keys():
                derivs[k] = FFPD.subs_all(derivs[k], sub_final)
        if rekey:
            # Rekey the derivs dictionary by the value of rekey.
            F = rekey
            if singleton:
                # F must be a singleton.
                derivs = dict( [(diff(F, list(k)), derivs[k])
                                for k in derivs.keys()] )
            else:
                # F must be a list.
                derivs = dict( [(diff(F[k[0]], list(k)[1:]), derivs[k])
                                for k in derivs.keys()] )
        return derivs

    @staticmethod
    def diff_op(A, B, AB_derivs, V, M, r, N):
        r"""
        Return the derivatives $DD^(l+k)(A[j] B^l)$ evaluated at a point
        $p$ for various natural numbers $j, k, l$ which depend on $r$ and $N$.
        Here $DD$ is a specific second-order linear differential operator
        that depends on $M$ , $A$ is a list of symbolic functions,
        $B$ is symbolic function, and $AB_derivs$ contains all the derivatives
        of $A$ and $B$ evaluated at $p$ that are necessary for the computation.
        For internal use by the functions asymptotics_smooth() and
        asymptotics_multiple().

        INPUT:

        - ``A`` - A single or length ``r`` list of symbolic functions in the
          variables ``V``.
        - ``B`` - A symbolic function in the variables ``V``.
        - ``AB_derivs`` - A dictionary whose keys are the (symbolic)
          derivatives of ``A[0], ..., A[r-1]`` up to order ``2*N-2`` and
          the (symbolic) derivatives of ``B`` up to order ``2*N``.
          The values of the dictionary are complex numbers that are
          the keys evaluated at a common point $p$.
        - ``V`` - The variables of the ``A[j]`` and ``B``.
        - ``M`` - A symmetric $l \times l$ matrix, where $l$ is the
          length of ``V``.
        - ``r, N`` - Natural numbers.

        OUTPUT:

        A dictionary whose keys are natural number tuples of the form
        $(j, k, l)$, where $l \le 2k$, $j \le r-1$, and $j+k \le N-1$,
        and whose values are $DD^(l+k)(A[j] B^l)$ evaluated at a point
        $p$, where $DD$ is the linear second-order differential operator
        $-\sum_{i=0}^{l-1} \sum_{j=0}^{l-1} M[i][j]
        \partial^2 /(\partial V[j] \partial V[i])$.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: T = var('x, y')
            sage: A = function('A',*tuple(T))
            sage: B = function('B',*tuple(T))
            sage: AB_derivs = {}
            sage: M = matrix([[1, 2],[2, 1]])
            sage: DD = FFPD.diff_op(A, B, AB_derivs, T, M, 1, 2)
            sage: DD.keys()
            [(0, 1, 2), (0, 1, 1), (0, 1, 0), (0, 0, 0)]
            sage: len(DD[(0, 1, 2)])
            246

        AUTHORS:

        - Alexander Raichev (2008-10-01, 2010-01-12)
        """
        if not isinstance(A, list):
            A = [A]

        # First, compute the necessary product derivatives of A and B.
        product_derivs = {}
        for (j, k) in mrange([r, N]):
            if j + k < N:
                for l in xrange(2*k + 1):
                    for s in UnorderedTuples(V, 2*(k + l)):
                        product_derivs[tuple([j, k, l] + s)] = \
                        diff(A[j]*B**l, s).subs(AB_derivs)

        # Second, compute DD^(k+l)(A[j]*B^l)(p) and store values in dictionary.
        DD = {}
        rows = M.nrows()
        for (j, k) in mrange([r, N]):
            if j + k < N:
                for l in xrange(2*k + 1):
                    # Take advantage of the symmetry of M by ignoring
                    # the upper-diagonal entries of M and multiplying by
                    # appropriate powers of 2.
                    if k + l == 0 :
                        DD[(j, k, l)] = product_derivs[(j, k, l)]
                        continue
                    S = [(a, b) for (a, b) in mrange([rows, rows]) if b <= a]
                    P =  cartesian_product_iterator([S for i in range(k+l)])
                    diffo = Integer(0)
                    for t in P:
                        if product_derivs[(j, k, l) + FFPD.diff_seq(V, t)] !=\
                          Integer(0):
                            MM = Integer(1)
                            for (a, b) in t:
                                MM = MM * M[a][b]
                                if a != b:
                                    MM = Integer(2) *MM
                            diffo = diffo + MM*product_derivs[(j, k, l) +\
                                           FFPD.diff_seq(V, t)]
                    DD[(j, k, l)] = (-Integer(1) )**(k+l)*diffo
        return DD

    @staticmethod
    def diff_seq(V, s):
        r"""
        Given a list ``s`` of tuples of natural numbers, return the
        list of elements of ``V`` with indices the elements of the elements
        of ``s``.
        This function is for internal use by the function diff_op().

        INPUT:

        - ``V`` - A list.
        - ``s`` - A list of tuples of natural numbers in the interval
          ``range(len(V))``.

        OUTPUT:

        The tuple ``tuple([V[tt] for tt in sorted(t)])``, where ``t`` is the
        list of elements of the elements of ``s``.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: V = list(var('x, t, z'))
            sage: FFPD.diff_seq(V,([0, 1],[0, 2, 1],[0, 0]))
            (x, x, x, x, t, t, z)

        AUTHORS:

        - Alexander Raichev (2009-05-19)
        """
        t = []
        for ss in s:
            t.extend(ss)
        return tuple([V[tt] for tt in sorted(t)])

    @staticmethod
    def diff_op_simple(A, B, AB_derivs, x, v, a, N):
        r"""
        Return $DD^(e k + v l)(A B^l)$ evaluated at a point $p$ for
        various natural numbers $e, k, l$ that depend on $v$ and $N$.
        Here $DD$ is a specific linear differential operator that depends
        on $a$ and $v$ , $A$ and $B$ are symbolic functions, and $AB_derivs$
        contains all the derivatives of $A$ and $B$ evaluated at $p$ that are
        necessary for the computation.
        For internal use by the function asymptotics_smooth().

        INPUT:

        - ``A, B`` - Symbolic functions in the variable ``x``.
        - ``AB_derivs`` - A dictionary whose keys are the (symbolic)
          derivatives of ``A`` up to order ``2*N`` if ``v`` is even or
          ``N`` if ``v`` is odd and the (symbolic) derivatives of ``B``
          up to order ``2*N + v`` if ``v`` is even or ``N + v``
          if ``v`` is odd.
          The values of the dictionary are complex numbers that are
          the keys evaluated at a common point $p$.
        - ``x`` - Symbolic variable.
        - ``a`` - A complex number.
        - ``v, N`` - Natural numbers.

        OUTPUT:

        A dictionary whose keys are natural number pairs of the form $(k, l)$,
        where $k < N$ and $l \le 2k$ and whose values are
        $DD^(e k + v l)(A B^l)$ evaluated at a point $p$.
        Here $e=2$ if $v$ is even, $e=1$ if $v$ is odd, and $DD$ is the
        linear differential operator
        $(a^{-1/v} d/dt)$ if $v$ is even and
        $(|a|^{-1/v} i \text{sgn}(a) d/dt)$ if $v$ is odd.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: A = function('A', x)
            sage: B = function('B', x)
            sage: AB_derivs = {}
            sage: FFPD.diff_op_simple(A, B, AB_derivs, x, 3, 2, 2)
            {(1, 0): 1/2*I*2^(2/3)*D[0](A)(x), (0, 0): A(x), (1, 1):
            1/4*(A(x)*D[0, 0, 0, 0](B)(x) + B(x)*D[0, 0, 0, 0](A)(x) +
            4*D[0](A)(x)*D[0, 0, 0](B)(x) + 4*D[0](B)(x)*D[0, 0, 0](A)(x) +
            6*D[0, 0](A)(x)*D[0, 0](B)(x))*2^(2/3)}

        AUTHORS:

        - Alexander Raichev (2010-01-15)
        """
        I = sqrt(-Integer(1))
        DD = {}
        if v.mod(Integer(2)) == Integer(0) :
            for k in xrange(N):
                for l in xrange(2*k + 1):
                    DD[(k, l)] = (a**(-Integer(1)/v))**(2*k + v*l)*\
                                 diff(A*B**l, x, 2*k + v*l).subs(AB_derivs)
        else:
            for k in xrange(N):
                for l in xrange(k + 1):
                    DD[(k, l)] = (abs(a)**(-Integer(1)/v)*I*\
                                 a/abs(a))**(k+v*l)*\
                                 diff(A*B**l, x, k + v*l).subs(AB_derivs)
        return DD

    @staticmethod
    def diff_prod(f_derivs, u, g, X, interval, end, uderivs, atc):
        r"""
        Take various derivatives of the equation $f = ug$,
        evaluate them at a point $c$, and solve for the derivatives of $u$.
        For internal use by the function asymptotics_multiple().

        INPUT:

        - ``f_derivs`` - A dictionary whose keys are all tuples of the form
          ``s + end``, where ``s`` is a sequence of variables from ``X`` whose
          length lies in ``interval``, and whose values are the derivatives
          of a function $f$ evaluated at $c$.
        - ``u`` - A callable symbolic function.
        - ``g`` - An expression or callable symbolic function.
        - ``X`` - A list of symbolic variables.
        - ``interval`` - A list of positive integers.
          Call the first and last values $n$ and $nn$, respectively.
        - ``end`` - A possibly empty list of repetitions of the
          variable ``z``, where ``z`` is the last element of ``X``.
        - ``uderivs`` - A dictionary whose keys are the symbolic
          derivatives of order 0 to order $n-1$ of ``u`` evaluated at $c$
          and whose values are the corresponding derivatives evaluated
          at $c$.
        - ``atc`` - A dictionary whose keys are the keys of $c$ and all
          the symbolic derivatives of order 0 to order $nn$ of ``g``
          evaluated $c$ and whose values are the corresponding
          derivatives evaluated at $c$.

        OUTPUT:

        A dictionary whose keys are the derivatives of ``u`` up to order
        $nn$ and whose values are those derivatives evaluated at $c$.

        EXAMPLES::

        I'd like to print out the entire dictionary, but that does not give
        consistent output for doctesting.
        Order of keys changes ::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: u = function('u', x)
            sage: g = function('g', x)
            sage: fd = {(x,):1,(x, x):1}
            sage: ud = {u(x=2): 1}
            sage: atc = {x: 2, g(x=2): 3, diff(g, x)(x=2): 5}
            sage: atc[diff(g, x, x)(x=2)] = 7
            sage: dd = FFPD.diff_prod(fd, u, g, [x], [1, 2], [], ud, atc)
            sage: dd[diff(u, x, 2)(x=2)]
            22/9

        NOTES:

        This function works by differentiating the equation $f = ug$
        with respect to the variable sequence ``s + end``,
        for all tuples ``s`` of ``X`` of lengths in ``interval``,
        evaluating at the point $c$ ,
        and solving for the remaining derivatives of ``u``.
        This function assumes that ``u`` never appears in the
        differentiations of $f = ug$ after evaluating at $c$.

        AUTHORS:

        - Alexander Raichev (2009-05-14, 2010-01-21)
        """
        for l in interval:
            D = {}
            rhs = []
            lhs = []
            for t in UnorderedTuples(X, l):
                s = t + end
                lhs.append(f_derivs[tuple(s)])
                rhs.append(diff(u*g, s).subs(atc).subs(uderivs))
                # Since Sage's solve command can't take derivatives as variable
                # names, make new variables based on t to stand in for
                # diff(u, t) and store them in D.
                D[diff(u, t).subs(atc)] = var('zing' +\
                                              ''.join([str(x) for x in t]))
            eqns = [lhs[i] == rhs[i].subs(uderivs).subs(D)
                    for i in xrange(len(lhs))]
            variables = D.values()
            sol = solve(eqns,*variables, solution_dict=True)
            uderivs.update(FFPD.subs_all(D, sol[Integer(0) ]))
        return uderivs

    def crit_cone_combo(self, p, alpha, coordinate=None):
        r"""
        Return an auxiliary point associated to the multiple
        point ``p`` of the factors ``self``.
        For internal use by asymptotics_multiple().

        INPUT:

        - ``p`` - A dictionary with keys that can be coerced to equal
          ``self.ring().gens()``.
        - ``alpha`` - A list of rationals.

        OUTPUT:

        A solution of the matrix equation $y \Gamma = \alpha'$ for $y$ ,
        where $\Gamma$ is the matrix given by
        ``[FFPD.direction(v) for v in self.log_grads(p)]`` and $\alpha'$
        is ``FFPD.direction(alpha)``

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y>= PolynomialRing(QQ)
            sage: p = exp(x)
            sage: df = [(1 - 2*x - y, 1), (1 - x - 2*y, 1)]
            sage: f = FFPD(p, df)
            sage: p = {x: 1/3, y: 1/3}
            sage: alpha = (var('a'), var('b'))
            sage: print f.crit_cone_combo(p, alpha)
            [1/3*(2*a - b)/b, -2/3*(a - 2*b)/b]

        NOTES:

        Use this function only when $\Gamma$ is well-defined and
        there is a unique solution to the matrix equation
        $y \Gamma = \alpha'$.
        Fails otherwise.

        AUTHORS:

        - Alexander Raichev (2008-10-01, 2008-11-25, 2009-03-04, 2010-09-08,
                        2010-12-02, 2012-08-02)
        """
        # Assuming here that each log_grads(f) has nonzero final component.
        # Then 'direction' will not throw a division by zero error.
        R = self.ring()
        if R is None:
            return None

        # Coerce keys of p into R.
        p = FFPD.coerce_point(R, p)

        d = self.dimension()
        n = len(self.denominator_factored())
        Gamma = matrix([FFPD.direction(v, coordinate)
                        for v in self.log_grads(p)])
        beta = FFPD.direction(alpha, coordinate)
        # solve_left() fails when working in SR :-(.
        # So use solve() instead.
        # Gamma.solve_left(vector(beta))
        V = [var('sss'+str(i)) for i in range(n)]
        M = matrix(V)*Gamma
        eqns = [M[0][j] == beta[j] for j in range(d)]
        s = solve(eqns, V, solution_dict=True)[0]  # Assume a unique solution.
        return [s[v] for v in V]

    @staticmethod
    def direction(v, coordinate=None):
        r"""
        Returns ``[vv/v[coordinate] for vv in v]`` where
        ``coordinate`` is the last index of v if not specified otherwise.

        INPUT:

        - ``v`` - A vector.
        - ``coordinate`` - (Optional; default=None) An index for ``v``.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: FFPD.direction([2, 3, 5])
            (2/5, 3/5, 1)
            sage: FFPD.direction([2, 3, 5], 0)
            (1, 3/2, 5/2)

        AUTHORS:

        - Alexander Raichev (2010-08-25)
        """
        if coordinate is None:
            coordinate = len(v) - 1
        return tuple([vv/v[coordinate] for vv in v])

    def grads(self, p):
        r"""
        Return a list of the gradients of the polynomials
        ``[q for (q, e) in self.denominator_factored()]`` evalutated at ``p``.

        INPUT:

        - ``p`` - (Optional: default=None) A dictionary whose keys are the
          generators of ``self.ring()``.


        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y>= PolynomialRing(QQ)
            sage: p = exp(x)
            sage: df = [(x**3 + 3*y^2, 5), (x*y, 2), (y, 1)]
            sage: f = FFPD(p, df)
            sage: print f
            (e^x, [(y, 1), (x*y, 2), (x^3 + 3*y^2, 5)])
            sage: print R.gens()
            (x, y)
            sage: p = None
            sage: print f.grads(p)
            [(0, 1), (y, x), (3*x^2, 6*y)]

        ::

            sage: p = {x: sqrt(2), y: var('a')}
            sage: print f.grads(p)
            [(0, 1), (a, sqrt(2)), (6, 6*a)]

        AUTHORS:

        - Alexander Raichev (2009-03-06)
        """
        R = self.ring()
        if R is None:
            return
        # Coerce keys of p into R.
        p = FFPD.coerce_point(R, p)

        X = R.gens()
        d = self.dimension()
        H = [h for (h, e) in self.denominator_factored()]
        n = len(H)
        return [tuple([diff(H[i], X[j]).subs(p) for j in xrange(d)])
                for i in xrange(n)]

    def log_grads(self, p):
        r"""
        Return a list of the logarithmic gradients of the polynomials
        ``[q for (q, e) in self.denominator_factored()]`` evalutated at ``p``.

        INPUT:

        - ``p`` - (Optional: default=None) A dictionary whose keys are the
          generators of ``self.ring()``.

        NOTE:

        The logarithmic gradient of a function $f$ at point $p$ is the vector
        $(x_1 \partial_1 f(x), \ldots, x_d \partial_d f(x) )$ evaluated at
        $p$.


        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y>= PolynomialRing(QQ)
            sage: p = exp(x)
            sage: df = [(x**3 + 3*y^2, 5), (x*y, 2), (y, 1)]
            sage: f = FFPD(p, df)
            sage: print f
            (e^x, [(y, 1), (x*y, 2), (x^3 + 3*y^2, 5)])
            sage: print R.gens()
            (x, y)
            sage: p = None
            sage: print f.log_grads(p)
            [(0, y), (x*y, x*y), (3*x^3, 6*y^2)]

        ::

            sage: p = {x: sqrt(2), y: var('a')}
            sage: print f.log_grads(p)
            [(0, a), (sqrt(2)*a, sqrt(2)*a), (6*sqrt(2), 6*a^2)]

        AUTHORS:

        - Alexander Raichev (2009-03-06)
        """
        R = self.ring()
        if R is None:
            return None

        # Coerce keys of p into R.
        p = FFPD.coerce_point(R, p)

        X = R.gens()
        d = self.dimension()
        H = [h for (h, e) in self.denominator_factored()]
        n = len(H)
        return [tuple([(X[j]*diff(H[i], X[j])).subs(p) for j in xrange(d)])
                for i in xrange(n)]

    def critical_cone(self, p, coordinate=None):
        r"""
        Return the critical cone of the convenient multiple point ``p``.

        INPUT:

        - ``p`` - A dictionary with keys that can be coerced to equal
          ``self.ring().gens()`` and values in a field.
        - ``coordinate`` - (Optional; default=None) A natural number.

        OUTPUT:

        A list of vectors that generate the critical cone of ``p`` and
        the cone itself, which is None if the values of ``p`` don't lie in QQ.
        Divide logarithmic gradients by their component ``coordinate`` entries.
        If ``coordinate=None``, then search from d-1 down to 0 for the
        first index j such that for all i ``self.log_grads()[i][j] != 0``
        and set ``coordinate=j``.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y, z>= PolynomialRing(QQ)
            sage: G = 1
            sage: H = (1 - x*(1 + y))*(1 - z*x**2*(1 + 2*y))
            sage: Hfac = H.factor()
            sage: G = 1/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: p = {x: 1/2, y: 1, z: 4/3}
            sage: print F.critical_cone(p)
            ([(2, 1, 0), (3, 1, 3/2)], 2-d cone in 3-d lattice N)

        AUTHORS:

        - Alexander Raichev (2010-08-25, 2012-08-02)
        """
        R = self.ring()
        if R is None:
            return

        # Coerce keys of p into R.
        p = FFPD.coerce_point(R, p)

        X = R.gens()
        d = self.dimension()
        lg = self.log_grads(p)
        n = len(lg)
        if coordinate not in xrange(d):
            # Search from d-1 down to 0 for a coordinate j such that
            # for all i we have lg[i][j] != 0.
            # One is guaranteed to exist in the case of a convenient multiple
            # point.
            for j in reversed(xrange(d)):
                if 0 not in [lg[i][j] for i in xrange(n)]:
                    coordinate = j
                    break
        Gamma = [FFPD.direction(v, coordinate) for v in lg]
        try:
            cone = Cone(Gamma)
        except TypeError:
            cone = None
        return (Gamma, cone)

    def is_convenient_multiple_point(self, p):
        r"""
        Return True if ``p`` is a convenient multiple point of ``self`` and
        False otherwise.
        Also return a short comment.

        INPUT:

        - ``p`` - A dictionary with keys that can be coerced to equal
          ``self.ring().gens()``.

        OUTPUT:

        A pair (verdict, comment).
        In case ``p`` is a convenient multiple point, verdict=True and
        comment ='No problem'.
        In case ``p`` is not, verdict=False and comment is string explaining
        why ``p`` fails to be a convenient multiple point.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y, z>= PolynomialRing(QQ)
            sage: H = (1 - x*(1 + y))*(1 - z*x**2*(1 + 2*y))
            sage: df = H.factor()
            sage: G = 1/df.unit()
            sage: F = FFPD(G, df)
            sage: p1 = {x: 1/2, y: 1, z: 4/3}
            sage: p2 = {x: 1, y: 2, z: 1/2}
            sage: print F.is_convenient_multiple_point(p1)
            (True, 'convenient in variables [x, y]')
            sage: print F.is_convenient_multiple_point(p2)
            (False, 'not a singular point')

        NOTES:

        See [RaWi2012]_ for more details.

        AUTHORS:

        - Alexander Raichev (2011-04-18, 2012-08-02)
        """
        R = self.ring()
        if R is None:
            return

        # Coerce keys of p into R.
        p = FFPD.coerce_point(R, p)

        H = [h for (h, e) in self.denominator_factored()]
        n = len(H)
        d = self.dimension()

        # Test 1: Are the factors in H zero at p?
        if [h.subs(p) for h in H] != [0 for h in H]:
            # Failed test 1.  Move on to next point.
            return (False, 'not a singular point')

        # Test 2: Are the factors in H smooth at p?
        grads = self.grads(p)
        for v in grads:
            if v == [0 for i in xrange(d)]:
                return (False, 'not smooth point of factors')

        # Test 3: Do the factors in H intersect transversely at p?
        if n <= d:
            M = matrix(grads)
            if M.rank() != n:
                return (False, 'not a transverse intersection')
        else:
            # Check all sub-multisets of grads of size d.
            for S in Subsets(grads, d, submultiset=True):
                M = matrix(S)
                if M.rank() != d:
                    return (False, 'not a transverse intersection')

        # Test 4: Is p convenient?
        M = matrix(self.log_grads(p))
        convenient_coordinates = []
        for j in xrange(d):
            if 0 not in M.columns()[j]:
                convenient_coordinates.append(j)
        if not convenient_coordinates:
            return (False, 'multiple point but not convenient')

        # Tests all passed
        X = R.gens()
        return (True, 'convenient in variables %s' %\
                [X[i] for i in convenient_coordinates])

    def singular_ideal(self):
        r"""
        Let $R$ be the ring of ``self`` and $H$ its denominator.
        Let $Hred$ be the reduction (square-free part) of $H$.
        Return the ideal in $R$ generated by $Hred$ and
        its partial derivatives.
        If the coefficient field of $R$ is algebraically closed,
        then the output is the ideal of the singular locus (which is a variety)
        of the variety of $H$.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y, z>= PolynomialRing(QQ)
            sage: H = (1 - x*(1 + y))**3*(1 - z*x**2*(1 + 2*y))
            sage: df = H.factor()
            sage: G = 1/df.unit()
            sage: F = FFPD(G, df)
            sage: F.singular_ideal()
            Ideal (x*y + x - 1, y^2 - 2*y*z + 2*y - z + 1, x*z + y - 2*z + 1)
            of Multivariate Polynomial Ring in x, y, z over Rational Field

        AUTHORS:

        - Alexander Raichev (2008-10-01, 2008-11-20, 2010-12-03, 2011-04-18,
                        2012-08-03)
        """
        R = self.ring()
        if R is None:
            return

        Hred = prod([h for (h, e) in self.denominator_factored()])
        J = R.ideal([Hred] + Hred.gradient())
        return R.ideal(J.groebner_basis())

    def smooth_critical_ideal(self, alpha):
        r"""
        Let $R$ be the ring of ``self`` and $H$ its denominator.
        Return the ideal in $R$ of smooth critical points of the variety
        of $H$ for the direction ``alpha``.
        If the variety $V$ of $H$ has no smooth points, then return the ideal
        in $R$ of $V$.

        INPUT:

        - ``alpha`` - A d-tuple of positive integers and/or symbolic entries,
          where d = ``self.ring().ngens()``.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y> = PolynomialRing(QQ)
            sage: H = (1-x-y-x*y)^2
            sage: Hfac = H.factor()
            sage: G = 1/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: alpha = var('a1, a2')
            sage: F.smooth_critical_ideal(alpha)
            Ideal (y^2 + 2*a1/a2*y - 1, x + (a2/(-a1))*y + (-a2 + a1)/(-a1)) of Multivariate Polynomial Ring in x, y over Fraction Field of Multivariate Polynomial Ring in a2, a1 over Rational Field        
        
        ::

            sage: R.<x, y> = PolynomialRing(QQ)
            sage: H = (1-x-y-x*y)^2
            sage: Hfac = H.factor()
            sage: G = 1/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: alpha = [7/3, var('a')]
            sage: F.smooth_critical_ideal(alpha)
            Ideal (y^2 + (-14/(-3*a))*y - 1, x + (-3/7*a)*y + 3/7*a - 1) of
            Multivariate Polynomial Ring in x, y over Fraction Field of
            Univariate Polynomial Ring in a over Rational Field

        NOTES:

        See [RaWi2012]_ for more details.

        AUTHORS:

        - Alexander Raichev (2008-10-01, 2008-11-20, 2009-03-09, 2010-12-02,
                        2011-04-18, 2012-08-03)
        """
        R = self.ring()
        if R is None:
            return

        Hred = prod([h for (h, e) in self.denominator_factored()])
        K = R.base_ring()
        d = self.dimension()

        # Expand K by the variables of alpha if there are any.
        indets = []
        for a in alpha:
            if a not in K and a in SR:
                indets.append(a)
        indets = list(Set(indets))   # Delete duplicates in indets.
        if indets:
            L = FractionField(PolynomialRing(K, indets))
            S = R.change_ring(L)
            # Coerce alpha into L.
            alpha = [L(a) for a in alpha]
        else:
            S = R

        # Find smooth, critical points for alpha.
        X = S.gens()
        Hred = S(Hred)
        J = S.ideal([Hred] +\
            [alpha[d - 1]*X[i]*diff(Hred, X[i]) -\
             alpha[i]*X[d - 1]*diff(Hred, X[d - 1])
             for i in xrange(d - 1)])
        return S.ideal(J.groebner_basis())

    def maclaurin_coefficients(self, multi_indices, numerical=0):
        r"""
        Returns the Maclaurin coefficients of self that have multi-indices
        in ``multi_indices``.
        
        INPUT:

        - ``multi_indices`` - A list of tuples of positive integers, where
          each tuple has length ``self.dimension()``.
        - ``numerical`` - (Optional; default=0) A natural number.
          If positive, return numerical
          approximations of coefficients with ``numerical`` digits of
          accuracy.

        OUTPUT:

        A dictionary of the form
        (nu, Maclaurin coefficient of index nu of self).

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x> = PolynomialRing(QQ)
            sage: H = 2 - 3*x 
            sage: Hfac = H.factor()
            sage: G = 1/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: print F
            (-1/3, [(x - 2/3, 1)])
            sage: print F.maclaurin_coefficients([(2*k,) for k in range(6)])
            {(0,): 1/2, (2,): 9/8, (8,): 6561/512, (4,): 81/32, (10,): 59049/2048, (6,): 729/128}
            
        ::
        
            sage: R.<x, y, z> = PolynomialRing(QQ)
            sage: H = (4 - 2*x - y - z) * (4 - x - 2*y - z)
            sage: Hfac = H.factor()
            sage: G = 16/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: alpha = vector([3, 3, 2])
            sage: interval = [1, 2, 4]
            sage: S = [r*alpha for r in interval]
            sage: print F.maclaurin_coefficients(S, numerical=10)
            {(6, 6, 4): 0.7005249476, (12, 12, 8): 0.5847732654,
            (3, 3, 2): 0.7849731445}

        NOTES:

        Uses iterated univariate Maclaurin expansions.
        Slow.

        AUTHORS:

        - Alexander Raichev (2011-04-08, 2012-08-03)
        """
        R = self.ring()
        if R is None:
           return

        d = self.dimension()
        coeffs = {}

        # Deal with the simple univariate case first.
        if d == 1:
            f = SR(self.quotient())
            x = SR(R.gens()[0])
            m = max(multi_indices)[0]
            f = f.taylor(x, 0, m)
            F = R(f)
            tmp = F.coefficients()
            for nu in multi_indices:
                val = tmp[nu[0]]
                if numerical:
                    val = val.n(digits=numerical)
                coeffs[tuple(nu)] = val            
            return coeffs                

        # Create biggest multi-index needed.
        alpha = []
        for i in xrange(d):
           alpha.append(max((nu[i] for nu in multi_indices)))

        # Compute Maclaurin expansion of self up to index alpha.
        # Use iterated univariate expansions.
        # Slow!
        f = SR(self.quotient())
        X = [SR(x) for x in R.gens()]
        for i in xrange(d):
           f = f.taylor(X[i], 0, alpha[i])
        F = R(f)

        # Collect coefficients.
        X = R.gens()
        for nu in multi_indices:
            monomial = prod([X[i]**nu[i] for i in xrange(d)])
            val = F.monomial_coefficient(monomial)
            if numerical:
                val = val.n(digits=numerical) 
            coeffs[tuple(nu)] = val
        return coeffs

    def relative_error(self, approx, alpha, interval, exp_scale=Integer(1),
                       digits=10):
        r"""
        Returns the relative error between the values of the Maclaurin
        coefficients of ``self`` with multi-indices ``r alpha`` for ``r`` in
        ``interval`` and the values of the functions (of the variable ``r``)
        in ``approx``.

        INPUT:

        - ``approx`` - An individual or list of symbolic expressions in
          one variable.
        - ``alpha`` - A list of positive integers of length
          ``self.ring().ngens()``
        - ``interval`` - A list of positive integers.
        - ``exp_scale`` - (Optional; default=1) A number.

        OUTPUT:

        A list whose entries are of the form
        ``[r*alpha, a_r, b_r, err_r]`` for ``r`` in ``interval``.
        Here ``r*alpha`` is a tuple; ``a_r`` is the ``r*alpha`` (multi-index)
        coefficient of the Maclaurin series for ``self`` divided by
        ``exp_scale**r``;
        ``b_r`` is a list of the values of the functions in ``approx``
        evaluated at ``r`` and divided by ``exp_scale**m``;
        ``err_r`` is the list of relative errors
        ``(a_r - f)/a_r`` for ``f`` in ``b_r``.
        All outputs are decimal approximations.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y>= PolynomialRing(QQ)
            sage: H = 1 - x - y - x*y
            sage: Hfac = H.factor()
            sage: G = 1/Hfac.unit()
            sage: F = FFPD(G, Hfac)
            sage: alpha = [1, 1]
            sage: r = var('r')
            sage: a1 = (0.573/sqrt(r))*5.83^r
            sage: a2 = (0.573/sqrt(r) - 0.0674/r^(3/2))*5.83^r
            sage: es = 5.83
            sage: F.relative_error([a1, a2], alpha, [1, 2, 4, 8], es) # long time
            Calculating errors table in the form
            exponent, scaled Maclaurin coefficient, scaled asymptotic values,
            relative errors...
            [((1, 1), 0.5145797599, [0.5730000000, 0.5056000000],
            [-0.1135300000, 0.01745066667]), ((2, 2), 0.3824778089,
            [0.4051721856, 0.3813426871], [-0.05933514614, 0.002967810973]),
            ((4, 4), 0.2778630595, [0.2865000000, 0.2780750000],
            [-0.03108344267, -0.0007627515584]), ((8, 8), 0.1991088276,
            [0.2025860928, 0.1996074055], [-0.01746414394, -0.002504047242])]

        AUTHORS:

        - Alexander Raichev (2009-05-18, 2011-04-18, 2012-08-03)
        """

        if not isinstance(approx, list):
            approx = [approx]
        av = approx[0].variables()[0]

        print "Calculating errors table in the form"
        print "exponent, scaled Maclaurin coefficient, scaled asymptotic values, relative errors..."

        # Get Maclaurin coefficients of self.
        multi_indices = [r*vector(alpha) for r in interval]
        mac = self.maclaurin_coefficients(multi_indices, numerical=digits)
        #mac = self.old_maclaurin_coefficients(alpha, max(interval))
        mac_approx = {}
        stats = []
        for r in interval:
            beta = tuple(r*vector(alpha))
            mac[beta] = (mac[beta]/exp_scale**r).n(digits=digits)
            mac_approx[beta] = [(f.subs({av:r})/exp_scale**r).n(digits=digits)
                                for f in approx]
            stats_row = [beta, mac[beta], mac_approx[beta]]
            if mac[beta] == 0:
                 stats_row.extend([None for a in mac_approx[beta]])
            else:
                 stats_row.append([(mac[beta] - a)/mac[beta]
                                   for a in mac_approx[beta]])
            stats.append(tuple(stats_row))
        return stats

    @staticmethod
    def coerce_point(R, p):
        r"""
        Coerce the keys of the dictionary ``p`` into the ring ``R``.

        Assume that it is possible.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x,y> = PolynomialRing(QQ)
            sage: f = FFPD()
            sage: p = {SR(x): 1, SR(y): 7/8}
            sage: print p
            {y: 7/8, x: 1}
            sage: for k in p.keys():
            ...       print k, k.parent()
            ...
            y Symbolic Ring
            x Symbolic Ring
            sage: q = f.coerce_point(R, p)
            sage: print q
            {y: 7/8, x: 1}
            sage: for k in q.keys():
            ...       print k, k.parent()
            ...
            y Multivariate Polynomial Ring in x, y over Rational Field
            x Multivariate Polynomial Ring in x, y over Rational Field
            
        
        AUTHORS:

        - Alexander Raichev (2009-05-18, 2011-04-18, 2012-08-03)
        """
        result = p
        if p is not None and p.keys() and p.keys()[0].parent() != R:
            try:
                result = dict([(x, p[SR(x)]) for x in R.gens()])
            except TypeError:
                pass
        return result


class FFPDSum(list):
    r"""
    A list representing the sum of FFPD objects with distinct
    denominator factorizations.

    AUTHORS:

    - Alexander Raichev (2012-06-25)
    """
    def __str__(self):
        r"""
        Returns a string representation of ``self``

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x,y> = PolynomialRing(QQ)
            sage: f = FFPD(x + y, [(y, 1), (x, 1)])
            sage: g = FFPD(x**2 + y, [(y, 1), (x, 2)])
            sage: print FFPDSum([f, g])
            [(x + y, [(y, 1), (x, 1)]), (x^2 + y, [(y, 1), (x, 2)])]
            
        """
        return str([r.list() for r in self])

    def __eq__(self, other):
        r"""
        Returns True if ``self`` is equal to ``other``

        EXAMPLES::
        
            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x,y> = PolynomialRing(QQ)
            sage: f = FFPD(x + y, [(y, 1), (x, 1)])
            sage: g = FFPD(x*(x + y), [(y, 1), (x, 2)])
            sage: s = FFPDSum([f])
            sage: t = FFPDSum([g])
            sage: print s, t
            [(x + y, [(y, 1), (x, 1)])] [(x + y, [(y, 1), (x, 1)])]
            sage: print s == t
            True

        """
        return sorted(self) == sorted(other)

    def __ne__(self, other):
        r"""
        Returns True if ``self`` is not equal to ``other``

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x,y> = PolynomialRing(QQ)
            sage: f = FFPD(x + y, [(y, 1), (x, 1)])
            sage: g = FFPD(x + y, [(y, 1), (x, 2)])
            sage: s = FFPDSum([f])
            sage: t = FFPDSum([g])
            sage: print s, t
            [(x + y, [(y, 1), (x, 1)])] [(x + y, [(y, 1), (x, 2)])]
            sage: print s != t
            True
            
        """
        return not (self == other)

    def ring(self):
        r"""
        Return the polynomial ring of the denominators of ``self``.

        If ``self`` does not have any denominators, then return None.

        EXAMPLES::
            
            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x,y> = PolynomialRing(QQ)
            sage: f = FFPD(x + y, [(y, 1), (x, 1)])
            sage: s = FFPDSum([f])
            sage: print s.ring()
            Multivariate Polynomial Ring in x, y over Rational Field
            sage: g = FFPD(x + y, [])
            sage: t = FFPDSum([g])
            sage: print t.ring()
            None

        """
        for r in self:
            R = r.ring()
            if R is not None:
                return R
        return None

    def whole_and_parts(self):
        r"""
        Rewrite ``self`` as a FFPDSum of a (possibly zero) polynomial
        FFPD followed by reduced rational expression FFPDs.

        Only useful for multivariate decompositions.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y> = PolynomialRing(QQ, 'x, y')
            sage: f = x**2 + 3*y + 1/x + 1/y
            sage: f = FFPD(quotient=f)
            sage: print f
            (x^3*y + 3*x*y^2 + x + y, [(y, 1), (x, 1)])
            sage: print FFPDSum([f]).whole_and_parts()
            [(x^2 + 3*y, []), (x + y, [(y, 1), (x, 1)])]

        ::

            sage: R.<x, y> = PolynomialRing(QQ)
            sage: f = cos(x)**2 + 3*y + 1/x + 1/y
            sage: print f
            1/x + 1/y + cos(x)^2 + 3*y
            sage: G = f.numerator()
            sage: H = R(f.denominator())
            sage: f = FFPD(G, H.factor())
            sage: print f
            (x*y*cos(x)^2 + 3*x*y^2 + x + y, [(y, 1), (x, 1)])
            sage: print FFPDSum([f]).whole_and_parts()
            [(0, []), (x*y*cos(x)^2 + 3*x*y^2 + x + y, [(y, 1), (x, 1)])]
        """
        whole = 0
        parts = []
        R = self.ring()
        for r in self:
            # Since r has already passed through FFPD.__init__()'s reducing
            # procedure, r is already in lowest terms.
            # Check if can write r as a mixed fraction: whole + fraction.
            p = r.numerator()
            q = r.denominator()
            if q == 1:
                # r is already whole
                whole += p
            else:
                try:
                    # Coerce p into R and divide p by q
                    p = R(p)
                    a, b = p.quo_rem(q)
                except TypeError:
                    # p is not in R and so can't divide p by q
                    a = 0
                    b = p
                whole += a
                parts.append(FFPD(b, r.denominator_factored(), reduce_=False))
        return FFPDSum([FFPD(whole, ())] + parts)

    def combine_like_terms(self):
        r"""
        Combine terms in ``self`` with the same denominator.
        Only useful for multivariate decompositions.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y>= PolynomialRing(QQ)
            sage: f = FFPD(quotient=1/(x * y * (x*y + 1)))
            sage: g = FFPD(quotient=x/(x * y * (x*y + 1)))
            sage: s = FFPDSum([f, g, f])
            sage: t = s.combine_like_terms()
            sage: print s
            [(1, [(y, 1), (x, 1), (x*y + 1, 1)]), (1, [(y, 1), (x*y + 1, 1)]),
            (1, [(y, 1), (x, 1), (x*y + 1, 1)])]
            sage: print t
            [(1, [(y, 1), (x*y + 1, 1)]), (2, [(y, 1), (x, 1), (x*y + 1, 1)])]

        ::

            sage: R.<x, y>= PolynomialRing(QQ)
            sage: H = x * y * (x*y + 1)
            sage: f = FFPD(1, H.factor())
            sage: g = FFPD(exp(x + y), H.factor())
            sage: s = FFPDSum([f, g])
            sage: print s
            [(1, [(y, 1), (x, 1), (x*y + 1, 1)]), (e^(x + y), [(y, 1), (x, 1),
            (x*y + 1, 1)])]
            sage: t = s.combine_like_terms()
            sage: print t
            [(e^(x + y) + 1, [(y, 1), (x, 1), (x*y + 1, 1)])]
        """
        if not self:
            return self

        # Combine like terms.
        FFPDs = sorted(self)
        new_FFPDs = []
        temp = FFPDs[0]
        for f in FFPDs[1:]:
            if  temp.denominator_factored() == f.denominator_factored():
                # Add f to temp.
                num = temp.numerator() + f.numerator()
                temp = FFPD(num, temp.denominator_factored())
            else:
                # Append temp to new_FFPDs and update temp.
                new_FFPDs.append(temp)
                temp = f
        new_FFPDs.append(temp)
        return FFPDSum(new_FFPDs)

    def sum(self):
        r"""
        Return the sum of the FFPDs in ``self`` as a FFPD.

        EXAMPLES::

            sage: from sage.combinat.asymptotics_multivariate_generating_functions import *
            sage: R.<x, y> = PolynomialRing(QQ)
            sage: df = (x, 1), (y, 1), (x*y + 1, 1)
            sage: f = FFPD(2, df)
            sage: g = FFPD(2*x*y, df)
            sage: print FFPDSum([f, g])
            [(2, [(y, 1), (x, 1), (x*y + 1, 1)]), (2, [(x*y + 1, 1)])]
            sage: print FFPDSum([f, g]).sum()
            (2, [(y, 1), (x, 1)])

        ::

            sage: R.<x, y> = PolynomialRing(QQ)
            sage: f = FFPD(cos(x), [(x, 2)])
            sage: g = FFPD(cos(y), [(x, 1), (y, 2)])
            sage: print FFPDSum([f, g])
            [(cos(x), [(x, 2)]), (cos(y), [(y, 2), (x, 1)])]
            sage: print FFPDSum([f, g]).sum()
            (y^2*cos(x) + x*cos(y), [(y, 2), (x, 2)])


        """
        if not self:
            return self

        # Compute the sum's numerator and denominator.
        R = self.ring()
        summy = sum((f.quotient() for f in self))
        numer = summy.numerator()
        denom = R(summy.denominator())

        # Compute the sum's denominator factorization.
        # Could use the factor() command, but it's probably faster to use
        # the irreducible factors of the denominators of self.
        df = [] # The denominator factorization for the sum.
        if denom == 1:
            # Done
            return FFPD(numer, df, reduce_=False)

        factors = []
        for f in self:
            factors.extend([q for (q, e) in f.denominator_factored()])

        # Eliminate repeats from factors and sort.
        factors = sorted(list(set(factors)))

        # The irreducible factors of denom lie in factors.
        # Use this fact to build df.
        for q in factors:
            e = 0
            quo, rem = denom.quo_rem(q)
            while rem == 0:
                e += 1
                denom = quo
                quo, rem = denom.quo_rem(q)
            if e > 0:
                df.append((q, e))
        return FFPD(numer, df, reduce_=False)