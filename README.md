
# ZCB 2.0 (Zeo's ClickBot)
**[Geometry Dash](https://en.wikipedia.org/wiki/Geometry_Dash)** Clickbot, written in [Python](https://www.python.org/). It is the rewrite of ZCB with better codebase, easier usage, better sound.

![ZCB logo made by Frigel](https://cdn.discordapp.com/attachments/952196428598501426/952630587162775562/icon.jpg)

> If you have any questions, visit our Discord server:
> [Click here](https://discord.gg/kGPAjmdpUX)
![Discord widget](https://discordapp.com/api/guilds/952180713803878431/widget.png?style=banner2)

# Example
![zcb](https://cdn.discordapp.com/attachments/783966433641365504/964760765225652274/zcb.gif)
Proper GUI will be added soon, until then I made an easy CLI tool.
# Download
[For binary builds with Pyinstaller, click here](https://github.com/zeopticz/zcb/releases)

# Supported files (macros)
[Echo](https://discord.gg/7yEHbBVswh) `(.echo)` (make sure you don't record the macro in binary, else, convert it (ask in the echo server))
[TASbot](https://discord.gg/RbWPSYPyrS) `(.json)`

# Click pack guide

 

    This is how to add your own clicks.
    Example folder: clicks-example.
    First up, add a "player1" folder inside it.
    You can optionally create a folder called "player2" if you want different clicks for the second player.
    
    In the folder, create the following folders:
    clicks (necessary)
    releases (optional)
    softclicks (optional)
    softreleases (optional)
    
    Clicks will be used when you click the mouse (in the macro.
    Releases will be used when you release the mouse. (if you don't specify it, it will use clicks instead of releases.)
    Softclicks are optional, but highly recommended. They make the clicks realistic in spams, for example.
    Softreleases are optional, they're played after softclicks. (if you dont specify it, it will use normal releases)
    
    In the folders, create sounds like this:
    1.wav
    2.wav
    3.wav
    4.wav
    and so on...
    
    Example directory tree:
    
    .
    └── Any Folder Name Which You Will Select/
        ├── player1/
        │   ├── clicks/
        │   │   ├── 1.wav
        │   │   ├── 2.wav
        │   │   ├── 3.wav
        │   │   └── 4.wav
        │   ├── releases/
        │   │   ├── 1.wav
        │   │   ├── 2.wav
        │   │   └── 3.wav
        │   ├── softclicks/
        │   │   ├── 1.wav
        │   │   └── 2.wav
        │   └── softreleases/
        │       ├── 1.wav
        │       ├── 2.wav
        │       ├── 3.wav
        │       └── 4.wav
        └── player2/
            ├── clicks/
            │   ├── 1.wav
            │   ├── 2.wav
            │   └── 3.wav
            ├── releases/
            │   └── 1.wav
            ├── softclicks/
            │   ├── 1.wav
            │   ├── 2.wav
            │   ├── 3.wav
            │   └── 4.wav
            └── softreleases/
                ├── 1.wav
                ├── 2.wav
                ├── 3.wav
                └── 4.wav

