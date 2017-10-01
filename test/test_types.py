"""Test suite for src/types.py."""

import sys
sys.path.append('..')
from src.types import Node, Network

nd_dnaDam = Node('DNAdam', 'NOT p53')
nd_p53 = Node('p53', 'NOT Mdm2nuc')
nd_mdm2cyt = Node('Mdm2cyt', 'p53')
nd_mdm2nuc = Node('Mdm2nuc', '((Mdm2cyt AND NOT p53) && !DNAdam)')

testNet = Network([nd_dnaDam, nd_p53, nd_mdm2cyt, nd_mdm2nuc])
