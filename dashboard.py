import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import tempfile

st.set_page_config(page_title="AI Construction Safety Monitor", layout="wide")

st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
# 🏗 AI Construction Safety Monitoring System
### Real-time PPE Compliance Analysis using Computer Vision
---
""")

model = YOLO("ppe_best.pt")

mode = st.radio("Select Input Type:", ["Image", "Video"])

# ---------------- IMAGE MODE ----------------
if mode == "Image":

    uploaded_image = st.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        image_np = np.array(image)

        results = model(image_np, conf=0.2)

        helmet_detected = 0
        vest_detected = 0

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls)
                class_name = model.names.get(cls_id, "unknown")
                conf = float(box.conf)

                if class_name == "helmet" and conf > 0.3:
                    helmet_detected = 1
                if class_name == "vest" and conf > 0.3:
                    vest_detected = 1

        helmet_violation = 0 if helmet_detected else 1
        vest_violation = 0 if vest_detected else 1

        violations = helmet_violation + vest_violation
        compliance_score = int(((2 - violations) / 2) * 100)

        if violations == 0:
            risk_level = "LOW"
        elif violations == 1:
            risk_level = "MODERATE"
        else:
            risk_level = "HIGH"

        annotated = results[0].plot()

        st.image(annotated, caption="Detection Result", use_column_width=True)

        col1, col2, col3 = st.columns(3)
        col1.metric("Helmet Status", "OK" if helmet_violation == 0 else "MISSING")
        col2.metric("Vest Status", "OK" if vest_violation == 0 else "MISSING")
        col3.metric("Compliance Score", f"{compliance_score}%")

        st.subheader(f"🚨 Risk Level: {risk_level}")


# ---------------- VIDEO MODE ----------------
# ---------------- VIDEO MODE ----------------
elif mode == "Video":

    uploaded_video = st.file_uploader("Upload a Video", type=["mp4", "mov", "avi"])

    if uploaded_video is not None:
        st.markdown("### 🎬 Uploaded Video")
        st.video(uploaded_video)

        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())

        cap = cv2.VideoCapture(tfile.name)

        helmet_violations_total = 0
        vest_violations_total = 0
        processed_frames = 0

        frame_skip = 5
        max_frames = 200

        preview_frames = []

        with st.spinner("Analyzing video for PPE compliance..."):

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                processed_frames += 1

                if processed_frames % frame_skip != 0:
                    continue

                if processed_frames > max_frames:
                    break

                frame = cv2.resize(frame, (640, 480))
                results = model(frame, conf=0.2)

                helmet_detected = 0
                vest_detected = 0

                for r in results:
                    for box in r.boxes:
                        cls_id = int(box.cls)
                        class_name = model.names.get(cls_id, "unknown")
                        conf = float(box.conf)

                        if class_name == "helmet" and conf > 0.3:
                            helmet_detected = 1

                        if class_name == "vest" and conf > 0.3:
                            vest_detected = 1

                if helmet_detected == 0:
                    helmet_violations_total += 1

                if vest_detected == 0:
                    vest_violations_total += 1

                # Store preview frames
                if len(preview_frames) < 20:
                    annotated = results[0].plot()
                    preview_frames.append(
                        cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                    )

        cap.release()

        total_frames = max(1, processed_frames // frame_skip)

        helmet_rate = 100 - int((helmet_violations_total / total_frames) * 100)
        vest_rate = 100 - int((vest_violations_total / total_frames) * 100)
        compliance_score = int((helmet_rate + vest_rate) / 2)

        if compliance_score > 80:
            risk_level = "LOW"
        elif compliance_score > 50:
            risk_level = "MODERATE"
        else:
            risk_level = "HIGH"

        st.subheader("📊 Safety Summary")
        col1, col2, col3 = st.columns([1,1,1])

        col1.metric("Helmet Compliance", f"{helmet_rate}%")
        col2.metric("Vest Compliance", f"{vest_rate}%")
        col3.metric("Overall Compliance", f"{compliance_score}%")

        if risk_level == "LOW":
          st.success(f"🟢 Risk Level: {risk_level}")
        elif risk_level == "MODERATE":
          st.warning(f"🟡 Risk Level: {risk_level}")
        else:
          st.error(f"🔴 Risk Level: {risk_level}")

        if helmet_rate < 100:
            st.error("🚨 Helmet compliance issue detected")

        if vest_rate < 100:
            st.error("🚨 Safety vest compliance issue detected")

        if helmet_rate == 100 and vest_rate == 100:
            st.success("✅ Full PPE compliance throughout analyzed video")

        st.markdown("---")
        st.subheader("🎥 Processed Video Preview (Sample Frames)")

        for frame in preview_frames:
            st.image(frame)