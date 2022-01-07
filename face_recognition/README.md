# Face Recognition Using Pytorch 
Fork from [facenet-pytorch](https://github.com/timesler/facenet-pytorch)

## Quick start

1. Install:
    
    ```bash
    # With pip:
    cd ./CG_Final_face_gan/face_recognition/
    pip install facenet-pytorch
    ```
    
1. Process crop an image:
    
    ```python
    from PIL import Image
    
    img = Image.open(<image path>)

    # Get cropped and prewhitened image tensor
    img_cropped = mtcnn(img, save_path=<optional save path>)
    ```

See `help(MTCNN)` and `help(InceptionResnetV1)` for usage and implementation details.