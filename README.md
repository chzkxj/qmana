# qmana吗哪工作室

## 自己使用的脚本工具
工作之余做一些感兴趣或提高工作效率的小工具，谈不上编程，我只是一个代码搬运工。

## 简介
所有小工具均由Python编写，希望自己能一直坚持下去。

## 目录
1. [个人数据备份廉价解决方案](#个人数据备份廉价解决方案)
2. [MusicBrainz数据库Sqlite3实现](#musicbrainz数据库sqlite3实现)
3. [在shell中发送邮件](#在shell中发送邮件)

### 个人数据备份廉价解决方案

解决公有云收费，数据安全、个人隐私无保障，下载缓慢以及私有云价格昂贵等需求痛点。利用现有旧硬盘、双盘硬盘盒快速实现数据多重备份。其实没有什么技术难度，但确实解决了身边的数据备份需求，回头看之前保存的各种电影、电子书才发现，原来自己拍摄的照片和视频才是无价的，时间不能重来，人生只有一次，且行且珍惜。

#### 使用方法
```bash
> bash$:python3 syn.py ~/udisk/music/ ~/music/ -s

#参数一为源文件夹，参数二为目标文件夹，不使用-s参数时是单向复制，使用-s时是同步源和目标文件夹，慎用！
```


### MusicBrainz数据库Sqlite3实现

MusicBrainz是一个2000年上线的音乐标签分享编辑网站，所有数据都是开源的，可以通过API调用（[XML](https://musicbrainz.org/doc/Development/XML_Web_Service/Version_2)/[Python](https://python-musicbrainzngs.readthedocs.io/en/v0.7.1/))有自家的APP，也可以下载[数据库文件](https://musicbrainz.org/doc/MusicBrainz_Database/Download)(支持导入PostgreSQL数据库）可以说是非常的良心了，官方自称是是社区维护的音乐信息开源百科全书。目前该数据库收纳了161万artist,244万release,2189万recording和192万条tag信息（对港台、大陆中文歌曲的收录也越来越全面）。

Sqlite3碰巧也是2000年推出的嵌入式、跨平台、开源的RDBMS。现在几乎所有的现代浏览器、操作系统都使用这个核心代码不到600K的数据库，C/C++、JAVA、PHP、Python等编程语言都原生支持（好像没有不支持的），如果没有Sqlite3，几乎所有的智能设备都无法正常工作，天啊，简直是神一样的存在！不需要像Oracle、Mysql、PostgreSQL等重型数据库复杂的配置，一个文件搞定全部工作。性能也是杠杠的，在树莓派3B+上insert操作达到1万条/秒（性能的瓶颈在I/O设备，不在CPU和内存，估计在M.2接口(NVMe协议)SSD上会有更好的表现。

基于对音乐和编程的热爱，我制作了这个小工具，用来更新我的音乐播放器中的tag信息，实现按音乐风格分类播放。在此，不得不吐槽一下网易云音乐和QQ音乐，即使是拥有付费版权的音乐也缺乏对tag信息的维护，除了artist、title信息可用外，其它信息要么不完整，要么错误百出，缺乏对音乐的执着，忘记了创业时的初心。

#### 使用方法
* 在官网下载最新的[数据库文件](https://musicbrainz.org/doc/MusicBrainz_Database/Download)并解压。
* 在sqlite3里执行.read musicbrainz.sql初始化数据库文件。
* 修改musicbrainz_import.py相关配置，与mbdump文件夹和sqlite3文件一一对应。
* 执行python3 musicbrainz.py,这个过程大概3个小时，毕竟要读取1亿多条记录。
* 更新过程和创建其实是一样的，需要下载最新的数据库文件然后一条一条的读，更新和创建花费的时间差不多。
* 快捷方式：直接下载已经建好的数据库文件（百度网盘上传太慢，待更新）

### 在shell中发送邮件

初看这个命题感觉没什么难度，网上教程一大把，可真到实施的时候发现大部分都不好使，一方面是配置邮件服务器要有自己的服务器，独立IP地址，独立域名，网站备案，黑白名单，想想就算了，我只是想耍个杂技，另一方面邮件提供商似乎没打算让你这么干，提供的配置信息要么不全，要么没什么卵用（网易、QQ邮箱之类）。之后就想到了自己比较擅长的Django，Django的django.core.mail模块把可能遇到的配置问题都给你搞定了，只需要配置个人信息就好了，一次性搞定。这下可以在linux上装一把大神了^-^。（为什么没直接用Python的smtplib,原因是要配置SSL或者TLS，多次试验未果，遂放弃）

### 使用方法
* 必备工具 python3 Django
* 新建一个Django项目，或者在再有项目的settings.py文件中配置以下参数(推荐支持独立密码的邮件服务商，比如苹果、微软：
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.me.com'
EMAIL_PORT=587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'yourname@icloud.com'
EMAIL_HOST_PASSWORD = 'yourpassword'
DEFAULT_FROM_EMAIL='yourname@icloud.com'
```
* 运行sendmail.py脚本。






