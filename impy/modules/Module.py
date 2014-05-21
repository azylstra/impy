""" Python-based abstract representation of a module. All post-processor modules must implement these methods.

:author: Alex Zylstra
:date: 2014-01-23
"""

__author__ = 'Alex Zylstra'
__date__ = '2014-01-23'
__version__ = '1.0.0'

from abc import ABCMeta, abstractmethod
import inspect


class Module(metaclass=ABCMeta):
    """Python-based abstract representation of a module. All post-processor modules must implement these methods.
    Each module must support a few options for constructing.

    :param type: The type of constructor to be used. Available options are:

    'GUI': The class should interact directly with the user to get required options (default)

    'CLI': Interact with user via CLI, or take info from args.

    :param args: Additional information, which depends on the type of constructor:

    type='GUI': unused

    type='CLI': A full list of arguments passed to the executable, to be interpreted as the module pleases.

    :param wm: A window manager to use for GUI windows during construction

    Notes for implementers of modules:

    * The constructor should not do any computationally intensive tasks. Those should be done in `run`, which
        will be invoked in its own Thread.
    * The `run` method should not interact with the user or display any results (for portability!)


    :author: Alex Zylstra
    :date: 2014-01-23
    """
    __author__ = 'Alex Zylstra'
    __date__ = '2014-01-23'
    __version__ = '0.1.0'

    # ----------------------------------------
    #           Generic methods
    # ----------------------------------------
    @abstractmethod
    def __init__(self, type='GUI', args='', wm=None):
        """Construct a new instance of this module."""
        pass

    @classmethod
    @abstractmethod
    def name(cls):
        """Get a string containing a name for this type of module."""
        pass

    @classmethod
    @abstractmethod
    def info(cls):
        """Get a brief description of this specific module."""
        pass

    @classmethod
    @abstractmethod
    def detailedInfo(cls):
        """Get any detailed description and explanation of this module."""
        pass


    # ----------------------------------------
    #       Execution and GUI control
    # ----------------------------------------
    @abstractmethod
    def run(self, imp):
        """Run the calculation.

        :param imp: An `Implosion` object.
        """
        pass

    @abstractmethod
    def display(self, type='GUI', refresh=False, wm=None):
        """Display the results.

        :param type: The type of interface to be used. Available options are 'GUI' and 'CLI'. Default is GUI.
        :param refresh: (optional) If set to True, only existing windows should be updated.
        :param wm: (optional) Window manager to use for displaying windows
        """
        pass

    @abstractmethod
    def progress(self):
        """Get the calculation's progress estimate.

        :returns: Scalar number between 0 and 1.
        """
        pass

    @abstractmethod
    def copy(self, other):
        """Copy the results from `other` to this module.

        :param other: Another instance of this class
        """
        pass

    @abstractmethod
    def getPlots(self):
        """Return a list of all :py:class:`matplot.pyplot.Figure` instances created by this module."""
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

    # ----------------------------------------
    #      Stuff needed for pickling
    # ----------------------------------------
    def __getstate__(self):
        """Get the current state of this object as a `dict`.
        If there are members of the object that cannot be pickled, such as
        open files or GUI windows, they must be removed from the returned `dict`.
        """
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        """Set the state of this object from a given `dict`"""
        # Restore instance attributes (i.e., filename and lineno).
        self.__dict__.update(state)

def allModules():
    """Get a list containing all implemented implosions. """
    temp = Module.__subclasses__() + [g for s in Module.__subclasses__()
                                   for g in s.__subclasses__()]
    temp2 = []
    for t in temp:
        if not inspect.isabstract(t):
            temp2.append(t)
    return temp2