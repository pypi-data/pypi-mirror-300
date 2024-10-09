from cfmtoolbox import app, CFM
import webbrowser

@app.command()
def rick_roll(cfm: CFM) -> CFM:
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return cfm
