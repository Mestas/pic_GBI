import streamlit as st
import numpy as np
from PIL import Image
import io

def swap_gb_channels_pil(pil_image):
    """使用PIL交换图片的G和B通道"""
    img_array = np.array(pil_image)
    
    # 确保图片有3个通道（RGB）
    if len(img_array.shape) != 3 or img_array.shape[2] < 3:
        return None
    
    # 交换G和B通道 (PIL是RGB格式)
    img_swapped = img_array.copy()
    img_swapped[:,:,1], img_swapped[:,:,2] = img_array[:,:,2], img_array[:,:,1]
    
    return Image.fromarray(img_swapped)

def swap_gb_channels_cv2(image_array):
    """使用OpenCV交换图片的G和B通道"""
    if len(image_array.shape) != 3 or image_array.shape[2] < 3:
        return None
    
    # 交换G和B通道 (OpenCV是BGR格式)
    img_swapped = image_array.copy()
    img_swapped[:,:,0], img_swapped[:,:,1] = image_array[:,:,1], image_array[:,:,0]
    
    return img_swapped

def main():
    st.set_page_config(
        page_title="BMP图片GB通道互换工具",
        page_icon="🎨",
        layout="centered"
    )
    
    st.title("🎨 BMP图片GB通道互换工具")
    st.markdown("---")
    
    # 文件上传
    uploaded_file = st.file_uploader(
        "选择BMP图片文件", 
        type=['bmp', 'BMP'],
        help="请上传BMP格式的图片文件"
    )
    
    if uploaded_file is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("原始图片")
            # 读取并显示原始图片
            original_image = Image.open(uploaded_file)
            st.image(original_image, use_column_width=True)
            
            # 显示图片信息
            st.info(f"""
            **图片信息：**
            - 尺寸: {original_image.size}
            - 模式: {original_image.mode}
            - 格式: {original_image.format}
            """)
        
        with col2:
            st.subheader("GB通道互换后")
            
            # 执行GB通道互换
            swapped_image = swap_gb_channels_pil(original_image)
            
            if swapped_image is not None:
                st.image(swapped_image, use_column_width=True)
                
                # 转换为BMP格式的字节数据
                img_buffer = io.BytesIO()
                swapped_image.save(img_buffer, format='BMP')
                img_buffer.seek(0)
                
                # 下载按钮
                st.download_button(
                    label="📥 下载处理后的BMP图片",
                    data=img_buffer,
                    file_name=f"gb_swapped_{uploaded_file.name}",
                    mime="image/bmp"
                )
                
                st.success("GB通道互换完成！点击上方按钮下载结果。")
            else:
                st.error("处理失败，请确保上传的是有效的RGB图片")
    
    # 使用说明
    with st.expander("📖 使用说明"):
        st.markdown("""
        ### 功能说明
        这个工具可以：
        1. 上传BMP格式的图片
        2. 自动交换绿色(G)和蓝色(B)通道
        3. 生成新的BMP图片并提供下载
        
        ### 效果说明
        - 原图中的绿色区域会变为蓝色
        - 原图中的蓝色区域会变为绿色
        - 红色区域基本保持不变
        
        ### 支持的格式
        - 输入：BMP格式图片
        - 输出：BMP格式图片
        """)
    
    # 技术说明
    with st.expander("🔧 技术细节"):
        st.markdown("""
        ### 实现原理
        使用Python的PIL库处理图片：
        - 读取图片的RGB通道数据
        - 交换G通道(索引1)和B通道(索引2)
        - 重新生成图片并保存为BMP格式
        
        ### 依赖库
        - streamlit: Web界面
        - PIL (Pillow): 图片处理
        - numpy: 数组操作
        """)

if __name__ == "__main__":
    main()
