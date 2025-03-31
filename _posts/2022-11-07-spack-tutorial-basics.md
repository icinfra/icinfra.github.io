---
layout: post
title: Spack教程（基础）
date: 2022-11-07 10:42+0800
description: 
tags: spack
giscus_comments: true
categories: icenv
---

# 准备
注：本教程均在Ubuntu:20.04镜像下演示。获取镜像并运行，

```bash
[wanlinwang@VM-119-18-tencentos ~]$ docker pull ubuntu:22.04
22.04: Pulling from library/ubuntu
aece8493d397: Pull complete 
Digest: sha256:2b7412e6465c3c7fc5bb21d3e6f1917c167358449fecac8176c6e496e5c1f05f
Status: Downloaded newer image for ubuntu:22.04
docker.io/library/ubuntu:22.04
[wanlinwang@VM-119-18-tencentos ~]$ docker run -ti ubuntu:22.04
root@284b243a39ec:/# cd
root@284b243a39ec:~#
```

安装相关依赖包（其中git用来与git仓库交互，python3用作spack的解析器，gcc gfortran fort77 g++ clang用作spack构建工具时的编译器，make构建），

```bash
root@284b243a39ec:~# apt update
root@284b243a39ec:~# apt install git python3
root@284b243a39ec:~# apt install gcc gfortran fort77 g++ clang
root@284b243a39ec:~# apt install make
```

下载spack，

```bash
root@284b243a39ec:~# git clone --depth=100 --branch=releases/v0.20 https://github.com/spack/spack.git ~/spack
Cloning into '/root/spack'...
remote: Enumerating objects: 19032, done.
remote: Counting objects: 100% (19032/19032), done.
remote: Compressing objects: 100% (10494/10494), done.
remote: Total 19032 (delta 2022), reused 12091 (delta 1506), pack-reused 0
Receiving objects: 100% (19032/19032), 12.33 MiB | 15.21 MiB/s, done.
Resolving deltas: 100% (2022/2022), done.
root@284b243a39ec:~# cd ~/spack
```

初始化，

```bash
root@284b243a39ec:~/spack# . share/spack/setup-env.sh
root@284b243a39ec:~/spack# spack compiler find
```

# 上手
`spack list`查看所有可用的包，
```bash
root@284b243a39ec:~/spack# spack list
```
![image](https://github.com/icinfra/icinfra.github.io/assets/32032219/e3c28374-ff18-485f-ae6a-abb367890a02)

`spack list`支持查询语句
```bash
root@284b243a39ec:~/spack# spack list pytho* #前缀匹配查询
python
==> 1 packages
root@284b243a39ec:~/spack# spack list pytho #模糊匹配查询
py-antlr4-python3-runtime    py-ipython                 py-mysql-connector-python  py-python-constraint  py-python-engineio    py-python-jose            py-python-louvain        py-python-memcached  py-python-socketio     py-python3-openid    py-systemd-python
py-avro-python3              py-ipython-cluster-helper  py-openslide-python        py-python-crfsuite    py-python-fmask       py-python-json-logger     py-python-lsp-jsonrpc    py-python-multipart  py-python-sotools      py-python3-xlib      py-types-python-dateutil
py-biopython                 py-ipython-genutils        py-psij-python             py-python-daemon      py-python-fsutil      py-python-keystoneclient  py-python-lsp-server     py-python-oauth2     py-python-subunit      py-pythonqwt         py-wxpython
py-bx-python                 py-kb-python               py-python-benedict         py-python-dateutil    py-python-gitlab      py-python-ldap            py-python-lzo            py-python-picard     py-python-swiftclient  py-pythonsollya      python
py-dnspython                 py-meson-python            py-python-bioformats       py-python-docs-theme  py-python-igraph      py-python-levenshtein     py-python-magic          py-python-ptrace     py-python-utils        py-saga-python       r-findpython
py-gitpython                 py-mkdocstrings-python     py-python-box              py-python-dotenv      py-python-javabridge  py-python-libsbml         py-python-mapnik         py-python-rapidjson  py-python-xlib         py-scientificpython  xtensor-python
py-google-api-python-client  py-mmtf-python             py-python-certifi-win32    py-python-editor      py-python-jenkins     py-python-logstash        py-python-markdown-math  py-python-slugify    py-python-xmp-toolkit  py-spython
==> 76 packages
```

安装一个包，命名`spack install <package_name>`
```bash
root@284b243a39ec:~/spack# spack install zlib
==> Installing zlib-1.2.13-ivmy4r5hq6uijii4yspbffl2dutqdxgb
==> No binary for zlib-1.2.13-ivmy4r5hq6uijii4yspbffl2dutqdxgb found: installing from source
==> Using cached archive: /root/spack/var/spack/cache/_source-cache/archive/b3/b3a24de97a8fdbc835b9833169501030b8977031bcb54b3b3ac13740f846ab30.tar.gz
==> No patches needed for zlib
==> zlib: Executing phase: 'edit'
==> zlib: Executing phase: 'build'
==> zlib: Executing phase: 'install'
==> zlib: Successfully installed zlib-1.2.13-ivmy4r5hq6uijii4yspbffl2dutqdxgb
  Stage: 0.04s.  Edit: 0.38s.  Build: 0.61s.  Install: 0.05s.  Post-install: 0.02s.  Total: 1.12s
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/zlib-1.2.13-ivmy4r5hq6uijii4yspbffl2dutqdxgb
```

Spack安装包时，支持从源码安装，或者从二进制缓存安装。二进制缓存的安全，由GPG签名保证。
```bash
root@284b243a39ec:~/spack# spack mirror add tutorial /mirror
root@284b243a39ec:~/spack# spack buildcache keys --install --trust
==> Fetching file:///mirror/build_cache/_pgp/0ACDCFDA91DB974A68C3DDC2F85815B32355CB19.pub
gpg: key F85815B32355CB19: public key "e4s-uo-spack-01" imported
gpg: Total number processed: 1
gpg:		   imported: 1
gpg: inserting ownertrust of 6
==> Fetching file:///mirror/build_cache/_pgp/2C8DD3224EF3573A42BD221FA8E0CA3C1C2ADA2F.pub
gpg: key A8E0CA3C1C2ADA2F: 5 signatures not checked due to missing keys
gpg: key A8E0CA3C1C2ADA2F: public key "Spack Project Official Binaries <maintainers@spack.io>" imported
gpg: Total number processed: 1
gpg:		   imported: 1
gpg: marginals needed: 3  completes needed: 1  trust model: pgp
gpg: depth: 0  valid:	1  signed:   0	trust: 0-, 0q, 0n, 0m, 0f, 1u
gpg: inserting ownertrust of 6
==> Fetching file:///mirror/build_cache/_pgp/78F3726939CA1B94893B66E8BC86F6FB94429164.pub
gpg: key A8E0CA3C1C2ADA2F: 7 signatures not checked due to missing keys
gpg: key A8E0CA3C1C2ADA2F: "Spack Project Official Binaries <maintainers@spack.io>" 3 new signatures
gpg: key A8E0CA3C1C2ADA2F: "Spack Project Official Binaries <maintainers@spack.io>" 1 new subkey
gpg: Total number processed: 1
gpg:		new subkeys: 1
gpg:	     new signatures: 3
gpg: marginals needed: 3  completes needed: 1  trust model: pgp
gpg: depth: 0  valid:	2  signed:   0	trust: 0-, 0q, 0n, 0m, 0f, 2u
```
```bash
spack install zlib %clang
==> Installing zlib-1.2.13-gephbceg3rl2e77o46xyzlk5e4kd3gt3
==> Fetching file:///mirror/build_cache/linux-ubuntu22.04-x86_64_v3-clang-14.0.0-zlib-1.2.13-gephbceg3rl2e77o46xyzlk5e4kd3gt3.spec.json.sig
==> Fetching file:///mirror/build_cache/linux-ubuntu22.04-x86_64_v3/clang-14.0.0/zlib-1.2.13/linux-ubuntu22.04-x86_64_v3-clang-14.0.0-zlib-1.2.13-gephbceg3rl2e77o46xyzlk5e4kd3gt3.spack
==> Extracting zlib-1.2.13-gephbceg3rl2e77o46xyzlk5e4kd3gt3 from binary cache
==> zlib: Successfully installed zlib-1.2.13-gephbceg3rl2e77o46xyzlk5e4kd3gt3
  Search: 0.00s.  Fetch: 0.11s.  Install: 0.02s.  Total: 0.13s
[+] /root/spack/opt/spack/linux-ubuntu22.04-x86_64_v3/clang-14.0.0/zlib-1.2.13-gephbceg3rl2e77o46xyzlk5e4kd3gt3
```

在运行安装命令前，可以先查看有哪些版本，
```bash
root@284b243a39ec:~/spack# spack versions zlib
==> Safe versions (already checksummed):
  1.2.13  1.2.12  1.2.11  1.2.8  1.2.3
==> Remote versions (not yet checksummed):
  1.3     1.2.9    1.2.7.2  1.2.7    1.2.6    1.2.5.2  1.2.5    1.2.4.4  1.2.4.2  1.2.4    1.2.3.8  1.2.3.6  1.2.3.4  1.2.3.2  1.2.2.4  1.2.2.2  1.2.2    1.2.1.1  1.2.0.8  1.2.0.6  1.2.0.4  1.2.0.2  1.2.0  1.1.3  1.1.1  1.0.9  1.0.7  1.0.5  1.0.2  1.0-pre  0.95  0.93  0.91  0.71  0.8
  1.2.10  1.2.7.3  1.2.7.1  1.2.6.1  1.2.5.3  1.2.5.1  1.2.4.5  1.2.4.3  1.2.4.1  1.2.3.9  1.2.3.7  1.2.3.5  1.2.3.3  1.2.3.1  1.2.2.3  1.2.2.1  1.2.1.2  1.2.1    1.2.0.7  1.2.0.5  1.2.0.3  1.2.0.1  1.1.4  1.1.2  1.1.0  1.0.8  1.0.6  1.0.4  1.0.1  0.99     0.94  0.92  0.79  0.9
```

安装时，可以传编译器flags，如cppflags, cflags, cxxflags, fflags, ldflags, 与 ldlibs 参数。
```bash
root@284b243a39ec:~/spack# spack install zlib@1.2.8 cflags=-O3
==> Warning: using "zlib@1.2.8" which is a deprecated version
==> Installing zlib-1.2.8-5o535gi4wwtrfcb3jcilmuelp57hnyxq
==> No binary for zlib-1.2.8-5o535gi4wwtrfcb3jcilmuelp57hnyxq found: installing from source
==> Warning: zlib@1.2.8 is deprecated and may be removed in a future Spack release.
==>   Fetch anyway? [y/N] y
==> Fetching https://mirror.spack.io/_source-cache/archive/36/36658cb768a54c1d4dec43c3116c27ed893e88b02ecfcb44f2166f9c0b7f2a0d.tar.gz
==> No patches needed for zlib
==> zlib: Executing phase: 'edit'
==> zlib: Executing phase: 'build'
==> zlib: Executing phase: 'install'
==> zlib: Successfully installed zlib-1.2.8-5o535gi4wwtrfcb3jcilmuelp57hnyxq
  Stage: 44.96s.  Edit: 0.38s.  Build: 0.56s.  Install: 0.07s.  Post-install: 0.02s.  Total: 46.01s
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/zlib-1.2.8-5o535gi4wwtrfcb3jcilmuelp57hnyxq
```

`spack find`查看已安装的包，
```bash
root@284b243a39ec:~/spack# spack find
-- linux-ubuntu22.04-cascadelake / clang@14.0.0 -----------------
zlib@1.2.12  zlib@1.2.13

-- linux-ubuntu22.04-cascadelake / gcc@11.4.0 -------------------
zlib@1.2.8  zlib@1.2.13
==> 4 installed packages
root@284b243a39ec:~/spack# spack find -lf
-- linux-ubuntu22.04-cascadelake / clang@14.0.0 -----------------
phqllhi zlib@1.2.12%clang   r5taitb zlib@1.2.13%clang 

-- linux-ubuntu22.04-cascadelake / gcc@11.4.0 -------------------
5o535gi zlib@1.2.8%gcc  cflags="-O3"   ivmy4r5 zlib@1.2.13%gcc 
==> 4 installed packages
```

Spack为每个spec都生成一个hash，任何不同版本组合都生成唯一的hash。
```bash
root@284b243a39ec:~/spack# spack install tcl
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/zlib-1.2.13-ivmy4r5hq6uijii4yspbffl2dutqdxgb
==> Installing tcl-8.6.12-m2wnkqeddps4xf5oyrxqd6i3lrvokfwp
==> No binary for tcl-8.6.12-m2wnkqeddps4xf5oyrxqd6i3lrvokfwp found: installing from source
==> Fetching https://mirror.spack.io/_source-cache/archive/26/26c995dd0f167e48b11961d891ee555f680c175f7173ff8cb829f4ebcde4c1a6.tar.gz
==> No patches needed for tcl
==> tcl: Executing phase: 'autoreconf'
==> tcl: Executing phase: 'configure'
==> tcl: Executing phase: 'build'
==> tcl: Executing phase: 'install'
==> tcl: Successfully installed tcl-8.6.12-m2wnkqeddps4xf5oyrxqd6i3lrvokfwp
  Stage: 14.43s.  Autoreconf: 0.00s.  Configure: 5.85s.  Build: 1m 2.43s.  Install: 3.53s.  Post-install: 0.59s.  Total: 1m 26.86s
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/tcl-8.6.12-m2wnkqeddps4xf5oyrxqd6i3lrvokfwp
```

使用`^`指定依赖
```bash
root@284b243a39ec:~/spack# spack install tcl ^zlib@1.2.13 %clang
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/clang-14.0.0/zlib-1.2.13-r5taitbmvh5nzn2jqjo2f2mignhvrabe
==> Installing tcl-8.6.12-lgob6rq7jo5q3dyd2qfhyrs3nk6ggpqe
==> No binary for tcl-8.6.12-lgob6rq7jo5q3dyd2qfhyrs3nk6ggpqe found: installing from source
==> Using cached archive: /root/spack/var/spack/cache/_source-cache/archive/26/26c995dd0f167e48b11961d891ee555f680c175f7173ff8cb829f4ebcde4c1a6.tar.gz
==> No patches needed for tcl
==> tcl: Executing phase: 'autoreconf'
==> tcl: Executing phase: 'configure'
==> tcl: Executing phase: 'build'
==> tcl: Executing phase: 'install'
==> tcl: Successfully installed tcl-8.6.12-lgob6rq7jo5q3dyd2qfhyrs3nk6ggpqe
  Stage: 0.36s.  Autoreconf: 0.00s.  Configure: 10.13s.  Build: 1m 13.37s.  Install: 3.34s.  Post-install: 0.58s.  Total: 1m 27.82s
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/clang-14.0.0/tcl-8.6.12-lgob6rq7jo5q3dyd2qfhyrs3nk6ggpqe
```

使用`^/5o5`指定依赖的hash。如上所示，其中5o5是zlib@1.2.8%gcc的hash。
```bash
root@284b243a39ec:~/spack# spack install tcl ^/5o5
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/zlib-1.2.8-5o535gi4wwtrfcb3jcilmuelp57hnyxq
==> Installing tcl-8.6.12-o6wvao34ytjgbpy2kpf63x4c34wn45ub
==> No binary for tcl-8.6.12-o6wvao34ytjgbpy2kpf63x4c34wn45ub found: installing from source
==> Using cached archive: /root/spack/var/spack/cache/_source-cache/archive/26/26c995dd0f167e48b11961d891ee555f680c175f7173ff8cb829f4ebcde4c1a6.tar.gz
==> No patches needed for tcl
==> tcl: Executing phase: 'autoreconf'
==> tcl: Executing phase: 'configure'
==> tcl: Executing phase: 'build'
==> tcl: Executing phase: 'install'
==> tcl: Successfully installed tcl-8.6.12-o6wvao34ytjgbpy2kpf63x4c34wn45ub
  Stage: 0.35s.  Autoreconf: 0.00s.  Configure: 6.08s.  Build: 1m 1.70s.  Install: 3.45s.  Post-install: 0.59s.  Total: 1m 12.21s
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/tcl-8.6.12-o6wvao34ytjgbpy2kpf63x4c34wn45ub
```

`spack find`还支持`-d`，用来显示依赖关系。
```bash
root@284b243a39ec:~/spack# spack find -ldf
-- linux-ubuntu22.04-cascadelake / clang@14.0.0 -----------------
lgob6rq tcl@8.6.12%clang 
r5taitb     zlib@1.2.13%clang 

phqllhi zlib@1.2.12%clang 

r5taitb zlib@1.2.13%clang 


-- linux-ubuntu22.04-cascadelake / gcc@11.4.0 -------------------
o6wvao3 tcl@8.6.12%gcc 
5o535gi     zlib@1.2.8%gcc  cflags="-O3" 

m2wnkqe tcl@8.6.12%gcc 
ivmy4r5     zlib@1.2.13%gcc 

5o535gi zlib@1.2.8%gcc  cflags="-O3" 

ivmy4r5 zlib@1.2.13%gcc 

==> 7 installed packages
```

我们来安装一个更复杂的包——HDF5，默认情况下，会将MPI依赖也装上。
```bash
root@284b243a39ec:~/spack# spack install hdf5
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/libpciaccess-0.17-pykx2euy2awtgyou2nnsjl2s6hi4n646
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/libiconv-1.17-yodoqmhmvqbqvjzl3s6snnatz6trv7iy
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/xz-5.4.1-dzgxjank6ou2hybibf5ub262lgc2lorn
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/zlib-1.2.13-ivmy4r5hq6uijii4yspbffl2dutqdxgb
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/ncurses-6.4-ujngusmjurwe2fa7l3b6kvt73gabtuor
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/numactl-2.0.14-r22sabf66foyohnzrm2vhslqhyvzaodc
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/bzip2-1.0.8-ddoyjf47vjlyagfc22epabwym5pymdr7
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/zstd-1.5.5-5e3alsszldfqzfm4bln3x2bxo63lgc5h
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/libxcrypt-4.4.33-gei6nykcbdwqnwkbtaapysokbdy5hsa5
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/pkgconf-1.9.5-sxbb6ve36mznc2trrpk4llouoi47yqlm
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/pigz-2.7-5gemoganu6n6ps7aca4llw5txrxgwcm7
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/openssl-1.1.1t-vmachqinwttmfsngz56nzjlsdxpvp7ki
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/libedit-3.1-20210216-d7fgamjkvusfpwqhdevl5u3ld2ajwelz
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/libxml2-2.10.3-5mmkszwox2ca75c274cebzp7yizhvant
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/tar-1.34-tfgqkhebvyigwree5sh4jxtt2r6ebkhn
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/libevent-2.1.12-zt3qad4mu4mlsfmedkakxw7ue4ekrudc
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/hwloc-2.9.1-fcfzcph73hlkt23vthevpninsi7jbfdp
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/gettext-0.21.1-y3smi3ultsqlwsrwzcykwzl52h4eekhg
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/pmix-4.2.3-h55tf5zun6v6kxuszej6imea7sfb7lku
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/krb5-1.20.1-imoj7v4sveupl2komhnb655d3jjxeyez
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/openssh-9.3p1-pi6fj3d4bnbsvdzjygatwmeppme2e57o
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/openmpi-4.1.5-z2lpbjfjf72tikfaxfuq7keby327rang
==> Installing hdf5-1.14.1-2-gqyhwfo3iyea3sdekxcolo5qrnnuzlqn
==> No binary for hdf5-1.14.1-2-gqyhwfo3iyea3sdekxcolo5qrnnuzlqn found: installing from source
==> Fetching https://mirror.spack.io/_source-cache/archive/cb/cbe93f275d5231df28ced9549253793e40cd2b555e3d288df09d7b89a9967b07.tar.gz
==> Ran patch() for hdf5
==> hdf5: Executing phase: 'cmake'
==> hdf5: Executing phase: 'build'
==> hdf5: Executing phase: 'install'
==> hdf5: Successfully installed hdf5-1.14.1-2-gqyhwfo3iyea3sdekxcolo5qrnnuzlqn
  Stage: 31.03s.  Cmake: 11.47s.  Build: 30.78s.  Install: 0.90s.  Post-install: 0.20s.  Total: 1m 14.55s
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/hdf5-1.14.1-2-gqyhwfo3iyea3sdekxcolo5qrnnuzlqn
```

Spack包也有build选项，通过+或~/-
```bash
root@284b243a39ec:~/spack# spack install hdf5~mpi
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/ncurses-6.4-ujngusmjurwe2fa7l3b6kvt73gabtuor
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/zlib-1.2.13-ivmy4r5hq6uijii4yspbffl2dutqdxgb
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/gmake-4.4.1-264topq36ww6abmwthbd7pouu65v7nwm
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/pkgconf-1.9.5-sxbb6ve36mznc2trrpk4llouoi47yqlm
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/openssl-1.1.1t-vmachqinwttmfsngz56nzjlsdxpvp7ki
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/cmake-3.26.3-ttvpnusqvmowfgfwiwil7dgkmkjaiqp5
==> Installing hdf5-1.14.1-2-thweeqbqmd7uqugx6iswe56zarcgg554
==> No binary for hdf5-1.14.1-2-thweeqbqmd7uqugx6iswe56zarcgg554 found: installing from source
==> Using cached archive: /root/spack/var/spack/cache/_source-cache/archive/cb/cbe93f275d5231df28ced9549253793e40cd2b555e3d288df09d7b89a9967b07.tar.gz
==> Ran patch() for hdf5
==> hdf5: Executing phase: 'cmake'
==> hdf5: Executing phase: 'build'
==> hdf5: Executing phase: 'install'
==> hdf5: Successfully installed hdf5-1.14.1-2-thweeqbqmd7uqugx6iswe56zarcgg554
  Stage: 0.83s.  Cmake: 10.69s.  Build: 27.12s.  Install: 0.88s.  Post-install: 0.18s.  Total: 39.84s
[+] /root/spack/opt/spack/linux-ubuntu22.04-cascadelake/gcc-11.4.0/hdf5-1.14.1-2-thweeqbqmd7uqugx6iswe56zarcgg554
```

Spack还可以通过^来指定依赖
```bash
root@284b243a39ec:~/spack# spack install hdf5+hl+mpi ^mpich
```

Spack可以打印依赖的单向无环图(DAG)
```bash
spack graph hdf5+hl+mpi ^mpich
```

再安装一个更复杂的，
```bash
spack install trilinos
```
这个直接依赖有23个，依赖又有自己的依赖。经验丰富的用户可能也需要花几天、几周来完成，而spack一条命令几秒钟搞定。


DAG输出到PDF文件，
```bash
spack graph --dot trilinos | dot -Tpdf > trilinos_graph.pdf
```

uninstall包
```bash
spack uninstall
```

`spack find`也支持高级查询，包括
```bash
spack find ^mpich #查询依赖mpich的包
spack find cflags=-O3 #查询带这个编译选项的
```

将spack安装的gcc加入spack编译器列表里，
```bash
spack compiler add "$(spack location -i gcc@12)"
```

将gcc编译器移出spack编译器列表，
```bash
spack compiler remove gcc@12
```

