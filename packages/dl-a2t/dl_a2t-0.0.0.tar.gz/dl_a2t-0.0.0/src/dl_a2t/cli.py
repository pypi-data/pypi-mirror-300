from json import dumps
from pathlib import Path
from tempfile import TemporaryDirectory

from typer import Typer

from .impl.download import extract_audio
from .impl.transcript import transcribe_audio

app = Typer()


@app.command()
def run(input_url: str, output_file: str):
    """
    下载音频并转录为文本

    输出文件必须以 .json, .txt 或 .jsonl 结尾
    """
    with TemporaryDirectory() as temp_dir:
        filename = f"{temp_dir}/audio.webm"
        extract_audio(input_url, filename)
        result = transcribe_audio(filename)

    if output_file.endswith(".json"):
        Path(output_file).write_text(dumps(result))
    elif output_file.endswith(".txt"):
        Path(output_file).write_text(result["text"])
    elif output_file.endswith(".jsonl"):
        Path(output_file).write_text("\n".join(map(dumps, result["segments"])))
    else:
        raise ValueError("Output file must end with .json, .txt, or .jsonl")


if __name__ == "__main__":
    app()
