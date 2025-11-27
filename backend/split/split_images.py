#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图片切分脚本
将imgs目录下的四格PNG图片切分成四张单独的图片，保存到new-imgs目录
"""

import os
from PIL import Image


def split_image(image_path, output_dir):
    """
    将图片切分成2x2的四张图片
    
    Args:
        image_path: 输入图片路径
        output_dir: 输出目录路径
    """
    try:
        # 打开图片
        img = Image.open(image_path)
        width, height = img.size
        
        # 计算每张切分图片的尺寸
        half_width = width // 2
        half_height = height // 2
        
        # 获取原文件名（不含扩展名）
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        
        # 切分成四张图片
        # 左上角 (0, 0)
        top_left = img.crop((0, 0, half_width, half_height))
        top_left.save(os.path.join(output_dir, f"{base_name}_1.png"))
        
        # 右上角 (half_width, 0)
        top_right = img.crop((half_width, 0, width, half_height))
        top_right.save(os.path.join(output_dir, f"{base_name}_2.png"))
        
        # 左下角 (0, half_height)
        bottom_left = img.crop((0, half_height, half_width, height))
        bottom_left.save(os.path.join(output_dir, f"{base_name}_3.png"))
        
        # 右下角 (half_width, half_height)
        bottom_right = img.crop((half_width, half_height, width, height))
        bottom_right.save(os.path.join(output_dir, f"{base_name}_4.png"))
        
        print(f"✓ 已切分: {os.path.basename(image_path)} -> 4张图片")
        
    except Exception as e:
        print(f"✗ 处理失败 {os.path.basename(image_path)}: {str(e)}")


def main():
    """主函数"""
    # 设置路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    imgs_dir = os.path.join(current_dir, "imgs")
    output_dir = os.path.join(current_dir, "new-imgs")
    
    # 检查imgs目录是否存在
    if not os.path.exists(imgs_dir):
        print(f"错误: 找不到目录 {imgs_dir}")
        return
    
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已创建输出目录: {output_dir}")
    
    # 遍历imgs目录下的所有PNG文件
    png_files = [f for f in os.listdir(imgs_dir) if f.lower().endswith('.png')]
    
    if not png_files:
        print(f"在 {imgs_dir} 目录下未找到PNG文件")
        return
    
    print(f"找到 {len(png_files)} 个PNG文件，开始处理...\n")
    
    # 处理每个PNG文件
    for png_file in png_files:
        image_path = os.path.join(imgs_dir, png_file)
        split_image(image_path, output_dir)
    
    print(f"\n处理完成！所有切分后的图片已保存到: {output_dir}")


if __name__ == "__main__":
    main()
