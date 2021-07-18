# import libraries
import time
import cv2
import face_recognition

# Read the video and get the length
input_movie = cv2.VideoCapture("data/sample_video.MOV")
length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

# Load the sample image
image = face_recognition.load_image_file("data/sample_image_1.png")
face_encoding = face_recognition.face_encodings(image)[0]

known_faces = [
    face_encoding,
]

# Output Image
codec = int(input_movie.get(cv2.CAP_PROP_FOURCC))
fps = int(input_movie.get(cv2.CAP_PROP_FPS))
frame_width = int(input_movie.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(input_movie.get(cv2.CAP_PROP_FRAME_HEIGHT))
output_movie = cv2.VideoWriter(
    "output.mp4", codec, fps, (frame_width, frame_height))

# Initialize variables
start_time = time.time()
face_locations = []
face_encodings = []
face_names = []
frame_number = 0

while True:
    # Grab a single frame of video
    ret, frame = input_movie.read()
    frame_number += 1

    # Quit when the input video file ends
    if not ret:
        break

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(rgb_frame, model="cnn")
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        match = face_recognition.compare_faces(
            known_faces, face_encoding, tolerance=0.50)

        name = None
        if match[0]:
            name = "Person Detected"

        face_names.append(name)

    # Label the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if not name:
            continue

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 25),
                      (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6),
                    font, 0.5, (255, 255, 255), 1)

    # Write the resulting image to the output video file
    print("Writing frame {} / {}.".format(frame_number, length))
    print("--- %s seconds ---" % (time.time() - start_time))
    output_movie.write(frame)

# All done!
input_movie.release()
print("--- %s seconds ---" % (time.time() - start_time))
cv2.destroyAllWindows()
