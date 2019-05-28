Using it with PuLP
**************************

.. highlight:: python

Nomenclature
=========================

.. glossary::

   Variable declaration
      A variable declaration is the creation of a group of decision variables that share the same naming and significance. In `PuLP` they are all created within a single call to :py:meth:`pulp.LpVariable.dicts` and they are all accessed by slicing the same `python` variable created. An optimization problem can have one variable declaration but thousands of variables.

   Variable domain
   	  The complete space over which variables are created. The length of the domain
   	  is the number of variables. Each variable declaration has its own domain
   	  and is indicated with the argument `index` when calling the function :py:meth:`pulp.LpVariable.dicts`. It usually consists of some kind of iterator where all its elements should be unique.

.. source directory
..   The directory which, including its subdirectories, contains all
..   source files for one Sphinx project.

When using :py:mod:`pulp`, I use the following guidelines for variable declaration:

1. Use :py:meth:`pulp.LpVariable.dicts`, unless there is a very good reason not to.
2. Use python lists for variable domains.
3. Use `pytups` to index parts of the domain for constraint generation.


Example: Scheduling problem
=============================

Assume we are given a set of jobs :math:`j` with processing times :math:`p_j`. For a single machine non-preemptive scheduling problem (which we assume here), a schedule of the jobs :math:`N` is given by specifying a start time, :math:`Y_j` , for each job. If job j starts at time :math:`Y_j`, it is processing during the time interval :math:`[Y_j , Y_j + p_j ]`. A schedule is feasible if no two jobs have overlapping processing times.

This means that, for every pair of jobs :math:`i` and :math:`j`, we have that either :math:`Y_j \geq Y_i +p_i` , or :math:`Y_i \geq Y_j +p_j`.

Job :math:`j` will complete at time :math:`C_j =(Y_j + p_j )`, and if it also has an associated due date, :math:`d_j` , its tardiness, :math:`T_j` , is defined to be:

.. math::
   :nowrap:

   \begin{eqnarray}
      T_j    & = & (C_j - d_j)^+ \\
      T_j    & = & (Y_j + p_j - d_j)^+
   \end{eqnarray}

If we are given a set of weights, :math:`w_j` , which indicate a relative importance between individual jobs, we can calculate the total weighted tardiness of a given feasible schedule:

.. math::
   :nowrap:

   \begin{eqnarray}
      TWT    & = & \sum_{j \in N} w_j T_j \\
      TWT    & = & \sum_{j \in N} w_j (Y_j + p_j - d_j)^+
   \end{eqnarray}

The objective is to schedule all the jobs without overlapping them and minimizing the total weighted tardiness :math:`TWT`.

Example: formulation
===================================

SETS
      					
======================================  ====================================
:math:`j \in J`		                     jobs
:math:`k \in K = \{1, ..., C_{max}\}`   	time periods
======================================  ====================================

DATA [UNITS]
     					
================ ====================================================
:math:`p_j`			processing time of job j [time periods]
:math:`d_j`  		due date of job j [time period]
:math:`w_j`			weight or priority of job j [dimensionless]
================ ====================================================


DERIVED DATA
   					
=================	===================================================================================================
:math:`C_{max}`		Size of planning horizon.
:math:`JK`  		Al possible starting periods (j, k) for job :math:`j \in J` in time periods :math:`k \in K`.
:math:`K_j`  		Al possible starting periods k for job :math:`j \in J`.
:math:`t_{jk}` 		Penalty for starting job :math:`j \in J` in time period :math:`k \in K`.
:math:`K2_{jk}`		All affected time periods :math:`k2 \in K2` when starting a job :math:`j` in time period :math:`k \in K`.
:math:`JK_{k2}` 	All possible starts of jobs :math:`(j, k) \in JK` that affect the availability of time period :math:`k2 \in K`.
=================	===================================================================================================

.. math::
   :nowrap:

   \begin{eqnarray}
      &C_{max} 	&= &\sum_{j \in J} p_j \\
      &JK 		&= &\{(j \in J, k \in K) \mid k + p_j \leq C_{max} \} \\
      &K_j 		&= &\{k \in K \mid (j, k) \in JK \} & j \in J \\
      &K2_{jk} 	&= &\{k \in K \mid k \leq k2 \leq k + p_j \} & (j, k) \in JK \\
      &JK_{k2} 	&= &\{(j, k) \in JK \mid k_2 \in K2_{jk} \} & k_2 \in K \\
      &t_{jk} 	&= &\max\{k + p_j - d_j, 0\} \times w_j & (j, k) \in JK \\
   \end{eqnarray}

DECISION VARIABLES

:math:`X_{jk}`. Binary. 1 if job :math:`j` starts at time slot :math:`k`, 0 otherwise. :math:`(j, k) \in JK`

FORMULATION

.. math::
   :nowrap:

   \begin{eqnarray}
      \min \sum_{(j, k) \in JK} t_{jk} X_{jk} \\
   \end{eqnarray}

Subject to:

.. math::
   :nowrap:

   \begin{eqnarray}
      & \sum_{k \in K_j} X_{jk} = 1 & j \in J \\
      & \sum_{(j, k) \in JK_{k2}} X_{jk} = 1 & k2 \in K \\
   \end{eqnarray}


Example: implementation
========================================

We import libraries and get input data.

.. literalinclude:: ./../../examples/machine_scheduling.py
   :lines: 1-8

We then calculate intermediate sets and parameters. Note the use of pytups functions to filter and convert from tuple lists to dictionaries.

.. literalinclude:: ./../../examples/machine_scheduling.py
   :lines: 9-38

We now create the PuLP model and solve it.

.. literalinclude:: ./../../examples/machine_scheduling.py
   :lines: 39-58

We get the solution from the variable contents. Not how we also use pytups to extract the content from the variable.

.. literalinclude:: ./../../examples/machine_scheduling.py
   :lines: 60-68

Finally, we do some tests on the solution using pytups to guarantee the solution is feasible:

.. literalinclude:: ./../../examples/machine_scheduling.py
   :lines: 69-80

The whole code is shown below:

.. literalinclude:: ./../../examples/machine_scheduling.py