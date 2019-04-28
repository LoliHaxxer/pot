#Process Open Tracker

from haxxer import sys, th, haxx, text
import os
import glob
import datetime
import time
import ast

pathogen = os.path.dirname(os.path.realpath(__file__))+"/POT"
export_files_extension = ".statisthicc"
if not os.path.exists(pathogen):open(pathogen,"w")
with open(pathogen,"r") as f:
	try:
		process_names = ast.literal_eval(f.readline()[:-1])
	except:
		process_names = []
	try:
		settings = ast.literal_eval(f.readline()[:-1])
		settings['partial']
		settings['caseInsensitive']
		settings['stdoutOnUpdate']
		settings['trackType']
		autorun_state = 1 if settings['autoRun']>=0 and settings['autoRun']<24 else 0
	except:
		settings = {
			"partial": True,
			"caseInsensitive": True,
			"stdoutOnUpdate": False,
			"trackType": 0,
			"autoRun": -1.
		}
		#trackType 0:ActiveWindow 1:OpenWindows 2:Processes
	#update_interval: interval of checking if the processes to track are still open
	try:
		update_interval = float(f.readline()[:-1])
	except ValueError:
		update_interval = 1.
	export_path = f.readline()[:-1]
	if not os.path.exists(export_path):
		export_path = os.getcwd()+"/"
	#loop_interval: interval of checking if another update interval is due
	try:
		loop_interval = float(f.readline()[:-1])
	except ValueError:
		loop_interval = 2.

def read_statisthicc_file(handle):
	r={}
	r["total"]=float(handle.readline()[:-1])
	r["content"]=ast.literal_eval(handle.readline()[:-1])
	return r
def stripname(full): return os.path.basename(full).replace(export_files_extension,"")
def pngen(): return "process name list("+str(len(process_names))+"): "+str(process_names)
def segen(): return "settings: "+str(settings)
def uigen(): return "update interval (s): "+str(update_interval)
def geta():
	r = {
		0: " - AW",
		1: " - OWs",
		2: " - Ps",
	}
	return r[settings["trackType"]]
def gettt():
	r = {
		0: "Now the active window is tracked",
		1: "Now the open windows are tracked",
		2: "Now the running processes are tracked",
	}
	return r[settings["trackType"]]
def listTo0Dict(list):
	r={}
	for l in list:r[l]=0
	return r
def write_stat(filename):
	with open(export_path+filename+export_files_extension,"w") as f:
		f.write(str(total)+"\n")
		f.write(str(statisthiccs)+"\n")
def write_vars():
	with open(pathogen,"w") as f:
		f.write(str(process_names)+"\n")
		f.write(str(settings)+"\n")
		f.write(str(update_interval)+"\n")
		f.write(str(export_path)+"\n")
		f.write(str(loop_interval)+"\n")
try:
	while 1:
		if autorun_state==1: inp='4'
		else: inp = input(pngen()+"\n"+uigen()+"\n"+segen()+"\n1: edit process name list\n2: settings\n3: set update interval\n4: run\n5: manage statistics\nq: exit\n")
		print()
		if inp == "1":
			while 1:
				print(pngen())
				inp = input("1: add\n2: index delete\n3: regex clear\n4: clear\nq: back\n")
				print()
				if inp=="1":
					while 1:
						print(pngen()+"\nstring: add new process name\nq: back")
						inp = input()
						if inp=="q":
							print()
							break
						if inp=="\\q":inp="q"
						if not inp in process_names:
							process_names.append(inp)
							print(inp+" was added to process name list")
						else:
							print(inp+" is already included")
						print()
				elif inp=="2":
					while 1:
						print(pngen()+"\n")
						for i in range(len(process_names)):
							print(str(i+1)+": "+process_names[i])
						print("q: exit\ninsert index of item to delete:")
						try:
							inp = input()
							if inp=="q":
								print()
								break
							print("you removed '" + process_names.pop(int(inp)-1) + "'")
						except ValueError:
							print("not an int, q to back")
						except IndexError:
							print("out of bounds")
						print()
				elif inp=="3":
					inp = input("regex of the purge\n")
					print()
					clear=[i for i in range(len(process_names)) if inp in process_names[i]]
					for c in clear: process_names.pop(c)
				elif inp=="4":
					process_names.clear()
				elif inp=="q":
					break
		elif inp == "2":
			while 1:
				inp = input(segen()+"\n1: toggle partial match\n2: toggle case sensitivity\n3: toggle print when updating during runtime\n4: enable tracking active window\n5: enable tracking open windows\n6: enable tracking running processes\n7: enable autorun\nq: back\n")
				if inp=="q":
					print()
					break
				if inp=="1":
					settings['partial'] = not settings['partial']
					print("the process names are now matched "+("" if settings['partial'] else "not ")+"partially")
				elif inp=="2":
					settings['caseInsensitive'] = not settings['caseInsensitive']
					print("the process names are now matched "+("case-insensitive"if settings['caseInsensitivity']else "case-sensitive"))
				elif inp=="3":
					settings['stdoutOnUpdate'] = not settings['stdoutOnUpdate']
					print("during runtime it is now " + ("" if settings['stdoutOnUpdate'] else "not ") + "printed whenever it updates")
				elif inp=="4":
					settings['trackType'] = 0
					print(gettt())
				elif inp=="5":
					settings['trackType'] = 1
					print(gettt())
				elif inp=="6":
					settings['trackType'] = 2
					print(gettt())
				elif inp=="7":
					while 1:
						inp=input("enter autorun stopping hour from 0 to 23.9:\n")
						try:
							settings['autoRun']=float(inp)
							print("autorun stopping hour set to "+str(settings['autoRun']))
							break
						except:
							print("didn't work xd\n")
				print()
		elif inp == "3":
			while 1:
				inp = input(uigen()+"\nfloat: new update interval in seconds\nq: back\n")
				print()
				if inp=="q":
					print()
					break
				try:
					update_interval = float(inp)
				except:
					print("not a float, try again")
				print()
		elif inp == "4":
			print("starting with\n"+pngen()+"\n"+uigen()+"\n"+segen())
			print("p to print temporary results, q to quit")
			from threading import Thread
			statisthiccs = listTo0Dict(process_names)
			abort = 0
			total = 0
			def loopdiloop():
				global total
				last = time.time()
				while not abort:
					time.sleep(loop_interval)
					now = time.time()
					elapsed = now - last
					if elapsed > update_interval:
						stdoutUpdate = settings['stdoutOnUpdate']
						if stdoutUpdate:
							print()
							print("updating")
						opened = set()
						tt = settings["trackType"]
						if tt==0:
							actives = sys.active_window(process_names,partial=settings['partial'],caseInsensitive=settings['caseInsensitive'])
							if stdoutUpdate:
								for name in actives: print(name+" is the active window")
							opened.update(actives)
						elif tt==1:
							opens = sys.open_windows(process_names,partial=settings['partial'],caseInsensitive=settings['caseInsensitive'])
							if stdoutUpdate:
								for name in opens: print(name+" is an open window")
							opened.update(opens)
						elif tt==2:
							running_processes = sys.processes_open(process_names,partial=settings['partial'],caseInsensitive=settings['caseInsensitive'])
							if stdoutUpdate:
								for name in running_processes: print(name+" is running")
							opened.update(running_processes)
						total+=elapsed
						for opn in opened: statisthiccs[opn]+=elapsed
						last=now
			thr = Thread(target=loopdiloop)
			thr.start()
			if autorun_state==1:
				now=datetime.datetime.now()
				autorunstop=datetime.datetime(now.year,now.month,now.day,int(settings['autoRun']),int(settings['autoRun']%1*60))
				if now>autorunstop: autorunstop += datetime.timedelta(days=1)
				def autorun():
					global abort
					while 1:
						t = datetime.datetime.now()
						if t > autorunstop:
							abort = 1
							break
						time.sleep((autorunstop-t).seconds)
					th.wait(lambda: thr.isAlive())
					filename = (inp if inp else str(datetime.datetime.now()).replace(":",""))
					write_stat(str(datetime.datetime.now()).replace(":","")+geta())
				settings['autoRun']=-1
				write_vars()
				thrr = Thread(target=autorun)
				thrr.daemon = True
				thrr.start()
				th.wait(lambda: thrr.isAlive())
				exit(0)
			while 1:
				inp = input()
				if inp == "q":
					abort = 1
					th.wait(lambda: thr.isAlive())
					break
				elif inp == "p":
					print("total: "+str(total))
					print(str(statisthiccs))
			print("total: "+str(total))
			inp = input("\nname: seconds\n" + str(statisthiccs)+"\nexport file path: "+export_path+"\ninsert an export file name:\n")
			if inp!="?q":
				filename = (inp if inp else str(datetime.datetime.now()).replace(":",""))+geta()
				write_stat(filename)
				print("file was saved to "+filepath)
			else:
				print("file was not saved!!!!!!!")
			print()
		elif inp == "5":
			while 1:
				globglob = glob.glob(export_path + "*" + export_files_extension)
				names = [stripname(i) for i in globglob]
				print("file path is '"+export_path+"'")
				for i in range(len(names)):
					print(str(i+1)+": "+names[i])
				print("w: edit file path\nq: back to main menu")
				inp = input("insert index of statisthicc file to view:\n")
				if inp=="q":
					print()
					break
				elif inp=="w":
					inp=input("insert new file path:\n")
					if os.path.exists(inp):
						lc = inp[-1:]
						export_path = inp if lc=="/" or lc=="\"" else inp+"/"
						print("file path was set to "+export_path)
					else:
						print(inp+" is not a pathial existence")
					print()
				else:
					try:
						inp = int(inp)
						selected_file_index = inp-1
					except:
						print("what you did was illegal and against the law\n\n")
					else:
						print()
						f_name = globglob[selected_file_index]
						short_f_name = names[selected_file_index]
						while 1:
							print("file: "+short_f_name)
							print("-------"+"-"*len(short_f_name))
							with open(f_name) as f:
								content_dict = read_statisthicc_file(f)
								print("total time in seconds: "+str(content_dict['total'])+"\n")
								print("process name : seconds")
								for n,t, in content_dict['content'].items():
									print(str(n)+" : "+str(t))
							print("----"+"-"*len(str(n))+"-"*len(str(t)))
							inp = input("1: delete\n2: merge with other statisthicc files\nq: back to file selection menu\n")
							if inp=="q":
								print()
								break
							elif inp=="1":
								try:
									os.remove(f_name)
									print(f_name+" was successfully eradicated from existence")
								except FileNotFoundError:
									print(f_name+" is already dead")
								print()
								break
							elif inp=="2":
								print()
								globglob_left = globglob.copy()
								merge = []
								globglob_left.remove(f_name)
								while 1:
									print("merge the files: "+str([stripname(i)for i in merge])+" into "+short_f_name)
									for i in range(len(globglob_left)):
										print(str(i + 1) + ": " + stripname(globglob_left[i]))
									print("w: merge\nq: back to file view")
									inp = input("insert index of statisthicc file to merge:\n")
									if inp=="q":
										print()
										break
									elif inp=="w":
										with open(f_name) as f:
											content_dict = read_statisthicc_file(f)
										for i in merge:
											with open(i) as f:
												haxx.dict_add_val(content_dict,read_statisthicc_file(f))
										print(content_dict)
										with open(f_name,"w") as f:
											f.write(str(content_dict['total'])+"\n")
											f.write(str(content_dict['content'])+"\n")
										print("successfully merged the files "+str([stripname(i)for i in merge])+" into "+short_f_name)
										print("path to the merged file: "+f_name)
										for i in merge:
											os.remove(i)
											print("removed "+i)
										print("done\n")
										break
									else:
										try:
											inp = int(inp)
											merge.append(globglob_left.pop(inp-1))
										except ValueError:
											print("that was not a number")
										except IndexError:
											print("index out of bounds")
									print()


		elif inp == "q":
			break
		else:
			print("unknown command\n")
finally:
	write_vars()