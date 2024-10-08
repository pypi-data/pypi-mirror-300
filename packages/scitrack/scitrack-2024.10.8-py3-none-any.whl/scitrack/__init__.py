"""
SciTrack provides basic logging capabilities to track scientific computations.
"""

import contextlib
import hashlib
import importlib
import inspect
import logging
import os
import platform
import socket
import sys
from getpass import getuser

__version__ = "2024.10.8"


VERSION_ATTRS = ["__version__", "version", "VERSION"]


def abspath(path):
    """returns an expanded, absolute path"""
    return os.path.abspath(os.path.expanduser(path))


def _create_path(path):
    """creates path"""
    if os.path.exists(path):
        return

    os.makedirs(path, exist_ok=True)


def get_package_name(object):
    """returns the package name for the provided object"""
    name = inspect.getmodule(object).__name__
    return name.split(".")[0]


def get_version_for_package(package):
    """returns the version of package"""
    if type(package) == str:
        try:
            mod = importlib.import_module(package)
        except ModuleNotFoundError as e:
            raise ValueError(f"Unknown package {package}") from e
    elif inspect.ismodule(package):
        mod = package
    else:
        raise ValueError(f"Unknown type, package {package}")

    vn = None

    for v in VERSION_ATTRS:
        with contextlib.suppress(AttributeError):
            vn = getattr(mod, v)
            if callable(vn):
                vn = vn()

            break
    if type(vn) in (tuple, list):
        vn = vn[0]

    del mod

    return vn


create_path = _create_path
FileHandler = logging.FileHandler


class CachingLogger:
    """stores log messages until a log filename is provided"""

    def __init__(self, log_file_path=None, create_dir=True, mode="w"):
        super(CachingLogger, self).__init__()
        self._log_file_path = None
        self._logfile = None
        self._started = False
        self.create_dir = create_dir
        self._messages = []
        self._hostname = socket.gethostname()
        self._mode = mode
        if log_file_path:
            self.log_file_path = log_file_path

    def _reset(self, mode="w"):
        self._mode = mode
        self._started = False
        self._messages = []
        if self._logfile is not None:
            self._logfile.flush()
            self._logfile.close()
            self._logfile = None

        self._log_file_path = None

    @property
    def log_file_path(self):
        return self._log_file_path

    @log_file_path.setter
    def log_file_path(self, path):
        """set the log file path and then dump cached log messages"""
        if self._log_file_path is not None:
            raise AttributeError(
                f"log_file_path already defined as {self._log_file_path}",
            )

        path = abspath(path)
        if self.create_dir:
            dirname = os.path.dirname(path)
            create_path(dirname)

        self._log_file_path = path

        self._logfile = set_logger(self._log_file_path, mode=self.mode)
        for m in self._messages:
            logging.info(m)

        self._messages = []
        self._started = True

    @property
    def mode(self):
        """the logfile opening mode"""
        return self._mode

    @mode.setter
    def mode(self, mode):
        """the logfile file opening mode"""
        self._mode = mode

    def _record_file(self, file_class, file_path):
        """writes the file path and md5 checksum to log file"""
        file_path = abspath(file_path)
        md5sum = get_file_hexdigest(file_path)
        self.log_message(file_path, label=file_class)
        self.log_message(md5sum, label=f"{file_class} md5sum")

    def input_file(self, file_path, label="input_file_path"):
        """logs path and md5 checksum

        Argument:
            - label is inserted before the message"""
        self._record_file(label, file_path)

    def output_file(self, file_path, label="output_file_path"):
        """logs path and md5 checksum

        Argument:
            - label is inserted before the message"""
        self._record_file(label, file_path)

    def text_data(self, data, label=None):
        """logs md5 checksum for input text data.

        Argument:
            - label is inserted before the message

        For this to be useful you must ensure the text order is persistent."""
        assert label is not None, "You must provide a data label"
        md5sum = get_text_hexdigest(data)
        self.log_message(md5sum, label=label)

    def log_message(self, msg, label=None):
        """writes a log message

        Argument:
            - label is inserted before the message"""
        label = label or "misc"
        data = [label, msg]
        msg = " : ".join(data)
        if not self._started:
            self._messages.append(msg)
        else:
            logging.info(msg)

    def log_args(self, args=None):
        """save arguments to file using label='params'
        Argument:
            - args: if None, uses inspect module to get locals
              from the calling frame"""
        if args is None:
            parent = inspect.currentframe().f_back
            args = inspect.getargvalues(parent).locals

        result = {
            k: args[k]
            for k in list(args)
            if type(args[k]) != self.__class__ and type(args[k]).__name__ != "module"
        }
        self.log_message(str(result), label="params")

    def shutdown(self):
        """safely shutdown the logger"""
        logging.getLogger().removeHandler(self._logfile)
        self._reset()

    def log_versions(self, packages=None):
        """logs version from the global namespace where
        method is invoked, plus from any named packages"""
        if type(packages) == str or inspect.ismodule(packages):
            packages = [packages]
        elif packages is None:
            packages = []

        for i, p in enumerate(packages):
            if inspect.ismodule(p):
                packages[i] = p.__name__

        parent = inspect.currentframe().f_back
        g = parent.f_globals
        name = g.get("__package__", g.get("__name__", ""))
        if name:
            vn = get_version_for_package(name)
        else:
            vn = [g.get(v, None) for v in VERSION_ATTRS if g.get(v, None)]
            vn = vn[0] if vn else None
            name = get_package_name(parent)

        versions = [(name, vn)]
        for package in packages:
            vn = get_version_for_package(package)
            versions.append((package, vn))

        for n_v in versions:
            self.log_message("%s==%s" % n_v, label="version")


def set_logger(log_file_path, level=logging.DEBUG, mode="w"):
    """setup logging"""
    handler = FileHandler(log_file_path, mode)
    handler.setLevel(level)
    hostpid = f"{socket.gethostname()}:{os.getpid()}"
    fmt = "%(asctime)s\t" + hostpid + "\t%(levelname)s\t%(message)s"
    formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logging.root.addHandler(handler)
    logging.root.setLevel(level)
    logging.info(f"system_details : system={platform.version()}")
    logging.info(f"python : {platform.python_version()}")
    logging.info(f"user : {getuser()}")
    logging.info(f'command_string : {" ".join(sys.argv)}')
    return handler


def get_file_hexdigest(filename):
    """returns the md5 hexadecimal checksum of the file

    NOTE
    ----
    The md5 sum of get_text_hexdigest can differ from get_file_hexdigest.
    This will occur if the line ending character differs from being read in
    'rb' versus 'r' modes.
    """
    # from
    # http://stackoverflow.com/questions/1131220/get-md5-hash-of-big-files-in-python
    with open(filename, "rb") as infile:
        md5 = hashlib.md5()
        while True:
            if data := infile.read(128):
                md5.update(data)
            else:
                break

    return md5.hexdigest()


def get_text_hexdigest(data):
    """returns md5 hexadecimal checksum of string/unicode data

    NOTE
    ----
    The md5 sum of get_text_hexdigest can differ from get_file_hexdigest.
    This will occur if the line ending character differs from being read in
    'rb' versus 'r' modes.
    """
    data_class = data.__class__
    # fmt: off
    if data_class in ("".__class__, "".__class__):
        data = data.encode("utf-8")
    elif data.__class__ != b"".__class__:
        raise TypeError("can only checksum string, unicode or bytes data")
    # fmt: on
    md5 = hashlib.md5()
    md5.update(data)
    return md5.hexdigest()
