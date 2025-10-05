import os
import shutil
import tkinter as tk
from tkinter import filedialog, ttk
import re

RäumendenFolder = ""
listeArtSortieren = []
def ordner_aussuchen():
    global RäumendenFolder
    global mainOrdnerInput
    #sucht nach ordner zum räumen
    RäumendenFolder = filedialog.askdirectory(title="Ordner auswählen")
    mainOrdnerInput.insert(tk.END, RäumendenFolder)
def OpenNeueRäumvariantefenster():
	#erstellt fenster
	fenster = tk.Toplevel(root)
	fenster.geometry("500x200+800+400")
	fenster.title("Datei zu ordner zuordnung")
	fenster.configure(bg="#383838")
	fenster.protocol("WM_DELETE_WINDOW", lambda: None)
	fenster.resizable(False,False)
	fenster.focus_force()
	fenster.lift()

	#erstellt input box
	Inputframe = tk.Frame(fenster, bg="grey",highlightthickness=2)
	Inputframe.pack(pady=20)
	dateiformatInput = tk.Entry(Inputframe,width=30,bg="#383838",relief="flat",fg="grey",insertbackground="grey")
	dateiformatInput.pack()
	Inputframe.place(x=5,y=75)
	zweiterInputframe = tk.Frame(fenster, bg="grey",highlightthickness=2)
	zweiterInputframe.pack(pady=20)
	ordnerInput = tk.Entry(zweiterInputframe,width=30,bg="#383838",relief="flat",fg="grey",insertbackground="grey")
	ordnerInput.pack()
	zweiterInputframe.place(x=260,y=75)
	#BeispielTexte
	BeispielLabelDateiVormat = tk.Label(fenster, text="Dateivormat z.B.: .png",font=("Arial", 10, "bold"),fg="white", bg="#383838" )
	BeispielLabelDateiVormat.pack(pady=20)
	BeispielLabelDateiVormat.place(x = 5, y = 50)
	BeispielLabelOrdner = tk.Label(fenster, text="Ordner z.B.: Picures",font=("Arial", 10, "bold"),fg="white", bg="#383838" )
	BeispielLabelOrdner.pack(pady=20)
	BeispielLabelOrdner.place(x = 260, y = 50)


	zuText = tk.Label(fenster, text="zu",font=("Arial", 10, "bold"),fg="white", bg="#383838" )
	zuText.pack(pady=20)
	zuText.place(x = 215, y = 75)
	

	vorauswahlZiel = ""
	#sperrt fenster
	fenster.grab_set()
	def ordnerZielsuchen():
		#sucht ordner
		ordnerInput.insert(0,filedialog.askdirectory(title="Ordner auswählen"))
	def abgeschlossen():
		#überprüft das die inputs nicht leer sind
		if(ordnerInput.get() != "" and dateiformatInput.get() != ""):
			#registriert die inputs und schliest das fenster
			global listbox
			global listeArtSortieren
			listeArtSortieren.append([dateiformatInput.get(),ordnerInput.get()])
			listbox.insert(tk.END, dateiformatInput.get() + " zu " + ordnerInput.get())
			fenster.destroy()
	def abgebrochen():
		fenster.destroy()
	#abbrechen und bestätigen Buttons
	OkButton = tk.Button(fenster,text="OK", command=abgeschlossen,width=10,height=1,bg="#003bc2",fg="white", activebackground="#02319e",activeforeground="white",  padx=10, pady=5, relief = "flat",bd=0)
	OkButton.pack(pady=10)
	OkButton.place(x=405,y=165)
	AbbrechenButton = tk.Button(fenster,text="Abbrechen", command=abgebrochen,width=10,height=1,bg="#003bc2",fg="white", activebackground="#02319e",activeforeground="white",  padx=10, pady=5, relief = "flat",bd=0,)
	AbbrechenButton.pack(pady=10)
	AbbrechenButton.place(x=307,y=165)

	#ordner aussuchen Button
	dritterInputframe = tk.Frame(fenster, bg="grey",highlightthickness=2)
	dritterInputframe.pack(pady=20)
	suchenButton = tk.Button(dritterInputframe,text="...",bg="#383838",fg="white", activebackground="#383838",activeforeground="white",  padx=10, pady=5, relief = "flat",borderwidth=2,command=ordnerZielsuchen)
	suchenButton.pack()
	
	dritterInputframe.place(x=458,y=75,width=30,height=22.5)



   
def Räumen():

	global listeArtSortieren
	#nimmt jede datei aus der zu räumenden datei
	for datei in os.listdir(RäumendenFolder):
		#zerteilt die datei in format und name
		basics, endung = os.path.splitext(datei)
		#geht die konfiguration durch
		for i in range(len(listeArtSortieren)):
			#checkt ob die endung dem konfigurations datei format entspricht 
			if(endung == listeArtSortieren[i][0]):
				#nimmt den path
				dateiPath = os.path.join(RäumendenFolder, datei)
				#prozess falls die datei im zugehörigem ordner schon existiert
				counter = 1
				#nimmt die datei die existiert vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv 
				if os.path.exists(os.path.join(listeArtSortieren[i][1], datei)):
					#gibt der datei einen neuen namen
					os.rename(dateiPath, os.path.normpath(os.path.join(RäumendenFolder,basics+str(counter)+endung)))
					dateiPath = os.path.normpath(os.path.join(RäumendenFolder,basics+str(counter)+endung))
					
					counter += 1
				# verschiebt die datei
				shutil.move(dateiPath, listeArtSortieren[i][1])
dateiname = ""

def saveSettings():
	global listeArtSortieren
	global RäumendenFolder
	global dateiname
	global saveSettingsListbox
	#schaut ob die settings vollständig ist
	if(len(listeArtSortieren) != 0 and RäumendenFolder != ""):
		#gibt der einstellung einen namen abhängig von den existierenden dateien
		dateiname = "settings" + str(saveSettingsListbox.size())
		#schreibt eine .txt datei mit allen settings in den ordner der .py app 
		with open(dateiname + ".txt", "w") as f:
			for i in range(len(listeArtSortieren)):
				f.write(f"{i}" + "= \n" + listeArtSortieren[i][0] + "\n")
				f.write(listeArtSortieren[i][1] + "\n" )
			f.write('RäumendenFolder ist = \n' + RäumendenFolder + "\n")
		# fügt die neue konfiguration in die listbox
		saveSettingsListbox.insert(tk.END, dateiname)

#setzt wet auf null
saveSettingsListboxElement = None


def playSettings(event):
	#nimmt den inhalt von dem element der ausgewählt wurde
	selection = saveSettingsListbox.curselection()
	if selection:
		global saveSettingsListboxElement 
		#wenn ein element ausgewählt wurde kann man die buttons benutzen
		index = selection[0]
		saveSettingsListboxElement = saveSettingsListbox.get(index)
		SavedSettingsAktiviernButton.config(state=tk.NORMAL, bg="#003bc2", relief="flat")
		SavedSettingsUmbennenenButton.config(state=tk.NORMAL, bg="#003bc2", relief="flat")
		SavedSettingsLöschenButton.config(state=tk.NORMAL, bg="#003bc2", relief="flat")

	else:
		#wenn kein element ausgewählt wurde kann man die buttons nicht benutzen
		SavedSettingsAktiviernButton.config(state=tk.DISABLED, bg="grey")
		SavedSettingsUmbennenenButton.config(state=tk.DISABLED, bg="grey")
		SavedSettingsLöschenButton.config(state=tk.DISABLED, bg="grey")




def settingAktivieren(event):
	global listeArtSortieren
	global listbox
	global RäumendenFolder
	global mainOrdnerInput
	# leert die liste
	listbox.delete(0,tk.END)
	listeArtSortieren = []
	with open(event+".txt", "r") as f:
		zeilen = f.readlines()
	#macht das zeilen kein usnichtbares \n haben
	for i in range(len(zeilen)):
		zeilen[i] = zeilen[i].strip() 

	for i in range(len(zeilen)):
		#sucht nach muster 
		#^ = anfang der zeile
		# \d+ = eine oder mehrere ziffern
		# =  = das Gleichheitszeichen
		# $ = Ende der zeile
		if re.match(r"^\d+=$", zeilen[i]):
			#fügt die werte der liste hinzu
			listbox.insert(tk.END, zeilen[i+1] + " zu " + zeilen[i+2])
			listeArtSortieren.append([zeilen[i+1], zeilen[i+2]])


		elif zeilen[i] == "RäumendenFolder ist =":
			#fügt die werte dem input hinzu
			RäumendenFolder = zeilen[i+1]
			mainOrdnerInput.delete(0,tk.END)
			mainOrdnerInput.insert(tk.END, RäumendenFolder)


def settingLöschen(event):
	global saveSettingsListboxElement
	#löscht die datei
	os.remove(event+".txt")
	#sucht nach dem listboxItem
	for i in range(len(saveSettingsListbox.get(0,tk.END))):
		if saveSettingsListbox.get(i) == event:
			#löscht das listboxItem
			saveSettingsListbox.delete(i)
			listbox.selection_clear(0, tk.END)
			saveSettingsListboxElement = ""
			
	#setzt die Buttons zurück		
	SavedSettingsAktiviernButton.config(state=tk.DISABLED, bg="grey")
	SavedSettingsUmbennenenButton.config(state=tk.DISABLED, bg="grey")
	SavedSettingsLöschenButton.config(state=tk.DISABLED, bg="grey")


def settingUmbennenen(event):
	#erstellt Fenster
	WindowSettings = tk.Toplevel(root)
	WindowSettings.geometry("470x100+800+400")
	WindowSettings.title("Einstellung Umbennen")
	WindowSettings.configure(bg="#383838")
	WindowSettings.protocol("WM_DELETE_WINDOW", lambda: None)
	WindowSettings.resizable(False,False)
	WindowSettings.focus_force()
	WindowSettings.lift()




	UmbennenenZu = tk.Label(WindowSettings, text="Zu was wollen sie Ihre Einstellung Umbennen: ",font=("Arial", 9, "bold"),fg="white", bg="#383838")
	UmbennenenZu.pack(pady = 10)
	UmbennenenZu.place(x = 0, y = 25)
	#input für den neuen EinstellungsNamen
	Inputframe = tk.Frame(WindowSettings, bg="grey",highlightthickness=2)
	Inputframe.pack(pady=20)
	dateiformatInput = tk.Entry(Inputframe,width=31,bg="#383838",relief="flat",fg="grey",insertbackground="grey")
	dateiformatInput.pack()
	Inputframe.place(x=270,y=25)

	def DateiUmbennenen():
		#schaut das der Neue DateiName Nicht Leer ist
		if dateiformatInput.get() != "":
			
			#sucht nach der datei
			for datei in os.listdir(os.path.dirname(os.path.abspath(__file__))):
				basics, endung = os.path.splitext(datei)
				if(basics == event):
					#gibt der datei ein neuen namen
					os.rename(datei,dateiformatInput.get()+ ".txt")
			#sucht nach dem ListboxItem
			for i in range(len(saveSettingsListbox.get(0,tk.END))):
				if saveSettingsListbox.get(i) == event:
					#löscht das listboxItem
					saveSettingsListbox.delete(i)
					saveSettingsListbox.insert(i,dateiformatInput.get())
					listbox.selection_clear(0, tk.END)
					saveSettingsListboxElement = ""

		WindowSettings.destroy()
		#setzt die Buttons zurück		
		SavedSettingsAktiviernButton.config(state=tk.DISABLED, bg="grey")
		SavedSettingsUmbennenenButton.config(state=tk.DISABLED, bg="grey")
		SavedSettingsLöschenButton.config(state=tk.DISABLED, bg="grey")
	def abgebrochen():
		WindowSettings.destroy()

	#Ok und AbbrechenButton um das Fenster zu Schliesen
	OkButton = tk.Button(WindowSettings,text="OK", command=DateiUmbennenen ,width=10,height=1,bg="#003bc2",fg="white", activebackground="#02319e",activeforeground="white",  padx=10, pady=5, relief = "flat",bd=0)
	OkButton.pack(pady=10)
	OkButton.place(x=370,y=65)
	AbbrechenButton = tk.Button(WindowSettings,text="Abbrechen", command=abgebrochen,width=10,height=1,bg="#003bc2",fg="white", activebackground="#02319e",activeforeground="white",  padx=10, pady=5, relief = "flat",bd=0,)
	AbbrechenButton.pack(pady=10)
	AbbrechenButton.place(x=270,y=65)





	



#erstellt fenster
root = tk.Tk()
root.title("Bereinigungs App")
root.geometry("700x500")
root.configure(bg="#383838")
root.resizable(False,False)
#paar labels für die expirience des kunden
labelTitel = tk.Label(root, text="Die Reinigungs app ihres vertrauens", font=("Arial", 16, "bold"),  fg="white", bg="#383838")
labelTitel.pack(pady=20)
ordnerAussuchenTitle = tk.Label(root, text="welchen Ordner wollen sie den heute aufräumen",font=("Arial", 10, "bold"),fg="white", bg="#383838" )
ordnerAussuchenTitle.pack(pady=20)
ordnerAussuchenTitle.place(x = 30, y = 70)
auszuräumendesTitle = tk.Label(root, text="welche datei art sollen wir in welchen folder umräumen",font=("Arial", 10, "bold"),fg="white", bg="#383838" )
auszuräumendesTitle.pack(pady=20)
auszuräumendesTitle.place(x = 30, y = 150)

#alles mit datei zu räumen gui
vierterInputframe = tk.Frame(root, bg="grey",highlightthickness=2)
vierterInputframe.pack(pady=20)
mainSuchenButton = tk.Button(vierterInputframe,text="...",bg="#383838",fg="white", activebackground="#383838",activeforeground="white",  padx=10, pady=5, relief = "flat",borderwidth=2,command=ordner_aussuchen)
mainSuchenButton.pack()
	
vierterInputframe.place(x=225,y=100,width=30,height=22.5)
fünfterInputframe = tk.Frame(root, bg="grey",highlightthickness=2)
fünfterInputframe.pack(pady=20)
mainOrdnerInput = tk.Entry(fünfterInputframe,width=30,bg="#383838",relief="flat",fg="grey",insertbackground="grey")
mainOrdnerInput.pack()
fünfterInputframe.place(x=30,y=100)



#alle buttons für datei art zu ordner
buttonRäumen = tk.Button(root,text="Ordner Räumen",font=("Arial", 12),bg="#003bc2",fg="white", activebackground="#02319e",activeforeground="white",  padx=10, pady=5, relief = "flat",bd=0, command = Räumen)
buttonRäumen.pack(pady=10)
buttonRäumen.place(x=275,y=450)
buttonVerschiebungsarHinzufügen = tk.Button(root,text="datei zu ordner weg hinzufügen",font=("Arial", 12),bg="#003bc2",fg="white", activebackground="#02319e",activeforeground="white",  padx=10, pady=5, relief = "flat",bd=0, command = OpenNeueRäumvariantefenster)
buttonVerschiebungsarHinzufügen.pack(pady=10)
buttonVerschiebungsarHinzufügen.place(x=30,y=260)

#alles gui für save system
saveSettingsButton = tk.Button(root,text="Einstellung speichern",font=("Arial", 12),bg="#003bc2",fg="white", activebackground="#02319e",activeforeground="white",  padx=10, pady=5, relief = "flat",bd=0, command=saveSettings)
saveSettingsButton.pack(pady=10)
saveSettingsButton.place(x=450,y=130)
saveSettingsFrame = tk.Frame(root)
saveSettingsFrame.pack(padx=20, pady=20)
saveSettingsFrame.place(x=450,y=180)

saveSettingsScrollbar = tk.Scrollbar(saveSettingsFrame, orient=tk.VERTICAL)
saveSettingsScrollbar.pack(side=tk.RIGHT, fill=tk.Y)  

saveSettingsListbox = tk.Listbox(saveSettingsFrame,width=37,height=5,yscrollcommand=saveSettingsScrollbar.set,bg="#383838",fg="lightgrey",font=("Arial", 8),relief="flat",bd=0)
saveSettingsListbox.pack(side=tk.LEFT, fill=tk.BOTH) 

saveSettingsScrollbar.config(command=saveSettingsListbox.yview)


#aktiviert wenn button losgelassen wird
saveSettingsListbox.bind("<ButtonRelease-1>", playSettings)


#alle buttons für save Settings
SavedSettingsAktiviernButton = tk.Button(root, text="Aktivieren",font=("Arial", 12),bg="grey",fg="white", activebackground="#02319e",activeforeground="white", relief = "flat",bd=0,state = tk.DISABLED, command = lambda: settingAktivieren(saveSettingsListboxElement))
SavedSettingsAktiviernButton.pack(pady=20)
SavedSettingsAktiviernButton.place(x = 612, y = 275)
SavedSettingsUmbennenenButton = tk.Button(root, text="Umbennen",font=("Arial", 12),bg="grey",fg="white", activebackground="#02319e",activeforeground="white", relief = "flat",bd=0,state = tk.DISABLED,command = lambda: settingUmbennenen(saveSettingsListboxElement))
SavedSettingsUmbennenenButton.pack(pady=20)
SavedSettingsUmbennenenButton.place(x = 522.5, y = 275)
SavedSettingsLöschenButton = tk.Button(root, text="Löschen",font=("Arial", 12),bg="grey",fg="white", activebackground="#02319e",activeforeground="white", relief = "flat",bd=0,state = tk.DISABLED, command = lambda: settingLöschen(saveSettingsListboxElement))
SavedSettingsLöschenButton.pack(pady=20)
SavedSettingsLöschenButton.place(x = 450, y = 275)





#füllt am anfang die settings listbox mit allen settings
ordner = os.path.dirname(os.path.abspath(__file__))
alleDateien = os.listdir(ordner)	
txtDateien = [datei for datei in alleDateien if datei.endswith(".txt") and os.path.isfile(os.path.join(ordner, datei))]
for i in range(len(txtDateien)):
	saveSettingsListbox.insert(tk.END, os.path.splitext(txtDateien[i])[0])




#liste für datei art zu ordner zuweisung
frame = tk.Frame(root)
frame.pack(padx=20, pady=20)
frame.place(x=30,y=180)

scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)  

listbox = tk.Listbox(frame,width=37,height=5,yscrollcommand=scrollbar.set,bg="#383838",fg="lightgrey",font=("Arial", 8),relief="flat",bd=0)
listbox.pack(side=tk.LEFT, fill=tk.BOTH) 

scrollbar.config(command=listbox.yview)








root.mainloop()


