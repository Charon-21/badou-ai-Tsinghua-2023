# 该文件负责读取Cifar-10数据并对其进行数据增强预处理
import os
import tensorflow as tf

num_classes = 10

# 设定用于训练和评估的样本总数
num_examples_pre_epoch_for_train = 50000
num_examples_pre_epoch_for_eval = 10000


# 定义一个空类，用于返回读取的Cifar-10的数据
class CIFAR10Record(object):
    pass


# 定义一个读取Cifar-10的函数read_cifar10()，这个函数的目的就是读取目标文件里面的内容
def read_cifar_10(file_queue):
    label_bytes = 1  # 如果是Cifar-100数据集，则此处为2

    result = CIFAR10Record()
    result.height = 32
    result.width = 32
    result.depth = 3  # 因为是RGB三通道，所以深度是3

    image_bytes = result.height * result.width * result.depth  # 图片样本总元素数量
    record_bytes = label_bytes + image_bytes  # 因为每一个样本包含图片和标签，所以最终的元素数量还需要图片样本数量加上一个标签值

    # 使用tf.FixedLengthRecordReader()创建一个文件读取类。该类的目的就是读取文件
    reader = tf.FixedLengthRecordReader(record_bytes=record_bytes)
    result.key, value = reader.read(file_queue)  # 使用该类的read()函数从文件队列里面读取文件

    record_bytes = tf.decode_raw(value, tf.uint8)  # 读取到文件以后，将读取到的文件内容从字符串形式解析为图像对应的像素数组

    # 取标签 tf.strided_slice 是 TensorFlow 中的一个操作，用于对张量进行切片操作，可以选择提取张量的特定部分。
    # input_: 要进行切片操作的输入张量。（record_bytes）
    # begin: 切片的起始位置，可以是一个整数列表或张量。（[0]）
    # end: 切片的结束位置，可以是一个整数列表或张量。（[label_bytes]） = [1]
    # 注意取值是：左闭右开
    result.label = tf.cast(tf.strided_slice(record_bytes, [0], [label_bytes]), tf.int32)

    # 取图片元素
    image_data = tf.strided_slice(record_bytes, [label_bytes], [label_bytes + image_bytes])
    image_data = tf.reshape(image_data, [result.depth, result.height, result.width])

    # 这一步是转换数据排布方式，变为(h,w,c)
    result.uint8image = tf.transpose(image_data, [1, 2, 0])
    return result


def inputs(data_dir, batch_size, distorted):  # 这个函数就对数据进行预处理---对图像数据是否进行增强进行判断，并作出相应的操作
    filenames = [os.path.join(data_dir, "data_batch_%d.bin" % i) for i in range(1, 6)]  # 拼接地址

    file_queue = tf.train.string_input_producer(filenames)  # 根据已经有的文件地址创建一个文件队列
    read_input = read_cifar_10(file_queue)  # 根据已经有的文件队列使用已经定义好的文件读取函数read_cifar10()读取队列中的文件

    reshaped_image = tf.cast(read_input.uint8image, tf.float32)  # 将已经转换好的图片数据再次转换为float32的形式

    num_examples_per_epoch = num_examples_pre_epoch_for_train

    if distorted is not None:  # 如果预处理函数中的distorted参数不为空值，就代表要进行图片增强处理
        cropped_image = tf.random_crop(reshaped_image, [24, 24, 3])  # 首先将预处理好的图片进行剪切，使用tf.random_crop()函数

        # 将剪切好的图片进行左右翻转，使用tf.image.random_flip_left_right()函数
        flipped_image = tf.image.random_flip_left_right(cropped_image)
        adjusted_brightness = tf.image.random_brightness(flipped_image, max_delta=0.8)
        # 对比度调节
        adjusted_contrast = tf.image.random_contrast(adjusted_brightness, lower=0.2, upper=1.8)
        # 进行标准化图片操作，tf.image.per_image_standardization()函数是对每一个像素减去平均值并除以像素方差
        float_image = tf.image.per_image_standardization(adjusted_contrast)
        float_image.set_shape([24, 24, 3])  # 设置图片数据及标签的形状
        read_input.label.set_shape([1])

        min_queue_examples = int(num_examples_pre_epoch_for_eval * 0.4)
        print("Filling queue with %d CIFAR images before starting to train.    This will take a few minutes."
              % min_queue_examples)

        images_train, labels_train = tf.train.shuffle_batch([float_image, read_input.label], batch_size=batch_size,
                                                            num_threads=16,
                                                            capacity=min_queue_examples + 3 * batch_size,
                                                            min_after_dequeue=min_queue_examples,
                                                            )
        # 使用tf.train.shuffle_batch()函数随机产生一个batch的image和label

        return images_train, tf.reshape(labels_train, [batch_size])

    else:  # 不对图像数据进行数据增强处理
        # 在这种情况下，使用函数tf.image.resize_image_with_crop_or_pad()对图片数据进行剪切
        resized_image = tf.image.resize_image_with_crop_or_pad(reshaped_image, 24, 24)

        float_image = tf.image.per_image_standardization(resized_image)  # 剪切完成以后，直接进行图片标准化操作
        float_image.set_shape([24, 24, 3])
        read_input.label.set_shape([1])

        min_queue_examples = int(num_examples_per_epoch * 0.4)
        images_test, labels_test = tf.train.batch([float_image, read_input.label],
                                                  batch_size=batch_size, num_threads=16,
                                                  capacity=min_queue_examples + 3 * batch_size)
        # 这里使用batch()函数代替tf.train.shuffle_batch()函数
        return images_test, tf.reshape(labels_test, [batch_size])
