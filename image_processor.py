# Import the OpenCV library for image processing
import cv2
# Import the subprocess module to execute external commands (e.g., ImageMagick)
import subprocess

# Function to calculate an appropriate font size for text in an image
def calculate_text_size(text, font, base_font_size, rect_width, rect_height):
    # Estimate the width per character based on the base font size
    estimated_width_per_char = base_font_size * 0.5
    # The estimated height of a line of text is roughly the font size
    estimated_height = base_font_size

    # Calculate the total width and height of the text
    text_width = estimated_width_per_char * len(text)
    text_height = estimated_height

    # Adjust the font size to fit the text within the specified rectangle
    while text_width > rect_width or text_height > rect_height:
        base_font_size *= 0.95  # Reduce font size by 5%
        text_width *= 0.95  # Update text width
        text_height *= 0.95  # Update text height

    # Return the adjusted font size
    return base_font_size

# Function to capture an image, process it, and print it with added text
def capture_and_print(settings, file_path='captured_image.jpg'):
    # Start video capture on the default webcam
    cap = cv2.VideoCapture(0)
    # Set the capture width and height
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    # Check if the webcam is successfully opened
    if not cap.isOpened():
        print("Error: Could not open the webcam.")
        return

    # Capture a single frame
    ret, frame = cap.read()

    # Check if the frame is captured successfully
    if not ret:
        print("Error: Could not capture an image.")
        cap.release()
        return

    # Rotate the captured frame by 90 degrees clockwise and save it
    rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite(file_path, rotated_frame)

    # Release the webcam
    cap.release()

    # Extract settings for text placement and font size calculation
    line1, line2 = settings['text_to_add'].split()
    font_size_line1 = calculate_text_size(line1, 'Arial', 90, int(settings['text_rect_width']), int(settings['text_rect_height']) // 2)
    font_size_line2 = calculate_text_size(line2, 'Arial', 90, int(settings['text_rect_width']), int(settings['text_rect_height']) // 2)

    # Calculate text width for centering
    text_width_line1 = len(line1) * font_size_line1 * 0.5
    text_width_line2 = len(line2) * font_size_line2 * 0.5

    # Calculate the position for each line of text
    text_x1 = int(settings['text_rect_x']) + (int(settings['text_rect_width']) - text_width_line1) // 2
    text_x2 = int(settings['text_rect_x']) + (int(settings['text_rect_width']) - text_width_line2) // 2
    vertical_center = int(settings['text_rect_y']) + int(settings['text_rect_height']) // 2
    text_y1 = vertical_center - font_size_line1
    text_y2 = vertical_center

    # Prepare the command for overlaying text on the image using ImageMagick's 'convert' tool
    convert_command = [
        'convert', settings['template_path'],
        '(', file_path, '-resize', '1101x500', ')',
        '-geometry', '+14+87', '-composite',
        '-gravity', 'NorthWest',
        '-fill', 'black',
        '-pointsize', str(font_size_line1),
        '-annotate', f'+{text_x1}+{text_y1}', line1,
        '-pointsize', str(font_size_line2),
        '-annotate', f'+{text_x2}+{text_y2}', line2,
        settings['output_path']
    ]

    # Execute the image processing command
    try:
        subprocess.run(convert_command)
        print(f"Image composed and saved to {settings['output_path']}")
    except Exception as e:
        print(f"Error in image processing: {e}")
