#! /bin/python3
#A tool using dd command to help rescueing data from a damaged disk that often disconnects.
#Usage: edit the params, start script, reconnect the disk every time it disconnects.
#Only linux is supported. LiveCD is OK.
#一个使用dd命令拯救损坏而经常断连的磁盘中的数据的工具。
#用法：编辑参数，运行脚本，每当磁盘断连时将其重连。
#只支持Linux。 可以使用LiveCD。

blocksize=1048576           #Blocksize
blockcount=1                #Blocks copied in each dd command.
cbs=blocksize*blockcount    
totalbytes=363417517056     #total bytes of the disk or partition to copy.磁盘/分区总大小(字节)。
device="/dev/sdX"          #Source disk to copy from.源磁盘。
outfile="out.img"         #can be an image or a disk/partition device file.可以为镜像或磁盘/分区设备文件。
startseek=261212            #Continues copying starting from this block.从此block继续开始复制。


import os
import math
count=math.floor(startseek/blockcount)


def dataf(bytes):
    if bytes<1024:
        return f"{bytes}B"
    elif bytes<math.pow(1024,2):
        return  format(bytes/1024,".2f")+"KiB"
    elif bytes<math.pow(1024,3):
        return  format(bytes/math.pow(1024,2),".2f")+"MiB"
    elif bytes<math.pow(1024,4):
        return  format(bytes/math.pow(1024,3),".2f")+"GiB"
    else:
        return  format(bytes/math.pow(1024,4),".2f")+"TiB"
operationcount=math.ceil(totalbytes/blocksize/blockcount)
print(f"operations={operationcount}")
while count<=operationcount:
    blocks=count*blockcount
    if not os.path.exists(device):
        print("Source disk missing,waiting...")
        while not os.path.exists(device):
            pass
    success=0
    command=f"sudo dd if={device} of={outfile} bs={blocksize} cbs={cbs} count={blockcount} seek={blocks} skip={blocks}"
    print(f"running '{command}'")
    success=(not os.system(command)) and os.path.exists(device)
    if success:
        count=count+1
    print(f"count={count},success={success},seek={blocks},copied:{dataf(count*blocksize*blockcount)}/{dataf(totalbytes)},{format(count*blocksize*blockcount/totalbytes*100,'.3f')}%")
