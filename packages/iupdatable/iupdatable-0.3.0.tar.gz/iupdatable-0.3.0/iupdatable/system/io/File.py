import csv
import os
import shutil
import asyncio
from typing import List
import datetime

import pathlib


class File:
    """
    文件操作类，提供文件的创建、读取、写入、追加、复制、移动、删除、替换、获取文件信息等操作。
    """

    @staticmethod
    def append_all_lines(path: str, contents: List[str], encoding: str = 'utf-8') -> None:
        """
        向一个文件中追加行，然后关闭该文件。如果指定文件不存在，此方法会创建一个文件，向其中写入指定的行，然后关闭该文件。
        :param path: 要追加的文件路径
        :param contents: 要追加的行列表
        :param encoding: 文件编码，默认为utf-8
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        with open(path, 'a', encoding=encoding) as file:
            file.writelines(line + '\n' for line in contents)

    @staticmethod
    async def append_all_lines_async(path: str, contents: List[str], encoding: str = 'utf-8') -> None:
        """
        异步向一个文件中追加行，然后关闭该文件。
        :param path: 要追加的文件路径
        :param contents: 要追加的行列表
        :param encoding: 文件编码，默认为utf-8
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        async with asyncio.Lock():
            with open(path, 'a', encoding=encoding) as file:
                for line in contents:
                    await asyncio.to_thread(file.write, line + '\n')

    @staticmethod
    def append_all_text(path: str, contents: str, encoding: str = 'utf-8') -> None:
        """
        将指定的字符串追加到该文件，如果该文件尚不存在，则创建该文件。
        :param path: 要追加的文件路径
        :param contents: 要追加的字符串
        :param encoding: 文件编码，默认为utf-8
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        with open(path, 'a', encoding=encoding) as file:
            file.write(contents)

    @staticmethod
    async def append_all_text_async(path: str, contents: str, encoding: str = 'utf-8') -> None:
        """
        异步将指定的字符串追加到该文件。
        :param path: 要追加的文件路径
        :param contents: 要追加的字符串
        :param encoding: 文件编码，默认为utf-8
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        async with asyncio.Lock():
            with open(path, 'a', encoding=encoding) as file:
                await asyncio.to_thread(file.write, contents)

    @staticmethod
    def copy(source_file_name: str, dest_file_name: str, overwrite: bool = False) -> None:
        """
        将现有文件复制到新文件。
        :param source_file_name: 源文件路径
        :param dest_file_name: 目标文件路径
        :param overwrite: 是否覆盖同名文件，默认为False
        """
        if os.path.isdir(source_file_name) or os.path.isdir(dest_file_name):
            raise ValueError("源文件或目标文件是一个目录，不是文件")
        shutil.copy2(source_file_name, dest_file_name) if overwrite else shutil.copy(source_file_name, dest_file_name)

    @staticmethod
    def create(path: str) -> None:
        """
        创建或覆盖指定路径处的文件。
        :param path: 要创建的文件路径
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        open(path, 'w').close()

    @staticmethod
    def delete(path: str) -> bool:
        """
        删除指定文件。
        :param path: 要删除的文件路径
        :return: 是否成功删除文件
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        try:
            os.remove(path)
            return True
        except OSError as e:
            print(f"删除文件失败: {e}")
            return False

    @staticmethod
    def exists(path: str) -> bool:
        """
        判断指定文件是否存在。
        :param path: 要检查的文件路径
        :return: 文件是否存在
        """
        return os.path.isfile(path)

    @staticmethod
    def get_creation_time(path: str) -> datetime.datetime:
        """
        获取指定文件的创建时间。
        :param path: 文件路径
        :return: 文件的创建时间
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        return datetime.datetime.fromtimestamp(os.path.getctime(path))

    @staticmethod
    def get_last_access_time(path: str) -> datetime.datetime:
        """
        获取指定文件的最后访问时间。
        :param path: 文件路径
        :return: 文件的最后访问时间
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        return datetime.datetime.fromtimestamp(os.path.getatime(path))

    @staticmethod
    def get_last_write_time(path: str) -> datetime.datetime:
        """
        获取指定文件的最后修改时间。
        :param path: 文件路径
        :return: 文件的最后修改时间
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        return datetime.datetime.fromtimestamp(os.path.getmtime(path))

    @staticmethod
    def move(source_file_name: str, dest_file_name: str, overwrite: bool = False) -> None:
        """
        将指定文件移动到新位置，可以指定新文件名。
        :param source_file_name: 源文件路径
        :param dest_file_name: 目标文件路径
        :param overwrite: 是否覆盖同名文件，默认为False
        """
        if os.path.isdir(source_file_name) or os.path.isdir(dest_file_name):
            raise ValueError("源文件或目标文件是一个目录，不是文件")
        if not overwrite and os.path.exists(dest_file_name):
            raise FileExistsError(f"目标文件 {dest_file_name} 已存在")
        shutil.move(source_file_name, dest_file_name)

    @staticmethod
    def open(path: str, mode: str = 'r', encoding: str = 'utf-8'):
        """
        打开指定路径处的文件。
        :param path: 要打开的文件路径
        :param mode: 打开模式，默认为'r'（只读）
        :param encoding: 文件编码，默认为utf-8
        :return: 文件对象
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        return open(path, mode, encoding=encoding)

    @staticmethod
    def read_all_bytes(path: str) -> bytes:
        """
        打开一个二进制文件，将文件的内容读入一个字节数组，然后关闭该文件。
        :param path: 要读取的文件路径
        :return: 文件内容的字节数组
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        with open(path, 'rb') as file:
            return file.read()

    @staticmethod
    async def read_all_bytes_async(path: str) -> bytes:
        """
        异步读取文件的所有字节。
        :param path: 要读取的文件路径
        :return: 文件内容的字节数组
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        async with asyncio.Lock():
            return await asyncio.to_thread(File.read_all_bytes, path)

    @staticmethod
    def read_all_lines(path: str, encoding: str = 'utf-8') -> List[str]:
        """
        打开一个文本文件，读取文件的所有行，然后关闭该文件。
        :param path: 要读取的文件路径
        :param encoding: 文件编码，默认为utf-8
        :return: 文件内容的行列表
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        with open(path, 'r', encoding=encoding) as file:
            return file.readlines()

    @staticmethod
    async def read_all_lines_async(path: str, encoding: str = 'utf-8') -> List[str]:
        """
        异步读取文件的所有行。
        :param path: 要读取的文件路径
        :param encoding: 文件编码，默认为utf-8
        :return: 文件内容的行列表
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        async with asyncio.Lock():
            return await asyncio.to_thread(File.read_all_lines, path, encoding)

    @staticmethod
    def read_all_text(path: str, encoding: str = 'utf-8') -> str:
        """
        打开一个文本文件，读取文件的所有文本，然后关闭该文件。
        :param path: 要读取的文件路径
        :param encoding: 文件编码，默认为utf-8
        :return: 文件的所有文本
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        with open(path, 'r', encoding=encoding) as file:
            return file.read()

    @staticmethod
    async def read_all_text_async(path: str, encoding: str = 'utf-8') -> str:
        """
        异步读取文件的所有文本。
        :param path: 要读取的文件路径
        :param encoding: 文件编码，默认为utf-8
        :return: 文件的所有文本
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        async with asyncio.Lock():
            return await asyncio.to_thread(File.read_all_text, path, encoding)

    @staticmethod
    def replace(source_file_name: str, dest_file_name: str, backup_file_name: str = None) -> None:
        """
        替换指定文件的内容，可以创建备份。
        :param source_file_name: 源文件路径
        :param dest_file_name: 目标文件路径
        :param backup_file_name: 备份文件路径，如果指定则创建备份
        """
        if os.path.isdir(source_file_name) or os.path.isdir(dest_file_name):
            raise ValueError("源文件或目标文件是一个目录，不是文件")
        if backup_file_name:
            shutil.copy2(dest_file_name, backup_file_name)
        shutil.copy2(source_file_name, dest_file_name)

    @staticmethod
    def set_creation_time(path: str, creation_time: datetime.datetime) -> None:
        """
        设置指定文件的创建时间。
        :param path: 文件路径
        :param creation_time: 要设置的创建时间
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        os.utime(path, (os.path.getatime(path), creation_time.timestamp()))

    @staticmethod
    def set_last_access_time(path: str, last_access_time: datetime.datetime) -> None:
        """
        设置指定文件的最后访问时间。
        :param path: 文件路径
        :param last_access_time: 要设置的最后访问时间
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        os.utime(path, (last_access_time.timestamp(), os.path.getmtime(path)))

    @staticmethod
    def set_last_write_time(path: str, last_write_time: datetime.datetime) -> None:
        """
        设置指定文件的最后修改时间。
        :param path: 文件路径
        :param last_write_time: 要设置的最后修改时间
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        os.utime(path, (os.path.getatime(path), last_write_time.timestamp()))

    @staticmethod
    def write_all_bytes(path: str, bytes: bytes) -> None:
        """
        创建一个新文件，在其中写入指定的字节数组，然后关闭该文件。如果目标文件已存在，则覆盖该文件。
        :param path: 要写入的文件路径
        :param bytes: 要写入的字节数组
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        with open(path, 'wb') as file:
            file.write(bytes)

    @staticmethod
    async def write_all_bytes_async(path: str, bytes: bytes) -> None:
        """
        异步创建一个新文件，在其中写入指定的字节数组。
        :param path: 要写入的文件路径
        :param bytes: 要写入的字节数组
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        async with asyncio.Lock():
            await asyncio.to_thread(File.write_all_bytes, path, bytes)

    @staticmethod
    def write_all_lines(path: str, contents: List[str], encoding: str = 'utf-8') -> None:
        """
        创建一个新文件，在其中写入指定的字符串集合，然后关闭该文件。
        :param path: 要写入的文件路径
        :param contents: 要写入的字符串列表
        :param encoding: 文件编码，默认为utf-8
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        with open(path, 'w', encoding=encoding) as file:
            file.writelines(line + '\n' for line in contents)

    @staticmethod
    async def write_all_lines_async(path: str, contents: List[str], encoding: str = 'utf-8') -> None:
        """
        异步创建一个新文件，在其中写入指定的字符串集合。
        :param path: 要写入的文件路径
        :param contents: 要写入的字符串列表
        :param encoding: 文件编码，默认为utf-8
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        async with asyncio.Lock():
            await asyncio.to_thread(File.write_all_lines, path, contents, encoding)

    @staticmethod
    def write_all_text(path: str, contents: str, encoding: str = 'utf-8') -> None:
        """
        创建一个新文件，在其中写入指定的字符串，然后关闭该文件。如果目标文件已存在，则覆盖该文件。
        :param path: 要写入的文件路径
        :param contents: 要写入的字符串
        :param encoding: 文件编码，默认为utf-8
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        with open(path, 'w', encoding=encoding) as file:
            file.write(contents)

    @staticmethod
    async def write_all_text_async(path: str, contents: str, encoding: str = 'utf-8') -> None:
        """
        异步创建一个新文件，在其中写入指定的字符串。
        :param path: 要写入的文件路径
        :param contents: 要写入的字符串
        :param encoding: 文件编码，默认为utf-8
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        async with asyncio.Lock():
            await asyncio.to_thread(File.write_all_text, path, contents, encoding)

    # ---------------------------------V0.2.4 及之前版本的函数------------------------------------------

    @staticmethod
    def read(path: str, encoding="utf-8") -> str:
        """"
        读取文件
        :param path: 完整的文件路径
        :param encoding: 编码格式，默认utf-8
        :return:
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        with open(path, 'r', encoding=encoding) as file:
            return file.read()

    @staticmethod
    def write(path: str, contents: str, encoding: str = 'utf-8') -> None:
        """
        创建一个新文件，在其中写入指定的字符串，然后关闭该文件。如果目标文件已存在，则覆盖该文件。
        :param path: 要写入的文件路径
        :param contents: 要写入的字符串
        :param encoding: 文件编码，默认为utf-8
        """
        if os.path.isdir(path):
            raise ValueError(f"{path} 是一个目录，不是文件")
        with open(path, 'w', encoding=encoding) as file:
            file.write(contents)

    @staticmethod
    def write_csv(file_path: str, rows: []) -> None:
        """
        写入CSV文件
        :param file_path: 完整的文件路径，如："D:\\12.csv","1.csv"
        :param rows: 待写入的多行数据，如：[['row11','row12','row13'],['row21','row22','row23']]
        :return:
        """
        with open(file_path, 'w', encoding='utf_8_sig', newline='') as f:
            csv_write = csv.writer(f)
            for oneRow in rows:
                csv_write.writerow(oneRow)

    @staticmethod
    def read_csv(file_path: str, encoding="utf_8_sig") -> []:
        """
        读取CSV文件
        :param file_path: 完整的文件路径，如："D:\\12.csv","1.csv"
        :param encoding: 文件编码，默认为utf_8_sig
        :return:
        """
        rows = []
        with open(file_path, 'r', encoding=encoding) as f:
            csv_reader = csv.reader(f)
            for oneRow in csv_reader:
                rows.append(oneRow)
        return rows

    @staticmethod
    def exist(file_path: str) -> bool:
        """
        检查一个文件是否存在
        :param file_path: 文件的路径
        :return: 有任意一种格式的存在即认为文件存在
        """
        if os.path.isfile(file_path):
            return True
        else:
            return False

    @staticmethod
    def exist_within_extensions(file_path: str, extension_list: []) -> bool:
        """
        检查一个文件是否存在（在指定的几种格式中）
        :param file_path: 文件的路径
        :param extension_list: 关心的格式,如：["jpg", "png", "bmp"]
        :return: 有任意一种格式的存在即认为文件存在
        """
        if os.path.isfile(file_path):
            return True
        win_path = pathlib.PureWindowsPath(file_path)
        file_path_no_extension = str(win_path.parent) + "\\" + win_path.stem
        for one_extension in extension_list:
            new_file_path = file_path_no_extension + "." + one_extension
            if os.path.isfile(new_file_path):
                return True
        return False

    @staticmethod
    def get_file_path_within_extensions(file_path: str, extension_list: []) -> str:
        """
        获取一个文件的路径（在指定的几种格式中）
        适用场景：
        想要获取一个指定路径下的文件，如：c:\testfile，
        但并不关心其具体是什么格式，只要是在extension_list指定的其中一种即可（靠前的优先）
        :param file_path: 文件的路径，如：c:\testfile，一个没有拓展名的文件（拓展名可有可无）
        :param extension_list: 关心的格式,如：["jpg", "png", "bmp"]
        :return: 不存在则返回None
        """
        if os.path.isfile(file_path):
            return file_path
        win_path = pathlib.PureWindowsPath(file_path)
        file_path_no_extension = str(win_path.parent) + "\\" + win_path.stem
        for one_extension in extension_list:
            new_file_path = file_path_no_extension + "." + one_extension
            if os.path.isfile(new_file_path):
                return new_file_path
        return None

    @staticmethod
    def append(file_path: str, content: str, encoding="utf_8_sig") -> None:
        """"
        追加写入文件
        :param file_path: 完整的文件路径
        :param content: 待写入内容
        :param encoding: 编码格式，默认utf_8_sig，这是Windows下记事本utf8的编码格式
        :return:
        """
        with open(file_path, "a", encoding=encoding) as f:
            f.write(content)

    @staticmethod
    def append_new_line(file_path: str, content: str, encoding="utf_8_sig") -> None:
        """"
        新建一行，然后追加写入文件
        新文件或空白文件，则不添加新行
        :param file_path: 完整的文件路径
        :param content: 待写入内容
        :param encoding: 编码格式，默认utf_8_sig，这是Windows下记事本utf8的编码格式
        :return:
        """
        is_exist = os.path.exists(file_path)

        if is_exist:
            with open(file_path, "a", encoding=encoding) as file:
                size = os.path.getsize(file_path)
                if size == 3 and encoding.lower() == "utf_8_sig":  # utf_8_sig的txt文件会在开头添加三个字节的标识
                    file.write(content)
                elif size == 0 and encoding.lower() != "utf_8_sig":
                    file.write(content)
                else:
                    file.write("\n" + content)
        else:
            with open(file_path, "a", encoding=encoding) as new_file:
                new_file.write(content)

    @staticmethod
    def read_lines(file_path: str, remove_empty_line=True, remove_empty_space=True, encoding="utf_8_sig") -> []:
        """
        按行一次性读取文件
        :param file_path: 完整的文件路径
        :param remove_empty_line: 是否去除空白行
        :param remove_empty_space: 是否移除每行前后的空白
        :param encoding: 编码格式，默认utf_8_sig，这是Windows下记事本utf8的编码格式
        :return:
        """
        lines = []
        with open(file_path, encoding=encoding) as f:  # 默认为utf8编码
            for line in f.readlines():
                if remove_empty_space:
                    line = line.strip()
                if remove_empty_line:
                    line = line.rstrip('\n')  # 去掉每行的回车
                    if line:  # 去掉空行
                        lines.append(line)
                else:
                    line = line.rstrip('\n')  # 去掉每行的回车
                    lines.append(line)
        return lines

    @staticmethod
    def write_lines(file_path: str, lines: [], encoding="utf_8_sig") -> None:
        """
        按行一次性写入文件
        :param file_path: 完整的文件路径
        :param lines: 待写入的多行内容
        :param encoding: 编码格式，默认utf_8_sig，这是Windows下记事本utf8的编码格式
        :return:
        """
        with open(file_path, "w", encoding=encoding) as f:
            str_lines = [str(line) for line in lines]  # 针对数组中有数字的情况
            f.write('\n'.join(str_lines))
