import streamlit as st
from rembg import remove, new_session
from PIL import Image
import io

# 1. Page Configuration (Title and Icon)
st.set_page_config(page_title="Background Remover Pro", page_icon="✨", layout="centered")

# Cache model session in RAM so it loads only once and stays lightweight
@st.cache_resource
def get_rembg_session():
    # 'u2net' is ~176MB (fits comfortably in Streamlit's 1GB RAM limit, unlike bria-rmbg which is 1.02GB)
    return new_session("u2net")

# 2. App UI Header
st.title("✨ Background Remover Pro")
st.write("Upload an image to magically remove its background in seconds!")

# 3. File Uploader
uploaded_file = st.file_uploader("📂 Choose an Image...", type=["jpg", "jpeg", "png", "webp", "bmp"])

if uploaded_file is not None:
    # Load the uploaded image using PIL
    original_image = Image.open(uploaded_file)
    
    # Create two columns for Before & After comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Image")
        st.image(original_image, use_container_width=True)
        
    with col2:
        st.subheader("Processed Result")
        # Empty placeholder until processed
        result_placeholder = st.empty() 
        result_placeholder.info("Click the button below to process.")

    st.markdown("---")
    
    # 4. Process Button
    if st.button("⚡ Remove Background", type="primary", use_container_width=True):
        
        # Display a loading spinner while processing
        with st.spinner("⏳ Removing background, please wait..."):
            try:
                # Remove background using the cached lightweight model
                session = get_rembg_session()
                result_image = remove(original_image, session=session)
                
                # Update the result placeholder with the new image
                with col2:
                    result_placeholder.image(result_image, use_container_width=True)
                
                st.success("✔ Background removed successfully!")
                
                # 5. Convert processed image to Bytes for Download
                img_buffer = io.BytesIO()
                result_image.save(img_buffer, format="PNG")
                byte_data = img_buffer.getvalue()
                
                # Download Button
                st.download_button(
                    label="💾 Download Result Image",
                    data=byte_data,
                    file_name="no_bg_image.png",
                    mime="image/png",
                    type="secondary",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"✖ Error occurred during processing: {e}")