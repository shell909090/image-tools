#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pad 拼图模块
处理 Pad 相关的图片拼接任务
"""

import logging
from pathlib import Path
from typing import Optional
from PIL import Image

# 尝试相对导入，如果失败则使用绝对导入
try:
    from .utils import (
        MOBILE_BLOCK_COVER,
        PAD_LOCK_COVER,
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
        MOBILE_BLOCK_COVER,
        PAD_LOCK_COVER,
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


def prepare_pad_images(work_dir: Path) -> bool:
    """
    准备 Pad desktop 和 lock 图片
    
    Args:
        work_dir: 工作目录
    
    Returns:
        是否成功
    """
    pad = work_dir / 'pad.png'
    if not pad.exists():
        logger.error(f"  缺少 pad.png")
        return False
    
    success = True
    
    # 处理 pad-desktop.png
    pad_desktop = work_dir / 'pad-desktop.png'
    if not pad_desktop.exists():
        # 根据 README，pad-desktop.png 使用 mobile-block-cover.png
        if not MOBILE_BLOCK_COVER.exists():
            logger.warning(f"  缺少覆盖图片: {MOBILE_BLOCK_COVER}，跳过 pad-desktop.png 生成")
        else:
            try:
                base_img = Image.open(pad)
                cover_img = Image.open(MOBILE_BLOCK_COVER)
                
                # 确保两张图片都是 4:3 比例
                target_ratio = 4 / 3
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
                result.save(pad_desktop, 'PNG')
                logger.info(f"  已生成 pad-desktop.png")
            except Exception as e:
                logger.error(f"  生成 pad-desktop.png 失败: {e}")
                success = False
    else:
        logger.info(f"  pad-desktop.png 已存在，跳过")
    
    # 处理 pad-lock.png
    pad_lock = work_dir / 'pad-lock.png'
    if not pad_lock.exists():
        if not PAD_LOCK_COVER.exists():
            logger.warning(f"  缺少覆盖图片: {PAD_LOCK_COVER}，跳过 pad-lock.png 生成")
        else:
            try:
                base_img = Image.open(pad)
                cover_img = Image.open(PAD_LOCK_COVER)
                
                # 确保两张图片都是 4:3 比例
                target_ratio = 4 / 3
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
                result.save(pad_lock, 'PNG')
                logger.info(f"  已生成 pad-lock.png")
            except Exception as e:
                logger.error(f"  生成 pad-lock.png 失败: {e}")
                success = False
    else:
        logger.info(f"  pad-lock.png 已存在，跳过")
    
    return success


def create_pad_puzzle(work_dir: Path, output_dir: Path, main_color: Optional[str] = None) -> bool:
    """
    创建 Pad 拼图
    
    Args:
        work_dir: 工作目录
        output_dir: 输出目录
        main_color: 主色调
    
    Returns:
        是否成功
    """
    pad_lock_file = get_image_file(work_dir, 'pad-lock')
    pad_desktop_file = work_dir / 'pad-desktop.png'
    
    # 优先使用 pad-lock.png，如果不存在则使用 pad-lock.jpg 等
    if not pad_lock_file:
        pad_lock_file = work_dir / 'pad-lock.png'
    
    if not pad_lock_file.exists() or not pad_desktop_file.exists():
        logger.error(f"  缺少 Pad 拼图所需文件")
        return False
    
    try:
        pad_lock = Image.open(pad_lock_file)
        pad_desktop = Image.open(pad_desktop_file)
        
        # 确保两张图片都是 4:3 比例
        target_input_ratio = 4 / 3
        pad_lock = resize_to_fit_ratio(pad_lock, target_input_ratio, (3000, 2250))
        pad_desktop = resize_to_fit_ratio(pad_desktop, target_input_ratio, (3000, 2250))
        
        # 统一两张图片的高度
        target_height = min(pad_lock.height, pad_desktop.height)
        lock_width = int(target_height * target_input_ratio)
        desktop_width = int(target_height * target_input_ratio)
        
        pad_lock = pad_lock.resize((lock_width, target_height), Image.Resampling.LANCZOS)
        pad_desktop = pad_desktop.resize((desktop_width, target_height), Image.Resampling.LANCZOS)
        
        # 添加阴影和圆角
        pad_lock = add_shadow_and_rounded_corners(pad_lock)
        pad_desktop = add_shadow_and_rounded_corners(pad_desktop)
        
        # 计算画布尺寸（横向排列，3:4 比例）
        total_width = pad_lock.width + pad_desktop.width + SPACING
        canvas_height = max(pad_lock.height, pad_desktop.height)
        canvas_width = int(canvas_height * (OUTPUT_RATIO[0] / OUTPUT_RATIO[1]))
        
        # 如果内容宽度超过画布宽度，需要缩放
        if total_width > canvas_width:
            scale = (canvas_width - SPACING) / total_width
            new_lock_width = int(pad_lock.width * scale)
            new_desktop_width = int(pad_desktop.width * scale)
            new_height = int(canvas_height * scale)
            
            pad_lock = pad_lock.resize((new_lock_width, new_height), Image.Resampling.LANCZOS)
            pad_desktop = pad_desktop.resize((new_desktop_width, new_height), Image.Resampling.LANCZOS)
            
            total_width = pad_lock.width + pad_desktop.width + SPACING
            canvas_height = max(pad_lock.height, pad_desktop.height)
        
        # 创建背景（使用原始图片提取主色调）
        original_pad_lock = Image.open(pad_lock_file)
        bg = create_background((canvas_width, canvas_height), main_color, original_pad_lock)
        
        # 计算居中位置
        x_offset = (canvas_width - total_width) // 2
        y_offset = (canvas_height - max(pad_lock.height, pad_desktop.height)) // 2
        
        # 粘贴图片
        bg.paste(pad_lock, (x_offset, y_offset), pad_lock)
        bg.paste(pad_desktop, (x_offset + pad_lock.width + SPACING, y_offset), pad_desktop)
        
        # 保存并优化文件大小
        output_file = output_dir / 'pad-combined.png'
        save_optimized_image(bg, output_file)
        
        logger.info(f"  已生成 pad-combined.png")
        return True
    except Exception as e:
        logger.error(f"  生成 Pad 拼图失败: {e}")
        return False

