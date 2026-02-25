import streamlit as st
from moviepy.editor import ImageClip, VideoFileClip, CompositeVideoClip
from PIL import Image
import tempfile
import os

# Your GIF — must be named exactly this in the repo root
PAW_GIF = "waving_hand.gif"

st.set_page_config(page_title="Cat + Waving Paw", layout="centered")

st.title("🐱 Cat + Waving Paw ✋")
st.write("Upload your cat photo → waving paw overlay on top!")

uploaded_cat = st.file_uploader("Upload cat photo (jpg/png)", type=["jpg", "jpeg", "png"])

if uploaded_cat is not None:
    with st.spinner("Processing..."):
        try:
            # Save uploaded cat photo
            with tempfile.TemporaryDirectory() as tmp:
                cat_path = os.path.join(tmp, "cat.png")
                Image.open(uploaded_cat).save(cat_path)

                # Background = your uploaded cat (static image)
                background = ImageClip(cat_path).set_duration(5.0)  # 5 seconds is enough

                # Foreground = your waving paw GIF (with transparency)
                paw = VideoFileClip(PAW_GIF, has_mask=True)  # has_mask=True is crucial for transparency

                # Resize paw to ~30% of cat width (adjust 0.3 if too big/small)
                paw_resized = paw.resize(width=int(background.w * 0.3))

                # Position bottom-right with padding
                pos_x = background.w - paw_resized.w - 40
                pos_y = background.h - paw_resized.h - 40

                # Overlay paw on cat background
                final = CompositeVideoClip([background, paw_resized.set_position((pos_x, pos_y))])

                # Make it 5 seconds long (paw loops automatically)
                final = final.set_duration(5.0)

                output_path = os.path.join(tmp, "final.gif")
                final.write_gif(output_path, fps=15)

            st.success("Done!")
            st.image(output_path, caption="Your cat with waving paw!", use_column_width=True)

            with open(output_path, "rb") as f:
                st.download_button("Download GIF", f, file_name="cat_waving.gif", mime="image/gif")

        except Exception as e:
            st.error(f"Error: {str(e)}\n\nMost likely the GIF file is not readable by MoviePy. Try a different GIF.")
