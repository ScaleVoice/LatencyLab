import typer

from latencylab import run

app = typer.Typer()
app.add_typer(run.app, name="run", help="Run LLM benchmark")
