# dl-a2t

dl-a2t 是一个从 YouTube 下载音频并转录为文本的工具。它使用 yt-dlp 下载音频，并使用 OpenAI 的 Whisper 模型进行转录。

## 使用方法

使用 dl-a2t 需要 Python 3.12 或更高版本。首先，确保你已经安装了 Python 和 pip。然后，使用以下命令安装 dl-a2t：

```sh
pip install dl-a2t
```

安装完成后，你可以使用以下命令来下载音频并转录为文本：

```sh
uv run cli.py <视频URL> <输出文件路径>
```

输出文件路径可以是 JSON、TXT 或 JSONL 格式。例如：

* 输出为 JSON 文件：`python -m dl_a2t.run <YouTube视频URL> output.json`
* 输出为 TXT 文件：`python -m dl_a2t.run <YouTube视频URL> output.txt`
* 输出为 JSONL 文件：`python -m dl_a2t.run <YouTube视频URL> output.jsonl`

## 依赖项

dl-a2t 依赖以下库：

* yt-dlp：用于下载 YouTube 视频的音频
* OpenAI Whisper：用于转录音频为文本
* Typer：用于命令行界面

## 文件结构

dl-a2t 的文件结构如下：

* `cli.py`：命令行界面
* `pyproject.toml`：项目配置文件
* `impl/download.py`：用于下载音频的实现
* `impl/transcript.py`：用于转录音频为文本的实现
* `README.md`：本文档
