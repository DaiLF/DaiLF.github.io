# 线程中的锁机制

> 当对一段代码加锁时，意味着在同一时间内只能有一个线程执行这段代码。

**Python中的锁可以分为两种：**

- 互斥锁
- 可重入锁

## 1.1 互斥锁（Lock）

```python
import threading

# 创建全局锁对象
lock = threading.Lock()
# 获取锁，未获取到锁的话会阻塞程序，直到获取到锁
lock.acquire()
# 释放锁
lock.release()
```

😂 `lock.acquire()` 和 `lock.release()` 必须成对使用，不然会造成死锁。

最佳使用方式是使用 `with` 上下文管理器：

```python
lock = threading.Lock()
with lock:
    # code block
    pass
```

## 1.2 可重入锁（RLock）

有时在同一个线程中，我们可能多次请求同一个资源，称为**嵌套锁**。

如果直接使用互斥锁，代码如下，会造成死锁：

```python
import threading

def main():
    num = 0
    lock = threading.Lock()
    with lock:
        for i in range(10):
            num += 1
            with lock:
                print(num)
t = threading.Thread(target=main)
t.start()
```

上面的代码会直接造成死锁，因为第二次获取锁的时候，第一次获取的锁并没有释放，所以会一直在 `lock.acquire()` 处阻塞。

为了解决这个问题，需要使用重入锁（RLock）来专门处理这个问题：

```python
import threding

def main():
    num = 0
    rlock = threading.RLock()
    with rlock:
        for i in range(10):
            num += 1 
    		with rlock:
                print(num)
t = threading.Thread(target=main)
t.start()
```

可重入锁只有在同一个线程中才可以重复获取锁，其他和互斥锁无异。



