# 多线程

> Python创建多线程的方法此处不再赘述。

## 1. 线程通信机制

要实现对多个线程进行控制，其实本质上就是消息机制，利用消息机制发送指令来控制线程。

**线程通信方法**

- 事件：`threading.Event`
- 条件：`threading.Condition`
- 队列：`queue.Queue`

## 2. Event 事件

Python 提供了非常简单的通信机制 `Threading.Event`，通用条件变量，多个线程可以通过等待某个事件的发生，在事件发生之后，所有的线程都会被激活。

```python
event = threading.Event()

# 重置event，使得该event处于待命状态
event.clear()
# 等待接收event的指令，决定是否阻塞程序的执行
event.wait()
# 发送event指令，使所有设置该event事件的线程执行
event.set()
```

**示例：**

```python
import time
import threading

class MyThread(threading.Thread):
    def __init__(self, name, event):
        super().__init__()
        self.name = name
        self.event = event
    
    def run(self):
        print("Thread: {0} start at {1}".format(self.name, time.ctime(time.time())))
        self.event.wait()
        print("Thread: {0} finished at {1}".format(self.name, time.ctime(time.time())))
        
event = threading.Event()
threads = [MyThread(str(i), event) for i in range(1, 5)]
event.clear()
for item in threads:
    item.start()
print('等待5s...')
time.sleep(5)
print('唤醒所有线程...')
event.start()
```

输出：

```
Thread: 1 start at Sun May 13 20:38:08 2018
Thread: 2 start at Sun May 13 20:38:08 2018
Thread: 3 start at Sun May 13 20:38:08 2018
Thread: 4 start at Sun May 13 20:38:08 2018
等待5s...
唤醒所有线程...
Thread: 1 finish at Sun May 13 20:38:13 2018
Thread: 4 finish at Sun May 13 20:38:13 2018
Thread: 2 finish at Sun May 13 20:38:13 2018
Thread: 3 finish at Sun May 13 20:38:13 2018
```

可见在所有线程启动后，线程并不会执行完成，而是在 `self.event.wait()` 处停止了，需要我们通过 `event.set()` 来给所有线程发送指令才能继续执行。

## 3. Condition

Condition和Event 是类似的，并没有多大区别。

```python
cond = threading.Condition()

# 类似lock.acquire()
cond.acquire()

# 类似lock.release()
cond.release()

# 等待指定触发，同时会释放对锁的获取,直到被notify才重新占有琐。
cond.wait()

# 发送指定，触发执行
cond.notify()
```

**示例：**

```python
import threading, time

class Hider(threading.Thread):
    def __init__(self, cond, name):
        super(Hider, self).__init__()
        self.cond = cond
        self.name = name

    def run(self):
        time.sleep(1)  #确保先运行Seeker中的方法
        self.cond.acquire()

        print(self.name + ': 我已经把眼睛蒙上了')
        self.cond.notify()
        self.cond.wait()
        print(self.name + ': 我找到你了哦 ~_~')
        self.cond.notify()

        self.cond.release()
        print(self.name + ': 我赢了')

class Seeker(threading.Thread):
    def __init__(self, cond, name):
        super(Seeker, self).__init__()
        self.cond = cond
        self.name = name

    def run(self):
        self.cond.acquire()
        self.cond.wait()
        print(self.name + ': 我已经藏好了，你快来找我吧')
        self.cond.notify()
        self.cond.wait()
        self.cond.release()
        print(self.name + ': 被你找到了，哎~~~')

cond = threading.Condition()
seeker = Seeker(cond, 'seeker')
hider = Hider(cond, 'hider')
seeker.start()
hider.start()
```

输出：

```
hider:   我已经把眼睛蒙上了
seeker:  我已经藏好了，你快来找我吧
hider:   我找到你了 ~_~
hider:   我赢了
seeker:  被你找到了，哎~~~
```

## 3. Queue

从一个线程向另一个线程发送数据的最安全的方式可能就是使用queue库中的队列了，创建一个被多个线程共享的 Queue 对象，这些线程使用 `put()` 和 `get()` 操作来向队列中发送和获取数据。

```python
from queue import Queue
# maxsize默认为0，不受限
# 一旦>0，而消息数又达到限制，q.put()也将阻塞
q = Queue(maxsize=0)

# 默认阻塞程序，等待队列消息，可设置超时时间
q.get(block=True, timeout=None)

# 发送消息：默认会阻塞程序至队列中有空闲位置放入数据
q.put(item, block=True, timeout=None)

# 等待所有的消息都被消费完
q.join()

# 通知队列任务处理已经完成，当所有任务都处理完成时，join() 阻塞将会解除
q.task_done()
```

