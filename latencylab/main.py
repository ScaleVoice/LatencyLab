import typer

from latencylab import run, prompt

app = typer.Typer()
app.add_typer(run.app, name="latency", help="Run LLM benchmark on constant prompt")
app.add_typer(prompt.app, name="prompt", help="Run LLM benchmark on various prompt sizes")
