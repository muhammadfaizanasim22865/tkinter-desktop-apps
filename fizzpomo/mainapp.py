import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class PomodoroTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro To-Do Manager")
        self.root.geometry("1400x750")
        self.root.configure(bg="#b8c04a")
        
        # Color scheme
        self.colors = {
            'bg': "#374c6b",
            'card': "#202935",
            'accent': "#460f60",
            'primary': "#bd6429",
            'success': "#16e26b",
            'warning': '#f39c12',
            'info': "#ced125",
            'text': '#eee',
            'text_dark': '#94a3b8',
            'timer_active': '#e74c3c'
        }
        
        # Timer settings (in minutes)
        self.pomodoro_time = 40
        self.short_break = 10
        self.long_break = 25
        
        # Timer state
        self.timer_running = False
        self.timer_paused = False
        self.current_time = self.pomodoro_time * 60
        self.timer_mode = "work"
        self.pomodoros_completed = 0
        
        # File paths
        self.tasks_file = "tasks.json"
        self.stats_file = "pomodoro_stats.json"
        
        # Load data
        self.load_tasks()
        self.load_stats()
        
        # Create UI
        self.create_sidebar()
        self.create_main_area()
        self.create_stats_panel()
        
    def load_tasks(self):
        """Load tasks from file"""
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as f:
                self.tasks = json.load(f)
        else:
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to file"""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=4)
    
    def load_stats(self):
        """Load statistics"""
        if os.path.exists(self.stats_file):
            with open(self.stats_file, 'r') as f:
                self.stats = json.load(f)
        else:
            self.stats = {
                'total_pomodoros': 0,
                'total_time_focused': 0,
                'tasks_completed': 0,
                'current_streak': 0,
                'best_streak': 0,
                'last_session_date': None,
                'daily_pomodoros': {},
                'weekly_tasks': []
            }
    
    def save_stats(self):
        """Save statistics"""
        with open(self.stats_file, 'w') as f:
            json.dump(self.stats, f, indent=4)
    
    def create_sidebar(self):
        """Create sidebar with timer"""
        sidebar = tk.Frame(self.root, bg=self.colors['card'], width=320)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)
        
        # Header
        header = tk.Frame(sidebar, bg=self.colors['card'])
        header.pack(pady=30)
        
        tk.Label(header, text="⏰", font=("Segoe UI", 40), 
                bg=self.colors['card']).pack()
        tk.Label(header, text="Pomodoro Timer", font=("Segoe UI", 18, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack()
        
        # Timer display
        timer_frame = tk.Frame(sidebar, bg=self.colors['accent'], relief="flat")
        timer_frame.pack(pady=20, padx=20, fill="x")
        
        self.timer_label = tk.Label(timer_frame, text="40:00", 
                                    font=("Segoe UI", 48, "bold"),
                                    bg=self.colors['accent'], fg=self.colors['text'])
        self.timer_label.pack(pady=30)
        
        self.mode_label = tk.Label(timer_frame, text="Work Session", 
                                   font=("Segoe UI", 14),
                                   bg=self.colors['accent'], fg=self.colors['text_dark'])
        self.mode_label.pack(pady=(0, 20))
        
        # Timer controls
        controls = tk.Frame(sidebar, bg=self.colors['card'])
        controls.pack(pady=20)
        
        self.start_btn = tk.Button(controls, text="▶ Start", font=("Segoe UI", 12, "bold"),
                                   bg=self.colors['success'], fg="white", padx=25, pady=10,
                                   relief="flat", cursor="hand2", command=self.start_timer)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.pause_btn = tk.Button(controls, text="⏸ Pause", font=("Segoe UI", 12, "bold"),
                                   bg=self.colors['warning'], fg="white", padx=25, pady=10,
                                   relief="flat", cursor="hand2", command=self.pause_timer,
                                   state="disabled")
        self.pause_btn.grid(row=0, column=1, padx=5)
        
        self.reset_btn = tk.Button(controls, text="⟳ Reset", font=("Segoe UI", 12, "bold"),
                                   bg=self.colors['primary'], fg="white", padx=25, pady=10,
                                   relief="flat", cursor="hand2", command=self.reset_timer)
        self.reset_btn.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Pomodoro count
        pomo_frame = tk.Frame(sidebar, bg=self.colors['card'])
        pomo_frame.pack(pady=20)
        
        tk.Label(pomo_frame, text="🍅 Pomodoros Today", font=("Segoe UI", 12, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack()
        self.pomo_count_label = tk.Label(pomo_frame, text="0", font=("Segoe UI", 36, "bold"),
                                        bg=self.colors['card'], fg=self.colors['primary'])
        self.pomo_count_label.pack()
        
        # Quick stats
        stats_frame = tk.Frame(sidebar, bg=self.colors['accent'])
        stats_frame.pack(pady=20, padx=20, fill="x")
        
        tk.Label(stats_frame, text="📊 Quick Stats", font=("Segoe UI", 14, "bold"),
                bg=self.colors['accent'], fg=self.colors['text']).pack(pady=10)
        
        self.stats_labels = {}
        stats_data = [
            ("Total Pomodoros", self.stats['total_pomodoros']),
            ("Tasks Completed", self.stats['tasks_completed']),
            ("Current Streak", self.stats['current_streak'])
        ]
        
        for label, value in stats_data:
            frame = tk.Frame(stats_frame, bg=self.colors['accent'])
            frame.pack(fill="x", padx=15, pady=5)
            tk.Label(frame, text=label, font=("Segoe UI", 10),
                    bg=self.colors['accent'], fg=self.colors['text_dark']).pack(anchor="w")
            lbl = tk.Label(frame, text=str(value), font=("Segoe UI", 14, "bold"),
                          bg=self.colors['accent'], fg=self.colors['text'])
            lbl.pack(anchor="w")
            self.stats_labels[label] = lbl
    
    def create_main_area(self):
        """Create main task area"""
        main = tk.Frame(self.root, bg=self.colors['bg'], width=700)
        main.pack(side="left", fill="both", expand=True)
        main.pack_propagate(False)
        
        # Header
        header = tk.Frame(main, bg=self.colors['bg'])
        header.pack(fill="x", padx=30, pady=20)
        
        tk.Label(header, text="✅ My Tasks", font=("Segoe UI", 24, "bold"),
                bg=self.colors['bg'], fg=self.colors['text']).pack(anchor="w")
        tk.Label(header, text="Stay focused and get things done!", font=("Segoe UI", 12),
                bg=self.colors['bg'], fg=self.colors['text_dark']).pack(anchor="w")
        
        # Add task section
        add_frame = tk.Frame(main, bg=self.colors['card'])
        add_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        add_content = tk.Frame(add_frame, bg=self.colors['card'])
        add_content.pack(padx=20, pady=20)
        
        # Task input
        input_frame = tk.Frame(add_content, bg=self.colors['card'])
        input_frame.pack(fill="x")
        
        tk.Label(input_frame, text="Task:", font=("Segoe UI", 11, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.task_entry = tk.Entry(input_frame, font=("Segoe UI", 11), width=30,
                                   bg=self.colors['accent'], fg=self.colors['text'],
                                   insertbackground=self.colors['text'], relief="flat")
        self.task_entry.grid(row=1, column=0, ipady=8, padx=(0, 10))
        self.task_entry.bind("<Return>", lambda e: self.add_task())
        
        # Priority dropdown
        tk.Label(input_frame, text="Priority:", font=("Segoe UI", 11, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).grid(row=0, column=1, sticky="w", pady=(0, 5))
        
        self.priority_var = tk.StringVar(value="Medium")
        priority_menu = ttk.Combobox(input_frame, textvariable=self.priority_var,
                                     values=["High", "Medium", "Low"], state="readonly", width=10)
        priority_menu.grid(row=1, column=1, ipady=8, padx=(0, 10))
        
        # Add button
        add_btn = tk.Button(input_frame, text="➕ Add", font=("Segoe UI", 11, "bold"),
                          bg=self.colors['primary'], fg="white", padx=15, pady=10,
                          relief="flat", cursor="hand2", command=self.add_task)
        add_btn.grid(row=1, column=2)
        
        # Filter buttons
        filter_frame = tk.Frame(main, bg=self.colors['bg'])
        filter_frame.pack(fill="x", padx=30, pady=(0, 10))
        
        self.filter_var = tk.StringVar(value="all")
        
        filters = [("All", "all"), ("Active", "active"), ("Completed", "completed")]
        for text, value in filters:
            btn = tk.Radiobutton(filter_frame, text=text, variable=self.filter_var,
                                value=value, font=("Segoe UI", 10, "bold"),
                                bg=self.colors['bg'], fg=self.colors['text'],
                                selectcolor=self.colors['accent'], activebackground=self.colors['bg'],
                                activeforeground=self.colors['primary'], command=self.filter_tasks)
            btn.pack(side="left", padx=10)
        
        # Tasks list
        list_frame = tk.Frame(main, bg=self.colors['bg'])
        list_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        canvas = tk.Canvas(list_frame, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        
        self.tasks_container = tk.Frame(canvas, bg=self.colors['bg'])
        
        self.tasks_container.bind("<Configure>",
                                 lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=self.tasks_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        self.display_tasks()
    
    def create_stats_panel(self):
        """Create statistics and charts panel"""
        stats_panel = tk.Frame(self.root, bg=self.colors['bg'], width=380)
        stats_panel.pack(side="right", fill="both", expand=True)
        stats_panel.pack_propagate(False)
        
        # Header
        header = tk.Frame(stats_panel, bg=self.colors['bg'])
        header.pack(fill="x", padx=20, pady=20)
        
        tk.Label(header, text="📊 Analytics", font=("Segoe UI", 20, "bold"),
                bg=self.colors['bg'], fg=self.colors['text']).pack(anchor="w")
        
        # Canvas for scrolling
        canvas = tk.Canvas(stats_panel, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = tk.Scrollbar(stats_panel, orient="vertical", command=canvas.yview)
        
        self.charts_container = tk.Frame(canvas, bg=self.colors['bg'])
        
        self.charts_container.bind("<Configure>",
                                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=self.charts_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
        scrollbar.pack(side="right", fill="y", padx=(0, 20))
        
        self.create_charts()
    
    def create_charts(self):
        """Create all charts"""
        for widget in self.charts_container.winfo_children():
            widget.destroy()
        
        # Chart 1: Weekly Pomodoros
        self.create_weekly_pomodoros_chart()
        
        # Chart 2: Task Priority Distribution
        self.create_priority_pie_chart()
        
        # Chart 3: Productivity Trend
        self.create_productivity_trend()
    
    def create_weekly_pomodoros_chart(self):
        """Create weekly pomodoros bar chart"""
        chart_frame = tk.Frame(self.charts_container, bg=self.colors['card'])
        chart_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(chart_frame, text="📅 Last 7 Days - Pomodoros", font=("Segoe UI", 12, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack(pady=10)
        
        # Get last 7 days data
        daily_data = self.stats.get('daily_pomodoros', {})
        last_7_days = [(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(6, -1, -1)]
        counts = [daily_data.get(day, 0) for day in last_7_days]
        labels = [(datetime.now() - timedelta(days=i)).strftime("%a") for i in range(6, -1, -1)]
        
        # Create matplotlib figure
        fig = Figure(figsize=(3.5, 2.5), facecolor=self.colors['card'])
        ax = fig.add_subplot(111)
        ax.set_facecolor(self.colors['card'])
        
        bars = ax.bar(labels, counts, color=self.colors['primary'], width=0.6)
        
        # # Customize
        # ax.set_ylabel('Pomodoros', color=self.colors['text'], fontsize=9)
        # ax.tick_params(colors=self.colors['text'], labelsize=8)
        # ax.spines['top'].set_visible(False)
        # ax.spines['right'].set_visible(False)
        # ax.spines['left'].set_color(self.colors['text_dark'])
        # ax.spines['bottom'].set_color(self.colors['text_dark'])
        # ax.grid(axis='y', alpha=0.3, color=self.colors['text_dark'], linestyle='--')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{int(height)}', ha='center', va='bottom',
                       color=self.colors['text'], fontsize=8)
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)
    
    def create_priority_pie_chart(self):
        """Create task priority distribution pie chart"""
        chart_frame = tk.Frame(self.charts_container, bg=self.colors['card'])
        chart_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(chart_frame, text="🎯 Tasks by Priority", font=("Segoe UI", 12, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack(pady=10)
        
        # Count tasks by priority
        priority_counts = {'High': 0, 'Medium': 0, 'Low': 0}
        for task in self.tasks:
            if not task['completed']:
                priority_counts[task['priority']] += 1
        
        # Only show if there are tasks
        if sum(priority_counts.values()) == 0:
            tk.Label(chart_frame, text="No active tasks yet!", font=("Segoe UI", 10),
                    bg=self.colors['card'], fg=self.colors['text_dark']).pack(pady=20)
        else:
            labels = [k for k, v in priority_counts.items() if v > 0]
            sizes = [v for v in priority_counts.values() if v > 0]
            colors_list = ['#e74c3c', '#f39c12', '#3498db']
            colors_filtered = [colors_list[i] for i, v in enumerate(priority_counts.values()) if v > 0]
            
            fig = Figure(figsize=(3.5, 2.5), facecolor=self.colors['card'])
            ax = fig.add_subplot(111)
            ax.set_facecolor(self.colors['card'])
            
            wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors_filtered,
                                               autopct='%1.0f%%', startangle=90)
            
            for text in texts:
                text.set_color(self.colors['text'])
                text.set_fontsize(9)
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(9)
                autotext.set_weight('bold')
            
            fig.tight_layout()
            
            canvas = FigureCanvasTkAgg(fig, chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)
    
    def create_productivity_trend(self):
        """Create productivity trend line chart"""
        chart_frame = tk.Frame(self.charts_container, bg=self.colors['card'])
        chart_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(chart_frame, text="📈 Productivity Trend", font=("Segoe UI", 12, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack(pady=10)
        
        # Summary stats
        stats_grid = tk.Frame(chart_frame, bg=self.colors['card'])
        stats_grid.pack(pady=10)
        
        stats_info = [
            ("🔥 Best Streak", f"{self.stats['best_streak']} days"),
            ("⏱️ Total Time", f"{self.stats['total_time_focused']} min"),
            ("✅ Completed", f"{self.stats['tasks_completed']} tasks")
        ]
        
        for i, (label, value) in enumerate(stats_info):
            frame = tk.Frame(stats_grid, bg=self.colors['accent'])
            frame.grid(row=i//2, column=i%2, padx=5, pady=5, sticky="ew")
            
            tk.Label(frame, text=label, font=("Segoe UI", 9),
                    bg=self.colors['accent'], fg=self.colors['text_dark']).pack(pady=(8, 2))
            tk.Label(frame, text=value, font=("Segoe UI", 11, "bold"),
                    bg=self.colors['accent'], fg=self.colors['text']).pack(pady=(0, 8))
    
    def add_task(self):
        """Add new task"""
        task_text = self.task_entry.get().strip()
        if not task_text:
            messagebox.showwarning("Empty Task", "Please enter a task!")
            return
        
        task = {
            'id': len(self.tasks) + 1,
            'text': task_text,
            'priority': self.priority_var.get(),
            'completed': False,
            'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'pomodoros_spent': 0
        }
        
        self.tasks.append(task)
        self.save_tasks()
        self.task_entry.delete(0, 'end')
        self.display_tasks()
        self.create_charts()
    
    def toggle_task(self, task_id):
        """Toggle task completion"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
                if task['completed']:
                    self.stats['tasks_completed'] += 1
                    self.save_stats()
                    self.update_stats_display()
                break
        self.save_tasks()
        self.display_tasks()
        self.create_charts()
    
    def delete_task(self, task_id):
        """Delete task"""
        self.tasks = [t for t in self.tasks if t['id'] != task_id]
        self.save_tasks()
        self.display_tasks()
        self.create_charts()
    
    def filter_tasks(self):
        """Filter tasks based on selection"""
        self.display_tasks()
    
    def display_tasks(self):
        """Display tasks"""
        for widget in self.tasks_container.winfo_children():
            widget.destroy()
        
        filter_type = self.filter_var.get()
        
        # Filter tasks
        if filter_type == "active":
            filtered_tasks = [t for t in self.tasks if not t['completed']]
        elif filter_type == "completed":
            filtered_tasks = [t for t in self.tasks if t['completed']]
        else:
            filtered_tasks = self.tasks
        
        # Sort by priority
        priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
        filtered_tasks.sort(key=lambda x: (x['completed'], priority_order[x['priority']]))
        
        if not filtered_tasks:
            tk.Label(self.tasks_container, text="No tasks yet. Add one above! 🎯",
                    font=("Segoe UI", 14), bg=self.colors['bg'],
                    fg=self.colors['text_dark']).pack(pady=50)
            return
        
        for task in filtered_tasks:
            self.create_task_card(task)
    
    def create_task_card(self, task):
        """Create task card"""
        priority_colors = {
            'High': '#e74c3c',
            'Medium': '#f39c12',
            'Low': '#3498db'
        }
        
        card = tk.Frame(self.tasks_container, bg=self.colors['card'], relief="flat")
        card.pack(fill="x", pady=5)
        
        # Priority indicator
        indicator = tk.Frame(card, bg=priority_colors[task['priority']], width=5)
        indicator.pack(side="left", fill="y")
        
        content = tk.Frame(card, bg=self.colors['card'])
        content.pack(side="left", fill="x", expand=True, padx=15, pady=15)
        
        # Checkbox and task text
        top_frame = tk.Frame(content, bg=self.colors['card'])
        top_frame.pack(fill="x")
        
        check_var = tk.BooleanVar(value=task['completed'])
        check = tk.Checkbutton(top_frame, variable=check_var, bg=self.colors['card'],
                              activebackground=self.colors['card'], selectcolor=self.colors['success'],
                              command=lambda: self.toggle_task(task['id']))
        check.pack(side="left")
        
        text_style = ("Segoe UI", 11, "overstrike" if task['completed'] else "normal")
        text_color = self.colors['text_dark'] if task['completed'] else self.colors['text']
        
        tk.Label(top_frame, text=task['text'], font=text_style,
                bg=self.colors['card'], fg=text_color, anchor="w").pack(side="left", fill="x", expand=True, padx=10)
        
        # Priority badge
        tk.Label(top_frame, text=task['priority'], font=("Segoe UI", 8, "bold"),
                bg=priority_colors[task['priority']], fg="white",
                padx=6, pady=2).pack(side="left", padx=5)
        
        # Delete button
        del_btn = tk.Button(top_frame, text="🗑", font=("Segoe UI", 11),
                          bg=self.colors['card'], fg=self.colors['primary'],
                          relief="flat", cursor="hand2", borderwidth=0,
                          command=lambda: self.delete_task(task['id']))
        del_btn.pack(side="left")
        
        # Task info
        info_frame = tk.Frame(content, bg=self.colors['card'])
        info_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(info_frame, text=f"🍅 {task['pomodoros_spent']}",
                font=("Segoe UI", 8), bg=self.colors['card'],
                fg=self.colors['text_dark']).pack(side="left", padx=(35, 10))
        
        tk.Label(info_frame, text=f"📅 {task['created'][:10]}",
                font=("Segoe UI", 8), bg=self.colors['card'],
                fg=self.colors['text_dark']).pack(side="left")
    
    def start_timer(self):
        """Start the timer"""
        if not self.timer_running:
            self.timer_running = True
            self.timer_paused = False
            self.start_btn.config(state="disabled")
            self.pause_btn.config(state="normal")
            self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
            self.timer_thread.start()
    
    def pause_timer(self):
        """Pause the timer"""
        if self.timer_running and not self.timer_paused:
            self.timer_paused = True
            self.pause_btn.config(text="▶ Resume")
        elif self.timer_running and self.timer_paused:
            self.timer_paused = False
            self.pause_btn.config(text="⏸ Pause")
    
    def reset_timer(self):
        """Reset the timer"""
        self.timer_running = False
        self.timer_paused = False
        self.current_time = self.pomodoro_time * 60
        self.timer_mode = "work"
        self.update_timer_display()
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled", text="⏸ Pause")
        self.mode_label.config(text="Work Session")
    
    def run_timer(self):
        """Run timer in background"""
        while self.timer_running and self.current_time > 0:
            if not self.timer_paused:
                time.sleep(1)
                self.current_time -= 1
                self.root.after(0, self.update_timer_display)
        
        if self.current_time == 0 and self.timer_running:
            self.root.after(0, self.timer_finished)
    
    def update_timer_display(self):
        """Update timer display"""
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
    
    def timer_finished(self):
        """Handle timer completion"""
        self.timer_running = False
        
        if self.timer_mode == "work":
            self.pomodoros_completed += 1
            self.pomo_count_label.config(text=str(self.pomodoros_completed))
            
            # Update stats
            self.stats['total_pomodoros'] += 1
            self.stats['total_time_focused'] += self.pomodoro_time
            
            # Update daily pomodoros
            today = datetime.now().strftime("%Y-%m-%d")
            if 'daily_pomodoros' not in self.stats:
                self.stats['daily_pomodoros'] = {}
            self.stats['daily_pomodoros'][today] = self.stats['daily_pomodoros'].get(today, 0) + 1
            
            # Update streak
            if self.stats['last_session_date'] != today:
                if self.stats['last_session_date'] == (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"):
                    self.stats['current_streak'] += 1
                else:
                    self.stats['current_streak'] = 1
                self.stats['last_session_date'] = today
            
            if self.stats['current_streak'] > self.stats['best_streak']:
                self.stats['best_streak'] = self.stats['current_streak']
            
            self.save_stats()
            self.update_stats_display()
            self.create_charts()
            
            # Switch to break
            if self.pomodoros_completed % 4 == 0:
                self.timer_mode = "long_break"
                self.current_time = self.long_break * 60
                self.mode_label.config(text="Long Break! 🎉")
                messagebox.showinfo("Break Time!", "Great work! Take a 30-minute break!")
            else:
                self.timer_mode = "short_break"
                self.current_time = self.short_break * 60
                self.mode_label.config(text="Short Break! ☕")
                messagebox.showinfo("Break Time!", "Good job! Take a 10-minute break!")
        else:
            # Break finished, back to work
            self.timer_mode = "work"
            self.current_time = self.pomodoro_time * 60
            self.mode_label.config(text="Work Session")
            messagebox.showinfo("Break Over!", "Ready to focus again? Let's go!")
        
        self.update_timer_display()
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled", text="⏸ Pause")
    
    def update_stats_display(self):
        """Update statistics display"""
        self.stats_labels["Total Pomodoros"].config(text=str(self.stats['total_pomodoros']))
        self.stats_labels["Tasks Completed"].config(text=str(self.stats['tasks_completed']))
        self.stats_labels["Current Streak"].config(text=str(self.stats['current_streak']))

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTodoApp(root)
    root.mainloop()