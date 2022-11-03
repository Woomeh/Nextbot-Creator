import io
import PySimpleGUI as sg
import webbrowser
import shutil
import os
from pydub import AudioSegment as aus
from PIL import Image
# Create the GUI
first_column = [[sg.Text("Nextbot Name", font=("TkFixedFont", 10, 'bold'))],
                [sg.Text("Category", font=("TkFixedFont", 10, 'bold'))],
                [sg.Text("Speed", font=("TkFixedFont", 10, 'bold'))],
                [sg.Text("Addon Folder", font=("TkFixedFont", 10, 'bold'))],
                [sg.Text("Chase Sound", font=("TkFixedFont", 10, 'bold'))],
                [sg.Text("Death Sound", font=("TkFixedFont", 10, 'bold'))],
                [sg.Text("Jump Sound", font=("TkFixedFont", 10, 'bold'))],
                [sg.Text("Nextbot PNG", font=("TkFixedFont", 10, 'bold'))],
                [sg.Text("Nextbot VTF", font=("TkFixedFont", 10, 'bold'))],
                [sg.Checkbox("Admin Only",font=("TkFixedFont", 10, 'bold'), default=True, key="-ADM-")], 
                [sg.Button("Create"), sg.Button("Tutorial")]]

second_column = [[sg.Input(key="-NAME-", enable_events=True)],
                 [sg.Input(key="-CAT-")],
                 [sg.Input(key="-SPD-"), sg.Text("500->default")],
                 [sg.Input(key="-ADDON-"), sg.FolderBrowse(target="-ADDON-", pad=(0,0))],
                 [sg.Input(key="-CHASE-"), sg.FileBrowse(file_types=(("MP3 Files", "*.mp3"),), target="-CHASE-", pad=(0,0))],
                 [sg.Input(key="-DEATH-"), sg.FileBrowse(file_types=(("MP3 Files", "*.mp3"),), target="-DEATH-", pad=(0,0))],
                 [sg.Input(key="-JUMP-"), sg.FileBrowse(file_types=(("MP3 Files", "*.mp3"),), target="-JUMP-", pad=(0,0))],
                 [sg.Input(key="-PNG-", enable_events=True), sg.FileBrowse(file_types=(("PNG Files", "*.png"),), target="-PNG-", pad=(0,0))],
                 [sg.Input(key="-VTF-"), sg.FileBrowse(file_types=(("VTF Files", "*.vtf"),), target="-VTF-", pad=(0,0))]]

layout = [[sg.Column(first_column, vertical_alignment='t'),
           sg.Column(second_column, vertical_alignment='t'),
           sg.VSeperator(),
           sg.Image(key="-IMAGE-")]]

window = sg.Window('Nextbot Maker', layout, size=(1000,350))
#Create Folders
def mkFolders():
    global npc; global luaFolder; global luaEntitiesFolder; global materialsFolder
    global materialsEntitiesFolder; global materialsNPCFolder; global soundFolder
    global soundNPCFolder; global Dir
    npc = 'npc_' + NEName
    luaFolder = os.path.join(values["-ADDON-"], "lua")
    luaEntitiesFolder = os.path.join(luaFolder, "entities")
    materialsFolder = os.path.join(values["-ADDON-"], "materials")
    materialsEntitiesFolder = os.path.join(materialsFolder, "entities")
    materialsNPCFolder = os.path.join(materialsFolder, npc)
    soundFolder = os.path.join(values["-ADDON-"], "sound")
    soundNPCFolder = os.path.join(soundFolder, npc)
    Dir = [luaFolder, luaEntitiesFolder, materialsFolder,
           materialsEntitiesFolder, materialsNPCFolder, soundFolder, soundNPCFolder]

#Create sound files
def mvSoundFiles():
    shutil.copy(values["-CHASE-"], soundNPCFolder)
    shutil.copy(values["-DEATH-"], soundNPCFolder)
    shutil.copy(values["-JUMP-"], soundNPCFolder)
    chaseFN = values["-CHASE-"].replace(os.path.dirname(values["-CHASE-"]), '')
    deathFN = values["-DEATH-"].replace(os.path.dirname(values["-DEATH-"]), '')
    jumpFN = values["-JUMP-"].replace(os.path.dirname(values["-JUMP-"]), '')
    chaseFN = chaseFN.replace('/', '', 1)
    deathFN = deathFN.replace('/', '', 1)
    jumpFN = jumpFN.replace('/', '', 1)
    os.chdir(soundNPCFolder)
    chase = aus.from_mp3(chaseFN)
    chase = chase.set_frame_rate(44100)
    chase = chase + 30
    chase.export("panic.mp3", format="mp3")
    death = aus.from_mp3(deathFN)
    death = death.set_frame_rate(44100)
    death = death + 30
    death.export("pieceofcake.mp3", format="mp3")
    jump = aus.from_mp3(jumpFN)
    jump = jump.set_frame_rate(44100)
    jump = jump + 30
    jump.export("jump.mp3", format="mp3")
    os.remove(chaseFN)
    os.remove(deathFN)
    os.remove(jumpFN)

def mvMaterials():
    os.chdir(materialsEntitiesFolder)
    pngFN = values["-PNG-"].replace(os.path.dirname(values["-PNG-"]),'')
    pngFN = pngFN.replace('/', '', 1)
    shutil.copy(values["-PNG-"], materialsEntitiesFolder)
    os.rename(pngFN, npc + '.png')
    os.chdir(materialsNPCFolder)
    vtfFN = values["-VTF-"].replace(os.path.dirname(values["-VTF-"]),'')
    vtfFN = vtfFN.replace('/', '', 1)
    shutil.copy(values["-VTF-"], materialsNPCFolder)
    os.rename(vtfFN, NEName + '.vtf')
    with open(NEName+'.txt', 'w') as f:
        f.write("\"UnlitGeneric\"\n")
        f.write("{\n")
        f.write("                \"$basetexture\" \"" + npc + '/' + NEName + "\"\n")
        f.write("                \"$alphatest\" 1\n")
        f.write("}")
    os.rename(NEName+'.txt', NEName+'.vmt')
    with open(NEName+'.txt', 'w') as f:
        f.write("\"UnlitGeneric\"\n")
        f.write("{\n")
        f.write("                \"$basetexture\" \"" + npc + '/' + NEName + "\"\n")
        f.write("                \"$translucent\" 1\n")
        f.write("                \"$vertexalpha\" 1\n")
        f.write("}")
    os.rename(NEName+'.txt', "killicon.vmt")

def mkLua():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    shutil.copy('nextbot_code.txt', luaEntitiesFolder)
    os.chdir(luaEntitiesFolder)
    luaF = open('nextbot_code.txt', 'r')
    luaFD = luaF.read()
    luaF.close()
    luaND = luaFD.replace("Name = \"smiley\"", "Name = \""+values["-NAME-"]+"\"").replace('smiley', NEName).replace('Speed(500)', 'Speed('+values["-SPD-"]+')').replace('tion(500)', 'tion('+values["-SPD-"]+')')
    if values["-ADM-"] == False:
        luaND = luaND.replace('AdminOnly = true', 'AdminOnly = false')
    luaF = open('nextbot_code.txt', 'w')
    luaF.write(luaND)
    luaF.close()
    os.rename('nextbot_code.txt', npc + '.lua')
        
#Main Code
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == "-NAME-" and values["-NAME-"] and values["-NAME-"][-1] not in ('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ._ '):
        window["-NAME-"].update(values["-NAME-"][:-1])
    if event == "-PNG-":
        if os.path.exists(values["-PNG-"]):
            image = Image.open(values["-PNG-"])
            image.thumbnail((400,400))
            image = image.resize((300, 300), resample=0)
            bio = io.BytesIO()
            image.save(bio, format="PNG")
            window["-IMAGE-"].update(data=bio.getvalue())
    elif event == "Tutorial":
        webbrowser.open("https:/youtube.com")
    elif event == "Create":
        NEName = values["-NAME-"].lower().replace(' ', '_')
        mkFolders()
        for i in range(len(Dir)):
            try:
                os.mkdir(Dir[i])
                print("Created Folder " + Dir[i])
            except:
                pass
        mvSoundFiles()
        mvMaterials()
        mkLua()
        print("Done")
window.close()
