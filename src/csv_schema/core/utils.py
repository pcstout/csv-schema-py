import os
import math


class Utils:
    KB = 1024
    MB = KB * KB
    CHUNK_SIZE = 10 * MB

    @staticmethod
    def expand_path(local_path):
        var_path = os.path.expandvars(local_path)
        expanded_path = os.path.expanduser(var_path)
        return os.path.abspath(expanded_path)

    @staticmethod
    def norm_os_path_sep(path):
        """Normalizes the path separator for the current operating system.

        Args:
            path: Path to normalize.

        Returns:
            Path with normalized path separators.
        """
        if os.sep == '/':
            return path.replace('\\', '/')
        else:
            return path.replace('/', '\\')

    @staticmethod
    def ensure_dirs(local_path):
        """Ensures the directories in local_path exist.

        Args:
            local_path: The local path to ensure.

        Returns:
            None
        """
        if not os.path.isdir(local_path):
            os.makedirs(local_path)

    @staticmethod
    def split_chunk(list, chunk_size):
        """Yield successive n-sized chunks from a list.

        Args:
            list: The list to chunk.
            chunk_size: The max chunk size.

        Returns:
            List of lists.
        """
        for i in range(0, len(list), chunk_size):
            yield list[i:i + chunk_size]

    @staticmethod
    def pretty_size(size):
        if size > 0:
            i = int(math.floor(math.log(size, 1024)))
            p = math.pow(1024, i)
            s = round(size / p, 2)
        else:
            i = 0
            s = 0
        return '{0} {1}'.format(s, Utils.PRETTY_SIZE_NAMES[i])
