import unittest
from .colors import *


class ColorizedTestResult(unittest.TextTestResult):
	def startTest(self, test):
		super().startTest(test)
		self.stream.write(f"{yellow(test._testMethodName)} ... ")
		self.stream.flush()


	def addSuccess(self, test):
		super().addSuccess(test)
		self.stream.write(green("OK\n"))


	def addFailure(self, test, err):
		super().addFailure(test, err)
		self.stream.write(red("FAIL\n"))


	def addError(self, test, err):
		super().addError(test, err)
		self.stream.write(red("ERROR\n"))



class ColorizedTestRunner(unittest.TextTestRunner):
	def __init__(self, *args, **kwargs):
		kwargs['verbosity'] = 0
		super().__init__(*args, **kwargs)

	def _makeResult(self):
		return ColorizedTestResult(self.stream, self.descriptions, self.verbosity)


def run_tests(test_case_class):
	suite = unittest.TestLoader().loadTestsFromTestCase(test_case_class)
	ColorizedTestRunner().run(suite)