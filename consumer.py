import pika
import logging
import os

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# RabbitMQ连接参数
connection_params = pika.ConnectionParameters('192.168.1.8')

def callback(ch, method, properties, body):
    logger.info(f"Received message: {body}")

try:
    # 建立连接
    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    
    # 声明队列
    channel.queue_declare(queue='hello')
    
    # 设置消费回调
    channel.basic_consume(queue='hello',
                          auto_ack=True,
                          on_message_callback=callback)
    
    logger.info('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

except pika.exceptions.AMQPConnectionError as e:
    logger.error(f"无法连接到RabbitMQ服务器: {e}")
except KeyboardInterrupt:
    logger.info("消费者已停止")
except Exception as e:
    logger.error(f"发生错误: {e}")
