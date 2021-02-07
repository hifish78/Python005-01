'''
选做:：
可以基于 Django+ redis 实现，使用 redis 作为 Django 后端可参考如下代码：
https://django-redis-chs.readthedocs.io/zh_CN/latest/

作业二：在使用短信群发业务时，公司的短信接口限制接收短信的手机号，每分钟最多发送五次，请基于 Python 和 redis 实现如下的短信发送接口：
已知有如下函数：
复制代码

	def sendsms(telephone_number: int, content: string, key=None)：
	    # 短信发送逻辑, 作业中可以使用 print 来代替
	    pass
	    # 请实现每分钟相同手机号最多发送五次功能, 超过 5 次提示调用方,1 分钟后重试稍后
	    pass
	    print("发送成功")

期望执行结果：

sendsms(12345654321, content=“hello”) # 发送成功
sendsms(12345654321, content=“hello”) # 发送成功
…
sendsms(88887777666, content=“hello”) # 发送成功
sendsms(12345654321, content=“hello”) # 1 分钟内发送次数超过 5 次, 请等待 1 分钟
sendsms(88887777666, content=“hello”) # 发送成功
'''
import redis
import time

# decode_response=True --> so no need to do decode()
client = redis.Redis(host='127.0.0.1', password='Test@1c',decode_responses=True)

def sendsms(telephone_number, context, key=None):
    # key- 手机号
    # value - 发送到次数
    # ex: key的过期时间
    client.set(telephone_number, 0, nx=True, ex=60)

    # move 到CHECK后面，减少不必要到INCR调用
    # client.incr(telephone_number)
    if int(client.get(telephone_number)) < 5:
        print(context)
        print('sent msg successfully')
    else:
        print('Please wait for 1 min since you have sent 5 msg in 1 min')
    client.incr(telephone_number)
client.delete(12345679)
while True:
    sendsms(12345679, 'hello world')
    time.sleep(1)

