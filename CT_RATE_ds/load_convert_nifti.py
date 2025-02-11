import nibabel as nib


def load_nifti_volume(self, nifti_path):
    # Load the 3D NIfTI file
    nifti_img = nib.load(nifti_path)
    volume = nifti_img.get_fdata()  # Shape: (Height, Width, Depth)

    total_slices = volume.shape[2]  # Depth = number of slices
    print("Total slices", total_slices)

    if total_slices < 30:
        raise ValueError(
            f"NIfTI file {nifti_path} has only {total_slices} slices, but 30 are required."
        )

    # Find middle slice
    middle_idx = total_slices // 2
    start_idx = max(
        0, middle_idx - 15 * 4
    )  # Go 15 frames left, skipping 4 each time
    end_idx = min(
        total_slices, middle_idx + 15 * 4
    )  # Go 15 frames right, skipping 4 each time

    # Select one frame every 4 frames
    selected_slices = volume[
        :, :, start_idx:end_idx:4
    ]  # Shape: (H, W, num_selected_frames)
    selected_slices = selected_slices.transpose(
        2, 0, 1
    )  # Shape: (num_selected_frames, H, W)

    print(f"Selected {selected_slices.shape[0]} slices")  # Debugging

    # Convert slices to PIL images and apply transforms
    transformed_frames = []
    for slice in selected_slices:
        slice_np = (slice - slice.min()) / (
            slice.max() - slice.min()
        )  # Normalize to [0, 1]
        slice_np = (slice_np * 255).astype(np.uint8)  # Convert to uint8
        # Convert to PIL image & Resize to (224, 224)
        slice_pil = (
            Image.fromarray(slice_np)
            .convert("L")  # for grayscale
            .resize((224, 224), Image.Resampling.BILINEAR)
        )
        transformed_frame = self.transforms(slice_pil)  # Apply transforms (H, W)
        transformed_frames.append(transformed_frame)

    # Stack frames into (num_frames, H, W)
    return torch.stack(transformed_frames)
