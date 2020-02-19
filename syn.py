'''
参数一为源文件夹，参数二为目标文件夹，参数三为是否同步源和目标文件夹
示例一：
bash$:python3 syn.py ~/udisk/music/ ~/music/ -s
需求分析
解决公有云收费，数据安全、个人隐私无保障，下载缓慢以及私有云价格昂贵等需求痛点。
利用现有旧硬盘、双盘硬盘盒快速实现数据多重备份。

'''

import os,sys,shutil

def synfile(Root,Dest,syn=None):

    i = 0
    for (root, dirs, files) in os.walk(Root):
        new_root = root.replace(Root, Dest, 1)
        if not os.path.exists(new_root):
            os.mkdir(new_root)
        for f in files:
            path = os.path.join(root,f)
            Dest_path=path.replace(Root,Dest,1)
            if os.path.exists(Dest_path):
                if os.path.getctime(path) > os.path.getctime(Dest_path ) or os.path.getmtime(path) > os.path.getmtime(Dest_path ):
                    try:
                        shutil.copy(path, Dest_path)
                        i += 1
                        print(i)
                    except IOError as e:
                        print("Unable to copy file. %s" % e)
                    except:
                        print("Unexpected error:", sys.exc_info())
            else:
                try:
                    shutil.copy(path, Dest_path)
                    i += 1
                    print(i)
                except IOError as e:
                    print("Unable to copy file. %s" % e)
                except:
                    print("Unexpected error:", sys.exc_info())

    if syn =='-s':
        for (root, dirs, files) in os.walk(Dest):
            new_root = root.replace(Dest, Root, 1)
            if not os.path.exists(new_root):
                shutil.rmtree(root)  #删除文件夹及其文件
            for f in files:#删除同级目录下不存在的文件
                path = os.path.join(root,f)
                Dest_path=path.replace(Dest,Root,1)
                if not os.path.exists(Dest_path):
                    try:
                        os.remove(path)
                    except:
                        continue

if __name__=="__main__":
    if len(sys.argv)==4:
        sysfile(sys.argv[1],sys.argv[2],sys.argv[3])
    if len(sys.argv)==3:
        sysfile(sys.argv[1],sys.argv[2])

