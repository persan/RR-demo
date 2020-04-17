"""This plugin provides so  convinient menues to RR, 
to do recored replay debugging see:
   https://rr-project.org/ 
for in-depth discusion.

"""


from gs_utils import hook, interactive
import GPS
import re
from os.path import *

unit = splitext(basename(__file__))[0]
port = GPS.Preference('Plugins/'+unit+'/port')

port.create('rr port',
            'integer',
            'Port used to comunicate with rr',
            12345)

rr = None


def enable_menues(enable):
    GPS.Menu.get('/Debug/rr/reverse-continue').set_sensitive(enable)
    GPS.Menu.get('/Debug/rr/reverse-finish').set_sensitive(enable)
    GPS.Menu.get('/Debug/rr/reverse-next').set_sensitive(enable)
    GPS.Menu.get('/Debug/rr/reverse-nexti').set_sensitive(enable)
    GPS.Menu.get('/Debug/rr/reverse-step').set_sensitive(enable)
    GPS.Menu.get('/Debug/rr/reverse-stepi').set_sensitive(enable)
    GPS.Menu.get('/Debug/rr/initialize replay').set_sensitive(not enable)


class Console_Process(GPS.Console, GPS.Process):
    def on_output(self, matched, unmatched):
        self.output = self.output + unmatched + matched
        self.write(unmatched + matched)
        self.evaluate(self.output)
        
    def evaluate(self, item):
        line = []
        matcher = re.compile("""Launch gdb with\s+gdb\s*(.+)""", re.M)
        matches = matcher.match(self.output)
        if not matches:
            return
        item = matches.group(1)
        l = ""
        instr = False
        for i in item:
            if i == "'":
                if instr:
                    instr = False
                else:
                    instr = True
            elif instr:
                l = l + i
            else:
                if i == ' ':
                    line.append(l)
                    l = ""
                else:
                    l = l + i
        if l:
            line.append(l)
        ix = 0
        post_commands = []
        while ix < len(line):
            element = line[ix]
            if element == "-l":
                ix = ix+2
            elif element == "-ex":
                cmd = line[ix+1]
                ix = ix+2
                post_commands.append(cmd)
            else:
                ix = ix+1
                file_to_load = element

        self.debugger = GPS.Debugger.spawn(executable=GPS.File(file_to_load))
        for cmd in post_commands:
            self.debugger.send(cmd)
        self.debugger.send("file %s" % file_to_load)
        self.debugger.send("-catch-exception")

    def on_exit(self, status, unmatched_output):
        global rr    
        rr = None
        enable_menues(False)

    def on_input(self, input):
        self.send(input)

    def on_destroy(self):
        self.kill()  # Will call on_exit

    def __init__(self, command):
        global rr
        if rr:
            GPS.Consle().write("On one replay at a time is allowed.\n") 
        self.debugger = None
        self.output = ""
        GPS.Console.__init__(self,
                             command[0],
                             on_input=Console_Process.on_input,
                             on_destroy=Console_Process.on_destroy,
                             force=False)
        self.clear()
        GPS.Process.__init__(self,
                             command, r"^.+$",
                             on_exit=Console_Process.on_exit,
                             on_match=Console_Process.on_output)
        rr = self
        enable_menues(True)


@interactive("Debug", menu="/Debug/rr/initialize replay")
def rr_replay():
    Console_Process(["rr", "replay", "-s", str(port.get())])


@interactive("Debug", menu="/Debug/rr/reverse-continue", key="control-F8")
def rr_reverse_continue(): 
    """Execute the progam in reverse until a break-/watch-point is reached"""
    rr.debugger.send("reverse-continue")    


@interactive("Debug", menu="/Debug/rr/reverse-finish", key="control-F7")
def rr_reverse_finish():
    """Execute the progam in reverse until entering another stackframe."""
    rr.debugger.send("reverse-finish")


@interactive("Debug", menu="/Debug/rr/reverse-next", key="control-F6")
def rr_reverse_next():
    """Execute the progam in reverse until the previous line in the """ +  \
        """current context is reached, dont step into subprograms."""
    rr.debugger.send("reverse-next")
    GPS.Console().write("reverse-next\n")


@interactive("Debug", menu="/Debug/rr/reverse-nexti", key="shift-control-F6")
def rr_reverse_nexti():
    """Execute the progam in reverse until the previous instruction in """ + \
        """the current context is reached."""
    rr.debugger.send("reverse-nexti")


@interactive("Debug", menu="/Debug/rr/reverse-step", key="control-F5")
def rr_reverse_step():
    """Execute the progam in reverse until the previous line is reached"""
    rr.debugger.get().send("reverse-step")


@interactive("Debug", menu="/Debug/rr/reverse-stepi", key="shift-control-F5")
def rr_reverse_stepi():
    """Execute the progam in reverse until the previous instruction""" + \
        """ is reached"""
    rr.debugger.get().send("reverse-stepi")

GPS.Preference("GPS6-Debugger-Debugger-Kind").set("Gdb")
enable_menues(False)
