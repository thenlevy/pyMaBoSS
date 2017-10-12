"""Test suite for the binding methods of Node."""

import sys
sys.path.append('..')
from maboss.types import Node, Network

nd_dnaDam = Node('DNAdam', '(!p53_b1 & DNAdam)', 1, 1)
nd_p53_b1 = Node('p53_b1', '((!p53_b2 & !Mdm2nuc) | p53_b2)', 1, 1)
nd_p53_b2 = Node('p53_b2', '(p53_b1 & !Mdm2nuc)', 1, 1)
nd_mdm2cyt = Node('Mdm2cyt', '(p53_b1 & p53_b2)', 1, 1)
nd_mdm2nuc = Node('Mdm2nuc', '((((!p53_b1 & !Mdm2cyt) & !DNAdam) | (!p53_b1 & Mdm2cyt) ) | (p53_b1 & Mdm2cyt))', 1, 1)

testNet = Network([nd_dnaDam, nd_p53_b1, nd_p53_b2, nd_mdm2cyt, nd_mdm2nuc])

testNet.set_istate(['p53_b1', 'p53_b2'],
                   {(0, 0): 1, (1, 0): 0, (1, 1): 0})
testNet.set_istate('Mdm2cyt', [1, 0])
testNet.set_istate('Mdm2nuc', [1, 0])
testNet.set_istate('DNAdam', [0.4, 0.6])

testNet.set_istate('p53_b1', [0.5, 0.5]) # Must triger a warning
testNet.set_istate(['p53_b1', 'p53_b2', 'Mdm2nuc'], {(0, 0, 0): 0.5, (0, 1, 1): 0.5})
testNet.set_istate(['p53_b1', 'p53_b2'],
                   {(0, 0): 1, (1, 0): 0, (1, 1): 0}) # Must triger a warning
