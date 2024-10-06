#!/usr/bin/env python

import os
import argparse
from PIL import Image


def convert_to_grayscale(image_path, output_path):
    """
    将图片转换为灰度图像并保存到指定目录。

    参数:
    - image_path: 输入图片的路径
    - output_path: 输出图片的路径
    """
    try:
        # 打开图像文件
        img = Image.open(image_path)
        # 将图像转换为灰度模式 ("L" 表示灰度模式)
        grayscale_img = img.convert("L")
        # 保存转换后的灰度图像到指定路径
        grayscale_img.save(output_path)
        print(f"已成功转换并保存: {output_path}")
    except Exception as e:
        # 如果发生异常，输出错误信息
        print(f"处理图片 {image_path} 时出错: {e}")


def contains_images(files):
    """
    检查文件列表中是否包含图片文件。

    参数:
    - files: 文件列表

    返回:
    - 如果列表中包含至少一个图片文件，返回 True；否则返回 False。
    """
    for file_name in files:
        # 检查文件名是否以常见图片扩展名结尾
        if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
            return True
    return False


def process_directory(input_dir, output_dir, recursive=False):
    """
    处理目录中的所有图片文件，支持递归处理。

    参数:
    - input_dir: 输入目录的路径
    - output_dir: 输出目录的路径
    - recursive: 是否递归处理子目录 (默认值为 False)
    """

    if recursive:
        # 使用 os.walk 遍历目录树，递归处理所有子目录
        for root, dirs, files in os.walk(input_dir):
            # 检查当前目录中是否包含图片文件
            if not contains_images(files):
                # 如果不包含图片文件，则跳过当前目录
                continue

            # 计算当前子目录相对于输入目录的相对路径
            relative_path = os.path.relpath(root, input_dir)
            # 在输出目录中创建相应的子目录
            output_subdir = os.path.join(output_dir, relative_path)
            if not os.path.exists(output_subdir):
                os.makedirs(output_subdir)

            # 处理当前目录中的每个文件
            for file_name in files:
                file_path = os.path.join(root, file_name)
                # 检查文件是否是图片文件
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                    # 分离文件名和扩展名
                    output_file_name, file_ext = os.path.splitext(file_name)
                    # 构建输出文件路径，添加 "_grayscale" 后缀以避免覆盖原图
                    output_path = os.path.join(
                        output_subdir, f"{output_file_name}_grayscale{file_ext}")
                    # 转换为灰度图像并保存
                    convert_to_grayscale(file_path, output_path)
    else:
        # 遍历输入目录中的所有文件
        for file_name in os.listdir(input_dir):
            file_path = os.path.join(input_dir, file_name)
            # 检查文件是否是图片文件
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                # 分离文件名和扩展名
                output_file_name, file_ext = os.path.splitext(file_name)
                # 构建输出文件路径
                output_path = os.path.join(
                    output_dir, f"{output_file_name}_grayscale{file_ext}")
                # 转换为灰度图像并保存
                convert_to_grayscale(file_path, output_path)


def main():
    """
    程序入口，解析命令行参数并执行相应的图片处理逻辑。
    """
    # 创建 ArgumentParser 对象用于解析命令行参数
    parser = argparse.ArgumentParser(description="将图片转换为灰度图像")
    # 添加输入路径参数，支持多个文件路径（必须提供）
    parser.add_argument("-i", "--input", required=True,
                        nargs='+', help="输入的图片文件路径（可接受多个文件或目录）")
    # 添加输出目录参数（必须提供）
    parser.add_argument("-o", "--output", required=True, help="输出目录")
    # 添加递归处理选项，使用 -r 时将递归处理子目录
    parser.add_argument("-r", "--recursive",
                        action="store_true", help="递归处理目录")

    # 解析命令行参数
    args = parser.parse_args()

    # 获取输入路径列表、输出目录和递归选项的值
    input_paths = args.input
    output_dir = args.output
    recursive = args.recursive

    # 确保输出目录存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 处理多个输入文件或目录
    for input_path in input_paths:
        if os.path.isfile(input_path):
            # 如果是单个文件，则进行单张图片处理
            file_base_name = os.path.basename(input_path)
            # 检查文件是否是图片文件
            if file_base_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
                # 分离文件名和扩展名
                file_name, file_ext = os.path.splitext(file_base_name)
                # 构建输出文件路径
                output_path = os.path.join(
                    output_dir, f"{file_name}_grayscale{file_ext}")
                # 转换为灰度图像并保存
                convert_to_grayscale(input_path, output_path)
        elif os.path.isdir(input_path):
            # 如果是目录，则处理目录中的图片
            process_directory(input_path, output_dir, recursive=recursive)
        else:
            # 如果输入路径无效，输出错误信息
            print(f"无效的输入路径: {input_path}")


if __name__ == "__main__":
    # 程序入口
    main()
