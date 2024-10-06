import os
import argparse
from PIL import Image

# 支持的图片格式
SUPPORTED_FORMATS = [".png", ".bmp", ".tiff"]


def get_output_file(input_path, output_path):
    ext = os.path.splitext(input_path)[1].lower()
    return os.path.join(output_path, os.path.basename(input_path).replace(ext, '_converted.jpeg'))


def convert_image(input_path, output_path):
    """
    将输入图片转换为 JPEG 格式并保存到指定路径
    :param input_path: 输入图片的路径
    :param output_path: 输出图片的路径
    """
    output_file = get_output_file(input_path, output_path)

    try:
        img = Image.open(input_path)

        # JPEG 格式不支持透明度或其他颜色模式
        if img.mode != 'RGB':
            img = img.convert('RGB')

        img.save(output_file, 'JPEG')

        print(f"已成功转换: {input_path} -> {output_file}")
    except Exception as e:
        print(f"转换失败: {input_path}，错误信息: {str(e)}")


def process_file(input_path, output_dir):
    """
    处理单个文件，检查是否为支持的格式，进行转换
    :param input_path: 输入文件路径
    :param output_dir: 输出目录路径
    """
    if any(input_path.lower().endswith(fmt) for fmt in SUPPORTED_FORMATS):
            convert_image(input_path, output_dir)


def process_directory(directory, output_dir, recursive):
    """
    处理目录，递归或非递归地查找支持的图片并进行转换
    :param directory: 输入目录路径
    :param output_dir: 输出目录路径
    :param recursive: 是否递归子目录
    """
    for root, dirs, files in os.walk(directory):
        # 如果该子目录没有支持的图片，跳过
        if not any(file.lower().endswith(tuple(SUPPORTED_FORMATS)) for file in files):
            continue

        # 创建对应的输出子目录
        relative_path = os.path.relpath(root, directory)
        target_output_dir = os.path.join(output_dir, relative_path)
        os.makedirs(target_output_dir, exist_ok=True)

        # 处理文件
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, target_output_dir)

        # 如果不递归子目录，处理完当前目录就跳出
        if not recursive:
            break


def parse_args():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description="将图片转换为JPEG格式")
    parser.add_argument('-i', '--input', nargs='+',
                        required=True, help="输入图片文件或目录的路径")
    parser.add_argument('-o', '--output', required=True, help="输出目录的路径")
    parser.add_argument('-r', '--recursive',
                        action='store_true', help="是否递归处理子目录")

    return parser.parse_args()


def main():
    """
    主函数，处理输入并执行相应操作
    """
    args = parse_args()
    input_paths = args.input
    output_dir = args.output
    recursive = args.recursive

    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    # 处理输入文件或目录
    for input_path in input_paths:
        if os.path.isfile(input_path):
            process_file(input_path, output_dir)
        elif os.path.isdir(input_path):
            process_directory(input_path, output_dir, recursive)
        else:
            print(f"无效的输入路径: {input_path}")


if __name__ == "__main__":
    main()
