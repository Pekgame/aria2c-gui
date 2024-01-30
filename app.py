# Code by Pekgame
# Version 0.0.1 Alpha
# Copyright (c) 2024 Pekgame

import re
import os
import shutil
import gradio as gr
import subprocess as sp


def rem_ansi(input_string):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', input_string)


def convert_to_bytes(memory_size: str):
    memory_size = memory_size.upper()

    if "GB" in memory_size:
        try:
            return int(memory_size.replace("GB", "")) * 1024**3
        except ValueError:
            return 404
    elif "MB" in memory_size:
        try:
            return int(memory_size.replace("MB", "")) * 1024**2
        except ValueError:
            return 404
    elif "KB" in memory_size:
        try:
            return int(memory_size.replace("KB", "")) * 1024
        except ValueError:
            return 404
    elif "B" in memory_size:
        try:
            return int(memory_size.replace("B", ""))
        except ValueError:
            return 404
    else:
        return 404


def cancle_download():
    global popen
    global canceled
    popen.terminate()
    canceled = True


def download(
    url,
    torrent_file,
    metalink_file,
    input_file,
    load_cookies,
    max_connection_per_server,
    directory,
    out,
    check_integrity,
    continue_download,
    force_sequential,
    show_files,
    enable_dht,
    enable_dht6,
    split,
    file_allocation,
    max_concurrent_downloads,
    min_split_size,
    ftp_user,
    ftp_passwd,
    http_user,
    http_passwd,
    max_overall_upload_limit,
    max_upload_limit,
    listen_port_start,
    listen_port_end,
    dht_listen_port_start,
    dht_listen_port_end,
    dht_listen_addr6,
    temp_folder,
    custom_arguments
):
    options = ["aria2c.exe", url]
    min_split_size = convert_to_bytes(min_split_size)
    if min_split_size != 404:
        options.append(f"--min-split-size={min_split_size}")
    else:
        return "Invalid Min Split Size!"
    if out != "auto":
        options.append("--out=" + out)
    if input_file:
        bname = os.path.basename(input_file)
        path2 = os.path.join(temp_folder, bname)
        shutil.copyfile(input_file.name, path2)
        options.append("--input-file=" + path2)
    if ftp_user:
        options.append("--ftp-user=" + ftp_user)
    if ftp_passwd:
        options.append("--ftp-passwd=" + ftp_passwd)
    if http_user:
        options.append("--http-user=" + http_user)
    if http_passwd:
        options.append("--http-passwd=" + http_passwd)
    if load_cookies:
        bname = os.path.basename(load_cookies)
        path4 = os.path.join(temp_folder, bname)
        shutil.copyfile(load_cookies.name, path4)
        options.append("--load-cookies=" + load_cookies)
    if torrent_file:
        bname = os.path.basename(torrent_file)
        path1 = os.path.join(temp_folder, bname)
        shutil.copyfile(torrent_file.name, path1)
        options.append("--torrent-file=" + path1)
    if dht_listen_addr6:
        options.append("--dht-listen-addr6=" + dht_listen_addr6)
    if metalink_file:
        bname = os.path.basename(input_file)
        path3 = os.path.join(temp_folder, bname)
        shutil.copyfile(input_file.name, path3)
        options.append("--metalink-file=" + metalink_file)
    if custom_arguments:
        options.append(custom_arguments)

    options.append(f"--dir={directory}")
    options.append(f"--max-connection-per-server={max_connection_per_server}")
    options.append(f"--split={split}")
    options.append(f"--check-integrity={str(check_integrity).lower()}")
    options.append(f"--continue={str(continue_download).lower()}")
    options.append(f"--force-sequential={str(force_sequential).lower()}")
    options.append(f"--show-files={str(show_files).lower()}")
    options.append(f"--enable-dht={str(enable_dht).lower()}")
    options.append(f"--enable-dht6={str(enable_dht6).lower()}")
    options.append(f"--file-allocation={file_allocation}")
    options.append(f"--max-concurrent-downloads={max_concurrent_downloads}")
    options.append(f"--max-overall-upload-limit={max_overall_upload_limit}")
    options.append(f"--max-upload-limit={max_upload_limit}")
    options.append(f"--listen-port={listen_port_start}-{listen_port_end}")
    options.append(f"--dht-listen-port={dht_listen_port_start}-{dht_listen_port_end}")

    try:
        global popen
        global canceled
        last = ""
        popen = sp.Popen(options, stdout=sp.PIPE, stderr=sp.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            if canceled:
                canceled = False
                popen.stdout.close()
                return "Download cancelled!"
            print(stdout_line, end="")
            last += stdout_line
            yield rem_ansi(last)
        popen.stdout.close()
    except KeyboardInterrupt:
        return "Download cancelled!"

    if torrent_file:
        os.remove(path1)
    if input_file:
        os.remove(path2)
    if metalink_file:
        os.remove(path3)

theme = gr.themes.Soft(
    font=[gr.themes.GoogleFont("Source Code Pro"), "Arial", "sans-serif"]
)

with gr.Blocks(theme=theme) as app:
    with gr.Tab(label="Main"):
        with gr.Column():
            inp = [
                gr.Textbox(
                    label="File URL",
                    info="URL of the file to download.",
                    placeholder="http://example.com/file.zip",
                )
            ]
            btn = gr.Button("Download")
        with gr.Row():
            inp += [
                gr.UploadButton(label="Upload Torrent File"),
                gr.UploadButton(label="Upload Metalink File"),
                gr.UploadButton(label="Upload Input File"),
                gr.UploadButton(label="Upload Cookies File"),
            ]
        with gr.Column():
            inp += [
                gr.Number(
                    label="Max Connection Per Server",
                    value=4,
                    minimum=1,
                    maximum=65535,
                    info="The maximum number of connections to one server for each download.",
                ),
                gr.Textbox(
                    label="Output Directory",
                    value="./downloads",
                    info="The directory to store the downloaded file.",
                ),
                gr.Textbox(
                    label="Output File",
                    value="auto",
                    info="The file name of the downloaded file."
                ),
            ]
        out = gr.Textbox(
            label="Console Output",
            lines=13,
            placeholder="Console output will appear here.",
        )
        cancle = gr.Button(value="Cancel Download")
    with gr.Tab(label="Advanced Options"):
        with gr.Row():
            with gr.Column():
                inp += [
                    gr.Checkbox(
                        label="Check Integrity",
                        value=False,
                        info="Check file integrity by validating hash of the file. (BitTorrent, Metalink only)",
                    ),
                    gr.Checkbox(
                        label="Continue Download",
                        value=False,
                        info="Continue downloading a partially downloaded file.",
                    ),
                    gr.Checkbox(
                        label="Force Sequential",
                        value=False,
                        info="Fetch URIs in the command-line sequentially and download each URI in a separate session.",
                    ),
                ]
            with gr.Column():
                inp += [
                    gr.Checkbox(
                        label="Show Files",
                        value=False,
                        info="Print file listing of torrent.",
                    ),
                    gr.Checkbox(
                        label="Enable DHT",
                        value=True,
                        info="Enable DHT (Distributed Hash Table).",
                    ),
                    gr.Checkbox(
                        label="Enable DHT6",
                        value=False,
                        info="Enable IPv6 DHT (Distributed Hash Table 6).",
                    ),
                ]
        with gr.Column():
            inp += [
                gr.Number(
                    label="Split",
                    value=5,
                    minimum=1,
                    info="Download a file using N connections.",
                ),
                gr.Dropdown(
                    label="File Allocation",
                    choices=["none", "prealloc", "trunc", "falloc"],
                    value="prealloc",
                    info="File allocation mode.",
                ),
                gr.Number(
                    label="Max Concurrent Downloads",
                    value=5,
                    minimum=1,
                    info="The maximum number of parallel downloads for every static file.",
                ),
                gr.Textbox(
                    label="Min Split Size", value="20MB", info="Minimum split size."
                ),
            ]
        with gr.Row():
            with gr.Row():
                inp += [
                    gr.Textbox(label="FTP Username", info="FTP user name."),
                    gr.Textbox(label="FTP Password", info="FTP password."),
                ]
            with gr.Row():
                inp += [
                    gr.Textbox(label="HTTP Username", info="HTTP user name."),
                    gr.Textbox(label="HTTP Password", info="HTTP password."),
                ]
        with gr.Column():
            inp += [
                gr.Number(
                    label="Max Overall Upload Limit",
                    value=0,
                    minimum=0,
                    info="The maximum upload speed in bytes per second for every download.",
                ),
                gr.Number(
                    label="Max Upload Limit",
                    value=0,
                    minimum=0,
                    info="The maximum upload speed in bytes per second for every torrent.",
                ),
            ]
        with gr.Row():
            with gr.Row():
                inp += [
                    gr.Number(
                        label="Listen Port Start Range",
                        value=6881,
                        minimum=1024,
                        maximum=65535,
                        info="The starting port of BitTorrent listen port range.",
                    ),
                    gr.Number(
                        label="Listen Port End Range",
                        value=6999,
                        minimum=1024,
                        maximum=65535,
                        info="The ending port of BitTorrent listen port range.",
                    ),
                ]
            with gr.Row():
                inp += [
                    gr.Number(
                        label="DHT Listen Port Start Range",
                        value=6881,
                        minimum=1024,
                        maximum=65535,
                        info="The starting port of DHT listen port range.",
                    ),
                    gr.Number(
                        label="DHT Listen Port End Range",
                        value=6999,
                        minimum=1024,
                        maximum=65535,
                        info="The ending port of DHT listen port range.",
                    ),
                ]
        with gr.Column():
            inp += [
                gr.Textbox(
                    label="DHT Listen Address6", info="The IPv6 address to bind to."
                ),
                gr.Textbox(
                    label="Temp Folder",
                    value="./temp",
                    info="The directory to store temporary files.",
                ),
                gr.Textbox(
                    label="Custom Arguments", info="Custom arguments to pass to aria2c."
                ),
            ]

    btn.click(fn=download, inputs=inp, outputs=out)
    cancle.click(fn=cancle_download, outputs=out)

if __name__ == "__main__":
    canceled = False
    app.launch()
