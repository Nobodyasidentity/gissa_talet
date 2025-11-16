try:
    from random import randint;M=0
    import os,sys,json
    if os.name=='nt':
        import ctypes
        kernel32=ctypes.windll.kernel32
        handle=kernel32.GetStdHandle(-11)
        mode=ctypes.c_ulong()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        mode.value |= 0x0004
        kernel32.SetConsoleMode(handle, mode)
    else:print('WARNING: this version is made for Windows, you might run into errors / wierd behaviures')
    def cls():os.system('cls' if os.name == 'nt' else 'clear');return''
    def get_base_path():return os.path.dirname(sys.executable) if getattr(sys,"frozen",False) else os.path.dirname(__file__)
    dir=get_base_path()
    class Storage:
        def __init__(self,directory=None):
            self.directory=directory or get_base_path()
            if not os.path.exists(self.directory):os.makedirs(self.directory)
        def _get_path(self, filename):return os.path.join(self.directory, filename)
        def save(self, filename, content: bytes):
            if isinstance(content, str):content=content.encode()
            content=bytes([b^0xAA for b in content])
            with open(self._get_path(filename),'wb') as f:f.write(content)
        def load(self,filename)->bytes:
            path=self._get_path(filename)
            if not os.path.exists(path):raise FileNotFoundError(f"No such file: {path}")
            with open(path,'rb') as f:content=f.read()
            content=bytes([b^0xAA for b in content])
            return content
        def delete(self, filename):
            path=self._get_path(filename)
            if os.path.exists(path):os.remove(path);return True
            return False
    savedata=Storage('savedata')
    save_name='default'
    try:high=json.loads(savedata.load(save_name+'.dat').decode())
    except:high={'e':2147483648,'m':2147483648,'h':2147483648}
    def inputInt(*s,sep=' ',Exit=None):
        while 1:
            r=input(sep.join(s)+'\033[36m')
            if r==Exit:print('\033[0m',end='');return 'exit'
            try:print('\033[0m',end='');return int(r)
            except ValueError:print(f'\033[33m"{r}" is not an integer!\033[0m')
    def Game(min=1,max=10,a=None,f=1,gm='c'):
        global high,savedata,save_name
        r,lowest,highest=randint(min,max),min,max
        while a!=r:
            a=inputInt(f'Guess a number \033[36m{min}\033[0m to \033[36m{max}\033[0m: 'if a==None else 'Try again: ',Exit='exit')
            if a=='exit':return 'exit'
            if a==r:
                if gm in high:
                    if high[gm]>f:high[gm]=f
                    savedata.save(save_name+'.dat',str(json.dumps(high)))
                input(f'\033[32mCorrect!! the number was "\033[36m{r}\033[32m"!\n\033[0mIt took you \033[36m{f}\033[0m attempt{"s"if f>1 else""} to figure that out!')
            else:
                if a>r:highest=a-1 if highest>a-1 else highest;print(cls()+f'Wrong! The number it smaller than "\033[36m{a}\033[0m" ({f"\033[36m{lowest}\033[0m - \033[36m{highest}\033[0m"if highest!=lowest else f"\033[36m{highest}\033[0m"})')
                else:lowest=a+1 if lowest<a+1 else lowest;print(cls()+f'Wrong! The number it higher than "\033[36m{a}\033[0m" ({f"\033[36m{lowest}\033[0m - \033[36m{highest}\033[0m"if highest!=lowest else f"\033[36m{highest}\033[0m"})')
            f+=1
            if f>=2147483648:print(f'Okay bro, how bad can someone be at a game? {f} attempts...');return'exit'
        return 0
    def Menu(o={'1':[1,10,'e'],'2':[1,100,'m'],'3':[1,1000,'h'],'easy':[1,10,'e'],'medium':[1,100,'m'],'hard':[1,1000,'h'],'e':[1,10,'e'],'m':[1,100,'m'],'h':[1,1000,'h'],'custom':['c'],'c':['c'],'4':['c'],'exit':['exit'],'reset':['reset'],'del':['reset'],'delete':['reset'],'chs':['chs'],'save':['chs'],'cd':['chs'],'commands':['cmd'],'cmd':['cmd'],'cmds':['cmd'],'command':['cmd']}):
        while 1:
            global high,savedata,save_name;a=input(cls()+'\033[0mPlaying on save: \033[32m'+save_name+'\n\033[4m\033[1m\033[31mGAME MODES\033[0m\033[31m:\n\033[33mEasy: \033[36m1\033[0m to \033[36m10'+(f' \033[0m(High: \033[36m{high["e"]}\033[0m)'if high['e']!=2147483648 else'')+'\n\033[33mMedium: \033[36m1\033[0m to \033[36m100'+(f' \033[0m(High: \033[36m{high["m"]}\033[0m)'if high['m']!=2147483648 else'')+'\n\033[33mHard: \033[36m1\033[0m to \033[36m1000'+(f' \033[0m(High: \033[36m{high["h"]}\033[0m)'if high['h']!=2147483648 else'')+'\n\033[33mCustom:\033[0m You decide!\n\033[31mDo "\033[36mcmd\033[31m" for command list.\n\033[32m>>> \033[36m').lower();print('\033[0m',end='')
            if a in o:
                if o[a][0]=='c':
                    tmin=inputInt(cls()+'Minimum: ',Exit='exit')
                    if tmin=='exit':return 0
                    while 1:
                        tmax=inputInt('Maximum: ',Exit='exit')
                        if tmax=='exit':return 0
                        elif tmax>=tmin:break
                        print(cls()+f"\033[32mMaximum\033[0m must be more than or equal to '\033[36m{tmin}\033[0m'")
                    cls();Game(tmin,tmax,gm='c')
                elif o[a][0]=='exit':return 2
                elif o[a][0]=='chs':
                    while 1:
                        a=input(cls()+f'Currently on: \033[32m{save_name}\n\033[0mSave name: ').lower()
                        if len(a)>0:break
                    save_name=str(a)
                    try:high=json.loads(savedata.load(save_name+'.dat').decode())
                    except:high={'e':2147483648,'m':2147483648,'h':2147483648}
                    return 0
                elif o[a][0]=='reset':
                    while 1:
                        a=input(cls()+'\033[31mARE YOU SURE YOU WANT TO DELETE YOUR SAVE FILE? (\033[33mY\033[31m / \033[33mN\033[31m):\033[0m ').lower()
                        if len(a)>0:
                            if a[0]=='y':high={'e':2147483648,'m':2147483648,'h':2147483648};savedata.delete(save_name+'.dat');return 0
                            elif a[0]=='n':return 0
                elif o[a][0]=='cmd':input('\033[31mCOMMANDS:\n\033[33m1 \033[36m/ \033[33me \033[36m/ \033[33measy\033[36m: \033[0mEasy mode\n\033[33m2 \033[36m/ \033[33mm \033[36m/ \033[33mmedium\033[36m: \033[0mMedium mode\n\033[33m3 \033[36m/ \033[33mh \033[36m/ \033[33mhard\033[36m: \033[0mHard mode\n\033[33m4 \033[36m/ \033[33mc \033[36m/ \033[33mcustom\033[36m: \033[0mCustom mode\n\033[33mexit\033[36m: \033[0mExit the game\n\033[33mdel \033[36m/ \033[33mdelete \033[36m/ \033[33mreset\033[36m: \033[0mReset highscores (and delete save file)\n\033[33mchs \033[36m/ \033[33mcd \033[36m/ \033[33msave\033[36m: \033[0mChange currently used save file\n\033[33mcmd \033[36m/ \033[33mcmds \033[36m/ \033[33mcommand \033[36m/ \033[33mcommands\033[36m: \033[0mSee command list\n\n\033[32mPress enter to return...');return 0
                else:cls();Game(o[a][0],o[a][1],gm=o[a][2])
                return 0
    while M==0:M=Menu()
except Exception as e:print(f'\033[31mError: {e}\033[0m');M=-1
input(f'\033[32mGame exited with code "\033[36m{M}\033[32m"\033[0m...')