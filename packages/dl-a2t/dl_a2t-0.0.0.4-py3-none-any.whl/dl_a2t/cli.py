from json import dumps
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Annotated

from typer import Option, Typer

from .impl.download import extract_audio
from .impl.transcript import transcribe_audio

app = Typer()


@app.command()
def run(
    input_url: str,
    output_file: Path,
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
        output_file.write_text(dumps(result))
    elif output_file.name.endswith(".txt"):
        output_file.write_text(result["text"])
    elif output_file.name.endswith(".jsonl"):
        output_file.write_text("\n".join(map(dumps, result["segments"])))
    else:
        raise ValueError("Output file must end with .json, .txt, or .jsonl")


if __name__ == "__main__":
    app()
