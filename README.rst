amgf
====
Let $F(x) = \sum_{\nu \in \NN^d} F_{\nu} x^\nu$ be a multivariate power series with complex coefficients that converges in a neighborhood of the origin. Assume that $F = G/H$ for some functions $G$ and $H$ holomorphic in a neighborhood of the origin.
Assume also that $H$ is a polynomial.

This Python module for use within `Sage <http://www.sagemath.org>`_ computes asymptotics for the coefficients $F_{r \alpha}$ as $r \to \infty$ with $r \alpha \in \NN^d$ for $\alpha$ in a permissible subset of $d$-tuples of positive reals.
More specifically, it computes arbitrary terms of the asymptotic expansion for $F_{r \alpha}$ when the asymptotics are controlled by a strictly minimal multiple point of the alegbraic variety $H = 0$.

The algorithms and formulas implemented here come from [RaWi2008a]_
and [RaWi2012]_.

.. [RaWi2008a] Alexander Raichev and Mark C. Wilson, "Asymptotics of coefficients of multivariate generating functions: improvements for smooth points", Electronic Journal of Combinatorics, Vol. 15 (2008), R89, `<http://arxiv.org/pdf/0803.2914.pdf>`_.

.. [RaWi2012] Alexander Raichev and Mark C. Wilson, "Asymptotics of coefficients of multivariate generating functions: improvements for smooth points", To appear in 2012 in the Online Journal of Analytic Combinatorics, `<http://arxiv.org/pdf/1009.5715.pdf>`_.

