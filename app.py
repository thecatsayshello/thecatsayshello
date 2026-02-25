import streamlit as st
from moviepy.video.VideoClip import ImageClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy import vfx  # ← this is the correct import for effects in MoviePy 2+
from PIL import Image
import tempfile
import os

HAND_GIF = "waving_hand.gif"  # must be the exact filename in the repo

st.set_page_config(page_title="Cat Waving Paw Maker", layout="centered")

st.title("🐱 Make The Cats Say Hello ✋")
st.markdown(
    "Upload any cat picture → the famous waving paw gets added automatically!\n"
    "Based on the paw from @0xGory's GIF."
)

uploaded_file = st.file_uploader(
    "Upload your cat photo (jpg, png, jpeg)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    with st.spinner("Adding waving paw... 🐾"):
        try:
            cat_img = Image.open(uploaded_file)

            with tempfile.TemporaryDirectory() as tmp:
                cat_path = os.path.join(tmp, "cat.png")
                cat_img.save(cat_path)

                cat_clip = ImageClip(cat_path)
                hand_clip = VideoFileClip(HAND_GIF, has_mask=True)

                duration = 4.0
                cat_clip.duration = duration

                # Correct way to loop in MoviePy 2+
                hand_looped = hand_clip.fx(vfx.loop, duration=duration)

                hand_resized = hand_looped.resize(width=int(cat_clip.w * 0.25))

                pos_x = cat_clip.w - hand_resized.w - 40
                pos_y = cat_clip.h - hand_resized.h - 40

                final = CompositeVideoClip([cat_clip, hand_resized.set_position((pos_x, pos_y))])

                output_path = os.path.join(tmp, "output.gif")
                final.write_gif(output_path, fps=15)

            st.success("Done!")
            st.image(output_path, caption="Your cat waving hello!", use_column_width=True)

            with open(output_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download GIF",
                    data=f,
                    file_name="waving_cat.gif",
                    mime="image/gif"
                )

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}\n\nTry a different image or smaller file size.")
