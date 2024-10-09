import multiprocessing
import time
from multiprocessing import Manager
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from cdef_converter.config import DEFAULT_ENCODING_CHUNK_SIZE, GREEN, OUTPUT_DIRECTORY
from cdef_converter.file_processing import process_file
from cdef_converter.logging_config import log, logger
from cdef_converter.progress import display_progress
from cdef_converter.utils import print_summary_table, save_summary

console = Console()


def process_file_wrapper(args):
    file_path, progress_queue, encoding_chunk_size = args
    return process_file(file_path, progress_queue, encoding_chunk_size)


def process_files_with_progress(
    files: list[Path],
    summary: dict[str, Any],
    num_processes: int | None = None,
    encoding_chunk_size: int = DEFAULT_ENCODING_CHUNK_SIZE,
) -> None:
    manager = Manager()
    progress_queue = manager.Queue()

    with multiprocessing.Pool(processes=num_processes) as pool:
        progress_display = multiprocessing.Process(
            target=display_progress, args=(progress_queue, len(files))
        )
        progress_display.start()

        results = pool.map(process_file_wrapper, [(file, progress_queue) for file in files])

        progress_display.join()

    for result in results:
        if result:
            register_name, year, data = result
            if register_name not in summary:
                summary[register_name] = {}
            summary[register_name][year or register_name] = data


def main(
    input_directory: Path,
    num_processes: int | None = None,
    encoding_chunk_size: int = DEFAULT_ENCODING_CHUNK_SIZE * 1024 * 1024,
    recursive: bool = False,
) -> None:
    start_time = time.time()
    try:
        console.print(
            Panel(
                Text("Starting file conversion and processing", style=GREEN),
                expand=False,
            )
        )

        if recursive:
            files = list(input_directory.rglob("*.parquet")) + list(input_directory.rglob("*.csv"))
        else:
            files = list(input_directory.glob("*.parquet")) + list(input_directory.glob("*.csv"))

        summary: dict[str, dict[str, Any]] = {}

        process_files_with_progress(files, summary, num_processes, encoding_chunk_size)
        end_time = time.time()
        total_time = end_time - start_time
        log(f"Total processing time: {total_time:.2f} seconds")
        log(f"Average time per file: {total_time / len(files):.2f} seconds")

        console.print(print_summary_table(summary))

        summary_file = OUTPUT_DIRECTORY / "register_summary.json"
        save_summary(summary, summary_file)

        console.print(Panel(Text("Processing complete!", style=GREEN), expand=False))
        console.print(f"[bold blue]Total registers processed: {len(summary)}")
        console.print(f"[bold blue]Summary saved to: {summary_file}")
        console.print(f"[bold blue]Parquet files saved to: {OUTPUT_DIRECTORY}/registers")
    except FileNotFoundError as e:
        console.print(
            Panel(Text(f"Input directory not found: {e}", style="bold red"), expand=False)
        )
        log(f"Input directory not found: {e}")
    except PermissionError as e:
        console.print(Panel(Text(f"Permission denied: {e}", style="bold red"), expand=False))
        log(f"Permission denied: {e}")
    except Exception as e:
        console.print(
            Panel(Text(f"An unexpected error occurred: {e}", style="bold red"), expand=False)
        )
        logger.exception("Detailed error information:")
