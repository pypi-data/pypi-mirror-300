IUpdatable
=======================
Common function package
封装常用函数

详细文档：https://www.cnblogs.com/IUpdatable/articles/12500039.html

Installation
-----

首次安装：

```bash
pip install iupdatable
```

更新安装：

```bash
pip install --upgrade iupdatable
```


-----

## 更新日志：

### v 0.3.1
* SelfCleaningBackgroundService中的后台任务函数改成异步函数；

### v 0.3.0
* 仿 C# 中的 File 类，完善了 File 类
* 仿 C# 中的 Directory 类，完善了 Directory 类
* Timer 中新增一些与 datetime 格式化相关的函数
* 新增 SelfCleaningBackgroundService 类，用于实现自清理的后台服务

**File 类新增函数演示**
```python
import asyncio
import os
from iupdatable import File
import datetime

# 测试文件路径
test_file = "test_file.txt"
test_file_copy = "test_file_copy.txt"
test_file_move = "test_file_move.txt"
test_file_replace = "test_file_replace.txt"
test_file_backup = "test_file_backup.txt"


async def run_tests():
    print("开始测试File类的方法")

    # 测试create方法
    print("\n测试 create 方法")
    File.create(test_file)
    print(f"文件创建成功: {File.exists(test_file)}")

    # 测试write_all_text方法
    print("\n测试 write_all_text 方法")
    File.write_all_text(test_file, "Hello, World!")
    print(f"文件内容: {File.read_all_text(test_file)}")

    # 测试append_all_text方法
    print("\n测试 append_all_text 方法")
    File.append_all_text(test_file, "\nAppended text")
    print(f"文件内容: {File.read_all_text(test_file)}")

    # 测试write_all_lines方法
    print("\n测试 write_all_lines 方法")
    File.write_all_lines(test_file, ["Line 1", "Line 2", "Line 3"])
    print(f"文件内容: {File.read_all_lines(test_file)}")

    # 测试append_all_lines方法
    print("\n测试 append_all_lines 方法")
    File.append_all_lines(test_file, ["Line 4", "Line 5"])
    print(f"文件内容: {File.read_all_lines(test_file)}")

    # 测试copy方法
    print("\n测试 copy 方法")
    File.copy(test_file, test_file_copy)
    print(f"复制成功: {File.exists(test_file_copy)}")

    # 测试move方法
    print("\n测试 move 方法")
    File.move(test_file_copy, test_file_move)
    print(f"移动成功: {File.exists(test_file_move) and not File.exists(test_file_copy)}")

    # 测试replace方法
    print("\n测试 replace 方法")
    File.write_all_text(test_file_replace, "Original content")
    File.replace(test_file, test_file_replace, test_file_backup)
    print(f"替换成功: {File.read_all_text(test_file_replace) == File.read_all_text(test_file)}")
    print(f"备份成功: {File.exists(test_file_backup)}")

    # 测试get_creation_time方法
    print("\n测试 get_creation_time 方法")
    creation_time = File.get_creation_time(test_file)
    print(f"创建时间: {creation_time}")

    # 测试get_last_access_time方法
    print("\n测试 get_last_access_time 方法")
    last_access_time = File.get_last_access_time(test_file)
    print(f"最后访问时间: {last_access_time}")

    # 测试get_last_write_time方法
    print("\n测试 get_last_write_time 方法")
    last_write_time = File.get_last_write_time(test_file)
    print(f"最后修改时间: {last_write_time}")

    # 测试set_creation_time方法
    print("\n测试 set_creation_time 方法")
    new_creation_time = datetime.datetime.now() - datetime.timedelta(days=1)
    File.set_creation_time(test_file, new_creation_time)
    print(f"新创建时间: {File.get_creation_time(test_file)}")

    # 测试set_last_access_time方法
    print("\n测试 set_last_access_time 方法")
    new_last_access_time = datetime.datetime.now() - datetime.timedelta(hours=2)
    File.set_last_access_time(test_file, new_last_access_time)
    print(f"新最后访问时间: {File.get_last_access_time(test_file)}")

    # 测试set_last_write_time方法
    print("\n测试 set_last_write_time 方法")
    new_last_write_time = datetime.datetime.now() - datetime.timedelta(minutes=30)
    File.set_last_write_time(test_file, new_last_write_time)
    print(f"新最后修改时间: {File.get_last_write_time(test_file)}")

    # 测试read_all_bytes方法
    print("\n测试 read_all_bytes 方法")
    bytes_content = File.read_all_bytes(test_file)
    print(f"文件字节内容: {bytes_content[:20]}...")

    # 测试write_all_bytes方法
    print("\n测试 write_all_bytes 方法")
    new_bytes = b"New binary content"
    File.write_all_bytes(test_file, new_bytes)
    print(f"新文件字节内容: {File.read_all_bytes(test_file)}")

    # 测试异步方法
    print("\n测试异步方法")
    await File.write_all_text_async(test_file, "Async content")
    async_content = await File.read_all_text_async(test_file)
    print(f"异步读写结果: {async_content}")

    # 测试delete方法
    print("\n测试 delete 方法")
    for file in [test_file, test_file_move, test_file_replace, test_file_backup]:
        if File.exists(file):
            success = File.delete(file)
            print(f"删除 {file}: {'成功' if success else '失败'}")

    print("\n测试完成")

# 运行测试
asyncio.run(run_tests())

```

**Directory 新增函数调用演示**
```python
import datetime
import os
from iupdatable import Directory

# 设置测试目录
test_dir = os.path.join(os.getcwd(), "test_directory")
sub_dir = os.path.join(test_dir, "sub_directory")
test_file = os.path.join(test_dir, "test_file.txt")

print("1. 测试 create_directory")
result = Directory.create_directory(test_dir)
print(f"创建目录结果: {result}")

print("\n2. 测试 exists")
print(f"目录是否存在: {Directory.exists(test_dir)}")

print("\n3. 测试 get_current_directory")
print(f"当前目录: {Directory.get_current_directory()}")

print("\n4. 测试 get_creation_time")
print(f"目录创建时间: {Directory.get_creation_time(test_dir)}")

print("\n5. 测试 create_directory (子目录)")
sub_dir_result = Directory.create_directory(sub_dir)
print(f"创建子目录结果: {sub_dir_result}")

print("\n6. 测试 get_directories")
print(f"子目录列表: {Directory.get_directories(test_dir)}")

print("\n7. 测试 get_directory_root")
print(f"目录根: {Directory.get_directory_root(test_dir)}")

print("\n8. 测试 get_files")
# 创建一个测试文件
with open(test_file, 'w') as f:
    f.write("This is a test file.")
print(f"目录中的文件: {Directory.get_files(test_dir)}")

print("\n9. 测试 get_file_system_entries")
print(f"目录中的所有项: {Directory.get_file_system_entries(test_dir)}")

print("\n10. 测试 get_last_access_time")
print(f"最后访问时间: {Directory.get_last_access_time(test_dir)}")

print("\n11. 测试 get_last_write_time")
print(f"最后修改时间: {Directory.get_last_write_time(test_dir)}")

print("\n12. 测试 get_logical_drives")
print(f"逻辑驱动器: {Directory.get_logical_drives()}")

print("\n13. 测试 get_parent")
print(f"父目录: {Directory.get_parent(test_dir)}")

print("\n14. 测试 move")
move_dir = os.path.join(os.getcwd(), "moved_directory")
Directory.move(test_dir, move_dir)
print(f"移动后目录是否存在: {Directory.exists(move_dir)}")

print("\n15. 测试 set_creation_time")
new_time = datetime.datetime.now() - datetime.timedelta(days=1)
Directory.set_creation_time(move_dir, new_time)
print(f"设置后的创建时间: {Directory.get_creation_time(move_dir)}")

print("\n16. 测试 set_last_access_time")
new_access_time = datetime.datetime.now() - datetime.timedelta(hours=2)
Directory.set_last_access_time(move_dir, new_access_time)
print(f"设置后的最后访问时间: {Directory.get_last_access_time(move_dir)}")

print("\n17. 测试 set_last_write_time")
new_write_time = datetime.datetime.now() - datetime.timedelta(minutes=30)
Directory.set_last_write_time(move_dir, new_write_time)
print(f"设置后的最后修改时间: {Directory.get_last_write_time(move_dir)}")

print("\n18. 测试 delete")
Directory.delete(move_dir, recursive=True)
print(f"删除后目录是否存在: {Directory.exists(move_dir)}")

print("\n19. 测试 get_absolute_directory")

print(f"当前路径的绝对路径: {Directory.get_absolute_directory("./")}")

```
**SelfCleaningBackgroundService类调用演示**

```python
import asyncio
from iupdatable import Timer
from iupdatable.services.SelfCleaningBackgroundService import SelfCleaningBackgroundService


class Demo(SelfCleaningBackgroundService):

    def __init__(self, name, is_debug=False, auto_start=True):
        super().__init__(is_debug=is_debug, auto_start=auto_start)
        self._name = name
        self._counter = 0

    async def _background_task(self):
        while True:
            self._counter += 1
            print(f"{Timer.get_now_time_str()}: {self._name} counter: {self._counter}")
            await asyncio.sleep(1)


async def main():
    # 创建一个自动启动的 Demo 实例
    demo1 = Demo(name="demo1", is_debug=True)
    print(f"{Timer.get_now_time_str()}: Demo1 created (auto-start)")
    await asyncio.sleep(3)

    # 停止 demo1
    print(f"{Timer.get_now_time_str()}: Stopping demo1")
    demo1.stop()
    await asyncio.sleep(3)

    # 重新启动 demo1
    print(f"{Timer.get_now_time_str()}: Restarting demo1")
    demo1.start()
    await asyncio.sleep(2)

    # 创建一个不自动启动的 Demo 实例
    demo2 = Demo(name="demo2", is_debug=True, auto_start=False)
    print(f"{Timer.get_now_time_str()}: Demo2 created (not auto-start)")
    await asyncio.sleep(2)

    # 手动启动 demo2
    print(f"{Timer.get_now_time_str()}: Starting demo2")
    demo2.start()
    await asyncio.sleep(3)

    print(f"{Timer.get_now_time_str()}: Main function ending")

if __name__ == "__main__":
    asyncio.run(main())


```

### v 0.2.4
* 增加  WeiXinCrawler 类, 用于抓取微信公众号历史消息。

### v 0.2.2
* 增加 Timer 类

> Timer 主要函数：
> * 获取 Unix 时间戳（精确到秒）：timestamp、unix、unix10
> * 获取 Unix 时间戳（精确到毫秒）：timestamp13、unix13
> * 随机等待若干秒：sleep_range、sleep_range_async
> * Unix 时间戳转换成 datetime：unix_to_datetime、timestamp_to_datetime
> * Unix 时间戳转换成 datetime 字符串：unix_to_datetime_str、timestamp_to_datetime_str

### v 0.2.0
修复多进程下写入日志报错问题
> * 多进程下操作日志会报错：[WinError 32] 另一个程序正在使用此文件，进程无法访问。
>   这里通过添加 concurrent_log_handler 模块 替换掉系统内置的 TimedRotatingFileHandler 解决。

### v 0.1.9
* 添加 Status 类
> * 详细说明文章：[[Python] iupdatable包：Status 模块使用介绍](https://www.cnblogs.com/IUpdatable/p/14140258.html)


#### 文件 - File
- read： 读取文件
- write： 写入文件
- append：追加写入文件
- append_new_line：新建一行，然后追加写入文件
- read_lines： 按行一次性读取文件
- write_lines：按行一次性写入文件
- write_csv：写入CSV文件
- read_csv：读取CSV文件
- exist_within_extensions: 检查一个文件是否存在（在指定的几种格式中）
- get_file_path_within_extensions: 获取一个文件的路径（在指定的几种格式中）

简单实例:

```python
from iupdatable.system.io.File import File


sample_text = 'this is sample text.'
sample_texts = ['123', 'abc', 'ABC']
append_text = 'this is append text.'

# 写入
File.write('1.txt', sample_text)
File.write_lines('2.txt', sample_texts)

File.append('1.txt', append_text)
File.append_new_line('2.txt', append_text)

# 读取
read_text1 = File.read('1.txt')
read_text2 = File.read_lines('2.txt')

# 打印输出
print(read_text1)
print(read_text2)
```

### 日志 - logging

简单实例：

```python
from iupdatable.logging.Logger import Logger
from iupdatable.logging.LogLevel import LogLevel


def test_logging():
    # 日志等级：
    # CRITICAL  同：FATEL，下同
    # ERROR
    # WARNING
    # INFO
    # DEBUG
    # NOTSET    按照 WARNING 级别输出

    # 设置为 DEBUG，输出所有信息
    # 设置为 WARNING, INFO、DEBUG 级别的日志就不会输出
    Logger.get_instance().config(log_level=LogLevel.DEBUG)

    Logger.get_instance().debug('debug message1')
    Logger.get_instance().info('info message1')
    Logger.get_instance().warning('warning message1')
    Logger.get_instance().error('error message1')
    Logger.get_instance().debug('debug message1', is_with_debug_info=True)  # 要想输出具体的调试信息
    Logger.get_instance().fatal('fatal message1')
    Logger.get_instance().critical('critical message1')  # fatal = critical

    # 也可以输出变量
    abc = [1, 2, 4]
    Logger.get_instance().info(abc)


test_logging()
```

### Base64
- encode：base64编码
- decode：base64解码
- encode_multilines：base64多行解码
- decode_multilines：base64多行解码

### CSProduct

```python
from iupdatable.system.hardware import CSProduct

# 一次性获取所有的CSProduct信息
cs_product = CSProduct.get()
print("CSProduct: " + str(cs_product))
print(cs_product["Caption"])

# 或者
# 使用各项函数单独获取
print("Caption: " + CSProduct.get_caption())
print("Description: " + CSProduct.get_description())
print("IdentifyingNumber: " + CSProduct.get_identifying_number())
print("Name: " + CSProduct.get_name())
print("SKUNumber: " + CSProduct.get_sku_number())
print("UUID: " + CSProduct.get_uuid())
print("Vendor: " + CSProduct.get_vendor())
print("Version: " + CSProduct.get_version())

```

### UMeng

友盟统计

这里使用了自定义事件统计的功能

创建网站类型的统计，第一个参数是统计代码中的id

```python
UMeng.log_stat(1211111111, '来源页面', '目录', '行为', '标签')
```

License
-------
MIT