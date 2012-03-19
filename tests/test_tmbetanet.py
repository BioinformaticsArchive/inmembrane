import os
import unittest

# hack to allow tests to find inmembrane in directory above
import sys
sys.path.insert(0, '..')

import inmembrane


class TestTmbetanet(unittest.TestCase):
  def setUp(self):
    top_tests_dir = os.path.dirname(__file__)
    test_dir = os.path.join(top_tests_dir, 'tmbeta_net')
    self.dir = os.path.abspath(test_dir)

  def test_tmbeta_net_web(self):
    save_dir = os.getcwd()
    os.chdir(self.dir)

    self.params = inmembrane.get_params()
    self.params['fasta'] = "bomps.fasta"
    self.prot_ids, self.proteins = \
        inmembrane.create_protein_data_structure(self.params['fasta'])

    # run TMBETA-NET
    self.output = inmembrane.tmbeta_net_web(self.params, self.proteins, force=True)
    
    self.expected_output = {'gi|107836852': [[2, 9], [13, 23], [27, 32], [46, 57], [83, 116], [118, 124], [145, 150], [152, 168], [176, 184], [193, 199], [203, 208], [214, 233], [242, 269]], 'gi|107837106': [[8, 27], [30, 37], [41, 54], [60, 70], [75, 89], [95, 100], [110, 116], [119, 136], [159, 170], [176, 191], [200, 219], [227, 258], [262, 267], [273, 279], [298, 309], [316, 325]], 'gi|107837101': [[4, 13], [18, 23], [25, 32], [45, 52], [57, 71], [83, 89], [117, 128], [161, 166], [217, 223], [346, 352], [366, 371], [375, 383], [398, 415], [420, 425], [429, 435], [449, 456], [530, 535], [624, 634], [636, 644], [659, 675], [693, 710], [712, 718], [756, 762], [789, 797]], 'gi|107836588': [[4, 22], [31, 41], [46, 52], [60, 80], [87, 104], [120, 128], [138, 154], [160, 192], [194, 212], [224, 240]], 'gi|107837107': [[5, 11], [27, 38], [47, 53], [59, 67], [73, 79], [90, 122], [145, 165], [172, 179]]}
    self.assertEqual(self.expected_output, self.output)

    os.chdir(save_dir)


if __name__ == '__main__':
  unittest.main()
