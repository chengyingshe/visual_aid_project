import threading
import time

def task(name, delay):
    """
    定义一个任务函数，接收线程名称和延迟时间作为参数，
    该任务将打印线程名称，并休眠指定的延迟时间。
    """
    print(f"线程 {name} 正在执行")
    time.sleep(delay)
    print(f"线程 {name} 执行完成")

# 创建线程对象列表
threads = []

# 定义要创建的线程数量
num_threads = 5

# 创建并启动线程
for i in range(num_threads):
    thread = threading.Thread(target=task, args=(f"`线程-{i+1}`", 2))  # 每个线程休眠2秒
    threads.append(thread)
    thread.start()

# 等待所有线程执行完毕
for thread in threads:
    thread.join()

print("所有线程执行完毕")
