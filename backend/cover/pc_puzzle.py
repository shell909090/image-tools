#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PC 拼图模块
处理 PC 相关的图片拼接任务
"""

import logging
from pathlib import Path
from typing import Optional
from PIL import Image

# 尝试相对导入，如果失败则使用绝对导入
try:
    from .utils import (
        PC_MAC_COVER,
        OUTPUT_RATIO,
        SPACING,
        overlay_images,
        add_shadow_and_rounded_corners,
        resize_to_fit_ratio,
        create_background,
        get_image_file,
        save_optimized_image
    )
except ImportError:
    from utils import (
        PC_MAC_COVER,
        OUTPUT_RATIO,
        SPACING,
        overlay_images,
        add_shadow_and_rounded_corners,
        resize_to_fit_ratio,
        create_background,
        get_image_file,
        save_optimized_image
    )

logger = logging.getLogger(__name__)


def prepare_pc_desktop_mac(work_dir: Path) -> bool:
    """
    准备 PC desktop mac 图片
    
    Args:
        work_dir: 工作目录
    
    Returns:
        是否成功
    """
    pc_desktop_mac = work_dir / 'pc-desktop-mac.png'
    if pc_desktop_mac.exists():
        logger.info(f"  pc-desktop-mac.png 已存在，跳过")
        return True
    
    pc = work_dir / 'pc.png'
    if not pc.exists():
        logger.error(f"  缺少 pc.png")
        return False
    
    if not PC_MAC_COVER.exists():
        logger.warning(f"  缺少覆盖图片: {PC_MAC_COVER}，跳过 pc-desktop-mac.png 生成")
        return False
    
    try:
        base_img = Image.open(pc)
        cover_img = Image.open(PC_MAC_COVER)
        
        # 确保两张图片都是 21:9 比例
        target_ratio = 21 / 9
        base_ratio = base_img.width / base_img.height
        cover_ratio = cover_img.width / cover_img.height
        
        # 调整底图尺寸
        if abs(base_ratio - target_ratio) > 0.01:
            new_height = base_img.height
            new_width = int(new_height * target_ratio)
            base_img = base_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 调整覆盖图尺寸
        if abs(cover_ratio - target_ratio) > 0.01:
            new_height = cover_img.height
            new_width = int(new_height * target_ratio)
            cover_img = cover_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 确保两张图片尺寸一致
        if base_img.size != cover_img.size:
            cover_img = cover_img.resize(base_img.size, Image.Resampling.LANCZOS)
        
        result = overlay_images(base_img, cover_img)
        result.save(pc_desktop_mac, 'PNG')
        logger.info(f"  已生成 pc-desktop-mac.png")
        return True
    except Exception as e:
        logger.error(f"  生成 pc-desktop-mac.png 失败: {e}")
        return False


def create_pc_puzzle(work_dir: Path, output_dir: Path, main_color: Optional[str] = None) -> bool:
    """
    创建 PC 拼图
    
    Args:
        work_dir: 工作目录
        output_dir: 输出目录
        main_color: 主色调
    
    Returns:
        是否成功
    """
    pc_block_file = get_image_file(work_dir, 'pc-block')
    pc_desktop_mac_file = work_dir / 'pc-desktop-mac.png'
    
    # 特殊情况：如果只存在其中一张图片，则将该图居中显示
    if not pc_block_file and not pc_desktop_mac_file.exists():
        logger.error(f"  缺少 PC 拼图所需文件")
        return False
    
    try:
        images = []
        
        if pc_block_file:
            pc_block = Image.open(pc_block_file)
            # 确保是 21:9 比例
            target_input_ratio = 21 / 9
            pc_block = resize_to_fit_ratio(pc_block, target_input_ratio, (4000, 2000))
            images.append(('block', pc_block))
        
        if pc_desktop_mac_file.exists():
            pc_desktop_mac = Image.open(pc_desktop_mac_file)
            # 确保是 21:9 比例
            target_input_ratio = 21 / 9
            pc_desktop_mac = resize_to_fit_ratio(pc_desktop_mac, target_input_ratio, (4000, 2000))
            images.append(('desktop', pc_desktop_mac))
        
        if not images:
            return False
        
        # 统一图片宽度
        target_width = min(img.width for _, img in images)
        target_input_ratio = 21 / 9
        target_height = int(target_width / target_input_ratio)
        
        processed_images = []
        for name, img in images:
            img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
            img = add_shadow_and_rounded_corners(img)
            processed_images.append(img)
        
        # 计算画布尺寸（纵向排列，3:4 比例）
        total_height = sum(img.height for img in processed_images) + SPACING * (len(processed_images) - 1)
        canvas_width = int(total_height * (OUTPUT_RATIO[0] / OUTPUT_RATIO[1]))
        
        # 如果内容高度超过画布高度，需要缩放
        if total_height > canvas_width * (OUTPUT_RATIO[1] / OUTPUT_RATIO[0]):
            max_canvas_height = int(canvas_width * (OUTPUT_RATIO[1] / OUTPUT_RATIO[0]))
            scale = (max_canvas_height - SPACING * (len(processed_images) - 1)) / total_height
            
            new_processed = []
            for img in processed_images:
                new_width = int(img.width * scale)
                new_height = int(img.height * scale)
                new_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                new_processed.append(new_img)
            processed_images = new_processed
            
            total_height = sum(img.height for img in processed_images) + SPACING * (len(processed_images) - 1)
        
        canvas_height = int(canvas_width * (OUTPUT_RATIO[1] / OUTPUT_RATIO[0]))
        
        # 创建背景（使用原始图片提取主色调）
        source_img = images[0][1] if images else None
        bg = create_background((canvas_width, canvas_height), main_color, source_img)
        
        # 计算居中位置
        y_start = (canvas_height - total_height) // 2
        x_offset = (canvas_width - max(img.width for img in processed_images)) // 2
        
        # 粘贴图片
        current_y = y_start
        for img in processed_images:
            x_pos = x_offset + (max(img.width for img in processed_images) - img.width) // 2
            bg.paste(img, (x_pos, current_y), img)
            current_y += img.height + SPACING
        
        # 保存并优化文件大小
        output_file = output_dir / 'pc-combined.png'
        save_optimized_image(bg, output_file)
        
        logger.info(f"  已生成 pc-combined.png")
        return True
    except Exception as e:
        logger.error(f"  生成 PC 拼图失败: {e}")
        return False

