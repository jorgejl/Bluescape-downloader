import json
import os
from PIL import Image, ImageDraw, UnidentifiedImageError
from moviepy.editor import VideoFileClip, VideoFileClipError
import inquirer

# First attempt to generate a high quality reference of the downloaded files.
# TODO: Using png for convenience, but PDF with link to the original files or
# HTML file with links to the original would be better probably.

def load_image(filepath):
    try:
        return Image.open(filepath)
    except (FileNotFoundError, UnidentifiedImageError) as e:
        print(f"Error loading image {filepath}: {e}")
        return None

def extract_video_frame(filepath):
    try:
        clip = VideoFileClip(filepath)
        frame = clip.get_frame(clip.duration / 2)
        frame_image = Image.fromarray(frame)
        
        # Add visual indicator
        draw = ImageDraw.Draw(frame_image)
        draw.rectangle([0, 0, 100, 50], fill="red")
        draw.text((10, 10), "Video", fill="white")
        
        return frame_image
    except (FileNotFoundError, VideoFileClipError, OSError) as e:
        print(f"Error processing video {filepath}: {e}")
        return None

def process_item(item, base_dir):
    filepath = os.path.join(base_dir, item['filename'])
    
    if item['type'] == 'Image':
        img = load_image(filepath)
    elif item['type'] == 'Video':
        img = extract_video_frame(filepath)
    else:
        print(f"Unsupported item type: {item['type']}")
        return None, 0, 0
    
    if img:
        try:
            img = img.resize((int(item['width'] * item['transform']['scaleX']),
                              int(item['height'] * item['transform']['scaleY'])))
        except Exception as e:
            print(f"Error resizing image {filepath}: {e}")
            return None, 0, 0
    
    return img, item['transform']['x'], item['transform']['y']

def calculate_canvas_size(items):
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')
    
    for item in items:
        x, y = item['transform']['x'], item['transform']['y']
        width = int(item['width'] * item['transform']['scaleX'])
        height = int(item['height'] * item['transform']['scaleY'])
        
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x + width)
        max_y = max(max_y, y + height)
    
    canvas_width = max_x - min_x
    canvas_height = max_y - min_y
    return canvas_width, canvas_height, min_x, min_y

def create_canvas(items, base_dir):
    canvas_width, canvas_height, offset_x, offset_y = calculate_canvas_size(items)
    canvas = Image.new('RGB', (canvas_width, canvas_height), (255, 255, 255))
    
    for item in items:
        img, x, y = process_item(item, base_dir)
        if img:
            canvas.paste(img, (x - offset_x, y - offset_y))
    
    return canvas

def list_folders_with_json(base_dir):
    folders = []
    for entry in os.listdir(base_dir):
        entry_path = os.path.join(base_dir, entry)
        if os.path.isdir(entry_path):
            json_file = os.path.join(entry_path, f"{entry}.json")
            if os.path.exists(json_file):
                folders.append(entry)
    return folders

def main():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    
    folders = list_folders_with_json(script_dir)
    if not folders:
        print("No folders with the required JSON file structure found.")
        return
    
    questions = [
        inquirer.List('folder',
                      message="Select the folder to process",
                      choices=folders),
    ]
    answers = inquirer.prompt(questions)
    selected_folder = answers['folder']
    json_file_path = os.path.join(script_dir, selected_folder, f"{selected_folder}.json")
    
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)['data']
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON file {json_file_path}: {e}")
        return
    
    canvas = create_canvas(data, os.path.join(script_dir, selected_folder))
    output_path = os.path.join(script_dir, selected_folder, 'workspace.png')
    
    try:
        canvas.save(output_path)
        print(f"Workspace saved to {output_path}")
    except Exception as e:
        print(f"Error saving canvas to {output_path}: {e}")

if __name__ == "__main__":
    main()
