import tkinter as tk
from tkinter import ttk, messagebox
import psutil


class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Task Manager")
        self.root.geometry("900x650")

        # -------------------------
        # TITLE
        # -------------------------

        title = tk.Label(
            root,
            text="Python Task Manager",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=10)

        # -------------------------
        # SYSTEM INFORMATION
        # -------------------------

        stats_frame = tk.Frame(root)
        stats_frame.pack(pady=10)

        self.cpu_label = tk.Label(
            stats_frame,
            text="CPU: 0%",
            font=("Arial", 12)
        )
        self.cpu_label.grid(row=0, column=0, padx=20)

        self.ram_label = tk.Label(
            stats_frame,
            text="RAM: 0%",
            font=("Arial", 12)
        )
        self.ram_label.grid(row=0, column=1, padx=20)

        self.disk_label = tk.Label(
            stats_frame,
            text="Disk: 0%",
            font=("Arial", 12)
        )
        self.disk_label.grid(row=0, column=2, padx=20)

        self.battery_label = tk.Label(
            stats_frame,
            text="Battery: N/A",
            font=("Arial", 12)
        )
        self.battery_label.grid(row=0, column=3, padx=20)

        self.process_count_label = tk.Label(
            root,
            text="Running Processes: 0",
            font=("Arial", 12)
        )
        self.process_count_label.pack(pady=5)

        # -------------------------
        # PROGRESS BARS
        # -------------------------

        bars_frame = tk.Frame(root)
        bars_frame.pack(pady=10)

        tk.Label(
            bars_frame,
            text="CPU"
        ).grid(row=0, column=0, padx=5)

        self.cpu_bar = ttk.Progressbar(
            bars_frame,
            length=200,
            maximum=100
        )
        self.cpu_bar.grid(row=0, column=1, padx=10)

        tk.Label(
            bars_frame,
            text="RAM"
        ).grid(row=0, column=2, padx=5)

        self.ram_bar = ttk.Progressbar(
            bars_frame,
            length=200,
            maximum=100
        )
        self.ram_bar.grid(row=0, column=3, padx=10)

        # -------------------------
        # SEARCH
        # -------------------------

        search_frame = tk.Frame(root)
        search_frame.pack(pady=10)

        tk.Label(
            search_frame,
            text="Search Process:"
        ).pack(side=tk.LEFT, padx=5)

        self.search_entry = tk.Entry(
            search_frame,
            width=30
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)

        search_button = tk.Button(
            search_frame,
            text="Search",
            command=self.refresh_processes
        )
        search_button.pack(side=tk.LEFT, padx=5)

        clear_button = tk.Button(
            search_frame,
            text="Clear",
            command=self.clear_search
        )
        clear_button.pack(side=tk.LEFT, padx=5)

        # -------------------------
        # PROCESS TABLE
        # -------------------------

        table_frame = tk.Frame(root)
        table_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "pid",
            "name",
            "cpu",
            "memory"
        )

        self.process_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        self.process_table.heading(
            "pid",
            text="PID"
        )

        self.process_table.heading(
            "name",
            text="Process Name"
        )

        self.process_table.heading(
            "cpu",
            text="CPU %"
        )

        self.process_table.heading(
            "memory",
            text="Memory %"
        )

        self.process_table.column(
            "pid",
            width=100
        )

        self.process_table.column(
            "name",
            width=350
        )

        self.process_table.column(
            "cpu",
            width=100
        )

        self.process_table.column(
            "memory",
            width=100
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient=tk.VERTICAL,
            command=self.process_table.yview
        )

        self.process_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.process_table.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        # -------------------------
        # BUTTONS
        # -------------------------

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        refresh_button = tk.Button(
            button_frame,
            text="Refresh Processes",
            width=20,
            command=self.refresh_processes
        )
        refresh_button.pack(
            side=tk.LEFT,
            padx=10
        )

        end_task_button = tk.Button(
            button_frame,
            text="End Task",
            width=20,
            command=self.end_task
        )
        end_task_button.pack(
            side=tk.LEFT,
            padx=10
        )

        # Start updating information
        self.update_stats()
        self.refresh_processes()

    # -------------------------
    # UPDATE SYSTEM INFORMATION
    # -------------------------

    def update_stats(self):

        cpu = psutil.cpu_percent()

        ram = psutil.virtual_memory().percent

        disk = psutil.disk_usage("/").percent

        battery = psutil.sensors_battery()

        process_count = len(psutil.pids())

        # Update labels

        self.cpu_label.config(
            text=f"CPU: {cpu}%"
        )

        self.ram_label.config(
            text=f"RAM: {ram}%"
        )

        self.disk_label.config(
            text=f"Disk: {disk}%"
        )

        # Battery information

        if battery is not None:

            if battery.power_plugged:
                charging = "Charging"

            else:
                charging = "Not Charging"

            self.battery_label.config(
                text=f"Battery: {battery.percent}% ({charging})"
            )

        else:

            self.battery_label.config(
                text="Battery: N/A"
            )

        # Process count

        self.process_count_label.config(
            text=f"Running Processes: {process_count}"
        )

        # Update progress bars

        self.cpu_bar["value"] = cpu
        self.ram_bar["value"] = ram

        # Run this function again after 2 seconds

        self.root.after(
            2000,
            self.update_stats
        )

    # -------------------------
    # GET RUNNING PROCESSES
    # -------------------------

    def refresh_processes(self):

        # Remove old processes from table

        for row in self.process_table.get_children():
            self.process_table.delete(row)

        # Get text from search box

        search_text = (
            self.search_entry.get()
            .lower()
            .strip()
        )

        processes = []

        # Look through running processes

        for process in psutil.process_iter(
            ["pid", "name", "cpu_percent", "memory_percent"]
        ):

            try:

                info = process.info

                name = info["name"]

                if name is None:
                    name = "Unknown"

                # Search filter

                if search_text and search_text not in name.lower():
                    continue

                processes.append(
                    (
                        info["pid"],
                        name,
                        info["cpu_percent"],
                        info["memory_percent"]
                    )
                )

            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied
            ):

                pass

        # Sort by memory usage

        processes.sort(
            key=lambda process: process[3],
            reverse=True
        )

        # Add processes to table

        for process in processes:

            pid = process[0]
            name = process[1]
            cpu = process[2]
            memory = process[3]

            self.process_table.insert(
                "",
                tk.END,
                values=(
                    pid,
                    name,
                    f"{cpu:.1f}",
                    f"{memory:.1f}"
                )
            )

    # -------------------------
    # CLEAR SEARCH
    # -------------------------

    def clear_search(self):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.refresh_processes()

    # -------------------------
    # END A PROCESS
    # -------------------------

    def end_task(self):

        selected = self.process_table.selection()

        # Check if user selected something

        if not selected:

            messagebox.showwarning(
                "No Process Selected",
                "Please select a process first."
            )

            return

        # Get selected process information

        item = self.process_table.item(
            selected[0]
        )

        pid = item["values"][0]

        process_name = item["values"][1]

        # Ask user before closing program

        answer = messagebox.askyesno(
            "End Task",
            f"Are you sure you want to end {process_name}?"
        )

        if answer:

            try:

                process = psutil.Process(pid)

                process.terminate()

                messagebox.showinfo(
                    "Success",
                    f"{process_name} was terminated."
                )

                self.refresh_processes()

            except psutil.NoSuchProcess:

                messagebox.showerror(
                    "Error",
                    "That process is no longer running."
                )

            except psutil.AccessDenied:

                messagebox.showerror(
                    "Access Denied",
                    "Windows would not allow this process to be terminated."
                )

            except Exception as error:

                messagebox.showerror(
                    "Error",
                    str(error)
                )


# -------------------------
# START THE PROGRAM
# -------------------------

root = tk.Tk()

app = TaskManagerApp(root)

root.mainloop()