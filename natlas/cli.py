import click
from rich.console import Console
from rich.markdown import Markdown
from natlas import NAtlasClient
import os

console = Console()

@click.group()
def app():
    """N-ATLAS SDK Command Line Interface"""
    pass

@app.command()
@click.argument('message', required=False)
@click.option('--language', '-l', default='en', help='Language code (en, yo, ha, ig)')
def chat(message, language):
    """Start an interactive chat REPL or send a one-shot message."""
    client = NAtlasClient()
    
    if message:
        response = client.chat(message, language=language)
        console.print(Markdown(response.text))
        return
        
    console.print(f"[bold green]Starting interactive chat ({language}). Type 'exit' to quit.[/bold green]")
    while True:
        try:
            user_input = console.input("[bold blue]You:[/bold blue] ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            response = client.chat(user_input, language=language)
            console.print(f"[bold purple]N-ATLAS:[/bold purple] ", end="")
            console.print(Markdown(response.text))
        except KeyboardInterrupt:
            break

@app.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--language', '-l', default=None, help='Force language code')
def transcribe(file_path, language):
    """Transcribe an audio file."""
    client = NAtlasClient()
    console.print("[yellow]Transcribing...[/yellow]")
    result = client.transcribe(file_path, language=language)
    console.print(f"[green]Language: {result.language}[/green]")
    console.print(f"[bold]Transcript:[/bold] {result.text}")

@app.command()
@click.option('--port', default=8000, help='Port to bind to')
def serve(port):
    """Start the API server."""
    import uvicorn
    console.print(f"[bold green]Starting N-ATLAS Server on port {port}...[/bold green]")
    uvicorn.run("natlas.server:app", host="0.0.0.0", port=port, reload=True)

@app.command()
def models():
    """List available models."""
    console.print("[bold]Available Models:[/bold]")
    console.print("- NCAIR1/N-ATLaS (LLM)")
    console.print("- NCAIR1/Hausa-ASR")
    console.print("- NCAIR1/Yoruba-ASR")
    console.print("- NCAIR1/Igbo-ASR")
    console.print("- NCAIR1/NigerianAccentedEnglish")

if __name__ == '__main__':
    app()
