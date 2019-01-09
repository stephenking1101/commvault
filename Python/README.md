# Tool to invoke Commvault API

## Package Step
打包命令：python setup.py sdist

## Installation Step
```
# python ./setup.py install
```

This tool depends on below packages:  
'PyYAML', 'requests', 'openpyxl'

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
```
for /f %i in (install.log) do (del "%i" )
```

## Usage
Use "cvctl" to run this tool if it is installed. Or run "src\commander.py" directly.

```
usage: commander.py [-h] userName password {batchJob} ...

positional arguments:
  userName    user to login the CommServe
  password    password of the specific user
  {batchJob}  batchJob -h to show help
    batchJob  Bulk client/subclient creation and configuration

optional arguments:
  -h, --help  show this help message and exit
```

Example:

For Windows
```
python src\commander.py user password batchJob "C:\clientconfig.xlsx"
```