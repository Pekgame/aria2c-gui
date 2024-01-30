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

def download(url,
             torrent_file,
             metalink_file,
             input_file,
             load_cookies,
             max_connection_per_server,
             directory,
             out,
             split,
             check_integrity,
             continue_download,
             force_sequential,
             show_files,
             enable_dht,
             enable_dht6,
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
             custom_arguments
             ):
    options = ["aria2c.exe", url]
    if out:
        options.append("--out=" + out)
    if input_file:
        path2 = TEMP + os.path.basename(input_file)
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
        path4 = TEMP + os.path.basename(load_cookies)
        shutil.copyfile(load_cookies.name, path4)
        options.append("--load-cookies=" + load_cookies)
    if torrent_file:
        path1 = TEMP + os.path.basename(torrent_file)
        shutil.copyfile(torrent_file.name, path1)
        options.append("--torrent-file=" + path1)
    if dht_listen_addr6:
        options.append("--dht-listen-addr6=" + dht_listen_addr6)
    if metalink_file:
        path3 = TEMP + os.path.basename(input_file)
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
    options.append(f"--min-split-size={min_split_size}")
    options.append(f"--max-overall-upload-limit={max_overall_upload_limit}")
    options.append(f"--max-upload-limit={max_upload_limit}")
    options.append(f"--listen-port={listen_port_start}-{listen_port_end}")
    options.append(f"--dht-listen-port={dht_listen_port_start}-{dht_listen_port_end}")

    try:
        output = sp.run(options, stdout=sp.PIPE).stdout.decode("utf-8")
        print(output)
    except KeyboardInterrupt:
        print("Download cancelled!")

    if torrent_file:
        os.remove(path1)
    if input_file:
        os.remove(path2)
    if metalink_file:
        os.remove(path3)

    return rem_ansi(output)

app = gr.Interface(
    fn=download,
    inputs=[
        gr.Textbox(label="File URL"),
        gr.UploadButton(label="Upload Torrent File"),
        gr.UploadButton(label="Upload Metalink File"),  
        gr.UploadButton(label="Upload Input File"),
        gr.UploadButton(label="Upload Cookies File"),
        gr.Number(label="Max Connection Per Server", value=4, minimum=1, maximum=65535),
        gr.Textbox(label="Output Directory", value="./downloads"),
        gr.Textbox(label="Output File"),
        gr.Number(label="Split", value=5),
        gr.Checkbox(label="Check Integrity", value=False),
        gr.Checkbox(label="Continue Download", value=False),
        gr.Checkbox(label="Force Sequential", value=False),
        gr.Checkbox(label="Show Files", value=False),
        gr.Checkbox(label="Enable DHT", value=True),
        gr.Checkbox(label="Enable DHT6", value=False),
        gr.Dropdown(label="File Allocation", choices=["none", "prealloc", "trunc", "falloc"], value="prealloc"),
        gr.Number(label="Max Concurrent Downloads", value=5, minimum=1),
        gr.Number(label="Min Split Size", value=20_971_520, minimum=1_048_576, maximum=1_073_741_824),
        gr.Textbox(label="FTP Username"),
        gr.Textbox(label="FTP Password"),
        gr.Textbox(label="HTTP Username"),
        gr.Textbox(label="HTTP Password"),
        gr.Number(label="Max Overall Upload Limit", value=0, minimum=0),
        gr.Number(label="Max Upload Limit", value=0, minimum=0),
        gr.Number(label="Listen Port Start Range", value=6881, minimum=1024, maximum=65535),
        gr.Number(label="Listen Port End Range", value=6999, minimum=1024, maximum=65535),
        gr.Number(label="DHT Listen Port Start Range", value=6881, minimum=1024, maximum=65535),
        gr.Number(label="DHT Listen Port End Range", value=6999, minimum=1024, maximum=65535),
        gr.Textbox(label="DHT Listen Address6"),
        gr.Textbox(label="Custom Arguments"),
    ],
    outputs=gr.Textbox(label="Console Output"),
    title="aria2c",
    description="Download a file using aria2c.exe.",
    allow_flagging="never",
    theme=gr.themes.Soft(
        font=[
            gr.themes.GoogleFont("Source Code Pro"),
            "Arial",
            "sans-serif"]
        ),
)

if __name__ == "__main__":
    TEMP = "temp/"
    app.launch()
