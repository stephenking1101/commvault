# Tool to invoke Commvault API

## Package Step
打包命令：python setup.py sdist

## Installation Step


## Uninstall Step
* 增加 –record 参数重新安装软件包，执行命令：
```
# python ./setup.py install --record install.log
```

* 删除安装文件，执行命令：
Linux:
```
# cat install.log | xargs rm -rf
```
Windows:
for /f %i in (install.log) do (del "%i" )