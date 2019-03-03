# ResourceManagement

## 简介

`ResourceManagement`是一个资源管理系统，目前支持 MySQL、Redis 实例的申请，实例运行在 Docker 里面。本系统以 RESTful API 接口的形式与外界进行交互。

## 快速开始

### 准备工作
* 安装 docker、redis、python3
* 配置环境变量
  * `DOCKER_PATH`，Docker 套接字地址，默认为`unix://var/run/docker.sock`
  * `REDIS_HOST`，redis 的地址，默认为`localhost`
  * `REDIS_PORT`，redis 的端口，默认为`6379`
  * `ENV`，当前所处的开发环境，默认为`dev`
    * `ENV == dev`时，为开发环境。具体表现为修改代码后服务会自动重启，发生异常时的返回信息更加详细
        ```json
        {
            "error": {
                "code": 500,
                "message": "Internal Server Error",
                "traceback": [
                    "Traceback (most recent call last):",
                    "File '/root/apps/ResourceManagement/env/lib/python3.5/site-packages/tornado/web.py'," ,
                    "line 1510, in _execute: result = method(*self.path_args, **self.path_kwargs)",
                    "TypeError: get() missing 1 required positional argument: 'resource_name'"
                ]
            }
        }
        ```

    * `ENV != dev` 时，为生产环境，发生异常时返回信息较为简略
        
        ```json
        {
            "error": {
                "code": 500,
                "message": "Internal Server Error"
            }
        }
        ```

### 构建

* 清除构建遗留文件
```shell
make clean
```

* 构建
```shell
make
```

### 运行

* 跑测试用例
```shell
make test
```

* 运行 web 服务
```shell
env/bin/web
# Options:
#
#     --port  # 指定服务运行的端口，默认为 8000
```

  
## API 接口

### 获取资源信息
#### Request
* Method: **GET**
* URL:  `/api/resources/{resource_type}/{resource_name}`
    * `resource_type`: 资源类型，目前有 redis, mysql
    * `resource_name`: 资源名称，唯一
    * 例子:
      * 查看 redis 实例信息: ```/api/resources/redis/r12```
      * 查看 mysql 实例信息:  ```/api/resources/mysql/m11```

#### Response
```
# get /api/resources/redis/r32
# return:
{
    # ID, 唯一
    "resource_id": "5c0d193556259ed8d09bb",
    # 资源名，唯一
    "resource_name": "r32",
    # 服务器公网IP
    "server_ip": "172.20.10.5",
    # 对外端口
    "exposed_port": "32793",
    # 数据库密码
    "db_password": "61VmB9Rh",
    # 运行平台
    "platform": "linux",
    # 容器状态
    "status": "running",
    # docker image version
    "image_version": "redis:5.0",
    # 连接数据库的语句
    "connect_string": "redis-cli -h 172.20.10.5 -p 32793 -a 61VmB9Rh"
}

# 实例不存在时
# return:
{
    "error": {
        "code": 404,
        "message": "Not such resource(redis:m23)"
    }
}
```

### 申请资源
#### Request
* Method: **POST**
* URL:  `/api/resources/{resource_type}`
    * `resource_type`: 资源类型，目前有 redis, mysql
    * 支持自定配置义资源, 只需在请求的 Body 里面附带参数即可:
      * redis 支持的参数
        * `dbfilename`: redis 持久化(全量)的文件名，默认为`dump.rdb`
        * `maxmemory`: 最大内存用量, 默认为`1GB`
        * `appendonly`: 是否使用 AOF 持久化，默认为`yes`
        * `appendfilename`: AOF 持久化的文件名，默认为`appendonly.aof`
      * mysql 支持的参数
        * `character`:数据库字符集，默认为`utf8`

  
> 注意：由于这些配置项的值很多，编写校验规则较为耗时和麻烦，加上没有找到现成的可以检查 mysql 或 redis 配置文件是否正确的库，所以暂时不做参数的检验，传入错误的配置参数时，会导致资源创建失败

#### Response
```
# post /api/resources/redis
# return:
{
    # ID, 唯一
    "resource_id": "5c0d193556259ed8d09bb",
    # 资源名，唯一
    "resource_name": "r32",
    # 服务器公网IP
    "server_ip": "172.20.10.5",
    # 对外端口
    "exposed_port": "32793",
    # 数据库密码
    "db_password": "61VmB9Rh",
    # 运行平台
    "platform": "linux",
    # 容器状态
    "status": "running",
    # docker image version
    "image_version": "redis:5.0",
    # 连接数据库的语句
    "connect_string": "redis-cli -h 172.20.10.5 -p 32793 -a 61VmB9Rh"
}

# 当创建失败时
# return:
{
    "error": {
        "code": 500,
        "message": "Failed to create resource, check your parameters(maybe your parameter is wrong)"
    }
}
```
  
## Q&A

**Q: 实例如何运行？**

A: 放到 Docker 上，容器化运行。

**Q: 容器的数据如何存放？**

A: 创建资源时，首先会创建一个`/docker_data/{resource_type}/{resource_name}/data`目录作为数据卷，然后在创建容器时，把该目录挂载到容器相应存储数据的目录即可(例如 mysql 在容器中存储数据的目录是`/var/lib/mysql`，就可以让服务器的 `/docker_data/{resource_type}/{resource_name}/data` 挂载到容器中的 `/var/lib/mysql`)

**Q: 怎么实现配置自定义？**

A: 预先写好配置文件的模板，然后在创建资源时，根据已有的配置模板和传进来的配置项，生成配置文件到指定的目录(例如mysql的为`/docker_data/{resource_type}/{resource_name}/my.cnf`), 然后把该文件挂载到容器即可。

**Q: 怎么保证资源名(resource_name)唯一？**

A: 用 redis 的 incr 来实现唯一ID的发放。


> 为了方便申请资源，服务已部署到云服务器上，可直接通过 http://119.23.223.90:9000 管理资源，例如使用 post http://119.23.223.90:9000/api/resources/redis 可申请 redis 资源