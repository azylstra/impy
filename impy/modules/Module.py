""" Python-based abstract representation of a module. All post-processor modules must implement these methods.

:author: Alex Zylstra
:date: 2014-01-05
"""

__author__ = 'Alex Zylstra'
__date__ = '2014-01-05'
__version__ = '1.0.0'

from abc import ABCMeta, abstractmethod


class Module(metaclass=ABCMeta):
    """Python-based abstract representation of a module. All post-processor modules must implement these methods.
    Each module must support a few options for constructing.

    :param type: The type of constructor to be used. Available options are:

    'GUI': The class should interact directly with the user to get required options (default)

    'CLI': Interact with user via CLI, or take info from args.

    :param args: Additional information, which depends on the type of constructor:

    type='GUI': unused

    type='CLI': A full list of arguments passed to the executable, to be interpreted as the module pleases.

    Notes for implementers of modules:

    * The constructor should not do any computationally intensive tasks. Those should be done in `run`, which
    will be invoked in its own Thread.

    * The `run` method should not interact with the user or display any results (for portability!)

    :author: Alex Zylstra
    :date: 2014-01-05
    """

    # ----------------------------------------
    #           Generic methods
    # ----------------------------------------
    @abstractmethod
    def __init__(self, type='GUI', args=''):
        """Construct a new instance of this module."""
        pass

    @classmethod
    @abstractmethod
    def name(cls):
        """Get a string containing a name for this type of module."""
        pass

    @abstractmethod
    def info(self):
        """Get a string of information about this specific module."""
        pass


    # ----------------------------------------
    #       Execution and GUI control
    # ----------------------------------------
    @abstractmethod
    def run(self):
        """Run the calculation."""
        pass

    @abstractmethod
    def display(self, type='GUI'):
        """Display the results.

        :param type: The type of interface to be used. Available options are 'GUI' and 'CLI'.
        """
        pass

    @abstractmethod
    def hide(self):
        """Hide the module (i.e. any windows and plots generated)"""
        pass

    @abstractmethod
    def abort(self):
        """Signal that the calculation should be interrupted."""
        pass

    @abstractmethod
    def progress(self):
        """Get the calculation's progress estimate.

        :returns: Scalar number between 0 and 1.
        """
        pass

    # ----------------------------------------
    #           Results handling
    # ----------------------------------------
    @abstractmethod
    def save(self, filename, type='CSV'):
        """Save the results to a file.

        :param filename: The file to save to
        :param type: The type of save file to create:

        'CSV': A CSV containing top-level results

        'pickle': Pickle the calculation results
        """
        pass

    @abstractmethod
    def savePlots(self, dir, prefix, type):
        """Save all generated plots.

        :param dir: The directory to save the plots to
        :param prefix: A prefix to append to any files generated by this module
        :param type: The type of plot to generate (e.g. 'eps')

        As a result, files generated in `dir` should have names like::

            prefix + my_name + '.' + type

        """
        pass