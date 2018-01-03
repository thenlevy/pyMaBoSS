.. api documutantion.

maboss API
==========

In the ``maboss`` module, the informations contained in the *MaBoSS*'s ``.cfg`` and ``.bnd`` files are represented by Python objects.

``Network`` objects represent most of the information contained in the ``.bnd``
file, and ``Simulation`` object contained the information contained in the ``.cfg`` file.

The ``maboss`` module can call the *MaBoSS* software via the ``run`` method of
``Simulation`` objects. This method writes a ``.cfg`` and a ``.bnd`` files and
run *MaBoSS* on them. Then, a ``Result`` object is created to interact with *MaBoSS* output files.

types
------------------

* **Node**

.. autoclass:: maboss.network.Node
	       :members:

* **Network**

.. autoclass:: maboss.network.Network
   :members:

* **Simulation**

.. autoclass:: maboss.simulation.Simulation
   :members:
   :special-members: __init__

* **Result**

.. autoclass:: maboss.result.Result

parser
------

.. automodule:: maboss.gsparser
		:members:
