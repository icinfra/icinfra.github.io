---
layout: post
title: 使用patchelf修改rpath
date: 2023-03-15 11:30:48+0800
description: 
tags: elf
giscus_comments: true
categories: linux
---

# 需求
很多时候拿到一个软件包，需要设置LD_LIBRARY_PATH才能够正确链接到共享库来运行。如何让软件能够自动找到其软件包里的共享库，而不需要用户做太多的运行前设置？


如从 https://sourceforge.net/projects/srecord/files/srecord/1.65/srecord-1.65.0-Linux.rpm 下载的rpm包，解压之后是这样的目录结构
```bash
[wanlinwang@computing-server-01 usr]$ ls *
bin:
srec_cat  srec_cmp  srec_info

include:
srecord

lib:
ld-linux-x86-64.so.2  libgcc_s.so.1    libgcrypt.so.20.3.4  libgpg-error.so.0.32.1  libm.so.6       libstdc++.so.6.0.30
libc.so.6             libgcrypt.so.20  libgpg-error.so.0    liblib_srecord.a        libstdc++.so.6

share:
doc  man
```

并且直接运行会包共享库找不到。

# 方案
根据需求，可以对ELF设置RPATH。
```bash
[wanlinwang@computing-server-01 bin]$ patchelf --set-rpath '$ORIGIN/../lib' --force-rpath *
[wanlinwang@computing-server-01 bin]$ readelf -d * | grep -i rpath
 0x000000000000000f (RPATH)              Library rpath: [$ORIGIN/../lib]
 0x000000000000000f (RPATH)              Library rpath: [$ORIGIN/../lib]
 0x000000000000000f (RPATH)              Library rpath: [$ORIGIN/../lib]
[wanlinwang@computing-server-01 bin]$ ldd *
srec_cat:
	linux-vdso.so.1 =>  (0x00007fff02d8d000)
	libgcrypt.so.20 => /nfs/home/wanlinwang/usr/bin/./../lib/libgcrypt.so.20 (0x00007f9b740a0000)
	libstdc++.so.6 => /nfs/home/wanlinwang/usr/bin/./../lib/libstdc++.so.6 (0x00007f9b73e76000)
	libgcc_s.so.1 => /nfs/home/wanlinwang/usr/bin/./../lib/libgcc_s.so.1 (0x00007f9b742d3000)
	libc.so.6 => /nfs/home/wanlinwang/usr/bin/./../lib/libc.so.6 (0x00007f9b73c4e000)
	libgpg-error.so.0 => /nfs/home/wanlinwang/usr/bin/./../lib/libgpg-error.so.0 (0x00007f9b742ac000)
	libm.so.6 => /nfs/home/wanlinwang/usr/bin/./../lib/libm.so.6 (0x00007f9b73b67000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f9b741de000)
srec_cmp:
	linux-vdso.so.1 =>  (0x00007fffa639e000)
	libgcrypt.so.20 => /nfs/home/wanlinwang/usr/bin/./../lib/libgcrypt.so.20 (0x00007f5fd42ca000)
	libstdc++.so.6 => /nfs/home/wanlinwang/usr/bin/./../lib/libstdc++.so.6 (0x00007f5fd4067000)
	libgcc_s.so.1 => /nfs/home/wanlinwang/usr/bin/./../lib/libgcc_s.so.1 (0x00007f5fd4047000)
	libc.so.6 => /nfs/home/wanlinwang/usr/bin/./../lib/libc.so.6 (0x00007f5fd3e1f000)
	libgpg-error.so.0 => /nfs/home/wanlinwang/usr/bin/./../lib/libgpg-error.so.0 (0x00007f5fd3df9000)
	libm.so.6 => /nfs/home/wanlinwang/usr/bin/./../lib/libm.so.6 (0x00007f5fd3d12000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f5fd4291000)
srec_info:
	linux-vdso.so.1 =>  (0x00007ffe78da2000)
	libgcrypt.so.20 => /nfs/home/wanlinwang/usr/bin/./../lib/libgcrypt.so.20 (0x00007f97be3fc000)
	libstdc++.so.6 => /nfs/home/wanlinwang/usr/bin/./../lib/libstdc++.so.6 (0x00007f97be19c000)
	libgcc_s.so.1 => /nfs/home/wanlinwang/usr/bin/./../lib/libgcc_s.so.1 (0x00007f97be17c000)
	libc.so.6 => /nfs/home/wanlinwang/usr/bin/./../lib/libc.so.6 (0x00007f97bdf54000)
	libgpg-error.so.0 => /nfs/home/wanlinwang/usr/bin/./../lib/libgpg-error.so.0 (0x00007f97bdf2e000)
	libm.so.6 => /nfs/home/wanlinwang/usr/bin/./../lib/libm.so.6 (0x00007f97bde47000)
	/lib64/ld-linux-x86-64.so.2 (0x00007f97be3c6000)
```

这样，运行命令时就能够优先从其lib目录找共享库了。

# 参考资料

共享库查找顺序，来自[The Linux Programming](https://learning.oreilly.com/library/view/the-linux-programming/9781593272203/xhtml/ch41.xhtml#ch41lev1sec11)
> When resolving library dependencies, the dynamic linker first inspects each dependency string to see if it contains a slash (/), which can occur if we specified an explicit library pathname when linking the executable. If a slash is found, then the dependency string is interpreted as a pathname (either absolute or relative), and the library is loaded using that pathname. Otherwise, the dynamic linker searches for the shared library using the following rules:
>
>1. If the executable has any directories listed in its DT_RPATH run-time library path list (rpath) and the executable does not contain a DT_RUNPATH list, then these directories are searched (in the order that they were supplied when linking the program).
>
>2. If the LD_LIBRARY_PATH environment variable is defined, then each of the colon-separated directories listed in its value is searched in turn. If the executable is a set-user-ID or set-group-ID program, then LD_LIBRARY_PATH is ignored. This is a security measure to prevent users from tricking the dynamic linker into loading a private version of a library with the same name as a library required by the executable.
>
>3. If the executable has any directories listed in its DT_RUNPATH run-time library path list, then these directories are searched (in the order that they were supplied when linking the program).
>
>4. The file /etc/ld.so.cache is checked to see if it contains an entry for the library.
>
>5. The directories /lib and /usr/lib are searched (in that order).