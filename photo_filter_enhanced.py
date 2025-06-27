import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ExifTags
import os
import shutil
from pathlib import Path
from datetime import datetime
import json
import threading
import concurrent.futures

class PhotoFilterApp:
    VERSION = "3.1.0"
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"Pickish - Photo Filter v{self.VERSION}")
        self.root.geometry("1200x900")  # Main window with large photo area
        self.root.configure(bg='#2c3e50')
        self.image_label = None
        self.current_image_size = (800, 600)
        # Photo formats to support
        self.photo_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif', '.webp', '.heic', '.heif'}
        # Variables
        self.input_folder = tk.StringVar()
        self.current_photo_index = 0
        self.photo_list = []
        self.current_photo_path = None
        self.liked_count = 0
        self.loved_count = 0
        self.skipped_count = 0
        self.decision_history = []  # (action, src_path, dest_path, index)
        self.max_history = 50
        # Thread pool for file operations
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        # Image caching
        self.image_cache = {}  # path -> PhotoImage
        # Move queue for sequential processing
        self.move_queue = []
        self.processing_move = False
        # Failed moves tracking
        self.failed_moves = {}  # src -> (attempts, action, subfolder)
        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title with version
        title_label = tk.Label(main_frame, text=f"Pickish v{self.VERSION}", font=('Arial', 24, 'bold'), 
                              fg='#ecf0f1', bg='#2c3e50')
        title_label.pack(pady=(0, 20))
        
        subtitle_label = tk.Label(main_frame, text="Photo Filter & Organizer", 
                                 font=('Arial', 12), fg='#bdc3c7', bg='#2c3e50')
        subtitle_label.pack(pady=(0, 30))
        
        # Stats frame at the top (always visible)
        self.stats_frame = tk.Frame(main_frame, bg='#34495e', relief=tk.RAISED, bd=2)
        self.stats_frame.pack(fill=tk.X, pady=(0, 20))
        self.liked_label = tk.Label(self.stats_frame, text="Liked: 0", 
                                   font=('Arial', 14, 'bold'), fg='#27ae60', bg='#34495e')
        self.liked_label.pack(side=tk.LEFT, padx=20, pady=10)
        self.loved_label = tk.Label(self.stats_frame, text="Loved: 0", 
                                   font=('Arial', 14, 'bold'), fg='#e67e22', bg='#34495e')
        self.loved_label.pack(side=tk.LEFT, padx=20, pady=10)
        self.skipped_label = tk.Label(self.stats_frame, text="Skipped: 0", 
                                     font=('Arial', 14, 'bold'), fg='#e74c3c', bg='#34495e')
        self.skipped_label.pack(side=tk.LEFT, padx=20, pady=10)
        self.total_label = tk.Label(self.stats_frame, text="Total: 0", 
                                   font=('Arial', 14, 'bold'), fg='#ecf0f1', bg='#34495e')
        self.total_label.pack(side=tk.RIGHT, padx=20, pady=10)
        
        # Main content area - horizontal layout
        content_frame = tk.Frame(main_frame, bg='#2c3e50')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Photo viewer
        self.photo_frame = tk.LabelFrame(content_frame, text="Photo Viewer", 
                                        font=('Arial', 12, 'bold'), fg='#ecf0f1', 
                                        bg='#34495e', relief=tk.RAISED, bd=2)
        self.photo_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Photo display area with canvas
        self.photo_canvas = tk.Canvas(self.photo_frame, bg='#2c3e50', highlightthickness=0)
        self.photo_canvas.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Bind resize event to canvas
        self.photo_canvas.bind('<Configure>', self._on_canvas_resize)
        
        # Progress frame
        self.progress_frame = tk.Frame(self.photo_frame, bg='#34495e')
        self.progress_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        self.progress_label = tk.Label(self.progress_frame, text="", 
                                      font=('Arial', 10), fg='#ecf0f1', bg='#34495e')
        self.progress_label.pack()
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(5, 0))
        
        # Control buttons frame
        self.control_frame = tk.Frame(self.photo_frame, bg='#34495e')
        self.control_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
        
        # Dislike/Undo/Like/Love buttons in a row with even spacing
        self.dislike_button = tk.Button(self.control_frame, text="👎 DISLIKE", 
                                       command=self.dislike_photo,
                                       bg='#e74c3c', fg='white', font=('Arial', 16, 'bold'),
                                       relief=tk.FLAT, padx=40, pady=15)
        self.dislike_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.undo_button = tk.Button(self.control_frame, text="↶ UNDO", 
                                    command=self.undo_last_decision,
                                    bg='#9b59b6', fg='white', font=('Arial', 14, 'bold'),
                                    relief=tk.FLAT, padx=30, pady=15)
        self.undo_button.pack(side=tk.LEFT, padx=10)
        
        self.like_button = tk.Button(self.control_frame, text="👍 LIKE", 
                                    command=self.like_photo,
                                    bg='#27ae60', fg='white', font=('Arial', 16, 'bold'),
                                    relief=tk.FLAT, padx=40, pady=15)
        self.like_button.pack(side=tk.LEFT, padx=10)
        
        self.love_button = tk.Button(self.control_frame, text="❤️ LOVE", 
                                    command=self.love_photo,
                                    bg='#e67e22', fg='white', font=('Arial', 16, 'bold'),
                                    relief=tk.FLAT, padx=40, pady=15)
        self.love_button.pack(side=tk.LEFT, padx=(10, 0))
        
        # Center the button frame
        self.control_frame.pack_configure(anchor=tk.CENTER)
        
        # Right side - Controls and settings
        right_frame = tk.Frame(content_frame, bg='#2c3e50')
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # Folder selection frame
        folder_frame = tk.LabelFrame(right_frame, text="Input Folder", 
                                    font=('Arial', 12, 'bold'), fg='#ecf0f1', 
                                    bg='#34495e', relief=tk.RAISED, bd=2)
        folder_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Input folder selection
        input_frame = tk.Frame(folder_frame, bg='#34495e')
        input_frame.pack(fill=tk.X, padx=15, pady=10)
        tk.Label(input_frame, text="Input Folder:", font=('Arial', 10, 'bold'), 
                fg='#ecf0f1', bg='#34495e').pack(anchor=tk.W)
        input_select_frame = tk.Frame(input_frame, bg='#34495e')
        input_select_frame.pack(fill=tk.X, pady=(5, 0))
        tk.Entry(input_select_frame, textvariable=self.input_folder, 
                font=('Arial', 10), state='readonly', width=30).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(input_select_frame, text="Browse", command=self.select_input_folder,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                 relief=tk.FLAT, padx=20).pack(side=tk.RIGHT, padx=(10, 0))
        
        # Action buttons frame
        action_frame = tk.Frame(right_frame, bg='#2c3e50')
        action_frame.pack(pady=20)
        
        # Start button
        self.start_button = tk.Button(action_frame, text="Start Filtering", 
                                     command=self.start_filtering,
                                     bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                                     relief=tk.FLAT, padx=30, pady=10)
        self.start_button.pack(fill=tk.X, pady=(0, 10))
        
        # Instructions
        instructions = tk.Label(right_frame, text="💡 Tip: Left=Skip, Right=Like, Down=Love, Up=Undo, Space=Like", 
                               font=('Arial', 10), fg='#bdc3c7', bg='#2c3e50', wraplength=300)
        instructions.pack(pady=20)
        
        # Warning display for failed moves
        self.warning_frame = tk.Frame(right_frame, bg='#2c3e50')
        self.warning_frame.pack(fill=tk.X, pady=(10, 0))
        self.warning_label = tk.Label(self.warning_frame, text="", 
                                     font=('Arial', 9), fg='#e74c3c', bg='#2c3e50', 
                                     wraplength=300, justify=tk.LEFT)
        self.warning_label.pack()
        
        # Move logger frame
        logger_frame = tk.LabelFrame(right_frame, text="Move Logger", 
                                    font=('Arial', 10, 'bold'), fg='#ecf0f1', 
                                    bg='#34495e', relief=tk.RAISED, bd=2)
        logger_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Create scrollable text widget for logging
        self.logger_text = tk.Text(logger_frame, height=8, width=35, 
                                  font=('Consolas', 8), bg='#2c3e50', fg='#ecf0f1',
                                  relief=tk.FLAT, wrap=tk.WORD, state=tk.DISABLED)
        self.logger_scrollbar = tk.Scrollbar(logger_frame, orient=tk.VERTICAL, command=self.logger_text.yview)
        self.logger_text.configure(yscrollcommand=self.logger_scrollbar.set)
        
        self.logger_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.logger_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Clear logger button
        clear_logger_button = tk.Button(logger_frame, text="Clear Log", 
                                       command=self.clear_logger,
                                       bg='#95a5a6', fg='white', font=('Arial', 8, 'bold'),
                                       relief=tk.FLAT, padx=10, pady=2)
        clear_logger_button.pack(pady=(0, 5))
        
        # Bind keyboard shortcuts
        self.root.bind('<Left>', lambda e: self.dislike_photo())  # Left = Skip
        self.root.bind('<Right>', lambda e: self.like_photo())    # Right = Like
        self.root.bind('<Down>', lambda e: self.love_photo())     # Down = Love
        self.root.bind('<Up>', lambda e: self.undo_last_decision())  # Up = Undo
        self.root.bind('<space>', lambda e: self.like_photo())    # Space = Like
        
        # Update button states
        self.update_button_states()
        
    def update_button_states(self):
        """Update the enabled/disabled state of action buttons"""
        has_history = len(self.decision_history) > 0
        
        self.undo_button.config(state='normal' if has_history else 'disabled')

    def select_input_folder(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder.set(folder)
            
    def start_filtering(self):
        if not self.input_folder.get():
            messagebox.showerror("Error", "Please select the input folder!")
            return
        self.photo_list = self.scan_photos()
        if not self.photo_list:
            messagebox.showinfo("No Photos", "No photos found in the selected folder!")
            return
        self.current_photo_index = 0
        self.liked_count = 0
        self.skipped_count = 0
        self.decision_history.clear()
        self.update_stats()
        self.display_current_photo()
        
    def scan_photos(self):
        photos = []
        input_path = Path(self.input_folder.get())
        for root, dirs, files in os.walk(input_path):
            # Remove FINAL and SKIPPED from dirs so os.walk doesn't visit them
            dirs[:] = [d for d in dirs if d not in ("FINAL", "SKIPPED")]
            for file in files:
                file_path = os.path.join(root, file)
                if Path(file).suffix.lower() in self.photo_extensions:
                    # Exclude files already in FINAL or SKIPPED
                    if "FINAL" not in Path(file_path).parts and "SKIPPED" not in Path(file_path).parts:
                        # Use creation time instead of modification time
                        try:
                            # Try to get creation time (Windows)
                            created_time = os.path.getctime(file_path)
                        except:
                            # Fallback to modification time if creation time not available
                            created_time = os.path.getmtime(file_path)
                        photos.append((file_path, created_time))
        photos.sort(key=lambda x: x[1], reverse=True)  # Sort by creation time, newest first
        return [photo[0] for photo in photos]
        
    def update_stats(self):
        self.liked_label.config(text=f"Liked: {self.liked_count}")
        self.loved_label.config(text=f"Loved: {self.loved_count}")
        self.skipped_label.config(text=f"Skipped: {self.skipped_count}")
        self.total_label.config(text=f"Total: {len(self.photo_list)}")
        
    def preload_next_image(self):
        """Preload the next image in the background"""
        if self.current_photo_index + 1 < len(self.photo_list):
            next_path = self.photo_list[self.current_photo_index + 1]
            if next_path not in self.image_cache:
                threading.Thread(target=self._cache_image, args=(next_path,), daemon=True).start()

    def _on_canvas_resize(self, event):
        """Handle canvas resize events"""
        if hasattr(self, 'current_photo_path') and self.current_photo_path:
            # Clear cache and redisplay current image with new dimensions
            self.image_cache.clear()
            self.show_image_in_canvas(self.current_photo_path)

    def get_canvas_dimensions(self):
        """Get current canvas dimensions"""
        self.photo_canvas.update_idletasks()
        canvas_w = self.photo_canvas.winfo_width()
        canvas_h = self.photo_canvas.winfo_height()
        if canvas_w < 100 or canvas_h < 100:
            # Fallback dimensions if canvas not yet properly sized
            canvas_w, canvas_h = 800, 600
        return canvas_w, canvas_h

    def _cache_image(self, image_path):
        """Cache an image in the background"""
        try:
            img = Image.open(image_path)
            # Apply EXIF rotation
            try:
                for orientation in ExifTags.TAGS.keys():
                    if ExifTags.TAGS[orientation] == 'Orientation':
                        break
                exif = img._getexif()
                if exif is not None:
                    orientation_value = exif.get(orientation, None)
                    if orientation_value == 3:
                        img = img.rotate(180, expand=True)
                    elif orientation_value == 6:
                        img = img.rotate(270, expand=True)
                    elif orientation_value == 8:
                        img = img.rotate(90, expand=True)
            except Exception:
                pass
            
            # Get canvas size for scaling
            canvas_w, canvas_h = self.get_canvas_dimensions()
            
            img_w, img_h = img.size
            scale = min(canvas_w / img_w, canvas_h / img_h, 1.0)
            new_w = int(img_w * scale)
            new_h = int(img_h * scale)
            img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            
            # Store in cache
            self.image_cache[image_path] = photo
        except Exception:
            pass  # Silently fail for caching

    def show_image_in_canvas(self, image_path):
        self.photo_canvas.delete("all")
        
        # Check if image is cached
        if image_path in self.image_cache:
            photo = self.image_cache[image_path]
            # Get canvas size for positioning
            canvas_w, canvas_h = self.get_canvas_dimensions()
            
            # Calculate position (center the image)
            img_w = photo.width()
            img_h = photo.height()
            x = (canvas_w - img_w) // 2
            y = (canvas_h - img_h) // 2
            
            self.photo_canvas.create_image(x, y, anchor=tk.NW, image=photo, tags="img")
            self.photo_canvas.image = photo
        else:
            # Fallback to original loading method
            try:
                img = Image.open(image_path)
                try:
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation] == 'Orientation':
                            break
                    exif = img._getexif()
                    if exif is not None:
                        orientation_value = exif.get(orientation, None)
                        if orientation_value == 3:
                            img = img.rotate(180, expand=True)
                        elif orientation_value == 6:
                            img = img.rotate(270, expand=True)
                        elif orientation_value == 8:
                            img = img.rotate(90, expand=True)
                except Exception:
                    pass
                # Get canvas size
                canvas_w, canvas_h = self.get_canvas_dimensions()
                img_w, img_h = img.size
                scale = min(canvas_w / img_w, canvas_h / img_h, 1.0)
                new_w = int(img_w * scale)
                new_h = int(img_h * scale)
                img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                x = (canvas_w - new_w) // 2
                y = (canvas_h - new_h) // 2
                self.photo_canvas.create_image(x, y, anchor=tk.NW, image=photo, tags="img")
                self.photo_canvas.image = photo
                # Cache the image
                self.image_cache[image_path] = photo
            except Exception as e:
                self.photo_canvas.create_text(10, 10, anchor=tk.NW, text=f"Error loading image: {str(e)}", fill="#e74c3c", font=("Arial", 12, "bold"))

    def display_current_photo(self):
        if self.current_photo_index >= len(self.photo_list):
            self.show_completion()
            self.clear_photo_canvas()
            return
        self.current_photo_path = self.photo_list[self.current_photo_index]
        progress = (self.current_photo_index + 1) / len(self.photo_list) * 100
        self.progress_bar['value'] = progress
        self.progress_label.config(text=f"Photo {self.current_photo_index + 1} of {len(self.photo_list)}")
        # Display image in canvas (will use cache if available)
        self.show_image_in_canvas(self.current_photo_path)
        # Preload next image
        self.preload_next_image()

    def clear_photo_canvas(self):
        self.photo_canvas.delete("all")
        self.photo_canvas.image = None
        # Clear cache to free memory
        self.image_cache.clear()
        
    def undo_last_decision(self):
        """Undo the last decision made"""
        if not self.decision_history:
            self.log_message("No actions to undo", "INFO")
            return
            
        # Get the last decision
        last_action, src, dest, original_index = self.decision_history.pop()
        filename = os.path.basename(src)
        
        try:
            if last_action == "like":
                # Undo like: move photo back from FINAL to input
                self.log_message(f"Undoing like: {filename} → input folder", "INFO")
                self.move_photo(dest, "..")
                self.liked_count -= 1
            elif last_action == "love":
                # Undo love: move photo back from PERFECT to input
                self.log_message(f"Undoing love: {filename} → input folder", "INFO")
                self.move_photo(dest, "..")
                self.loved_count -= 1
            elif last_action == "dislike":
                # Undo dislike: move photo back from SKIPPED to input
                self.log_message(f"Undoing dislike: {filename} → input folder", "INFO")
                self.move_photo(dest, "..")
                self.skipped_count -= 1
            
            # Go back to the photo that was just acted upon
            if original_index < len(self.photo_list):
                self.current_photo_index = original_index
            else:
                self.current_photo_index = max(0, len(self.photo_list) - 1)
            
            # Rescan and update
            self.photo_list = self.scan_photos()
            self.update_stats()
            self.display_current_photo()
            
            self.log_message(f"Undo successful: {filename}", "SUCCESS")
            
        except Exception as e:
            error_msg = str(e)
            self.log_message(f"Undo failed: {filename} - {error_msg}", "ERROR")
            messagebox.showerror("Undo Error", f"Failed to undo action: {error_msg}\n\nIf the file was already moved or deleted, you may need to manually restore it.")
            
    def record_decision(self, action, src, dest):
        """Record a decision in the history"""
        self.decision_history.append((action, src, dest, self.current_photo_index))
        
        # Keep only the last max_history decisions
        if len(self.decision_history) > self.max_history:
            self.decision_history.pop(0)
            
    def set_buttons_state(self, state):
        self.like_button.config(state=state)
        self.love_button.config(state=state)
        self.dislike_button.config(state=state)
        self.undo_button.config(state=state)

    def like_photo(self):
        if not self.current_photo_path:
            return
        src = self.current_photo_path
        # Update UI immediately without advancing index
        self.liked_count += 1
        self.record_decision("like", src, None)
        # Don't advance index - let the rescan handle it after move
        # Queue the move operation
        self.queue_move(src, "FINAL", "like")

    def dislike_photo(self):
        if not self.current_photo_path:
            return
        src = self.current_photo_path
        # Update UI immediately without advancing index
        self.skipped_count += 1
        self.record_decision("dislike", src, None)
        # Don't advance index - let the rescan handle it after move
        # Queue the move operation
        self.queue_move(src, "SKIPPED", "dislike")

    def love_photo(self):
        if not self.current_photo_path:
            return
        src = self.current_photo_path
        # Update UI immediately without advancing index
        self.loved_count += 1
        self.record_decision("love", src, None)
        # Don't advance index - let the rescan handle it after move
        # Queue the move operation
        self.queue_move(src, "PERFECT", "love")

    def advance_photo_index(self):
        """Advance to next photo without rescanning"""
        self.current_photo_index += 1
        self.display_current_photo()

    def queue_move(self, src, subfolder, action):
        """Add a move operation to the queue"""
        filename = os.path.basename(src)
        self.log_message(f"Queued: {filename} → {subfolder}", "INFO")
        self.move_queue.append((src, subfolder, action))
        if not self.processing_move:
            self.process_next_move()

    def process_next_move(self):
        """Process the next move in the queue"""
        if not self.move_queue or self.processing_move:
            return
        
        self.processing_move = True
        src, subfolder, action = self.move_queue.pop(0)
        filename = os.path.basename(src)
        self.log_message(f"Moving: {filename} → {subfolder}", "INFO")
        
        # Start the move in background
        threading.Thread(target=self._move_file_background, args=(src, subfolder, action), daemon=True).start()

    def _move_file_background(self, src, subfolder, action):
        """Move file in background thread without blocking UI"""
        filename = os.path.basename(src)
        try:
            dest = self._move_photo_async(src, subfolder)
            
            # Validate that the file was actually moved
            if self._validate_move(src, dest):
                # Update decision history with destination
                for i in range(len(self.decision_history)-1, -1, -1):
                    if (self.decision_history[i][1] == src and 
                        self.decision_history[i][2] is None and 
                        self.decision_history[i][0] == action):
                        self.decision_history[i] = (action, src, dest, self.decision_history[i][3])
                        break
                # Remove from failed moves if it was there
                if src in self.failed_moves:
                    del self.failed_moves[src]
                # Log success
                self.root.after(0, lambda: self.log_message(f"Success: {filename} → {subfolder}", "SUCCESS"))
                # Rescan photo list after move is complete
                self.root.after(0, self._rescan_after_move)
            else:
                # Move appeared to succeed but validation failed
                raise Exception("File move validation failed - file not found at destination")
                
        except Exception as e:
            # Handle failed move with retry logic
            self._handle_failed_move(src, subfolder, action, str(e))
        finally:
            # Process next move in queue
            self.root.after(0, self._finish_move)

    def _validate_move(self, src, dest):
        """Validate that the file was actually moved to the destination"""
        try:
            # Check if source file no longer exists
            if os.path.exists(src):
                self.log_message(f"Validation failed: Source still exists: {os.path.basename(src)}", "ERROR")
                return False
            
            # Check if destination file exists
            if not os.path.exists(dest):
                self.log_message(f"Validation failed: Destination not found: {os.path.basename(dest)}", "ERROR")
                return False
            
            # Check if file sizes match (basic integrity check)
            if os.path.getsize(dest) == 0:
                self.log_message(f"Validation failed: Destination file is empty: {os.path.basename(dest)}", "ERROR")
                return False
            
            self.log_message(f"Validation passed: {os.path.basename(src)} → {os.path.basename(dest)}", "SUCCESS")
            return True
            
        except Exception as e:
            self.log_message(f"Validation error: {str(e)}", "ERROR")
            return False

    def _finish_move(self):
        """Finish current move and process next in queue"""
        self.processing_move = False
        self.process_next_move()

    def _rescan_after_move(self):
        """Rescan photo list after file move is complete"""
        old_list_length = len(self.photo_list)
        old_index = self.current_photo_index
        self.photo_list = self.scan_photos()
        self.update_stats()
        
        # Log the rescan details for debugging
        self.log_message(f"Rescan: {old_list_length} → {len(self.photo_list)} photos, index was {old_index}", "INFO")
        
        # After rescan, handle the index properly
        if self.photo_list:
            # The list shrunk by 1, so we should stay at the same index
            # (the photo at that index is now the next photo we want to see)
            if old_index >= len(self.photo_list):
                # Index is now out of bounds, go to last photo
                self.current_photo_index = len(self.photo_list) - 1
                self.log_message(f"Index out of bounds, going to last photo ({self.current_photo_index + 1} of {len(self.photo_list)})", "INFO")
            else:
                # Stay at the same index (which now points to the next photo)
                self.current_photo_index = old_index
                self.log_message(f"Staying at photo {self.current_photo_index + 1} of {len(self.photo_list)}", "INFO")
            
            self.display_current_photo()
        else:
            # No photos left, show completion
            self.log_message("No photos remaining", "INFO")
            self.show_completion()

    def _move_photo_async(self, src, subfolder):
        """Move photo in background thread without blocking UI"""
        input_dir = Path(self.input_folder.get())
        rel_path = Path(src).relative_to(input_dir)
        dest_dir = input_dir / subfolder / rel_path.parent
        os.makedirs(dest_dir, exist_ok=True)
        dest = dest_dir / rel_path.name
        counter = 1
        base, ext = os.path.splitext(dest.name)
        while dest.exists():
            dest = dest_dir / f"{base}_{counter}{ext}"
            counter += 1
        
        # This is the blocking operation - now running in thread pool
        shutil.move(str(src), str(dest))
        return str(dest)

    def move_photo(self, src, subfolder):
        input_dir = Path(self.input_folder.get())
        rel_path = Path(src).relative_to(input_dir)
        dest_dir = input_dir / subfolder / rel_path.parent
        os.makedirs(dest_dir, exist_ok=True)
        dest = dest_dir / rel_path.name
        counter = 1
        base, ext = os.path.splitext(dest.name)
        while dest.exists():
            dest = dest_dir / f"{base}_{counter}{ext}"
            counter += 1
        shutil.move(str(src), str(dest))
        return str(dest)
        
    def next_photo(self):
        # This method is now only used for undo operations
        prev_index = self.current_photo_index
        self.photo_list = self.scan_photos()
        self.update_stats()
        if not self.photo_list:
            self.current_photo_index = 0
        elif prev_index >= len(self.photo_list):
            self.current_photo_index = len(self.photo_list) - 1
        else:
            self.current_photo_index = prev_index
        self.display_current_photo()
        
    def show_completion(self):
        self.clear_photo_canvas()
        
        completion_text = "🎉 Photo filtering completed!"
            
        completion_label = tk.Label(self.photo_canvas, text=completion_text, 
                                   font=('Arial', 18, 'bold'), fg='#27ae60', bg='#2c3e50')
        completion_label.pack(expand=True)
        
        stats_text = f"Total Photos: {len(self.photo_list)}\nLiked: {self.liked_count}\nLoved: {self.loved_count}\nSkipped: {self.skipped_count}"
        stats_label = tk.Label(self.photo_canvas, text=stats_text, 
                              font=('Arial', 12), fg='#ecf0f1', bg='#2c3e50')
        stats_label.pack(pady=(20, 0))
        
        self.dislike_button.pack_forget()
        self.like_button.pack_forget()
        self.love_button.pack_forget()
        restart_button = tk.Button(self.control_frame, text="Start New Session", 
                                  command=self.restart_app,
                                  bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                                  relief=tk.FLAT, padx=30, pady=10)
        restart_button.pack(fill=tk.X, pady=20)
        
    def restart_app(self):
        self.current_photo_index = 0
        self.photo_list = []
        self.current_photo_path = None
        self.liked_count = 0
        self.loved_count = 0
        self.skipped_count = 0
        self.decision_history.clear()  # Clear undo history
        self.update_stats()
        self.clear_photo_canvas()
        self.start_button.pack(pady=20)
        self.progress_bar['value'] = 0
        self.progress_label.config(text="")
        self.dislike_button.pack(side=tk.LEFT, padx=(0, 20))
        self.like_button.pack(side=tk.LEFT, padx=10)
        self.love_button.pack(side=tk.LEFT, padx=(10, 0))
        self.update_button_states()

    def _handle_failed_move(self, src, subfolder, action, error_msg):
        """Handle a failed move with retry logic"""
        filename = os.path.basename(src)
        
        if src not in self.failed_moves:
            self.failed_moves[src] = (1, action, subfolder)
        else:
            attempts, _, _ = self.failed_moves[src]
            self.failed_moves[src] = (attempts + 1, action, subfolder)
        
        attempts, _, _ = self.failed_moves[src]
        
        if attempts < 5:
            # Log retry attempt
            self.root.after(0, lambda: self.log_message(f"Retry {attempts}/5: {filename} → {subfolder}", "RETRY"))
            # Retry the move
            self.root.after(1000, lambda: self.queue_move(src, subfolder, action))
        else:
            # Max attempts reached, show warning and log error
            self.root.after(0, lambda: self.log_message(f"Failed after 5 attempts: {filename}", "ERROR"))
            self.root.after(0, lambda: self._show_failed_move_warning(src, error_msg))

    def _show_failed_move_warning(self, src, error_msg):
        """Show warning for failed move without popup"""
        filename = os.path.basename(src)
        warning_text = f"⚠️ Failed to move: {filename}\nAttempts: 5/5\nError: {error_msg[:50]}..."
        
        # Update warning display
        current_warnings = self.warning_label.cget("text")
        if current_warnings:
            new_warnings = current_warnings + "\n\n" + warning_text
        else:
            new_warnings = warning_text
        
        self.warning_label.config(text=new_warnings)
        
        # Auto-clear warning after 30 seconds
        self.root.after(30000, lambda: self._clear_warning(filename))

    def _clear_warning(self, filename):
        """Clear warning for a specific file"""
        current_warnings = self.warning_label.cget("text")
        lines = current_warnings.split('\n\n')
        filtered_lines = [line for line in lines if filename not in line]
        new_warnings = '\n\n'.join(filtered_lines)
        self.warning_label.config(text=new_warnings)

    def log_message(self, message, level="INFO"):
        """Add a message to the logger"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if level == "SUCCESS":
            color = "#27ae60"  # Green
            prefix = "✓"
        elif level == "ERROR":
            color = "#e74c3c"  # Red
            prefix = "✗"
        elif level == "RETRY":
            color = "#f39c12"  # Orange
            prefix = "↻"
        else:
            color = "#3498db"  # Blue
            prefix = "→"
        
        log_entry = f"[{timestamp}] {prefix} {message}\n"
        
        self.logger_text.config(state=tk.NORMAL)
        self.logger_text.insert(tk.END, log_entry)
        
        # Apply color to the last line
        last_line_start = self.logger_text.index("end-2c linestart")
        last_line_end = self.logger_text.index("end-1c")
        self.logger_text.tag_add(f"color_{level}", last_line_start, last_line_end)
        self.logger_text.tag_config(f"color_{level}", foreground=color)
        
        self.logger_text.config(state=tk.DISABLED)
        self.logger_text.see(tk.END)  # Auto-scroll to bottom
        
        # Limit log entries to prevent memory issues
        lines = self.logger_text.get("1.0", tk.END).split('\n')
        if len(lines) > 100:  # Keep only last 100 lines
            self.logger_text.config(state=tk.NORMAL)
            self.logger_text.delete("1.0", f"{len(lines)-100}.0")
            self.logger_text.config(state=tk.DISABLED)

    def clear_logger(self):
        """Clear the logger display"""
        self.logger_text.config(state=tk.NORMAL)
        self.logger_text.delete("1.0", tk.END)
        self.logger_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    app = PhotoFilterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 