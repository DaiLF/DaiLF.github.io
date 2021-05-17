## Dcoker安装Clickhouse


### 1. 安装 Docker

> 该教程指针对 CentOS，其它 Linux 发行版安装方法大同小异，百度即可。

⚡Docker 支持以下的 64 位 CentOS 版本：

- CentOS 7
- CentOS 8
- 更高版本...

#### 1.1 使用官方安装脚本自动安装

安装命令如下：

```shell
curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun
```

也可以使用国内 daocloud 一键安装命令：

```shell
curl -sSL https://get.daocloud.io/docker | sh
```

#### 1.2 手动安装

##### 1.2.1 先卸载旧版本（初次安装可以跳过）

```shell
sudo yum remove docker \
                docker-client \
                docker-client-latest \
                docker-common \
                docker-latest \
                docker-latest-logrotate \
                docker-logrotate \
                docker-engine
```

##### 1.2.2 使用 Docker 仓库进行安装

在新主机上首次安装 Docker Engine-Community 之前，需要设置 Docker 仓库。之后，您可以从仓库安装和更新 Docker。

###### 1.2.2.1 安装依赖

安装所需的软件包。yum-utils 提供了 yum-config-manager ，并且 device mapper 存储驱动程序需要 device-mapper-persistent-data 和 lvm2。

```shell
sudo yum install -y yum-utils \
                    device-mapper-persistent-data \
                    lvm2
```

###### 1.2.2.2 设置仓库

**阿里云**

```shell
sudo yum-config-manager --add-repo 
\ http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```

**清华大学**

```shell
sudo yum-config-manager --add-repo 
\ https://mirrors.tuna.tsinghua.edu.cn/docker-ce/linux/centos/docker-ce.repo
```

###### 1.2.2.3 安装 Docker Engine-Community

安装最新版本的 Docker Engine-Community 和 containerd，或者安装指定版本（自行百度）。

```shell
sudo yum install docker-ce docker-ce-cli containerd.io
```

#### 1.3 卸载 Docker 

删除安装包：

```shell
yum remove docker-ce
```

删除镜像、容器、配置文件等内容：

```shell
rm -rf /var/lib/docker
```

### 2. 安装 Clickhouse

#### 2.1 创建 Docker Clickhouse 挂载卷目录

> 创建挂载卷的目的是为了方便对 clickhouse 的配置文件修改，以及 clickhouse 数据、日志文件的保存等，关于 docker 挂载卷的具体详情，请自行百度。

```shell
mkdir -p /opt/ck/data
mkdir -p /opt/ck/conf
mkdir -p /opt/ck/log
 
chmod -R 777 /opt/ck/data
chmod -R 777 /opt/ck/conf
chmod -R 777 /opt/ck/log
```

#### 2.2 拉取 Clickhouse 的 Docker 镜像

默认拉取最新镜像，也可以拉去指定版本。

```shell
docker pull yandex/clickhouse-server
docker pull yandex/clickhouse-clinet
```

#### 2.3 创建临时 Clickhouse 容器

目的是为了将配置文件复制到宿主机

```shell
docker run --rm -d --name=clickhouse-server \
           --ulimit nofile=262144:262144 \
           -p 8123:8123 -p 9009:9009 -p 9090:9000 \
           yandex/clickhouse-server:latest
```

复制临时容器内配置文件到宿主机

```shell
docker cp clickhouse-server:/etc/clickhouse-server/config.xml /opt/ck/conf/config.xml
docker cp clickhouse-server:/etc/clickhouse-server/users.xml /opt/ck/conf/users.xml
```

关闭临时容器

```shell
docker stop clickhouse-server
```

修改clickhouse的用户密码需要在users.xml中配置，需要注意的是: 密码必须为加密过的形式, 否则会一直连不上。我们这次采用SHA256的方式加密。

```shell
PASSWORD=$(base64 < /dev/urandom | head -c8); echo "你的密码"; echo -n "你的密码" | sha256sum | tr -d '-'
```

执行以上命令后会在命令行打印密码明文和密码密文, 如下:

```
A940922h
dd2cef99d7122cd3e2455491f79b567400ce238b7eca309f73e089670df70eb6 
```

`vim /opt/ck/conf/user.xml` 修改用户密码

将`<password></password>` 修改为：

```xml
<password_sha256_hex> 密码密文 </password_sha256_hex>
```

#### 2.4 创建 Clickhouse 容器

```shell
docker run -d --name=clickhouse-server \
           -p 8123:8123 -p 9009:9009 -p 9090:9000 \
           --ulimit nofile=262144:262144 \
           -v /opt/ck/data:/var/lib/clickhouse:rw \
           -v /opt/ck/conf/config.xml:/etc/clickhouse-server/config.xml \
           -v /opt/ck/conf/users.xml:/etc/clickhouse-server/users.xml \
           -v /opt/ck/log:/var/log/clickhouse-server:rw \
           yandex/clickhouse-server:latest
```

### 3. 连接测试

Clickhouse 的 Python 驱动库比较多，下面使用 `clickhouse-driver` 和 `clickhouse-sqlalchemy` 进行连接测试。

#### 3.1 安装驱动

```shell
pip install clickhouse-driver
pip install clickhouse-sqlalchemy
```

#### 3.2 连接测试

```python
from clickhouse_driver import Client

client = Client(
    host="192.168.112.110",
    port="9000",
    user="default",
    password="admin"
)

sql = "show databases"
result = client.execute(sql)
print(result)
```

```python
from sqlalchemy import create_engine, Column, MetaData, literal
from clickhouse_sqlalchemy import Table, make_session, get_declarative_base, types, engines
from datetime import date, timedelta

uri = "clickhouse://default:<your_passwd>@<your_ip>:8123/<your_data_base>"
engine = create_engine(uri)
session = make_session(engine)
metadata = MetaData(bind=engine)
Base = get_declarative_base(metadata=metadata)


class Rate(Base):
    day = Column(types.Date, primary_key=True)
    value = Column(types.Int32)
    other_value = Column(
        types.DateTime,
        clickhouse_codec=('DoubleDelta', 'ZSTD'),
    )

    __table_args__ = (
        engines.Memory(),
    )


another_table = Table('another_rate', metadata,
                      Column('day', types.Date, primary_key=True),
                      Column('value', types.Int32, server_default=literal(1)),
                      engines.Memory()
                      )


table = Rate.__table__
table.create()
another_table.create()

today = date.today()
rates = [{'day': today - timedelta(i), 'value': 200 - i} for i in range(100)]

session.execute(table.insert(), rates)

data = session.query(Rate).all()
for item in data:
    print(item.day, " ", item.value)
```

