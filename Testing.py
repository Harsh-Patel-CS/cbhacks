import webbrowser as wb
import requests
import os
import subprocess
from langchain_ollama import OllamaLLM
import customtkinter as ctk
import tkinter as tk

def Startup(window):
    startpage = ctk.CTkFrame(window, fg_color="transparent")
    title = ctk.CTkLabel(startpage, text="Installing Ollama...", font=("Arial", 50))
    title.pack(pady=20)
    progress_bar = ctk.CTkProgressBar(startpage, orientation="horizontal", width=300)
    progress_bar.pack(pady=20)
    progress_bar.set(0) 
    startpage.pack()
    url = "https://ollama.com/download/OllamaSetup.exe"
    response = requests.get(url, stream=True)

    total_size = int(response.headers.get('Content-Length', 0))
    downloaded_size = 0

    with open("OllamaSetup.exe", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                downloaded_size += len(chunk)
                percent = (downloaded_size / total_size) #percent downloaded
                progress_bar.set(percent)

    startpage.destroy()
    installpage = ctk.CTkFrame(window, fg_color="transparent")
    install_title = ctk.CTkLabel(installpage, text="Ollama setup installer will now open. Please install", font=("Arial", 50)) 
    install_title.pack(pady=20)
    installpage.pack()

    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Path to ollama.exe in the same folder
    ollama_path = os.path.join(current_dir, 'OllamaSetup.exe')

    # Run the executable
    subprocess.run([ollama_path])

    installpage.destroy()





def find_ollama(start_path="C:\\"):
    for root, dirs, files in os.walk(start_path):
        if "ollama.exe" in files:
            return os.path.join(root, "ollama.exe")
    return None


def askquestion(textbox, model, chat_title):
    question = textbox.get("0.0", "end-1c")  # Get the text from the textbox
    answer = model.invoke(input=question)

    chat_title.configure(text=answer)
    textbox.delete("0.0", "end") 

def openollama(window):
    ollama_path = find_ollama()

    # Command to run
    command = [ollama_path, "pull", "llama3"]
    waitpage = ctk.CTkFrame(window, fg_color="transparent")
    wait_title = ctk.CTkLabel(waitpage, text="Waiting for Ollama to install the Ai model...", font=("Arial", 50))
    wait_title.pack(pady=20)
    waitpage.pack()

   
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',  # ← Force UTF-8 decoding
        errors='replace'
    )

    process.wait() 
    waitpage.destroy()

    model = OllamaLLM(model="llama3")
    chatpage = ctk.CTkFrame(window, fg_color="transparent")
    chat_title = ctk.CTkLabel(chatpage, text="Ask your question to the Ai", font=("Arial", 20))
    chat_title.pack(pady=20)
    textbox = ctk.CTkTextbox(chatpage, width=1000, height=200)
    textbox.pack(pady=20)
    ask_button = ctk.CTkButton(chatpage, text="Ask", command=lambda: askquestion(textbox, model, chat_title), width=200, height=50)
    ask_button.pack(pady=20)
    chatpage.pack()
      



window = ctk.CTk()
window.title("Student Assistant")
window.geometry("1740x800")
def destroy_intropage(intro_page,window):
    intro_page.destroy()
    setup_file = "setup_done.txt"
    if not os.path.exists(setup_file):
        
        Startup(window)
        # Do setup tasks here...put setup fuction

        # Create the file to indicate setup is done
        with open(setup_file, "w") as f:
            f.write("Setup completed")
        
        openollama(window)
    else:
        #put home page function here
        openollama(window)

def intropage(window):
    intro_page = ctk.CTkFrame(window, fg_color="transparent")
    intro_title = ctk.CTkLabel(intro_page, text="Welcome to Student Assistant", font=("Arial", 50))
    intro_title.pack(pady=20)
    next_button = ctk.CTkButton(intro_page, text="Next", command=lambda: destroy_intropage(intro_page, window), width=200, height=50)
    next_button.pack(pady=20)

    intro_page.pack()


intropage(window)







window.mainloop()