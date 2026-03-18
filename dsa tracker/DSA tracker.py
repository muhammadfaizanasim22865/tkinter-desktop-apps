import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime
import json
import os

class DSATracker:
    def __init__(self, root):
        self.root = root
        self.root.title("DSA Progress Tracker & Journal")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0f172a")
        
        # Color Palette
        self.colors = {
            'primary': '#6366f1',
            'secondary': '#8b5cf6',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'dark': '#0f172a',
            'darker': '#1e293b',
            'card': '#1e293b',
            'text': '#f1f5f9',
            'text_secondary': '#cbd5e1',
            'border': '#334155',
            'hover': '#475569'
        }
        
        # File paths
        self.progress_file = "dsa_progress.json"
        self.journal_file = "dsa_journal.json"
        
        # Load data
        self.load_data()
        
        # Create UI
        self.create_sidebar()
        self.create_main_content()
        self.show_frame("progress")
        
    def load_data(self):
        """Load progress and journal data from files"""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r') as f:
                self.progress_data = json.load(f)
        else:
            self.progress_data = self.initialize_progress()
        
        if os.path.exists(self.journal_file):
            with open(self.journal_file, 'r') as f:
                self.journal_data = json.load(f)
        else:
            self.journal_data = []
    
    def initialize_progress(self):
        """Initialize DSA topics based on roadmap"""
        return {
            "01. Learn Python Programming": {
                "Python Basics & Syntax": False,
                "Data Types & Variables": False,
                "Control Flow (if/else, loops)": False,
                "Functions & Lambda": False,
                "OOP Concepts": False,
                "Exception Handling": False,
                "File I/O": False
            },
            "02. Arrays & Strings": {
                "Array Basics & Operations": False,
                "Multi-dimensional Arrays": False,
                "Array Manipulation": False,
                "String Operations": False,
                "String Methods in Python": False,
                "Two Pointer Technique": False,
                "Sliding Window": False,
                "Kadane's Algorithm": False
            },
            "03. Linked Lists": {
                "Singly Linked List": False,
                "Doubly Linked List": False,
                "Circular Linked List": False,
                "Fast & Slow Pointers": False,
                "Reversal of Linked List": False,
                "Cycle Detection": False
            },
            "04. Stack & Queue": {
                "Stack Implementation": False,
                "Stack using List/Array": False,
                "Queue Implementation": False,
                "Circular Queue": False,
                "Deque (Double-ended Queue)": False,
                "Priority Queue": False,
                "Monotonic Stack": False,
                "Stack Applications": False
            },
            "05. Hashing & Heap": {
                "Hash Map/Dictionary": False,
                "Hash Set": False,
                "Collision Handling": False,
                "Min Heap": False,
                "Max Heap": False,
                "Heapq module in Python": False,
                "Heap Applications": False
            },
            "06. Recursion & Backtracking": {
                "Understanding Recursion": False,
                "Base Cases & Recursive Cases": False,
                "Recursive Algorithms": False,
                "Backtracking Basics": False,
                "N-Queens Problem": False,
                "Rat in a Maze": False,
                "Sudoku Solver": False,
                "Permutations & Combinations": False
            },
            "07. Searching & Sorting": {
                "Linear Search": False,
                "Binary Search": False,
                "Binary Search Variations": False,
                "Bubble Sort": False,
                "Selection Sort": False,
                "Insertion Sort": False,
                "Merge Sort": False,
                "Quick Sort": False,
                "Heap Sort": False,
                "Counting Sort": False,
                "Radix Sort": False
            },
            "08. Mathematical Algorithms": {
                "GCD & LCM": False,
                "Prime Numbers & Sieve": False,
                "Modular Arithmetic": False,
                "Fast Exponentiation": False,
                "Fibonacci Variations": False,
                "Combinatorics": False,
                "Number Theory": False
            },
            "09. Bitwise Operations & Tricks": {
                "Bitwise Operators": False,
                "Bit Manipulation": False,
                "Power of 2": False,
                "Count Set Bits": False,
                "XOR Properties": False,
                "Bit Masking": False
            },
            "10. Greedy Algorithms": {
                "Greedy Method": False,
                "Activity Selection": False,
                "Fractional Knapsack": False,
                "Job Sequencing": False,
                "Huffman Coding": False,
                "Divide and Conquer": False
            },
            "11. Dynamic Programming": {
                "Memoization Basics": False,
                "Tabulation Method": False,
                "1D DP Problems": False,
                "2D DP Problems": False,
                "Knapsack (0/1, Unbounded)": False,
                "LCS (Longest Common Subsequence)": False,
                "LIS (Longest Increasing Subsequence)": False,
                "Matrix Chain Multiplication": False,
                "DP on Strings": False,
                "DP on Trees": False,
                "DP on Grids": False
            },
            "12. Advanced DP Techniques": {
                "State Space Reduction": False,
                "Digit DP": False,
                "Bitmask DP": False,
                "DP with Bitmasking": False,
                "Probability DP": False
            },
            "13. Graph Algorithms": {
                "Graph Representation (Adjacency List/Matrix)": False,
                "BFS (Breadth-First Search)": False,
                "DFS (Depth-First Search)": False,
                "Connected Components": False,
                "Cycle Detection": False,
                "Bipartite Graph": False,
                "Topological Sort": False,
                "Shortest Path in Unweighted Graph": False
            },
            "14. Advanced Graph Algorithms": {
                "Dijkstra's Algorithm": False,
                "Bellman-Ford Algorithm": False,
                "Floyd-Warshall Algorithm": False,
                "Prim's Algorithm (MST)": False,
                "Kruskal's Algorithm (MST)": False,
                "Union-Find (Disjoint Set)": False,
                "Articulation Points": False,
                "Bridges in Graph": False,
                "Strongly Connected Components": False
            },
            "15. DSU & MST": {
                "Disjoint Set Union": False,
                "Path Compression": False,
                "Union by Rank": False,
                "Minimum Spanning Tree": False,
                "MST Applications": False
            },
            "16. Network Flow Algorithms": {
                "Max Flow Problem": False,
                "Ford-Fulkerson Algorithm": False,
                "Edmonds-Karp Algorithm": False,
                "Min Cut": False,
                "Bipartite Matching": False
            },
            "17. String Algorithms": {
                "KMP Algorithm": False,
                "Rabin-Karp Algorithm": False,
                "Z-Algorithm": False,
                "Manacher's Algorithm": False,
                "String Hashing": False
            },
            "18. Computational Geometry": {
                "Convex Hull": False,
                "Line Intersection": False,
                "Point in Polygon": False,
                "Closest Pair of Points": False
            },
            "19. Segment Trees & Fenwick Tree": {
                "Segment Tree Basics": False,
                "Range Query": False,
                "Lazy Propagation": False,
                "Fenwick Tree (BIT)": False,
                "Range Update": False
            },
            "20. Sparse Table & Binary Lifting": {
                "Sparse Table": False,
                "Range Minimum Query": False,
                "Binary Lifting": False,
                "LCA (Lowest Common Ancestor)": False
            },
            "21. Advanced Tree Techniques": {
                "Heavy-Light Decomposition": False,
                "Centroid Decomposition": False,
                "Tree DP": False,
                "Euler Tour": False
            },
            "22. Tries & Suffix Trees": {
                "Trie Implementation": False,
                "Trie Operations": False,
                "Suffix Array": False,
                "Suffix Tree": False,
                "Applications": False
            },
            "23. Game Theory & Nim Game": {
                "Nim Game": False,
                "Sprague-Grundy Theorem": False,
                "Minimax Algorithm": False,
                "Game States": False
            },
            "24. Approximation & Randomized Algorithms": {
                "Approximation Algorithms": False,
                "Randomized Algorithms": False,
                "Monte Carlo Methods": False,
                "Las Vegas Algorithms": False
            },
            "25. Trees (Binary & BST)": {
                "Binary Tree Basics": False,
                "Tree Traversals (Inorder, Preorder, Postorder)": False,
                "Level Order Traversal": False,
                "Binary Search Tree": False,
                "BST Operations": False,
                "AVL Tree": False,
                "Red-Black Tree": False,
                "Tree Construction": False
            }
        }
    
    def save_progress(self):
        """Save progress to file"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress_data, f, indent=4)
    
    def save_journal(self):
        """Save journal to file"""
        with open(self.journal_file, 'w') as f:
            json.dump(self.journal_data, f, indent=4)
    
    def create_sidebar(self):
        """Create modern sidebar navigation"""
        self.sidebar = tk.Frame(self.root, bg=self.colors['darker'], width=280)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Logo/Header
        header_frame = tk.Frame(self.sidebar, bg=self.colors['darker'])
        header_frame.pack(fill="x", pady=30, padx=20)
        
        logo_label = tk.Label(header_frame, text="🐍", font=("Segoe UI", 40), 
                             bg=self.colors['darker'])
        logo_label.pack()
        
        title_label = tk.Label(header_frame, text="DSA Tracker", 
                              font=("Segoe UI", 18, "bold"), 
                              bg=self.colors['darker'], fg=self.colors['text'])
        title_label.pack()
        
        subtitle_label = tk.Label(header_frame, text="Python Edition", 
                                 font=("Segoe UI", 10), 
                                 bg=self.colors['darker'], fg=self.colors['text_secondary'])
        subtitle_label.pack()
        
        # Navigation buttons
        nav_frame = tk.Frame(self.sidebar, bg=self.colors['darker'])
        nav_frame.pack(fill="x", pady=20)
        
        self.nav_buttons = {}
        
        nav_items = [
            ("📊 Progress", "progress", self.colors['primary']),
            ("📝 Journal", "journal", self.colors['secondary']),
            ("📈 Statistics", "stats", self.colors['success'])
        ]
        
        for text, key, color in nav_items:
            btn = tk.Button(nav_frame, text=text, font=("Segoe UI", 12, "bold"),
                          bg=self.colors['darker'], fg=self.colors['text_secondary'],
                          activebackground=color, activeforeground="white",
                          relief="flat", anchor="w", padx=30, pady=15,
                          cursor="hand2", borderwidth=0,
                          command=lambda k=key: self.show_frame(k))
            btn.pack(fill="x", padx=10, pady=3)
            self.nav_buttons[key] = btn
            
            btn.bind("<Enter>", lambda e, b=btn, c=color: b.config(bg=c, fg="white"))
            btn.bind("<Leave>", lambda e, b=btn, k=key: b.config(
                bg=color if self.current_frame == k else self.colors['darker'],
                fg="white" if self.current_frame == k else self.colors['text_secondary']
            ))
        
        # Footer
        footer = tk.Label(self.sidebar, text="Made with ❤️ for DSA Learning", 
                         font=("Segoe UI", 9), bg=self.colors['darker'], 
                         fg=self.colors['text_secondary'])
        footer.pack(side="bottom", pady=20)
    
    def create_main_content(self):
        """Create main content area"""
        self.main_container = tk.Frame(self.root, bg=self.colors['dark'])
        self.main_container.pack(side="right", fill="both", expand=True)
        
        self.frames = {}
        
        # Progress Frame
        self.frames['progress'] = self.create_progress_frame()
        
        # Journal Frame
        self.frames['journal'] = self.create_journal_frame()
        
        # Stats Frame
        self.frames['stats'] = self.create_stats_frame()
        
        self.current_frame = None
    
    def show_frame(self, frame_name):
        """Show selected frame"""
        if self.current_frame:
            self.frames[self.current_frame].pack_forget()
        
        self.frames[frame_name].pack(fill="both", expand=True)
        self.current_frame = frame_name
        
        # Update navigation button colors
        for key, btn in self.nav_buttons.items():
            if key == frame_name:
                color = self.colors['primary'] if key == 'progress' else \
                       self.colors['secondary'] if key == 'journal' else self.colors['success']
                btn.config(bg=color, fg="white")
            else:
                btn.config(bg=self.colors['darker'], fg=self.colors['text_secondary'])
        
        if frame_name == 'stats':
            self.update_stats()
    
    def create_progress_frame(self):
        """Create progress tracking frame"""
        frame = tk.Frame(self.main_container, bg=self.colors['dark'])
        
        # Header
        header = tk.Frame(frame, bg=self.colors['dark'])
        header.pack(fill="x", padx=30, pady=20)
        
        tk.Label(header, text="DSA Roadmap Progress", 
                font=("Segoe UI", 24, "bold"), 
                bg=self.colors['dark'], fg=self.colors['text']).pack(anchor="w")
        
        tk.Label(header, text="Track your learning journey through Data Structures & Algorithms", 
                font=("Segoe UI", 11), 
                bg=self.colors['dark'], fg=self.colors['text_secondary']).pack(anchor="w", pady=(5, 0))
        
        # Scrollable content
        canvas = tk.Canvas(frame, bg=self.colors['dark'], highlightthickness=0)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview,
                                bg=self.colors['darker'], troughcolor=self.colors['dark'])
        scrollable_frame = tk.Frame(canvas, bg=self.colors['dark'])
        
        scrollable_frame.bind("<Configure>", 
                             lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for category, topics in self.progress_data.items():
            self.create_category_card(scrollable_frame, category, topics)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(30, 0), pady=(0, 20))
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=(0, 20))
        
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        return frame
    
    def create_category_card(self, parent, category, topics):
        """Create modern category card"""
        card = tk.Frame(parent, bg=self.colors['card'], relief="flat")
        card.pack(fill="x", pady=10)
        
        # Card header
        header = tk.Frame(card, bg=self.colors['primary'], height=8)
        header.pack(fill="x")
        
        # Card content
        content = tk.Frame(card, bg=self.colors['card'])
        content.pack(fill="x", padx=25, pady=20)
        
        tk.Label(content, text=category, font=("Segoe UI", 13, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor="w", pady=(0, 15))
        
        # Topics
        for topic, status in topics.items():
            topic_frame = tk.Frame(content, bg=self.colors['card'])
            topic_frame.pack(fill="x", pady=4)
            
            var = tk.BooleanVar(value=status)
            
            cb = tk.Checkbutton(topic_frame, text="", variable=var,
                               bg=self.colors['card'], activebackground=self.colors['card'],
                               selectcolor=self.colors['success'], fg=self.colors['text'],
                               font=("Segoe UI", 10), relief="flat", borderwidth=0,
                               command=lambda c=category, t=topic, v=var: self.update_progress(c, t, v))
            cb.pack(side="left", padx=(0, 10))
            
            tk.Label(topic_frame, text=topic, font=("Segoe UI", 10),
                    bg=self.colors['card'], fg=self.colors['text']).pack(side="left", anchor="w")
    
    def update_progress(self, category, topic, var):
        """Update progress"""
        self.progress_data[category][topic] = var.get()
        self.save_progress()
    
    def create_journal_frame(self):
        """Create journal frame"""
        frame = tk.Frame(self.main_container, bg=self.colors['dark'])
        
        # Header
        header = tk.Frame(frame, bg=self.colors['dark'])
        header.pack(fill="x", padx=30, pady=20)
        
        tk.Label(header, text="Daily Journal", 
                font=("Segoe UI", 24, "bold"), 
                bg=self.colors['dark'], fg=self.colors['text']).pack(anchor="w")
        
        tk.Label(header, text="Document your learning progress and achievements", 
                font=("Segoe UI", 11), 
                bg=self.colors['dark'], fg=self.colors['text_secondary']).pack(anchor="w", pady=(5, 0))
        
        # Entry card
        entry_card = tk.Frame(frame, bg=self.colors['card'])
        entry_card.pack(fill="x", padx=30, pady=(0, 20))
        
        entry_content = tk.Frame(entry_card, bg=self.colors['card'])
        entry_content.pack(fill="x", padx=25, pady=25)
        
        tk.Label(entry_content, text="What did you accomplish today?", 
                font=("Segoe UI", 12, "bold"), 
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor="w", pady=(0, 10))
        
        self.journal_text = scrolledtext.ScrolledText(entry_content, height=6, 
                                                      font=("Segoe UI", 10), wrap="word",
                                                      bg=self.colors['darker'], fg=self.colors['text'],
                                                      insertbackground=self.colors['text'],
                                                      relief="flat", padx=10, pady=10)
        self.journal_text.pack(fill="x", pady=(0, 15))
        
        # Input fields
        input_grid = tk.Frame(entry_content, bg=self.colors['card'])
        input_grid.pack(fill="x", pady=(0, 15))
        
        # Topic
        tk.Label(input_grid, text="📚 Topic Studied", font=("Segoe UI", 10, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.topic_entry = tk.Entry(input_grid, font=("Segoe UI", 10), width=40,
                                    bg=self.colors['darker'], fg=self.colors['text'],
                                    insertbackground=self.colors['text'], relief="flat")
        self.topic_entry.grid(row=1, column=0, sticky="ew", padx=(0, 10), ipady=8)
        
        # Problems
        tk.Label(input_grid, text="🎯 Problems Solved", font=("Segoe UI", 10, "bold"),
                bg=self.colors['card'], fg=self.colors['text']).grid(row=0, column=1, sticky="w", pady=(0, 5))
        self.problem_entry = tk.Entry(input_grid, font=("Segoe UI", 10), width=40,
                                      bg=self.colors['darker'], fg=self.colors['text'],
                                      insertbackground=self.colors['text'], relief="flat")
        self.problem_entry.grid(row=1, column=1, sticky="ew", ipady=8)
        
        input_grid.columnconfigure(0, weight=1)
        input_grid.columnconfigure(1, weight=1)
        
        # Save button
        save_btn = tk.Button(entry_content, text="💾 Save Journal Entry", 
                            command=self.save_journal_entry,
                            font=("Segoe UI", 11, "bold"), bg=self.colors['success'], 
                            fg="white", padx=30, pady=12, cursor="hand2", relief="flat",
                            activebackground="#059669", borderwidth=0)
        save_btn.pack()
        
        # History
        history_label = tk.Label(frame, text="📖 Journal History", 
                                font=("Segoe UI", 16, "bold"), 
                                bg=self.colors['dark'], fg=self.colors['text'])
        history_label.pack(anchor="w", padx=30, pady=(10, 10))
        
        history_card = tk.Frame(frame, bg=self.colors['card'])
        history_card.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        self.journal_display = scrolledtext.ScrolledText(history_card, 
                                                        font=("Segoe UI", 10), wrap="word",
                                                        bg=self.colors['darker'], fg=self.colors['text'],
                                                        state="disabled", relief="flat", padx=15, pady=15)
        self.journal_display.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.display_journal_history()
        
        return frame
    
    def save_journal_entry(self):
        """Save journal entry"""
        content = self.journal_text.get("1.0", "end-1c").strip()
        problems = self.problem_entry.get().strip()
        topic = self.topic_entry.get().strip()
        
        if not content:
            messagebox.showwarning("Empty Entry", "Please write something in your journal!")
            return
        
        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "content": content,
            "problems": problems if problems else "N/A",
            "topic": topic if topic else "N/A"
        }
        
        self.journal_data.insert(0, entry)
        self.save_journal()
        
        self.journal_text.delete("1.0", "end")
        self.problem_entry.delete(0, "end")
        self.topic_entry.delete(0, "end")
        
        self.display_journal_history()
        
        messagebox.showinfo("Success", "✅ Journal entry saved successfully!")
    
    def display_journal_history(self):
        """Display journal history"""
        self.journal_display.config(state="normal")
        self.journal_display.delete("1.0", "end")
        
        if not self.journal_data:
            self.journal_display.insert("1.0", "No journal entries yet. Start your DSA journey today! 🚀")
        else:
            for i, entry in enumerate(self.journal_data):
                if i > 0:
                    self.journal_display.insert("end", "\n" + "─"*100 + "\n\n", "separator")
                
                self.journal_display.insert("end", f"📅 {entry['date']}\n", "date")
                self.journal_display.insert("end", f"📚 Topic: {entry['topic']}  ", "topic")
                self.journal_display.insert("end", f"🎯 Problems: {entry['problems']}\n\n", "problems")
                self.journal_display.insert("end", f"{entry['content']}\n", "content")
        
        self.journal_display.tag_config("separator", foreground=self.colors['border'])
        self.journal_display.tag_config("date", foreground=self.colors['primary'], 
                                       font=("Segoe UI", 10, "bold"))
        self.journal_display.tag_config("topic", foreground=self.colors['success'])
        self.journal_display.tag_config("problems", foreground=self.colors['secondary'])
        self.journal_display.tag_config("content", foreground=self.colors['text'])
        
        self.journal_display.config(state="disabled")
    
    def create_stats_frame(self):
        """Create statistics frame"""
        frame = tk.Frame(self.main_container, bg=self.colors['dark'])
        
        # Header
        header = tk.Frame(frame, bg=self.colors['dark'])
        header.pack(fill="x", padx=30, pady=20)
        
        tk.Label(header, text="Statistics & Analytics", 
                font=("Segoe UI", 24, "bold"), 
                bg=self.colors['dark'], fg=self.colors['text']).pack(anchor="w")
        
        tk.Label(header, text="Visualize your progress and achievements", 
                font=("Segoe UI", 11), 
                bg=self.colors['dark'], fg=self.colors['text_secondary']).pack(anchor="w", pady=(5, 0))
        
        self.stats_container = tk.Frame(frame, bg=self.colors['dark'])
        self.stats_container.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        
        return frame
    
    def update_stats(self):
        """Update statistics"""
        for widget in self.stats_container.winfo_children():
            widget.destroy()
        
        total_topics = sum(len(topics) for topics in self.progress_data.values())
        completed_topics = sum(sum(1 for status in topics.values() if status) 
                              for topics in self.progress_data.values())
        progress_percent = (completed_topics / total_topics * 100) if total_topics > 0 else 0
        
        # Stats cards
        stats_row = tk.Frame(self.stats_container, bg=self.colors['dark'])
        stats_row.pack(fill="x", pady=(0, 20))
        
        self.create_stat_card(stats_row, "Total Topics", str(total_topics), 
                             self.colors['primary'], "📚", 0)
        self.create_stat_card(stats_row, "Completed", str(completed_topics), 
                             self.colors['success'], "✅", 1)
        self.create_stat_card(stats_row, "Remaining", str(total_topics - completed_topics), 
                             self.colors['warning'], "⏳", 2)
        self.create_stat_card(stats_row, "Progress", f"{progress_percent:.0f}%", 
                             self.colors['secondary'], "📈", 3)
        
        # Progress bar
        progress_card = tk.Frame(self.stats_container, bg=self.colors['card'])
        progress_card.pack(fill="x", pady=(0, 20))
        
        progress_content = tk.Frame(progress_card, bg=self.colors['card'])
        progress_content.pack(fill="x", padx=25, pady=25)
        
        tk.Label(progress_content, text="Overall Completion", 
                font=("Segoe UI", 14, "bold"), 
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor="w", pady=(0, 15))
        
        bar_container = tk.Frame(progress_content, bg=self.colors['darker'], height=40)
        bar_container.pack(fill="x")
        bar_container.pack_propagate(False)
        
        bar_fill = tk.Frame(bar_container, bg=self.colors['success'], height=40)
        bar_fill.place(relx=0, rely=0, relwidth=progress_percent/100, relheight=1)
        
        tk.Label(bar_container, text=f"{progress_percent:.1f}%", 
                font=("Segoe UI", 14, "bold"), 
                bg=self.colors['darker'], fg=self.colors['text']).place(relx=0.5, rely=0.5, anchor="center")
        
        # Journal stats
        journal_card = tk.Frame(self.stats_container, bg=self.colors['card'])
        journal_card.pack(fill="x", pady=(0, 20))
        
        journal_content = tk.Frame(journal_card, bg=self.colors['card'])
        journal_content.pack(fill="x", padx=25, pady=25)
        
        journal_count = len(self.journal_data)
        tk.Label(journal_content, text="📝 Journal Entries", 
                font=("Segoe UI", 14, "bold"), 
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor="w", pady=(0, 10))
        
        tk.Label(journal_content, text=f"Total Entries: {journal_count}", 
                font=("Segoe UI", 12), 
                bg=self.colors['card'], fg=self.colors['text_secondary']).pack(anchor="w")
        
        # Category breakdown
        breakdown_card = tk.Frame(self.stats_container, bg=self.colors['card'])
        breakdown_card.pack(fill="both", expand=True)
        
        breakdown_header = tk.Frame(breakdown_card, bg=self.colors['card'])
        breakdown_header.pack(fill="x", padx=25, pady=(25, 15))
        
        tk.Label(breakdown_header, text="📊 Category-wise Progress", 
                font=("Segoe UI", 14, "bold"), 
                bg=self.colors['card'], fg=self.colors['text']).pack(anchor="w")
        
        # Scrollable breakdown
        canvas = tk.Canvas(breakdown_card, bg=self.colors['card'], highlightthickness=0, height=300)
        scrollbar = tk.Scrollbar(breakdown_card, orient="vertical", command=canvas.yview,
                                bg=self.colors['darker'])
        scrollable = tk.Frame(canvas, bg=self.colors['card'])
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for category, topics in self.progress_data.items():
            cat_total = len(topics)
            cat_completed = sum(1 for status in topics.values() if status)
            cat_percent = (cat_completed / cat_total * 100) if cat_total > 0 else 0
            
            cat_item = tk.Frame(scrollable, bg=self.colors['darker'])
            cat_item.pack(fill="x", padx=25, pady=5)
            
            info_frame = tk.Frame(cat_item, bg=self.colors['darker'])
            info_frame.pack(fill="x", padx=15, pady=12)
            
            tk.Label(info_frame, text=category, font=("Segoe UI", 10, "bold"),
                    bg=self.colors['darker'], fg=self.colors['text']).pack(anchor="w")
            
            tk.Label(info_frame, text=f"{cat_completed}/{cat_total} topics ({cat_percent:.0f}%)",
                    font=("Segoe UI", 9), bg=self.colors['darker'], 
                    fg=self.colors['text_secondary']).pack(anchor="w", pady=(2, 0))
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y", padx=(0, 15), pady=(0, 15))
    
    def create_stat_card(self, parent, label, value, color, icon, col):
        """Create a modern stat card"""
        card = tk.Frame(parent, bg=color)
        card.grid(row=0, column=col, padx=10, sticky="nsew")
        
        content = tk.Frame(card, bg=color)
        content.pack(padx=30, pady=25)
        
        tk.Label(content, text=icon, font=("Segoe UI", 32), bg=color).pack()
        tk.Label(content, text=value, font=("Segoe UI", 28, "bold"), 
                bg=color, fg="white").pack(pady=(10, 5))
        tk.Label(content, text=label, font=("Segoe UI", 11), 
                bg=color, fg="white").pack()
        
        parent.grid_columnconfigure(col, weight=1)

if __name__ == "__main__":
    root = tk.Tk()
    app = DSATracker(root)
    root.mainloop()




    