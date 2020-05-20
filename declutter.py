from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import zipfile
import os
import shutil
import time
from pathlib import Path

def initial_declutter():
    for file in mylistdir(current_folder):
        #assuming these files are unnecessary and extracted from 
        if ".dmg" in file or ".exe" in file or ".zip" in file or "Integration" in file:
            #dealing with exception where file has already been moved or removed
            try:
                os.remove(current_folder+"/"+file)
            except Exception:
                continue
        #common document names used by document scanning apps
        elif "Office Lens" in file or "New Doc " in file:
            if not os.path.exists(current_folder+"/ScannedDocuments"):
                os.mkdir(current_folder+"/ScannedDocuments")
            for file_name in mylistdir(current_folder):
                if "Office Lens" in file_name or "New Doc" in file_name:
                    os.rename(f"{current_folder}/{file_name}", f"{current_folder}/ScannedDocuments/{file_name}")
        #combining all WhatsApp images manually to avoid subfolders caused by images downloaded on the same day 
        elif "WhatsApp Image" in file:
            if not os.path.exists(current_folder+"/WhatsApp_Images"):
                os.mkdir(current_folder+"/WhatsApp_Images")
            for file_name in mylistdir(current_folder):
                if "WhatsApp Image" in file_name:
                    os.rename(f"{current_folder}/{file_name}", f"{current_folder}/WhatsApp_Images/{file_name}")
        else:
            duplicates = []
            for file_name in mylistdir(current_folder):
                if file[:file.rfind(".")] in file_name and not_main(file_name) and file[file.rfind(".")+1:] in file_name:
                    duplicates.append(file_name)
                elif file in file_name:
                    duplicates.append(file_name)
            if len(duplicates) > 1 and not "WhatsApp Image" in file:
                duplicates.sort(key=before_dot)
                #trying for an exception in case the duplicate is a folder and not a file
                try:
                    os.remove(f"{current_folder}/{file}")
                except PermissionError:
                    shutil.rmtree(f"{current_folder}/{file}")
                if duplicates[len(duplicates) - 1] != file:
                    os.rename(f"{current_folder}/{(duplicates)[len(duplicates) - 1]}", f"{current_folder}/{file}")
                duplicates.pop(len(duplicates) - 1)
                duplicates.pop(0)
                for files in duplicates:
                    try:
                        os.remove(f"{current_folder}/{files}") 
                    except Exception:
                        shutil.rmtree(f"{current_folder}/{files}")
                        
                        
    #checking for similarities between different file names
    for file in mylistdir(current_folder):
        
        words = file.split()
        for i in range(len(words)):
            similar = []
            found = 0
            for file_name in mylistdir(current_folder):
                if words[i] in file_name and not_main(file_name):   
                    similar.append(file_name)
                if len(similar) < 2:
                    continue
                bigger_similar = similar
                lpointer = i
                rpointer = i
                left_similar = []
                right_similar = []
                lword = words[i]
                rword = words[i]
                final_word = words[i]
                finding_final_word = words[i]
                while len(bigger_similar) > 0.5 * len(similar) and (lpointer > 0 or rpointer < (len(words) - 1)):
                    similar = bigger_similar
                    final_word = finding_final_word
                    left_similar = []
                    right_similar = []
                    if lpointer > 0:
                        lword = words[lpointer - 1] + " "+lword
                        for file_name in mylistdir(current_folder):
                            if lword in file_name and not_main(file_name):  
                                left_similar.append(file_name)
                        lpointer-=1
                    if rpointer < (len(words) - 1):
                        rword = rword + " "+words[rpointer + 1]
                        for file_name in mylistdir(current_folder):
                            if rword in file_name and not_main(file_name):
                                right_similar.append(file_name)
                        rpointer+=1
                    bigger_similar =  left_similar if len(left_similar) > len(right_similar) else right_similar
                    finding_final_word = lword if len(left_similar) > len(right_similar) else rword    
                print(similar)            
                if len(final_word)> 3 or (len(final_word)>1 and final_word.isupper()):
                    if any(c.isalpha() for c in final_word):
                        if(os.path.exists(f"{current_folder}/{final_word}")):
                            final_word = final_word + " ALL"
                        if not os.path.exists(f"{current_folder}/{final_word}"):
                            os.mkdir(f"{current_folder}/{final_word}")
                        for each_file in similar:
                            os.rename(f"{current_folder}/{each_file}",f"{current_folder}/{final_word}/{each_file}")
                        found = 1
                break
            if found == 1:
                break
    for file in mylistdir(current_folder):
        if not_main(file):
            if "tibet" in file.lower() or "goldstein" in file.lower():
                Path(f"{current_folder}/Tibet_Files").mkdir(parents=True, exist_ok=True)
                os.rename(f"{current_folder}/{file}", f"{current_folder}/Tibet_Files/{file}")
            else:
                if "resume" in file.lower() or "coverletter" in file.lower() or "cover_letter" in file.lower() or "internship" in file.lower():
                    Path(f"{current_folder}/Career").mkdir(parents=True, exist_ok=True)
                    os.rename(f"{current_folder}/{file}", f"{current_folder}/Career/{file}")
                else:
                    college_stuff = ["exam", "assignment", "project", "worksheet", "midterm", "cwru", "SI ", "hw", "class", "engineering", "homework", "eecs", "phys", "sages", "essay", "syllabus", " math", "lab"]
                    for index in college_stuff:
                        if index in file.lower():
                            additional_path=""
                            if "syllabus" in file.lower():
                                additional_path = "Syllabus/"
                            elif "homework" in file.lower():
                                additional_path = "Homework/"
                            Path(f"{current_folder}/College/{additional_path}").mkdir(parents=True, exist_ok=True)
                            os.rename(f"{current_folder}/{file}", f"{current_folder}/College/{additional_path}{file}")
                            break

    for file in mylistdir(current_folder):
        if os.path.isdir(current_folder+"/"+file) and not_main(file):      
            file_types_dic = {}
            for i in all_files(current_folder+"/"+file):
                final_type = type_of(i[i.rfind("."):])
                section = final_type[:final_type.index("/")]
                file_types_dic[section] = file_types_dic.get(section, 0) + 1
            if len(file_types_dic) > 0:
                file_type = keywithmaxval(file_types_dic)
                if not os.path.exists(current_folder+"/"+file_type):
                    Path(current_folder+"/"+file_type).mkdir(parents=True, exist_ok=True)
                os.rename(f"{current_folder}/{file}", f"{current_folder}/{file_type}/{file}")            
        elif not_main(file):
            file_type = file[file.rfind("."):]
            folder_name = type_of(file_type)
            if not os.path.exists(current_folder+"/"+folder_name[:folder_name.rfind("/")]):
                Path(current_folder+"/"+folder_name[:folder_name.rfind("/")]).mkdir(parents=True, exist_ok=True)
            os.rename(f"{current_folder}/{file}", f"{current_folder}/{folder_name}{file}")
            

def mylistdir(directory):
    """A specialized version of os.listdir() that ignores files that
    start with a leading period."""
    filelist = os.listdir(directory)
    return [x for x in filelist
            if not (x.startswith('.'))]

def not_main(file):
    return file != "Media" and file != "Unknown" and file != "Programming" and file != "Docs"
def before_dot(e):
    return e[:e.rfind(".")]     
def type_of(file_type):
    if file_type == ".jpg" or file_type == ".jpeg" or file_type == ".png":
        folder_type = "Media/Pictures/"
    elif file_type == ".java" or file_type == ".class":
        folder_type = "Programming/Java/"
    elif file_type == ".py":
        folder_type = "Programming/Python/"
    elif file_type == ".js":
        folder_type = "Programming/JavaScript/"
    elif file_type == ".mp4" or file_type == ".mov":
        folder_type = "Media/Videos/"
    elif file_type == ".mp3" or file_type == ".m4a":
        folder_type = "Media/Music/"
    elif file_type == ".docx" or file_type == ".doc":
        folder_type = "Docs/Word_Documents/"
    elif file_type == ".pdf":
        folder_type = "Docs/PDFS/"
    elif file_type == ".pptx" or file_type == ".ppt":
        folder_type = "Docs/Powerpoints/"
    elif file_type == ".xlsx":
        folder_type = "Docs/Excel"
    elif file_type == ".txt":
        folder_type = "Docs/Text_Files/"
    elif file_type == ".psd":
        folder_type = "Docs/Photoshop/"
    elif file_type == ".indd":
        folder_type = "Docs/InDesign/"
    elif file_type == ".v":
        folder_type = "Programming/Verilog/"
    elif file_type == ".epub":
        folder_type = "Media/Books/"
    elif file_type == ".csv" or file_type == ".css" or file_type == ".scss" or file_type == ".html" or file_type == ".sql" or file_type ==".ASM" or file_type==".sv":
        folder_type = f"Programming/{file_type[1:].upper()}/"
    elif file_type==".ical" or file_type==".ics":
        folder_type = "Docs/Calendar_Docs/"
    else:
        folder_type = "Unknown/"
        
    return folder_type

def all_files(path):
    filelist = []
    for root, dirs, files in os.walk(path):
	    for file in files:
		    filelist.append(os.path.join(root,file))      
    return filelist  

def keywithmaxval(d):
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]      
        
class DownloadsHandler(FileSystemEventHandler):

    last_modified = ""
        
    def on_modified(self, event):
        time.sleep(5)
        initial_declutter()
        time.sleep(10)
        for src in all_files(current_folder):
            file = src[src.index(current_folder)+len(current_folder)+1:]
            new_location = new_folder + "/" + file
            if not os.path.exists(new_location[:new_location.rfind("/")]):
                 Path(new_location[:new_location.rfind("/")]).mkdir(parents=True, exist_ok=True)
            if file.endswith(".zip"):
                new_location = new_location[:new_location.index(".zip")]
                with zipfile.ZipFile(src,"r") as zip_ref:
                    zip_ref.extractall(new_location)
                os.remove(src)
            else:
                os.rename(src, new_location)
                if file.endswith(".dmg"):
                    time.sleep(100)
                    os.remove(new_location)
        for folders in mylistdir(current_folder):
            shutil.rmtree(f"{current_folder}/{folders}")
            '''
        latest_file = max(all_files(new_folder), key=os.path.getctime)
        if latest_file != self.last_modified and not latest_file.startswith("."):
            os.system("open " + latest_file)
            self.last_modified = latest_file
            '''

current_folder = "/Users/starkiller/Downloads copy"
new_folder = "/Users/starkiller/new-downloads"
initial_declutter()
time.sleep(10)
event_handler = DownloadsHandler()
observer = Observer()
observer.schedule(event_handler, current_folder, recursive=True)
observer.start()

try:
    while(True):
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()