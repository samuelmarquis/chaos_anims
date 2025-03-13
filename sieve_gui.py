import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import json
import os

# Thanks Grok

PATH_BASE = "vid_pipe/scream3"
FRAME_INDEX = 0
IMAGE_PATH = f"{PATH_BASE}/src_frames/{FRAME_INDEX:05d}.png"
ANN_PATH = f"{PATH_BASE}/annotations.json"

class ImageAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Annotator")

        self.original_image = Image.open(IMAGE_PATH)
        self.tk_image = ImageTk.PhotoImage(self.original_image)
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.tk_image)

        self.scale = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.current_object_id = 1

        self.annotations = {}  # {object_id: {"points": [], "labels": []}}
        self.circles = []
        self.history = []

        self.canvas.bind("<Button-2>", self.start_pan)  # Middle click
        self.canvas.bind("<B2-Motion>", self.do_pan)
        self.canvas.bind("<Button-1>", self.add_blue_point)  # Left click
        self.canvas.bind("<Button-3>", self.add_red_point)  # Right click
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.root.bind("n", lambda e: self.next_object())
        self.root.bind("p", lambda e: self.prev_object())
        self.root.bind("s", lambda e: self.save_json())
        self.root.bind("u", lambda e: self.undo())
        self.root.bind("o", lambda e: self.load_image())
        self.root.bind("l", lambda e: self.load_json())

    def update_image(self):
        width = int(self.original_image.width * self.scale)
        height = int(self.original_image.height * self.scale)
        resized = self.original_image.resize((width, height), Image.Resampling.LANCZOS)
        self.tk_image = ImageTk.PhotoImage(resized)
        self.canvas.delete(self.image_id)
        self.image_id = self.canvas.create_image(self.pan_x, self.pan_y, anchor="nw", image=self.tk_image)
        for circle in self.circles:
            self.canvas.tag_lower(self.image_id, circle)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if not file_path:
            return

        self.original_image = Image.open(file_path)
        self.tk_image = ImageTk.PhotoImage(self.original_image)
        self.canvas.delete(self.image_id)
        self.image_id = self.canvas.create_image(self.pan_x, self.pan_y, anchor="nw", image=self.tk_image)

        basename = os.path.basename(file_path)
        frame_num = os.path.splitext(basename)[0]
        try:
            self.FRAME_INDEX = int(frame_num)
        except ValueError:
            self.FRAME_INDEX = 0

    def load_json(self):
        file_path = filedialog.askopenfilename(
            title="Select JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if not file_path:
            return

        with open(file_path, 'r') as f:
            data = json.load(f)

        self.annotations.clear()
        self.history.clear()
        for circle in self.circles:
            self.canvas.delete(circle)
        self.circles.clear()

        for entry in data:
            object_id = entry["object_id"]
            self.annotations[object_id] = {
                "points": entry["points"],
                "labels": entry["labels"]
            }

        if self.annotations:
            self.current_object_id = max(self.annotations.keys()) + 1
        else:
            self.current_object_id = 1

        self.update_circles()

        # Reset view
        self.scale = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.update_image()
        self.update_circles()

    def start_pan(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def do_pan(self, event):
        dx = event.x - self.drag_start_x
        dy = event.y - self.drag_start_y
        self.pan_x += dx
        self.pan_y += dy
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.update_image()
        for circle in self.circles:
            coords = self.canvas.coords(circle)
            self.canvas.coords(circle, coords[0] + dx, coords[1] + dy, coords[2] + dx, coords[3] + dy)

    def zoom(self, event):
        factor = 1.1 if event.delta > 0 else 0.9
        old_scale = self.scale
        self.scale *= factor
        mx = event.x - self.pan_x
        my = event.y - self.pan_y
        self.pan_x = event.x - mx * (self.scale / old_scale)
        self.pan_y = event.y - my * (self.scale / old_scale)
        self.update_image()
        self.update_circles()

    def update_circles(self):
        for circle in self.circles:
            self.canvas.delete(circle)
        self.circles.clear()
        if self.current_object_id in self.annotations:
            points = self.annotations[self.current_object_id]["points"]
            labels = self.annotations[self.current_object_id]["labels"]
            for (x, y), label in zip(points, labels):
                self.draw_circle(x, y, label)

    def draw_circle(self, x, y, label):
        canvas_x = self.pan_x + x * self.scale
        canvas_y = self.pan_y + y * self.scale
        radius = 5
        color = "blue" if label == 1 else "red"
        circle = self.canvas.create_oval(
            canvas_x - radius, canvas_y - radius,
            canvas_x + radius, canvas_y + radius,
            fill=color, outline=color
        )
        self.circles.append(circle)
        return circle

    def add_point(self, event, label):
        x = (event.x - self.pan_x) / self.scale
        y = (event.y - self.pan_y) / self.scale

        if self.current_object_id not in self.annotations:
            self.annotations[self.current_object_id] = {"points": [], "labels": []}

        point = [int(x), int(y)]
        self.annotations[self.current_object_id]["points"].append(point)
        self.annotations[self.current_object_id]["labels"].append(label)
        circle = self.draw_circle(x, y, label)

        # Add to history
        self.history.append({
            "object_id": self.current_object_id,
            "point": point,
            "label": label,
            "circle": circle
        })

    def add_blue_point(self, event):
        self.add_point(event, 1)

    def add_red_point(self, event):
        self.add_point(event, 0)

    def undo(self):
        if not self.history:
            return

        last_action = self.history.pop()
        obj_id = last_action["object_id"]

        if obj_id in self.annotations:
            # Remove the last point and label
            if self.annotations[obj_id]["points"]:
                self.annotations[obj_id]["points"].pop()
                self.annotations[obj_id]["labels"].pop()

            # Remove the circle from display
            if last_action["circle"] in self.circles:
                self.canvas.delete(last_action["circle"])
                self.circles.remove(last_action["circle"])

            # Clean up empty object
            if not self.annotations[obj_id]["points"]:
                del self.annotations[obj_id]

    def next_object(self):
        self.current_object_id += 1
        self.update_circles()

    def prev_object(self):
        if self.current_object_id > 1:
            self.current_object_id -= 1
            self.update_circles()

    def save_json(self):
        output = []
        for object_id, data in self.annotations.items():
            if data["points"]:
                output.append({
                    "frame_index": FRAME_INDEX,
                    "object_id": object_id,
                    "points": data["points"],
                    "labels": data["labels"]
                })

        with open(ANN_PATH, "w") as f:
            json.dump(output, f, indent=2)
        print(f"Saved to {ANN_PATH}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageAnnotator(root)
    root.mainloop()