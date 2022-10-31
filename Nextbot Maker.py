import PySimpleGUI as sg
import webbrowser
import shutil
import os
from pydub import AudioSegment as aus
# Create the GUI
layout = [[sg.Text("Nextbot Name", font=("TkFixedFont", 10, 'bold')),sg.Input(key="-NAME-", enable_events=True)],
          [sg.Text("Category        ", font=("TkFixedFont", 10, 'bold')),sg.Input(key="-CAT-")],
          [sg.Text("Addon Folder ", font=("TkFixedFont", 10, 'bold')),sg.Input(key="-ADDON-"), sg.FolderBrowse(target="-ADDON-")],
          [sg.Text("Chase Sound ", font=("TkFixedFont", 10, 'bold')),sg.Input(key="-CHASE-"), sg.FileBrowse(file_types=(("MP3 Files", "*.mp3"),), target="-CHASE-")],
          [sg.Text("Death Sound ", font=("TkFixedFont", 10, 'bold')),sg.Input(key="-DEATH-"), sg.FileBrowse(file_types=(("MP3 Files", "*.mp3"),), target="-DEATH-")],
          [sg.Text("Jump Sound  ", font=("TkFixedFont", 10, 'bold')),sg.Input(key="-JUMP-"), sg.FileBrowse(file_types=(("MP3 Files", "*.mp3"),), target="-JUMP-")],
          [sg.Text("Nextbot PNG ", font=("TkFixedFont", 10, 'bold')),sg.Input(key="-PNG-"), sg.FileBrowse(file_types=(("PNG Files", "*.png"),), target="-PNG-")],
          [sg.Text("Nextbot VTF ", font=("TkFixedFont", 10, 'bold')),sg.Input(key="-VTF-"), sg.FileBrowse(file_types=(("VTF Files", "*.vtf"),), target="-VTF-")],
          [sg.Checkbox("Admin Only",font=("TkFixedFont", 10, 'bold'), default=True, key="-ADM-")], 
          [sg.Button("Create"), sg.Button("Tutorial")]]

window = sg.Window('Nextbot Maker', layout, size=(600,350))
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
    luaND = luaFD.replace("Name = \"smiley\"", "Name = \""+values["-NAME-"]+"\"").replace('smiley', NEName).replace('NextbotMaker', values["-CAT-"])
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
