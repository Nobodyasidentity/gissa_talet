#!/usr/bin/env python3
MAXINT=9223372036854775807
VERSION='3.1.pre3'
from random import randint
from pathlib import Path
import json,os,sys,tempfile,pickle,atexit,signal,traceback,datetime,re
class _Log:
    ansi=re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~]|c)')
    def __init__(s,f):s.f=f
    def write(s,x):sys.__stdout__.write(x);s.f.write(_Log.ansi.sub('',x))
    def flush(s):sys.__stdout__.flush();s.f.flush()
_log=open(f"gissa_talet_latest_log.txt","w",encoding="utf-8")
_log.write(f'gissa_talet_latest_log.txt: {datetime.datetime.now():%Y/%m/%d %H:%M:%S}'+'\n\n')
sys.stdout=_Log(_log)
sys.excepthook=lambda t,v,tb:traceback.print_exception(t,v,tb)
def cls(*s):print("\033c",end="",flush=True);return''
class ansi:
    u033,n='\033','\n'
    def enable():
        try:import ctypes;ctypes.windll.kernel32.SetConsoleMode(ctypes.windll.kernel32.GetStdHandle(-11),7)
        except Exception:pass
    def c(s, code):return f"\033[{code}m{s}\033[0m"
    GREEN,CYAN,YELLOW,RED,BOLD,CLEAR,UNDERLINE=u033+'[32m',u033+'[36m',u033+'[33m',u033+'[31m',u033+'[1m',u033+'[0m',u033+'[4m'
    green,cyan,yellow,red,bold,underline=(lambda s='':ansi.c(str(s),"32")),(lambda s='':ansi.c(str(s),"36")),(lambda s='':ansi.c(str(s),"33")),(lambda s='':ansi.c(str(s),"31")),(lambda s='':ansi.c(str(s),"1")),(lambda s='':ansi.c(str(s),"4"))
def get_base_path():return os.path.dirname(sys.executable if getattr(sys,"frozen",0) else os.path.abspath(sys.argv[0]))
dir=get_base_path().replace('\\','/');print(f'Got "{dir}" as current path.')
read_line=(lambda:(__import__("msvcrt").getch().decode()if os.name=="nt"else __import__("sys").stdin.read(1)))
class storage:
    _key=0x55
    def __init__(s,n):
        b=os.path.dirname(sys.executable if getattr(sys,"frozen",0) else os.path.abspath(sys.argv[0]))
        s.p=os.path.join(b,n); os.makedirs(s.p,exist_ok=True)
    def _encode(s,b):return bytes([x^s._key for x in b])
    def save(s,f,d):
        with open(os.path.join(s.p,f),"wb") as file:file.write(s._encode(pickle.dumps(d, protocol=pickle.HIGHEST_PROTOCOL)))
    def load(s,f):
        with open(os.path.join(s.p,f),"rb") as file: return pickle.loads(s._encode(file.read()))
    def delete(s,f):p=os.path.join(s.p,f);os.path.exists(p) and os.remove(p)
    def exists(s,f):return os.path.exists(os.path.join(s.p,f))
    def list(s):return os.listdir(s.p)
ansi.enable()
def _Stfu(*s):
    global savedata
    while 1:
        _=oinput(cls()+'Current save file: '+ansi.green(savedata['name'])+'\n'+ansi.red('Are you sure you want to override the save file version?')+f' ( {ansi.cyan("Y")} / {ansi.cyan("N")} ): ').lower()
        if (_=='y')or(_=='yes'):break
        elif (_=='n')or(_=='no'):return
    savedata[0]['version']=VERSION
    savedata['pc'].save(savedata['name']+'.dat',savedata[0])
default_savedata_0={'version':VERSION,'highscores':{'easy':int(MAXINT),'medium':int(MAXINT),'hard':int(MAXINT)}}
def _Reset(*s):
    global savedata
    while 1:
        _=oinput(cls()+'Current save file: '+ansi.green(savedata['name'])+'\n'+ansi.red('Are you sure you want to delete your save file?')+f' ( {ansi.cyan("Y")} / {ansi.cyan("N")} ): ').lower()
        if (_=='y')or(_=='yes'):break
        elif (_=='n')or(_=='no'):return
    savedata[0]=dict(default_savedata_0)
    savedata['pc'].delete(savedata['name']+'.dat')
def _FIX_SAVEFILE(sf):
    try:
        if isinstance(sf,(bytes,bytearray)): sf=sf.decode()
        if isinstance(sf,str): sf=json.loads(sf)
        if isinstance(sf,dict) and set(sf)=={'e','m','h'}:
            _={'version':'unknown','highscores':{}}
            _['highscores']['easy']  = MAXINT if sf['e']==2147483648 else int(sf['e'])
            _['highscores']['medium']= MAXINT if sf['m']==2147483648 else int(sf['m'])
            _['highscores']['hard']  = MAXINT if sf['h']==2147483648 else int(sf['h'])
            return _
        if isinstance(sf,dict) and 'highscores'in sf:
            sf.setdefault('version','unknown')
            return sf
    except: pass
    _=dict(default_savedata_0); _['version']='unknown'
    return _
def _Cd(*s, sep=' '):
    global savedata
    savedata['name']=sep.join(str(i)for i in s)
    f=savedata['name']+'.dat'
    p=os.path.join(savedata['pc'].p,f)
    if not os.path.isfile(p) or not os.access(p,os.R_OK):
        _=dict(default_savedata_0);_['version']='unknown'
        savedata[0]=_;return
    try:savedata[0]=_FIX_SAVEFILE(savedata['pc'].load(f));return
    except:pass
    try:
        r=open(p,'rb').read()
        for k in (savedata['pc']._key,0xAA):
            try:
                d=bytes(b^k for b in r)
                try:savedata[0]=_FIX_SAVEFILE(pickle.loads(d));return
                except:
                    try:savedata[0]=_FIX_SAVEFILE(json.loads(d.decode()));return
                    except:pass
            except:pass
        raise Exception
    except:
        _=dict(default_savedata_0); _['version']='unknown'
        savedata[0]=dict(default_savedata_0); _['version']='unknown'
savedata={'pc':storage('savedata'),'name':'default','menu_options':{
    'exit':{'keywords':['exit'],'function':sys.exit,'cmd':'Exits the game'},
    'easy':{'keywords':['easy','e','1'],'function':(lambda*s:Gissa_talet(1,10,'easy')),'description':(ansi.yellow('Easy')+': '+ansi.cyan(1)+' to '+ansi.cyan(10)),'cmd':f'Game mode {ansi.red("->")} easy ( {ansi.cyan("1")} to {ansi.cyan("10")} )'},
    'medium':{'keywords':['medium','m','2'],'function':(lambda*s:Gissa_talet(1,100,'medium')),'description':(ansi.yellow('Medium')+': '+ansi.cyan(1)+' to '+ansi.cyan(100)),'cmd':f'Game mode {ansi.red("->")} medium ( {ansi.cyan("1")} to {ansi.cyan("100")} )'},
    'hard':{'keywords':['hard','h',3],'function':(lambda*s:Gissa_talet(1,1000,'hard')),'description':(ansi.yellow('Hard')+': '+ansi.cyan(1)+' to '+ansi.cyan(1000)),'cmd':f'Game mode {ansi.red("->")} medium ( {ansi.cyan("1")} to {ansi.cyan("1000")} )'},
    'custom':{'keywords':['custom','c','4'],'function':(lambda*s:Gissa_talet(oinput(ansi.CLEAR+'Minimum: '+ansi.CYAN,type=int,Error=ansi.yellow(f'"{ansi.cyan("{}")+ansi.YELLOW}" is not an integer.')),oinput(ansi.CLEAR+'Maximum: '+ansi.CYAN,type=int,Error=ansi.yellow(f'"{ansi.cyan("{}")+ansi.YELLOW}" is not an integer.')),'custom')),'description':(ansi.yellow('Custom')+': You decide!'),'cmd':f'Game mode {ansi.red("->")} custom ( you decide )'},
    'debug':{'keywords':['debug'],'function':(lambda*s:print(VERSION,MAXINT,dir,get_base_path(),__file__,savedata['pc'].list(),savedata)+read_line()),'cmd':'Info for nerds'},
    'reset':{'keywords':['del','delete','reset'],'function':_Reset,'cmd':' Deletes the save file and resets all saved data'},
    'cd':{'keywords':['chd','save','chs','cs','cd'],'function':(lambda*s:_Cd(oinput(cls()+f'Current save: {ansi.green(savedata["name"])}'+'\nExisting:\n'+ansi.yellow('\n'.join(str(f).removesuffix('.dat')for f in savedata['pc'].list()))+'\nSave name: '+ansi.GREEN))+cls()),'cmd':'Change the currently used save file'},
    'stfu':{'keywords':['stfu'],'cmd':'Force updates the save file version','function':_Stfu},
    }}
_Cd('default')
def oinput(*s,sep=' ',type=str,Error="'{}' is not valid",Exit=None,Exit_code=None):
    while 1:
        user_input=input(sep.join(str(i) for i in s))
        if user_input==Exit:return Exit_code
        try:return type(user_input)
        except (ValueError,TypeError):print(Error.format(user_input))
def onexit(*s):
    print('Game exited.')
    input('<<<')
atexit.register(onexit);signal.signal(signal.SIGINT,(lambda*s:0))
def Gissa_talet(minimum,maximum,gamemode='custom',ans=None,attempts=1):
    global savedata
    def _cls(*s):global savedata;print(f'{cls()}Gissa Talet ({ansi.yellow(gamemode)}) on {ansi.green(savedata['name'])}');return''
    _cls();rand,possible_max,possible_min=randint(minimum,maximum),int(maximum),int(minimum)
    while 1:
        ans=oinput(f'Guess a number {ansi.cyan(minimum)} to {ansi.cyan(maximum)}: {ansi.CYAN}'if ans==None else f'Try again: {ansi.CYAN}',type=int,Exit='exit',Error=ansi.yellow(f'"{ansi.cyan("{}")+ansi.YELLOW}" is not an integer.'));print(end=ansi.CLEAR)
        if ans==None:return
        if ans==rand:
            print(f"{ansi.green('Correct!')} The answer was '{ansi.cyan(rand)}'. It took you {ansi.cyan(attempts)} attempt{"s"if attempts!=1 else""}.")
            if gamemode in savedata[0]['highscores']:
                if savedata[0]['highscores'][gamemode]>attempts:
                    savedata[0]['highscores'][gamemode]=int(attempts);print(ansi.bold(ansi.green('That is a new highscore!')))
                    savedata['pc'].save(savedata['name']+'.dat',savedata[0])
            read_line();return
        else:
            if ans>rand:possible_max=ans-1 if possible_max>ans-1 else possible_max
            else:possible_min=ans+1 if possible_min<ans+1 else possible_min
            attempts+=1;print(f"{_cls()+ansi.red('Wrong!')} The number is {'higher'if ans<rand else 'smaller'} than '{ansi.cyan(ans)}'. ({ansi.cyan(possible_min)+' - '+ansi.cyan(possible_max)if possible_min!=possible_max else ansi.cyan(possible_max)})")
def init():
    global savedata
    while 1:
        print(cls()+(f'{ansi.RED}WARNING: SAVE FILE VERSION ({ansi.CYAN+savedata[0]['version']+ansi.RED}) DOES NOT MATCH GAME VERSION ({ansi.CYAN+VERSION+ansi.RED})'+ansi.CLEAR+'\n' if savedata[0]['version']!=VERSION else'')+f'Playing on save: {ansi.green(savedata["name"])+ansi.n+ansi.red(ansi.bold(ansi.underline("GAME MODES")))+ansi.red(":")}')
        for option in savedata['menu_options']:
            if 'description'in savedata['menu_options'][option]:
                print(savedata['menu_options'][option]['description'],((f"(Highscore: {ansi.cyan(savedata[0]['highscores'][option])} attempt{'s'if savedata[0]['highscores'][option]!=1 else""})"if savedata[0]['highscores'][option]!=MAXINT else'')if option in savedata[0]['highscores'] else''))
        
        ans=oinput(f"{ansi.RED}Do '{ansi.CYAN}cmd{ansi.RED}' for the command list{ansi.n}"+ansi.green('>>> ')+ansi.CYAN).lower();print(end=ansi.CLEAR,flush=True)
        if ans in ['cmd','commands','cmds']:
            print(f'{ansi.red(ansi.bold("COMMANDS")+":")}'+(f"{ansi.n+ansi.yellow('cmd')+ansi.CYAN} / {ansi.yellow('commands')+ansi.CYAN} / {ansi.yellow('cmds')+ansi.CYAN}:{ansi.CLEAR} Command list"))
            for option in savedata['menu_options']:
                if not'keywords'in savedata['menu_options'][option]:print(end=ansi.yellow(option)+ansi.cyan(': '),flush=True)
                elif len(savedata['menu_options'][option]['keywords'])==1:print(end=ansi.yellow(savedata['menu_options'][option]['keywords'][0])+ansi.cyan(': '),flush=True)
                elif len(savedata['menu_options'][option]['keywords'])==0:print(end=ansi.yellow(option)+ansi.cyan(': '),flush=True)
                else:
                    for kw in savedata['menu_options'][option]['keywords'][0:-1]:print(end=ansi.yellow(kw)+ansi.cyan(' / '))
                    print(end=ansi.yellow(savedata['menu_options'][option]['keywords'][-1])+ansi.cyan(': '))
                print(savedata['menu_options'][option]['cmd']if'cmd'in savedata['menu_options'][option]else ansi.bold('No description.'))
            print(ansi.green('Press any key to go back... '),end='',flush=True);read_line()
        for option in savedata['menu_options']:
            if 'keywords'in savedata['menu_options'][option]:
                if len(savedata['menu_options'][option]['keywords'])==0 and ans==option:return savedata['menu_options'][option]['function']()
                if ans in savedata['menu_options'][option]['keywords']:return savedata['menu_options'][option]['function']()
            elif ans==option:return savedata['menu_options'][option]['function']()

if __name__=='__main__':
    while 1:
        try:init()
        except(Exception,KeyboardInterrupt)as e:pass
