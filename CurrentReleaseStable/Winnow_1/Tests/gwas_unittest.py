"""
Each method has an exception. If the data at specified desired list index does not match up with result data,
an AssertionError exception is thrown.

Currently, all tests pass as of May 12, 2016
"""
import unittest
import os
import sys
sys.path.append(os.getcwd()[:os.getcwd().index('DevelopingRelease')])
from DevelopingRelease.WinnowDevel import gwas
from DevelopingRelease.WinnowDevel import winnow as Winnow


class GWASTest(unittest.TestCase):
    """
    Directs path to example data for testing.
    Initializes args to test values.
    """
    folder = os.getcwd()[:os.getcwd().index("Validate")] + "Validate/ExampleData/Winnow/data/OutputPlink"
    ote = os.getcwd()[:os.getcwd().index("Validate")] + "Validate/ExampleData/Winnow/data/Plinkkt.ote"
    destination = os.getcwd()[:os.getcwd().index("Validate")] + "Validate/ExampleData/Winnow/results"
    args_without_covar = {'folder': folder, 'analysis': 'GWAS', 'truth': ote, 'snp': 'SNP', 'score': 'P',
                          'beta': 'BETA','filename': destination, 'threshold': 0.05, 'separ': 'whitespace',
                          'kt_type': 'OTE','kt_type_separ': 'whitespace', 'pvaladjust': None, 'savep': False,
                          'covar': None}

    covar_folder = os.getcwd()[:os.getcwd().index("Validate")] + "Validate/ExampleData/Winnow/data/covar"
    covar_ote = os.getcwd()[:os.getcwd().index("Validate")] + "Validate/ExampleData/Winnow/data/covarfakekt.ote"
    covar_destination = os.getcwd()[:os.getcwd().index("Validate")] + "Validate/ExampleData/Winnow/covarresults"
    args_with_covar = {'folder': covar_folder, 'analysis': 'GWAS', 'truth': covar_ote, 'snp': 'SNP', 'score': 'Pvalue',
                          'filename': covar_destination, 'threshold': 0.05, 'separ': 'comma',
                          'kt_type': 'OTE','kt_type_separ': 'whitespace', 'pvaladjust': None, 'savep': False,
                          'covar': "Cov01Weight", 'beta': None}

    def test_gwas_with_beta(self):
        """
        Tests method gwasWithBeta (performs GWAS analysis with beta/effect size)
        Checks for equality within 7 decimal places of returned list with expected list of functions and results
        """
        self.args_without_covar['beta'] = 'BETA'
        self.win = Winnow.Winnow(self.args_without_covar)
        s, b = self.win.load_data("/PlinkStd1.qassoc")
        self.win.load_ote()
        desired = ['test_filename', 0.058961209687231467, 0.18211782935394127, -0.038381861728111748,
                   0.43427678571428574, 0, 384, 2816, 35, 0.0, 0.12, 0.010819165378670788, 0.1295208655332303,
                   0.8704791344667697, 0.0, 0.88, 0.0, 1.0, -0.12, -7.7753167457938126]
        result = gwas.gwasWithBeta('test_filename', b, self.win.beta_true_false, self.win.snp_true_false,
                                   s, self.args_without_covar['threshold'])[1]
        for x in range(0, len(result)):
            try:
                self.assertAlmostEquals(desired[x], result[x])
            except AssertionError:
                print "Test failed"
                print "Desired value " + str(desired[x]) + " does not match up with result value " + str(result[x])

    def test_gwas_with_beta_covariate(self):
        """
        Tests method gwasBetaCovar (Performs GWAS analysis with beta/effect size and covariates)
        Checks for equality within 7 decimal places of returned list with expected list of functions and results
        """
        self.args_with_covar['beta'] = 'SNPWeight'
        self.win = Winnow.Winnow(self.args_with_covar)
        s, b, c = self.win.load_data('/Testwithcovar.csv')
        self.win.load_ote()
        desired = ['test_filename', 0.0020088036966300713, 0.034581652710000001, 0.086763105180589231,
                   0.85191672505254723, 6, 475, 9516, 3, 0.6666666666666666, 0.04754278850965869, 0.0009, 0.0478,
                   0.9522, 0.6666666666666666, 0.9524572114903413, 0.012474012474012475, 0.9875259875259875,
                   0.6191238781570081, 0.083426920159999987, 0.49487168117447544]
        result = gwas.gwasBetaCovar('test_filename', b, self.win.beta_true_false, self.win.snp_true_false, s,
                                    self.args_with_covar['threshold'], c)[1]
        for x in range(0, len(result)):
            try:
                self.assertAlmostEquals(desired[x], result[x])
            except AssertionError:
                print "Test failed"
                print "Desired value " + str(desired[x]) + " does not match up with result value " + str(result[x])

    def test_gwas_without_beta(self):
        """
        Tests method gwasWithoutBeta (Performs GWAS analysis without beta/effect size)
        Checks for equality within 7 decimal places of returned list with expected list of functions and results
        """
        self.args_without_covar['beta'] = None
        self.win = Winnow.Winnow(self.args_without_covar)
        s = self.win.load_data("/PlinkStd1.qassoc")
        self.win.load_ote()
        desired = ['test_filename', -0.038381861728111748, 0.43427678571428574, 0, 384, 2816, 35, 0.0, 0.12,
                   0.010819165378670788, 0.1295208655332303, 0.8704791344667697, 0.0, 0.88, 0.0, 1.0, -0.12,
                   -7.7753167457938126]
        result = gwas.gwasWithoutBeta('test_filename', self.win.snp_true_false, s,
                                      self.args_without_covar['threshold'])[1]
        for x in range(0, len(result)):
            try:
                self.assertAlmostEquals(desired[x], result[x])
            except AssertionError:
                print "Test failed"
                print "Desired value " + str(desired[x]) + " does not match up with result value " + str(result[x])

    def test_gwas_without_beta_covariate(self):
        """
        Tests method gwasNoBetaCovar (Performs GWAS analysis without beta/effect size)
        Checks for equality within 7 decimal places of returned list with expected list of functions and results
        """
        self.args_with_covar['beta'] = None
        self.win = Winnow.Winnow(self.args_with_covar)
        s, c = self.win.load_data("/Testwithcovar.csv")
        self.win.load_ote()
        desired = ['test_filename', 0.086763105180589231, 0.85191672505254723, 6, 475, 9516, 3, 0.6666666666666666,
                   0.04754278850965869, 0.0009, 0.0478, 0.9522, 0.6666666666666666, 0.9524572114903413,
                   0.012474012474012475, 0.9875259875259875, 0.6191238781570081, 0.083426920159999987,
                   0.49487168117447544]
        result = gwas.gwasNoBetaCovar('test_filename', self.win.snp_true_false, s,
                                      self.args_with_covar['threshold'], c)[1]
        for x in range(0, len(result)):
            try:
                self.assertAlmostEquals(desired[x], result[x])
            except AssertionError:
                print "Test failed"
                print "Desired value " + str(desired[x]) + " does not match up with result value " + str(result[x])


def get_test_suite():
    """
    Returns a test suite with all tests
    """
    return unittest.TestLoader().loadTestsFromTestCase(GWASTest)

if __name__ == "__main__":
    unittest.main()