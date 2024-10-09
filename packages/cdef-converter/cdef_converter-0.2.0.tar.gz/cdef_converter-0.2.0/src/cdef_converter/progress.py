import time
from queue import Queue
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.text import Text

from cdef_converter.config import GREEN
from cdef_converter.utils import create_status_table

console = Console()


def display_progress(progress_queue: Queue[Any], total_files: int) -> None:
    completed_files = 0
    process_status = {}
    start_time = time.time()
    last_status_update = time.time()

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        TextColumn("{task.fields[speed]:.2f} files/sec"),
        console=console,
        expand=True,
    ) as progress:
        task = progress.add_task("[cyan]Processing files...", total=total_files, speed=0)

        while completed_files < total_files:
            current_time = time.time()
            while not progress_queue.empty():
                process_name, file_name, status = progress_queue.get()
                process_status[process_name] = (file_name, status)
                if status == "Completed":
                    completed_files += 1
                    progress.update(
                        task, advance=1, speed=completed_files / (current_time - start_time)
                    )

            # Update status table every 5 seconds
            if current_time - last_status_update > 5:
                progress.console.print(create_status_table(process_status))
                last_status_update = current_time

            time.sleep(0.1)

    console.print(Panel(Text("Processing complete!", style=GREEN), expand=False))
