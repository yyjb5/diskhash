import psutil
import hashlib


def list_disks():
    # 获取所有磁盘分区信息
    partitions = psutil.disk_partitions()

    print("磁盘列表：")
    for partition in partitions:
        print(f"磁盘名称: {partition.device}， 文件系统: {partition.fstype}")


def hash_sector(disk, start_sector, num_sectors, hasher, update_step=None):
    with open(disk, 'rb') as f:
        for sector_number in range(start_sector, start_sector + num_sectors):
            # 移动文件指针到当前扇区位置
            f.seek(sector_number * 512)

            # 读取一个扇区的内容（512 字节）
            sector_content = f.read(512)
            # 哈希扇区内容
            hasher.update(sector_content)
            if hasattr(update_step, '__call__'):
                update_step((sector_number - start_sector) / num_sectors)
    return hasher.digest()


def list_sector_range(disk):
    # 获取磁盘总扇区数
    total_sectors = psutil.disk_usage(disk).total // 512

    print(f"磁盘 {disk} 的扇区范围：0 到 {total_sectors - 1}")


# 列出磁盘列表
list_disks()


# 输入要读取的磁盘、起始扇区和扇区数
selected_disk = input("请输入要读取扇区的磁盘名称（例如 '/dev/sda'）: ")

list_sector_range(selected_disk)

start_sector = int(input("请输入起始扇区号："))
num_sectors = int(input("请输入要读取的扇区数："))

sha256 = hashlib.sha1()


def print_step(str: str):
    print("\r", str, end="", flush=True)


# 循环读取并打印指定数量的扇区内容
hashstr = hash_sector(selected_disk, start_sector,
                      num_sectors, sha256, print_step)
print(hashstr.hex())
