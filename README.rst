amgf
====
Let :math:`F(x) = \sum_{\nu \in \NN^d} F_{\nu} x^\nu` be a multivariate power series with complex coefficients that converges in a neighborhood of the origin. Assume that :math:`F = G/H` for some functions :math:`G` and :math:`H` holomorphic in a neighborhood of the origin.
Assume also that :math:`H` is a polynomial.

This Python 2.7 module for use within `Sage <http://www.sagemath.org>`_ computes asymptotics for the coefficients :math:`F_{r \alpha}` as :math:`r \to \infty` with :math:`r \alpha \in \NN^d` for :math:`\alpha` in a permissible subset of :math:`d`-tuples of positive reals.
More specifically, it computes arbitrary terms of the asymptotic expansion for :math:`F_{r \alpha}` when the asymptotics are controlled by a strictly minimal multiple point of the alegbraic variety :math:`H = 0`.

The algorithms and formulas implemented here come from [RaWi2008a]_
and [RaWi2012]_.

For more detailed information, see the latest PDF file in the docs.
For examples, see the latest Sage worksheet (SWS) file in this directory.

``amgf-0.8.py`` has also been submitted to the Sage Trac server as `ticket/patch 10519 <http://trac.sagemath.org/sage_trac/ticket/10519>`_ for incorporation into the Sage code base.
You are welcome to review the patch. 

.. [RaWi2008a] Alexander Raichev and Mark C. Wilson, "Asymptotics of coefficients of multivariate generating functions: improvements for smooth points", Electronic Journal of Combinatorics, Vol. 15 (2008), R89, `<http://arxiv.org/pdf/0803.2914.pdf>`_.

.. [RaWi2012] Alexander Raichev and Mark C. Wilson, "Asymptotics of coefficients of multivariate generating functions: improvements for smooth points", To appear in 2012 in the Online Journal of Analytic Combinatorics, `<http://arxiv.org/pdf/1009.5715.pdf>`_.