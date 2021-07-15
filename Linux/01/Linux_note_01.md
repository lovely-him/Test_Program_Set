---
typora-root-url: ./
---

# Linux开发板 - 01 - 远程通讯/控制（SSH/VNC/FTP）

> 前言：最近向学校实验室借了一块Linux开发板（我一开始还以为是树莓派，本来想借树莓派的），开始接下来一段时间会记录学习过程。我借的是韦东山的**JZ2440开发板**，我本来以为韦东山和野火或正点原子类似，开发板收发，教程免费。万万没想到原来韦东山是二者都收费……虽然部分免费，但是很乱很旧。
>
> 说实话，我想着，都22年了，为什么还xp界面的教程还拿得出手啊，看得难受啊……（或许背后有我不懂的道理？如果有当我没说）



@[TOC](目录)



# 一、本文目的

>  Linux开发板 和 普通开发板 的学习过程 有什么不一样？

- 我大致看了一下使用Linux开发板的路线，大致流程可总结为：代码工程在Linux环境下编译，然后下载到Linux开发板内，然后运行。和普通的开发板差不多，都是编译、下载、运行，三步走。唯一特别的就是**编译需要在Linux环境下**……

> 学习 Linux开发板 需要先准备什么？

- 所以除了手上的Linux开发板外，我还需要一个能编译程序的Linux的系统。一般有两种选择：虚拟机，也是大部分推荐的，因为成本低；另一个就是实打实的装了Linux系统。如果是给废弃旧电脑装，装失败了还可以反复尝试，如果是只有一台电脑然后装双系统，那就有点危险了。
- 因为我前段时间刚好租了一个轻量级云服务器（详情：[基于Node.js与WebSocket搭建服务器 笔记 - 00 - 初建云服务器](https://blog.csdn.net/Lovely_him/article/details/117927381?spm=1001.2014.3001.5501)），所以我想着，能不能用这台云服务器来帮我编译程序呢，虽然配置低了点。但又不是不能用 ~~

>  跳过第一步安装Linux，“**本文目的**”是第二步。

- 在装好Linux系统后，难免需要与其他主机通信。比如最基本的传文件，把pc已有的文件弄到Linux系统上。
- *~~以前比较笨。如果是工程的话就pc上传git，linux再从git下载。又或者直接用u盘传输。因为我是用废弃旧电脑实打实的安装ubuntu（Linux）。又或者，可以使用宝塔面板等系统，上传文件或远程控制。~~*
- 为了更贴合实际工作（一般也都是24小时运作的云服务器吧），现在尝试使用云服务器学习Linux。所以学习常规的远程通讯方式：`SSH`/`VNC`/`FTP`。

## 1.相关概念

- 概念定义看百科： [ssh（安全外壳协议）](https://baike.baidu.com/item/SSH/10407#:~:text=SSH%20%E4%B8%BA%20Secure%20Shell%20%E7%9A%84%E7%BC%A9%E5%86%99%EF%BC%8C%E7%94%B1%20IETF%20%E7%9A%84%E7%BD%91%E7%BB%9C%E5%B0%8F%E7%BB%84%EF%BC%88Network,Working%20Group%EF%BC%89%E6%89%80%E5%88%B6%E5%AE%9A%EF%BC%9BSSH%20%E4%B8%BA%E5%BB%BA%E7%AB%8B%E5%9C%A8%E5%BA%94%E7%94%A8%E5%B1%82%E5%9F%BA%E7%A1%80%E4%B8%8A%E7%9A%84%E5%AE%89%E5%85%A8%E5%8D%8F%E8%AE%AE%E3%80%82.%20SSH%20%E6%98%AF%E8%BE%83%E5%8F%AF%E9%9D%A0%EF%BC%8C%E4%B8%93%E4%B8%BA%20%E8%BF%9C%E7%A8%8B%E7%99%BB%E5%BD%95%20%E4%BC%9A%E8%AF%9D%E5%92%8C%E5%85%B6%E4%BB%96%E7%BD%91%E7%BB%9C%E6%9C%8D%E5%8A%A1%E6%8F%90%E4%BE%9B%E5%AE%89%E5%85%A8%E6%80%A7%E7%9A%84%E5%8D%8F%E8%AE%AE%E3%80%82.) 、[VNC](https://baike.baidu.com/item/VNC/2906305#:~:text=VNC.%20VNC%20%5B1%5D%20%28Virtual%20Network%20Console%29%E6%98%AF%20%E8%99%9A%E6%8B%9F%E7%BD%91%E7%BB%9C%20%E6%8E%A7%E5%88%B6%E5%8F%B0%E7%9A%84%E7%BC%A9%E5%86%99%E3%80%82.,%E5%9C%A8%20Linux%20%E4%B8%AD%EF%BC%8CVNC%20%E5%8C%85%E6%8B%AC%E4%BB%A5%E4%B8%8B%E5%9B%9B%E4%B8%AA%E5%91%BD%E4%BB%A4%EF%BC%9Avncserver%EF%BC%8Cvncviewer%EF%BC%8Cvncpasswd%EF%BC%8C%E5%92%8C%20vncconnect%E3%80%82.%20%E5%A4%A7%E5%A4%9A%E6%95%B0%E6%83%85%E5%86%B5%E4%B8%8B%E7%94%A8%E6%88%B7%E5%8F%AA%E9%9C%80%E8%A6%81%E5%85%B6%E4%B8%AD%E7%9A%84%E4%B8%A4%E4%B8%AA%E5%91%BD%E4%BB%A4%EF%BC%9Avncserver%20%E5%92%8C%20vncviewer%E3%80%82.) 、[FTP（传输协议）](https://baike.baidu.com/item/ftp/13839#:~:text=%E6%96%87%E4%BB%B6%E4%BC%A0%E8%BE%93%E5%8D%8F%E8%AE%AE%EF%BC%88File%20Transfer%20Protocol%EF%BC%8CFTP%EF%BC%89%E6%98%AF%E7%94%A8%E4%BA%8E%E5%9C%A8%20%E7%BD%91%E7%BB%9C%20%E4%B8%8A%E8%BF%9B%E8%A1%8C%E6%96%87%E4%BB%B6%E4%BC%A0%E8%BE%93%E7%9A%84%E4%B8%80%E5%A5%97%E6%A0%87%E5%87%86%E5%8D%8F%E8%AE%AE%EF%BC%8C%E5%AE%83%E5%B7%A5%E4%BD%9C%E5%9C%A8%20OSI%20%E6%A8%A1%E5%9E%8B%E7%9A%84%E7%AC%AC%E4%B8%83%E5%B1%82%EF%BC%8C%20TCP,%E4%BC%A0%E8%BE%93%E8%80%8C%E4%B8%8D%E6%98%AF%20UDP%EF%BC%8C%20%E5%AE%A2%E6%88%B7%E5%9C%A8%E5%92%8C%E6%9C%8D%E5%8A%A1%E5%99%A8%E5%BB%BA%E7%AB%8B%E8%BF%9E%E6%8E%A5%E5%89%8D%E8%A6%81%E7%BB%8F%E8%BF%87%E4%B8%80%E4%B8%AA%E2%80%9C%E4%B8%89%E6%AC%A1%E6%8F%A1%E6%89%8B%E2%80%9D%E7%9A%84%E8%BF%87%E7%A8%8B%EF%BC%8C%20%E4%BF%9D%E8%AF%81%E5%AE%A2%E6%88%B7%E4%B8%8E%E6%9C%8D%E5%8A%A1%E5%99%A8%E4%B9%8B%E9%97%B4%E7%9A%84%E8%BF%9E%E6%8E%A5%E6%98%AF%E5%8F%AF%E9%9D%A0%E7%9A%84%EF%BC%8C%20%E8%80%8C%E4%B8%94%E6%98%AF%E9%9D%A2%E5%90%91%E8%BF%9E%E6%8E%A5%EF%BC%8C%20%E4%B8%BA%E6%95%B0%E6%8D%AE%E4%BC%A0%E8%BE%93%E6%8F%90%E4%BE%9B%E5%8F%AF%E9%9D%A0%E4%BF%9D%E8%AF%81%E3%80%82.%20%5B1%5D%20FTP%E5%85%81%E8%AE%B8%E7%94%A8%E6%88%B7%E4%BB%A5%E6%96%87%E4%BB%B6%E6%93%8D%E4%BD%9C%E7%9A%84%E6%96%B9%E5%BC%8F%EF%BC%88%E5%A6%82%E6%96%87%E4%BB%B6%E7%9A%84%E5%A2%9E%E3%80%81%E5%88%A0%E3%80%81%E6%94%B9%E3%80%81%E6%9F%A5%E3%80%81%E4%BC%A0%E9%80%81%E7%AD%89%EF%BC%89%E4%B8%8E%E5%8F%A6%E4%B8%80%E4%B8%BB%E6%9C%BA%E7%9B%B8%E4%BA%92%E9%80%9A%E4%BF%A1%E3%80%82.) 。
- 关于FTP，可以看看这个科普视频：[FTP，SFTP和TFTP](https://www.bilibili.com/video/BV17t41127xQ) 。



# 二、SSH

## 1.使用Win10普通终端

- 我在讲云服务器时也详细讲了一遍`SSH`的使用方法：[基于Node.js与WebSocket搭建服务器 笔记 - 00 - 初建云服务器](https://blog.csdn.net/Lovely_him/article/details/117927381?spm=1001.2014.3001.5501) 。推荐教程：[win10 开启ssh server服务 远程登录](https://blog.csdn.net/weixin_43064185/article/details/90080815) 。

- 大致上只需要记住以下一条Win10连接指令即可，**Linux不需要配置什么**（除了**防火墙**）。

```c
ssh 用户名@IP地址
```

- ①记得Linux防火墙开放端口号；②如果连接过再连接时失败了，就删除配置文件重新连接。



## 2.使用软件 MobaXterm Personal

- 这是一款集众多小工具于一身的神器，可在Win10中使用。有免费版，也有收费版，有安装版，也有免安装版。很方便，本文的目的之一，其实也包含介绍该工具。

- 该软件的官网国内也可以上，挺快的，不卡顿。直接搜索软件名、找到官网，点击下载、点击免费、点击便携版。

![](/img/20210705162928.gif)

- 下载完成后打开解压，点击exe打开软件，然后流程如下。

> 1. 点击工具栏第一个图标`Session`；选择上方第一个图标`SSH`。
> 2. 填表：`Remote host`填写连接的IP地址，`Specify usename`选择用户名和密码，`Port`填写端口号，默认ssh连接就是22.
> 3. 其他设置不需要改动，如果没有预设用户名和密码的，点图标创建。
> 4. 需要填写的个信息分别是：“`Name`该预设的名字”，“`Username`用户名”，“`Password密码`”。注意预设的名字随便，只是在软件选择时显示，用户名和密码才是关键。
> 5. 最后点击`OK`连接，就会自动连接上了。

![](/img/20210705164402.gif)

> 下面的教程操作就是在该SSH界面操作，因为是远程云服务器，该ssh窗口就是我的控制终端了。

- `MobaXterm Personal`工具的SSH连接，除了可以当远程终端外，还可以在左侧的工具栏中查看文件目录，很方便，可以在线浏览和修改文件，也能上传一些小文件。




# 三、VNC

> - 可以参考教程：我是几个教程交叉看的，只看一个教程会出现新问题，为了解决新的问题就会再参考其他教程。
> - 可以先安装我的步骤来，如果不成功再看其他教程。
>
> 1. [如何在Ubuntu 20.04上安装和配置VNC](https://blog.csdn.net/cukw6666/article/details/107984759)；
> 2. [Windows下通过VNC访问Linux服务器(可视化界面)](https://blog.csdn.net/qq_38451119/article/details/82461855)；
> 3. [windows下通过VNC图形化访问Ubuntu桌面环境](https://blog.csdn.net/lanxuezaipiao/article/details/25552675)；

## 1.Linux端设置：安装VNC服务 和 xfce4桌面服务

- 新主机上可能没有相关的下载源，然后报错，可以参考教程：[Package ‘vnc4server‘ has no installation candidate](https://wwwenb.blog.csdn.net/article/details/108891958)，添加需要的源。

> vim工具的退出指令是`:wq`，其中冒号代表指令，w代表保存，q代表退出。输入指令是`i`。更多操作可以参考：[Linux Vim三种工作模式](http://c.biancheng.net/view/804.html) 。

```c
sudo vim /etc/apt/sources.list
```

- 在文本末尾加上。

```c
 deb http://archive.ubuntu.com/ubuntu/ bionic universe
```

- 使用指令更新源，等待更新完毕。

```c
sudo apt update
```

- 安装软件，输入如下指令。

```c
sudo apt-get install vnc4server
```
- 在终端输入指令，开启vnc服务，冒号后的数值代表端口号，**完整的默认端口号**是`5902`,如果后面的数字是1，那就是`5901`。数字从1开始。记得，如果是云服务器要**开放防火墙**，输入完整的端口号。

```c
vncserver :2
```

- 第一次会有提示需要设定密码，成功后会显示类似如下信息。

> New 'VM-4-11-ubuntu:2 (ubuntu)' desktop is VM-4-11-ubuntu:2
>
> Starting applications specified in /home/ubuntu/.vnc/xstartup
> Log file is /home/ubuntu/.vnc/VM-4-11-ubuntu:2.log

- 其中文件`/home/ubuntu/.vnc/xstartup`就是配置文件，我们需要修改一些配置文件。使用以下指令打开配置文件。

```
sudo vim /home/ubuntu/.vnc/xstartup
```

- 如果不修改配置文件，进入后可能会是全灰的界面，或是雪花屏。其原因是没有设置正确的桌面环境。参考教程的解释：[windows下通过VNC图形化访问Ubuntu桌面环境](https://blog.csdn.net/lanxuezaipiao/article/details/25552675)。

```c
#!/bin/sh                                                                       

# Uncomment the following two lines for normal desktop:
# unset SESSION_MANAGER
# exec /etc/X11/xinit/xinitrc


[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup
[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
xsetroot -solid grey
vncconfig -iconic &
x-terminal-emulator -geometry 80x24+10+10 -ls -title "$VNCDESKTOP Desktop" &
x-window-manager &
```

- 文件内有一段注释写着：“**对普通的桌面，取消以下两行注释**”，我的是云服务器，所以没有普通桌面。我需要设定一个新的“桌面服务”（*本文暂不扩展探究显示普通桌面的设置*）。参考教程使用`xfce4`桌面服务，把最后一行的注释掉，然后添加以下内容。添加完后保存退出。

```c
#下面这块主要是针对运用xfce4管理桌面
x-session-manager & xfdesktop & xfce4-panel &
xfce4-menu-plugin &
xfsettingsd &
xfconfd &
xfwm4 &
```

- 修改完配置后，使用以下指令安装`xfce4`桌面服务。安装过程中，终端会有个类似弹窗的界面，按一下回车确认即可。

```
sudo apt install xfce4 xfce4-goodies
```

- 安装完毕后使用指令关闭vnc服务，再启动vnc，Linux端就算完成了。

```
vncserver -kill :2
vncserver :2
```

## 2.Win10端设置：RealVNC

- 该软件也是可以免费白嫖使用的，下载方式也是搜索官网下载，也有免安装版。请看下面gif动图。

![](/img/20217520403900.gif)

- 可以注意到在软件内新建窗口后，只输入了2个内容，第一个是`IP地址:端口号`，第二个是一个窗口名字，随便写。重点是第一个，端口是只需要填缩写（比如后缀2）就可以了。
- 创建窗口后，第一次打开窗口时会弹出需要输入密码，注意这个就是前面在Linux中**设定vnc服务时**填写的密码，一般要求6位以上。同时注意到窗口上还写着`IP地址::完整的端口号`，端口号被自动补全了，表示`590`就是公认默认vnc连接端口（？）。
- `MobaXterm Personal`软件也有vnc连接功能，不过我感觉好像不太好用，所以就选择之前用习惯的`RealVNC`。



# 四、FTP

> 参考教程：[Ubuntu系统搭建FTP服务器](https://blog.csdn.net/abraham_ly/article/details/107808007)，这篇教程讲得和完整，一篇就够用了。

## 1.Linux端设置

- 安装软件包

```c
sudo apt-get install vsftpd
```

- 通过查看版本，判断是否安装成功

```c
vsftpd -version
```

- 修改配置文件（和上面操作类似）。

```c
sudo vim /etc/confign
```

- 你可以在文本内看到以下被注释掉的代码，细心的找出他们，然后一条条取消注释

```
anonymous_enable=NO

local_enable=YES

write_enables=YES

chroot_list_enable=YES

chroot_list_file=/etc/vsftpd.chroot_list

secure_chroot_dir=/var/run/vsftpd/empty

pam_service_namevsftpd

rsa_cert_file=/etc/ss1/certs/ss1-cert-snakeoil.pem

rsa_private_key_file=/etc/ss1/private/ss1-certsnakeoil.key

ss1_enable=NO
```

- 同时，还需要在文本的最后，添加上一段代码，这个代码作用是指定FTP连接上后，默认处于的文件夹。该文件夹默认没有，要自己手动创建。

```c
local_root=/home/用户目录/ftp
allow_writeable_chroot=YES
```

- 开启FTP服务，*在教程里还有一段修改文件夹权限的，感觉不修改也没问题吧。如果是自己用的话*。

```c
sudo /etc/init.d/vsftpd restart
```

- 如果看到如下提示，就表示FTP服务器正常开启并运行了。

```c
Restarting vsftpd (via systemctl)：vsftpd.service
```

## 2.Win10端设置

### 1）使用文件浏览器访问

- 可以选择直接使用文件夹访问！Win10的文件夹居然有这种功能……直接在文件浏览器中输入网址即可。

```c
ftp://IP地址/
```

- 如果是第一次进入，是会提示需要用户名和密码的，这个是ubuntu的用户名和密码。然后就会到达之前设定好的`ftp`文件夹中，接着就是正常的拖拽文件操作了。

### 2）使用软件 MobaXterm Personal

- 操作和上面的类似，在选择用户时，我直接选择了在ssh中已经设置好的预设，端口默认`21`，输入好IP地址后就可以使用了。

![](/img/20210705214334.gif)

- 和使用文件浏览器打开差不多，都是默认直接打开了预设的`ftp`文件。注意，我无法返回`ftp`文件夹的上一级中目录。表示我**只能在该目录**下进行文件传输下载或修改。（*~~暂时够用，就不改了~~*）



# 五、总结

## 1.共同点 与 差异点

- 共同点：SSH、VNC、FTP都可以进行文件传输，且文件传输的专用程度是逐渐递增。
- 差异点 - SSH：主要命令行操作，连接时Linux设置少，登陆时，需要用Linux的用户名和密码；
- 差异点 - VNC：主要图形界面操作，连接时Linux设置多，登陆时，需要用vnc的专属密码；
- 差异点 - FTP：主要文件界面操作，连接时Linux设置中，登陆时，需要用Linux的用户名和密码；

## 2. 个人使用

- 用云服务器没有核显，只有单核+2G内存，用VNC显示图形界面时，卡得要死，所以不适合。因为我是用云服务器，所以要操作就一定要SSH远程登陆终端。上传文件用FTP挺方便的，直接使用文件浏览器查看，十分方便。

> *~~拖稿几天，终于写完了。~~*

