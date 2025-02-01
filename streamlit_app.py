import os
import tempfile
import numpy as np
from PIL import Image   
import nibabel as nib
import streamlit as st

import torch
import torchvision.transforms.functional as TF

from src.utils import load_model, post_process

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model_path = "best.pth"
model = load_model(model_path, device)

def main():

    st.title('Liver & Tumor Segmentation')
    st.sidebar.title('Atlas Application')
    st.sidebar.subheader('Parameters')
    st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 400px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 400px;
        margin-left: -400px;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

    uploaded_file = st.sidebar.file_uploader("Choose a NIfTI file..", type=["nii", "nii.gz"])
    
    st.sidebar.caption('Version v1.0')
    st.sidebar.image('logo.png', use_container_width=True)

    if uploaded_file is not None:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".nii.gz") as temp_file:
            temp_file.write(uploaded_file.read())
            temp_file_path = temp_file.name

        # Load the NIfTI file
        nifti_image = nib.load(temp_file_path)
        image_data = nifti_image.get_fdata()

        slice_2d = image_data[:, :, image_data.shape[-1] // 2]  # Extract the middle 2D slice

        # Convert the slice to RGB and then to a tensor
        slice_2d_rgb = Image.fromarray(slice_2d).convert("RGB")
        slice_2d_tensor = TF.to_tensor(np.array(slice_2d_rgb)).float().to(device)

        # Perform model inference
        with torch.no_grad():
            prediction = model(slice_2d_tensor.unsqueeze(0))  # Add batch dimension

        # Get the predicted class for each pixel
        segmented_slice = torch.argmax(prediction, dim=1).squeeze(0)  # Remove batch dimension

        # Convert to NumPy array
        segmented_slice_np = segmented_slice.cpu().numpy()

        segmented_slice_np = segmented_slice_np.astype(np.uint8)  # Convert to uint8

        # Convert NumPy array to PIL Image and back if necessary
        segmented_slice_image = Image.fromarray(segmented_slice_np).convert("L")

        segmented_slice_np = post_process(np.array(segmented_slice_image))

        os.remove(temp_file_path)

        st.image(segmented_slice_np, use_container_width=True)



if __name__ == "__main__":
    main()