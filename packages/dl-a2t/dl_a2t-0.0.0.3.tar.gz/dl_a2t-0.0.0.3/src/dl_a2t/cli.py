from json import dumps
from tempfile import TemporaryDirectory
from typing import Annotated

from typer import FileBinaryWrite, Option, Typer

from .impl.download import extract_audio
from .impl.transcript import transcribe_audio

app = Typer()


@app.command()
def run(
    input_url: str,
    output_file: FileBinaryWrite,
    *,
    model: Annotated[str, Option(help="Whisper model to use")] = "tiny",
):
    """
    下载音频并转录为文本

    输出文件必须以 .json, .txt 或 .jsonl 结尾
    """
    with TemporaryDirectory() as temp_dir:
        filename = f"{temp_dir}/audio.webm"
        extract_audio(input_url, filename)
        result = transcribe_audio(filename, model)

    if output_file.name.endswith(".json"):
        output_file.write(dumps(result).encode())
    elif output_file.name.endswith(".txt"):
        output_file.write(result["text"].encode())
    elif output_file.name.endswith(".jsonl"):
        output_file.write("\n".join(map(dumps, result["segments"])).encode())
    else:
        raise ValueError("Output file must end with .json, .txt, or .jsonl")


if __name__ == "__main__":
    app()
