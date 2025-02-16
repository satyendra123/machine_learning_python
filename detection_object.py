import torch

# Path to your local yolov5 repository and model
yolov5_path = r'C:\Users\Satyendra Singh\yolov5'  # Use raw string for Windows paths
model_path = r'D:\machine_learning_python\best.pt'  # Path to your best.pt model

# Force reload to avoid cache issues and load from local path
model = torch.hub.load(yolov5_path, 'custom', path=model_path, source='local', force_reload=True)

# Path to your test video (dogs and cats.mp4)
video_path = r'D:\machine_learning_python\dogs and cats.mp4'  # Use raw string for Windows paths

# Run inference on the video
results = model(video_path)

# Display the results
results.show()  # This will display the bounding boxes and labels on the video

# Optionally save the output video
results.save()  # Save the output video with detections
