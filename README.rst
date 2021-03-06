amgf
====
**Update**: On 2016-02-17 this work and added improvements were incorporated into the Sage codebase, then released in Sage version 7.1. So use Sage 7.1 or later instead of this repository.  Thanks to all the contributors!

Let :math:`F(x) = \sum_{\nu \in \NN^d} F_{\nu} x^\nu` be a multivariate power series with complex coefficients that converges in a neighborhood of the origin. Assume that :math:`F = G/H` for some functions :math:`G` and :math:`H` holomorphic in a neighborhood of the origin.
Assume also that :math:`H` is a polynomial.

This Python 2.7 module for use within `Sage <http://www.sagemath.org>`_ computes asymptotics for the coefficients :math:`F_{r \alpha}` as :math:`r \to \infty` with :math:`r \alpha \in \NN^d` for :math:`\alpha` in a permissible subset of :math:`d`-tuples of positive reals.
More specifically, it computes arbitrary terms of the asymptotic expansion for :math:`F_{r \alpha}` when the asymptotics are controlled by a strictly minimal multiple point of the alegbraic variety :math:`H = 0`.

The algorithms and formulas implemented here come from [RaWi2008a]_
and [RaWi2012]_.

``amgf-0.8.py`` has also been submitted to the Sage Trac server as ``trac_10519-v7.patch`` on `ticket 10519 <http://trac.sagemath.org/sage_trac/ticket/10519>`_ for incorporation into the Sage code base.
You are welcome to review the patch. 

Main Files
--------------
- amgf-0.8.py, Python source file (version date 8 October 2012)
- amgf-0.8_examples.sws, Sage worksheet of examples
- docs/amgf-0.8.pdf, documentation
- trac_10519-v7.patch, Sage patch

Installation
-------------
You can install the code as a Sage patch file, a process that's a bit technical and described `here <http://ask.sagemath.org/question/1276/how-to-install-patches-or-should-we>`_.
Alternatively, you can import amgf-0.8.py as a module in a Sage notebook session as follows.

#. Download and install the latest version of Sage from `here <http://sagemath.org>`_.
#. Download amgf-0.8.py, amgf-0.8_examples, and amgf-0.8.pdf.
#. Run Sage and open a Sage notebook window. (Type 'notebook()' if you are running Sage from the command line.)
#. Upload amgf-0.8_examples.sws into your Sage notebook.
#. Open the worksheet, customize the first cell to point to the location of your copy of amgf-0.8.py, and modify the examples to your liking.


.. [RaWi2008a] Alexander Raichev and Mark C. Wilson, "Asymptotics of coefficients of multivariate generating functions: improvements for smooth points", Electronic Journal of Combinatorics, Vol. 15 (2008), R89, `<http://arxiv.org/pdf/0803.2914.pdf>`_.

.. [RaWi2012] Alexander Raichev and Mark C. Wilson, "Asymptotics of coefficients of multivariate generating functions: improvements for smooth points", To appear in 2012 in the Online Journal of Analytic Combinatorics, `<http://arxiv.org/pdf/1009.5715.pdf>`_.
