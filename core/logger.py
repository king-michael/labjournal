import os # logfile

class Logger():
    def __init__(self,*args,**kwargs):
        self.defaults={
            "file_log" : "text.log",
            'file_debug' : 'debug.log',
            'DEBUG' : 5,
            'LOGMODE' : 'screen', # ['screen', 'file', 'both']
            'DEBUGMODE' : 'log', # ['log', 'own', 'both']
        }
        
        self.init_kwargs(**self.defaults) # set defaults
        self.init_kwargs(**kwargs) # set kwargs
        
        if os.environ.get('DEBUG') is not None: 
            if os.environ['DEBUG'] in [0, "0", "False", False]: self.DEBUG=0
            else:
                try: self.DEBUG=int(os.environ['DEBUG'])
                except: self.DEBUG=1
        self.assing_env('LOGMODE', ['screen', 'file', 'both'])
        self.assing_env('DEBUGMODE', ['log', 'own', 'both'])
        
    def assing_env(self,str_env,options=None):
        '''assing enviroment variables'''
        try:
            attr=os.environ[str_env]
            if options is None:
                setattr(self,'str_env',attr)
            else:
                if attr in options: 
                    self.LOGMODE=attr
                else:
                    self.write('Did not recognize env({})'.format(str_env),
                                '\n option({}) not in {}'.format(attr,options))
        except:
            pass
        
    def init_kwargs(self,**kwargs):
        '''set kwargs'''
        self.kwargs = kwargs
        for k,v in kwargs.iteritems(): setattr(self,k,v)
            
    def __call__(self,*args,**kwargs):
        '''log=logger(); log(bla) -> log.write(bla)'''
        self.write(*args,**kwargs)
        
    def write(self,*args,**kwargs):
        logfile = self.file_log if 'file_log' not in kwargs.keys() else kwargs['file_log'] 
        try:
            args="".join([i for i in args])
        except: pass
        if self.LOGMODE=='screen' or 'both':
            if type(args) == type(str()):
                print(args)
            else:
                pprint(args)
        if self.LOGMODE=='file' or 'both':
            with open(logfile, 'a') as fp:
                if type(args) == type(str()):
                    fp.write(args)
                else:
                    fp.write(pformat(args))
    
    def debug(self,*args,**kwargs):
        lvl = 1 if 'lvl' not in kwargs.keys() else kwargs['lvl'] 
        if self.DEBUG >= lvl:
            if self.DEBUGMODE in ['log', 'both']:
                self.write("DEBUG:) ",*args)
            if self.DEBUGMODE in ['own', 'both']:
                self.write("DEBUG:) ",*args, logfile=self.file_debug)

    def info(self,*args,**kwargs):
        if self.DEBUGMODE in ['log', 'both']:
            self.write("Info:) ", *args)
        if self.DEBUGMODE in ['own', 'both']:
            self.write("Info:) ", *args, logfile=self.file_debug)

if __name__ == '__main__':
    #%env LOGMODE=1
    #%env DEBUG=1
    os.environ['LOGMODE']=1
    os.environ['DEBUG']=2

    log=Logger()
    log("Test",1)
    log.debug("das")
    log.debug("das 1 ",lvl=1)
    log.debug("das 2 ",lvl=2)
    log.debug("das 3 ",lvl=3)