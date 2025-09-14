#!/usr/bin/env python3

import subprocess
import os
import shutil
import concurrent.futures
from pathlib import Path
from argparse import ArgumentParser
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn, TaskID
from rich.panel import Panel
from rich.table import Table

console = Console()

def check_dependencies():
    if not shutil.which("xcodebuild"):
        console.print(Panel(
            "[bold red]❌ Error: 'xcodebuild' command not found.[/bold red]\nPlease ensure Xcode and its Command Line Tools are installed and configured in your system's PATH.",
            title="Dependency Check Failed",
            border_style="red"
        ))
        exit(1)

def export_single_archive(
    archive_path: Path, 
    output_dir: Path, 
    export_method: str, 
    progress: Progress, 
    task_id: TaskID
) -> dict:
    progress.log(f"▶️ Starting: [magenta]{archive_path.name}[/magenta]")
    archive_name = archive_path.stem
    export_path = output_dir / archive_name
    export_path.mkdir(exist_ok=True)

    plist_path = export_path / "exportOptions.plist"
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key><string>{export_method}</string>
    <key>signingStyle</key><string>automatic</string>
    <key>stripSwiftSymbols</key><true/>
    <key>compileBitcode</key><false/>
</dict>
</plist>
"""
    
    result = {"archive": archive_path}
    try:
        with open(plist_path, "w") as f:
            f.write(plist_content)

        cmd = [
            "xcodebuild", "-exportArchive", "-archivePath", str(archive_path),
            "-exportPath", str(export_path), "-exportOptionsPlist", str(plist_path)
        ]
        
        process = subprocess.run(
            cmd, capture_output=True, text=True, check=False, encoding='utf-8'
        )
        
        if process.returncode == 0:
            final_ipa = next(export_path.glob("*.ipa"), None)
            if final_ipa and final_ipa.exists():
                result.update({
                    "success": True,
                    "ipa_path": final_ipa,
                    "size": final_ipa.stat().st_size
                })
                progress.log(f"✅ Success: [magenta]{archive_path.name}[/magenta]")
            else:
                result.update({
                    "success": False,
                    "log": "Export succeeded, but the final .ipa file was not found."
                })
                progress.log(f"❌ Failed: [magenta]{archive_path.name}[/magenta] (IPA not found)")
        else:
            log = process.stdout + process.stderr
            result.update({"success": False, "log": log.strip()})
            progress.log(f"❌ Failed: [magenta]{archive_path.name}[/magenta]")
            
    except Exception as e:
        result.update({"success": False, "log": f"An unexpected Python error occurred: {e}"})
        progress.log(f"❌ Failed: [magenta]{archive_path.name}[/magenta] (Python Error)")
    finally:
        progress.update(task_id, advance=1)
        if plist_path.exists():
            plist_path.unlink()
    
    return result


def main():
    check_dependencies()
    
    default_workers = os.cpu_count() or 1
    parser = ArgumentParser(description="iOS XCArchive to IPA Exporter CLI")
    parser.add_argument("-i", "--input", type=str, default="input", help="Folder containing .xcarchive files")
    parser.add_argument("-o", "--output", type=str, default="output", help="Folder to save exported .ipa files")
    parser.add_argument("-m", "--method", type=str, default="development", choices=["development", "ad-hoc", "app-store", "enterprise"], help="Export method")
    parser.add_argument("-w", "--workers", type=int, default=default_workers, help=f"Number of parallel export processes (default: {default_workers})")
    args = parser.parse_args()

    INPUT_DIR = Path(args.input)
    OUTPUT_DIR = Path(args.output)
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    archives = sorted([f for f in INPUT_DIR.iterdir() if f.suffix == ".xcarchive"])

    if not archives:
        console.print(f"[red]❌ No .xcarchive files found in the '{INPUT_DIR}' folder.[/red]")
        return

    console.print(Panel.fit("[bold cyan]📦 arc2ipa Exporter[/bold cyan]\nModern XCArchive to IPA Converter", border_style="green"))
    console.print(f"🔹 Found [bold cyan]{len(archives)}[/bold cyan] archives. Starting export with [bold cyan]{args.workers}[/bold cyan] parallel workers.")

    results = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold green]Processing Archives...[/bold green]"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        overall_task = progress.add_task("Total Progress", total=len(archives))
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_to_archive = {
                executor.submit(export_single_archive, archive, OUTPUT_DIR, args.method, progress, overall_task)
                for archive in archives
            }
            for future in concurrent.futures.as_completed(future_to_archive):
                results.append(future.result())

    successful_exports = [r for r in results if r.get("success")]
    failed_exports = [r for r in results if not r.get("success")]

    console.print(Panel.fit("[bold]✨ Export Summary ✨[/bold]", border_style="blue"))

    if successful_exports:
        success_table = Table(title="✅ Successful Exports", show_header=True, header_style="bold green", box=None)
        success_table.add_column("Archive", style="magenta", no_wrap=True)
        success_table.add_column("IPA Name", style="cyan")
        success_table.add_column("Size", style="yellow", justify="right")
        success_table.add_column("Output Path")
        for res in successful_exports:
            ipa_path = res.get('ipa_path')
            size_in_mb = res.get('size', 0) / (1024 * 1024)
            ipa_name = ipa_path.name if ipa_path else "N/A"
            output_folder = str(ipa_path.parent) if ipa_path else "N/A"
            success_table.add_row(res['archive'].name, ipa_name, f"{size_in_mb:.2f} MB", output_folder)
        console.print(success_table)

    if failed_exports:
        failure_table = Table(title="❌ Failed Exports", show_header=True, header_style="bold red", box=None)
        failure_table.add_column("Archive", style="magenta", no_wrap=True)
        failure_table.add_column("Reason / Log")
        for res in failed_exports:
             failure_table.add_row(res['archive'].name, res.get('log', 'Unknown error'))
        console.print(failure_table)

    console.print("\n🎉 [bold green]All tasks finished![/bold green]")

if __name__ == "__main__":
    main()

