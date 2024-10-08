import os
import shutil
import datetime
import platform
from typing import List, Union  # Union: python 3.10


class Directory:
    """
    Directory 类提供了一组用于操作目录的静态方法
    """

    @staticmethod
    def create_directory(path: str) -> Union[str, bool]:
        """
        创建指定路径的目录
        :param path: 要创建的目录路径(可以是绝对路径或相对路径)
        :return: 创建成功返回完整路径，失败返回False
        """
        try:
            os.makedirs(path, exist_ok=True)
            return os.path.abspath(path)
        except Exception:
            return False

    @staticmethod
    def delete(path: str, recursive: bool = False) -> None:
        """
        删除指定目录。
        :param path: 要删除的目录路径
        :param recursive: 是否递归删除子目录及文件，默认为False
        """
        if not os.path.isdir(path):
            raise ValueError(f"{path} 不是一个有效的目录")

        if recursive:
            shutil.rmtree(path)
        else:
            os.rmdir(path)

    @staticmethod
    def exists(path: str) -> bool:
        """
        判断目录是否存在。
        :param path: 要检查的目录路径
        :return: 如果目录存在返回True，否则返回False
        """
        return os.path.isdir(path)

    @staticmethod
    def get_creation_time(path: str) -> datetime.datetime:
        """
        获取指定目录的创建时间。
        :param path: 目录路径
        :return: 目录的创建时间
        """
        if not os.path.isdir(path):
            raise ValueError(f"{path} 不是一个有效的目录")

        return datetime.datetime.fromtimestamp(os.path.getctime(path))

    @staticmethod
    def get_current_directory() -> str:
        """
        获取当前应用程序运行的绝对路径。
        :return: 当前应用程序运行的绝对路径
        """
        return os.getcwd()

    @staticmethod
    def get_directories(path: str) -> List[str]:
        """
        返回指定目录中的子目录的名称（包括其路径）。
        :param path: 要检索子目录的目录路径
        :return: 子目录路径列表
        """
        if not os.path.isdir(path):
            raise ValueError(f"{path} 不是一个有效的目录")

        return [os.path.join(path, d) for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]

    @staticmethod
    def get_directory_root(path: str) -> str:
        """
        获取指定路径的根目录信息。
        :param path: 要获取根目录的路径
        :return: 根目录路径
        """
        return os.path.splitdrive(os.path.abspath(path))[0] + os.sep

    @staticmethod
    def get_files(path: str, recursive: bool = True) -> List[str]:
        """
        获取指定目录下的所有文件。
        :param path: 要检索文件的目录路径
        :param recursive: 是否递归获取所有子目录下的文件，默认为True
        :return: 文件路径列表
        """
        if not os.path.isdir(path):
            raise ValueError(f"{path} 不是一个有效的目录")

        if recursive:
            return [os.path.join(root, file) for root, _, files in os.walk(path) for file in files]
        else:
            return [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

    @staticmethod
    def get_file_system_entries(path: str, recursive: bool = True) -> List[str]:
        """
        返回指定路径中的所有文件和子目录的名称。
        :param path: 要检索的目录路径
        :param recursive: 是否递归获取所有子目录下的子目录和文件，默认为True
        :return: 所有文件和子目录的路径列表
        """
        if not os.path.isdir(path):
            raise ValueError(f"{path} 不是一个有效的目录")

        if recursive:
            return [os.path.join(root, name) for root, dirs, files in os.walk(path) for name in dirs + files]
        else:
            return [os.path.join(path, name) for name in os.listdir(path)]

    @staticmethod
    def get_last_access_time(path: str) -> datetime.datetime:
        """
        获取指定目录的最后访问时间。
        :param path: 目录路径
        :return: 目录的最后访问时间
        """
        if not os.path.isdir(path):
            raise ValueError(f"{path} 不是一个有效的目录")

        return datetime.datetime.fromtimestamp(os.path.getatime(path))

    @staticmethod
    def get_last_write_time(path: str) -> datetime.datetime:
        """
        获取指定目录的最后修改时间。
        :param path: 目录路径
        :return: 目录的最后修改时间
        """
        if not os.path.isdir(path):
            raise ValueError(f"{path} 不是一个有效的目录")

        return datetime.datetime.fromtimestamp(os.path.getmtime(path))

    @staticmethod
    def get_logical_drives() -> List[str]:
        """
        获取当前计算机上的逻辑驱动器名称。
        :return: 逻辑驱动器名称列表
        """
        if platform.system() == "Windows":
            return [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:")]
        else:
            return ["/"]

    @staticmethod
    def get_parent(path: str) -> str:
        """
        检索指定路径的父目录。
        :param path: 要检索父目录的路径（可以是绝对路径或相对路径）
        :return: 父目录的路径
        """
        return os.path.dirname(os.path.abspath(path))

    @staticmethod
    def move(source_dir: str, dest_dir: str) -> None:
        """
        将源目录移动到新位置。
        :param source_dir: 要移动的源目录路径
        :param dest_dir: 目标位置路径
        """
        if not os.path.isdir(source_dir):
            raise ValueError(f"{source_dir} 不是一个有效的目录")

        shutil.move(source_dir, dest_dir)

    @staticmethod
    def set_creation_time(path: str, creation_time: datetime.datetime) -> None:
        """
        设置指定目录的创建时间。
        :param path: 目录路径
        :param creation_time: 要设置的创建时间
        """
        if not os.path.isdir(path):
            raise ValueError(f"{path} 不是一个有效的目录")

        os.utime(path, (os.path.getatime(path), creation_time.timestamp()))

    @staticmethod
    def set_last_access_time(path: str, last_access_time: datetime.datetime) -> None:
        """
        设置指定目录的最后访问时间。
        :param path: 目录路径
        :param last_access_time: 要设置的最后访问时间
        """
        if not os.path.isdir(path):
            raise ValueError(f"{path} 不是一个有效的目录")

        os.utime(path, (last_access_time.timestamp(), os.path.getmtime(path)))

    @staticmethod
    def set_last_write_time(path: str, last_write_time: datetime.datetime) -> None:
        """
        设置指定目录的最后修改时间。
        :param path: 目录路径
        :param last_write_time: 要设置的最后修改时间
        """
        if not os.path.isdir(path):
            raise ValueError(f"{path} 不是一个有效的目录")

        os.utime(path, (os.path.getatime(path), last_write_time.timestamp()))

    @staticmethod
    def get_absolute_directory(path: str) -> str:
        """
        获取绝对路径
        :param path: 要检索的相对路径
        :return: 绝对路径
        """
        if not os.path.isdir(path):
            raise ValueError(f"{path} 不是一个有效的目录")
        return os.path.abspath(path)
