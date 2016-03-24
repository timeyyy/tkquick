#~ Copyright 2015 Timothy C Eichler (c) , All rights reserved.
#~ Restrictive license being used whereby the following apply.
#~ 1. Non-commercial use only
#~ 2. Cannot modify source-code for any purpose (cannot create derivative works)
#~ The full license can be viewed at the link below
#~ http://www.binpress.com/license/view/l/9dfa4dbfe85c336d16d1dd71a2e2cfb2

"""
Notes on Styles etc

Images need a reference saved in a variable somehwere or else they are
garbage collected, _load_imgs will load all pictures in the passed directory

This Script is using a custom theme, Plastik, which is loaded at the start

#-------TTk Style Basics ---------#
To customize you need to define styles,
Each Widget type has a different style
Configuring a style will change all widgets that have that style

If you need a new style than the default ones provided here you can
simple inherit from them and change what you want.

#-------TTk Advanced Stuff -------#
Defineing your own layouts

#------- What I've Done and why ------#

All Styles (regardless of widget) i.e TFrame, TEntry, TLabel,
Will mostly want to share same attributes. 

The usual cases will be a default setting for normal frames/fonts etc
And a special case for borders/headings etc

SOOO all styles recieve their settings from one variable based on application
i.e
NORMAL_COLOUR
style.configure(TFrame, background = NORMAL_COLOUR)
style.configure(TEntry, background = NORMAL_COLOUR)

BORDER_COLOUR
style.configure(Border.TFrame, bavkground = BORDER_COLOUR
style.configure(Border.TEntry, bavkground = BORDER_COLOUR

So all the that you have to do is change the attributes
NORMAL_COLOUR and BORDER_COLOUR and magic will happen

All you have to do is to use the styles defined here

Because we modifiy the widget default styles i.e TFrame, TEntry as defined
by ttk, then you don't have to explicitly set it, but for border and other derivitves
that you may choose to set. All you need to do is widget.config(style='styleName')

#--------- Tkquick Builder -------------#
Not all options are configured by a style, i.e padding
And in some cases styles are buggy or whatever. So when setting styles

i make a dictionary avalibe that contains all changes (not just style changes)
so cfg_frame = {'style':ass,'padx':10} # also borderwidth

Now you have a true default that will take all your default settings into account 
widget.config(**cfg_frame)

Problems with ttk Styles,
Mapping states seems to be buggy, i wanted to make a button change background
permanently, for somereason it wasnt changing the style image however the
image property of the button, overiding the text etc... argh

my soulution was to create an entirley new button without using maps... gay , this is ToggleButton


another problem was with entry widget, i removed the white in the gif so that the colour can be set with a mapping,
however we get a slight tiny bit of colour coming through now on the corners...
shit


#http://wiki.tcl.tk/37973   ##colouring examples
#http://stackoverflow.com/questions/17635905/ttk-entry-background-colour   for windows 7 /. 8!
#http://stackoverflow.com/questions/7893561/ttk-treeview-selected-color
#http://stackoverflow.com/questions/3295659/how-do-i-get-a-windows-border-like-this-in-tkinter
#http://stackoverflow.com/questions/5973371/setting-window-styles-with-tkinter-tcl
#https://mail.python.org/pipermail/tutor/2005-November/043006.html
#http://stackoverflow.com/questions/17860278/how-to-create-a-custom-gui-design-for-a-python-program


#----------TroubleShooting and Problems ---------#
Cannot add borderwidth to ttk.Frame, don't configure the option using a style use

another problem is some features arent avalibel in ttk, forinstance for ttk.Entry you cannot
change the cursor colour holy fuck.

FFS COULDNT GET MAP TO WORK WITH LABEL, only when the foreground was set to diabled wtf

----------------
themed image prombelsm... button background have to be set in the gif..

"""
import tkinter as tk
import tkinter.ttk as ttk
import sys
import os
import glob

try:
    from . import plastik_theme
except SystemError:
    import plastik_theme
#~ if os.name == 'posix':sys.path.append('/home/timeyyy/Desktop/pyttk-samples-0.1.7')
#~ if os.name == 'nt':sys.path.append('C:\Python33\pyttk-samples-0.1.7')
#~ sys.path.append('C:\Python33\tile-themes\plastik\plastik')
imgs = {}
def _load_imgs(imgdir):
    '''
    Invoked when you call loadstyle
    This function loads all images in the passed in folder, or defaults
    to cwd/img/preload
    So you can forgot about keeping a reference(otherwise garbage collected)
    '''
    imgdir = os.path.expanduser(imgdir)
    #~ print("imgdir ", imgdir)
    if not os.path.isdir(imgdir):
        raise Exception("%r is not a directory, can't load images for preload!!" % imgdir)
    for f in glob.glob("%s/*.gif" % imgdir):
        img = os.path.split(f)[1]
        name = img[:-4]
        imgs[name] = tk.PhotoImage(name, file=f, format="gif89")

def loadStyle(root, preload=None, plastik_folder=None):
    s = ttk.Style()
    if not preload:
        try:
            _load_imgs(os.path.join('img', 'preload'))
        except Exception:pass
    else:
        _load_imgs(preload)
    if not plastik_folder:
        # todo this code works now... but doesnt work when frozen! the location of the file is a bad
        folder = os.path.join(os.path.dirname(__file__), 'img', 'plastik')
        plastik_theme.install(folder)
    elif plastik_folder in s.theme_names():
        s.theme_use(plastik_folder)
    else:
        plastik_theme.install(plastik_folder)
    #~ s.theme_use('clam')
    #~ s.theme_use('alt')       #ASS, ok on windows
    #~ s.theme_use('default')   #ASS
    #~ s.theme_use('classic')
    #~ s.theme_use('vista')
    #~ s.theme_names()
    #~ return
    style = ttk.Style(root)
    ## Gui Window Main Defaults
    style.configure('TFrame', foreground=TIMS_fg, background=TIMS_bg, relief=TIMS_relief, cursor=TIMS_cursor)
    style.configure('TButton',foreground=TIMS_fgButton, background=TIMS_bgButton, relief=TIMS_relief, font=TIMS_font)
    style.configure('TLabel', foreground=TIMS_fg, background=TIMS_bg, relief=TIMS_relief, font=TIMS_font,borderwidth=TIMS_bd)
    style.configure('heading.TLabel',font=TIMS_heading)
    style.configure('headingS.TLabel',font=TIMS_headingS)
    style.configure('TRadiobutton', foreground=TIMS_fg, background=TIMS_bg, relief=TIMS_relief, font=TIMS_font)
    style.configure('TCheckbutton', foreground=TIMS_fg, background=TIMS_bg, relief=TIMS_relief, font=TIMS_font)
    style.configure('TEntry', foreground=TIMS_fg, background=TIMS_bg, relief=TIMS_relief, font=TIMS_font)

    #~ style.layout("TNotebook",
#~ [('Notebook.tab', {'sticky': 'nswe', 'children':
    #~ [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
        #~ [('Notebook.focus', {'side': 'top', 'sticky': 'nswe', 'children':
            #~ [('Notebook.label', {'side': 'top', 'sticky': ''})],
        #~ })],
    #~ })],
#~ })]
#~ )

    style.configure('TNotebook', foreground=TIMS_fg_heading, background=TIMS_bg, relief=TIMS_relief, font=TIMS_font, borderwidth=TIMS_bd, tabmargins=0, expand =0)
    style.configure('TNotebook.Tab', foreground=TIMS_fg_heading, background=TIMS_bg, relief=TIMS_relief, font=TIMS_heading, borderwidth=TIMS_bd, tabmargins=0, expand =0)
    style.configure('TNotebook.Padding', relief=TIMS_relief)
    style.configure('hidden.TNotebook',foreground=TIMS_fg_heading, background=TIMS_bg, relief=TIMS_relief, font=TIMS_font, borderwidth=TIMS_bd)
    style.layout('hidden.TNotebook.Tab', '')
    style.configure('hidden.TNotebook.tab',foreground=TIMS_fg_heading, background='green', relief=TIMS_relief, font=TIMS_font, borderwidth=TIMS_bd)
    style.configure('hyperlink.TLabel', foreground ='blue')
    style.configure('bold.TLabel', font=TIMS_fontB)
    style.configure('white.TLabel', background='snow', font=TIMS_font)
    style.map('white.TLabel',
                        borderwidth=[('focus', 1)], 
                        highlightthickness=[('focus', 10)],
                        highlightcolor=[('focus', 'green')],
                        highlightbackground=[('focus', 'green')],
                        highlightborder=[('focus', 20)],
                        #~ background=[('focus','snow')],
                        relief=[('focus','sunken')])
    style.configure('main.TButton', background=TIMS_bg)
    
    style.configure('test.TFrame', foreground=TIMS_fg, background=TEST, relief=TIMS_relief, cursor=TIMS_cursor)
    style.configure('test.TLabel', foreground=TIMS_fg, background=TEST, relief=TIMS_relief, font=TIMS_font,borderwidth=TIMS_bd)
    
    #mainwidg or book or pagetype
    style.configure('books.TFrame', relief=TIMS_relief2, background=TIMS_bg2, padding='0.5i')#TIMS_bg2)
    style.configure('books.TPanedwindow',background=TIMS_bg2)
    style.configure('Sash',sashthickness='5')
    style.configure('books.TEntry',padding=5,relief=TIMS_relief2,fieldbackground=TIMS_bg2,troughcolor=TIMS_bg2,background=TIMS_bg2,font=TIMS_font2,foreground=TIMS_fg2,borderwidth=TIMS_bd2)
    #~ style.configure('hs.books.TEntry',font=TIMS_font2,foreground=TIMS_fg2)
    #~ style.configure('books.TEntry.field',fieldbackground=TIMS_bg2)
    style.configure('books.TLabel', relief=TIMS_relief2, background=TIMS_bg2,font=TIMS_heading2,padding=TIMS_bd2)
    #~ style.map("books.TEntry.field",fieldbackground=[('!disabled', TIMS_fgA),('focus',TIMS_bg2)])
    
    style.map('plastikEntry', foreground=[('!disabled', 'black'),('disabled', 'grey')],
                        background=[('disabled', TIMS_bgD)])
                        
    style.map("books.TEntry",
                        foreground=[('!disabled', TIMS_fgA),('disabled', TIMS_fg2)],        # active meands !disabled
                        fieldbackground=[('!disabled', TIMS_bgA)],
                        background=[('!disabled', TIMS_bgA)],
                        highlightcolor=[('focus', 'green'),('!focus', 'red')],
                        relief= [('!disabled', TIMS_reliefA)],
                        borderwidth=[('!disabled', TIMS_bdA)])
    style.map("books.TLabel",background=[('!disabled', TIMS_bg2)])
    style.map("books.TPanedwindow",background=[('!disabled', TIMS_bgP)])
    
    #basewin Toolbar
    style.configure('basewinToolbar.TFrame',background=TIMS_bg4, relief=TIMS_relief4)
    style.configure('basewinToolbar.ToggleButton',background=TIMS_bg4, relief=TIMS_relief4)
    
    #~ style.configure('basewinToolbar.Button.button',image='test')
    #~ style.configure('test.TButton.button',
        #~ image='test',
        #~ background='green',
        #~ backgroundcolor='green',
        #~ SystemButtonFace='green',
        #~ fieldbackground='test',
        #~ foreground='blue',
        #~ highlightthickness='20',
        #~ font=('Helvetica', 18, 'bold'))
    #What i am trying do here is subclass, the original buztton, but its being gay and overwriting my
    # text as well for so i am creating a new button in plastik theme, and just mappiong to that... subclassing being gay fuck
    style.map('test.TButton',
        #~ foreground=[
                    #~ ('pressed', 'red'),
                    #~ ('alternate', 'pink')],
        image=[("alternate", 'tbutton-p'),
            ("pressed", 'test2'),
            ("active", 'button-h')])
            #~ {"border": [4, 10], "padding": 4, "sticky":"ewns"}])z
        #~ textarea=[("alternate", 'tbutton-p')],
        #~ text=[('alternate', 'pink'),
                    #~ ('pressed', '!focus', 'cyan'),
                    #~ ('active', 'green')])
        #~ highlightcolor=[('focus', 'green'),
                        #~ ('!focus', 'red')],
        #~ relief=[('pressed', 'groove'),
                #~ ('!pressed', 'ridge'),
                #~ ('alternate', 'sunken')])
    style.map('test.ToggleButton',
        foreground=[
                    ('pressed', 'red'),
                    ('alternate', 'pink')])#,
        #~ image=[("alternate", 'tbutton-p'),
            #~ ("pressed", 'test2'),
            #~ ("active", 'button-h')])
    return style
                    
TEST = 'red'    
    
### DEFAULTS
### GUI MENUS
TIMS_bg='grey93'#'grey93'
TIMS_fg='grey23'
TIMS_fg_heading='grey23'
TIMS_font='calibri 12 bold'
TIMS_fontB = ' '.join((TIMS_font,'bold'))
TIMS_heading='helvetica 11 bold'
TIMS_headingL='helvetica 13 bold'
TIMS_headingM='helvetica 11 bold'
TIMS_headingS='helvetica 9 bold'
TIMS_relief=tk.FLAT
TIMS_bd=0
TIMS_cursor='hand2'
TIMS_padx=0
TIMS_pady=0

TIMS_bgButton='grey97'  #Buttons
TIMS_fgButton=TIMS_fg

c_test={'style':'test.TFrame'}
c_label_test={'style':'test.TLabel'}

c_frame={'style':'TFrame'}
c_button={'style':'TButton'}
c_label={'style':'TLabel'}
c_labelB = {'style':'bold.TLabel'}
c_hyperlink={'style':'hyperlink.TLabel','cursor':'hand2'}
c_labelH={'style':'heading.TLabel'}
c_labelHS={'style':'headingS.TLabel'}   #normal, large medium small, 1 ,2 , 3 - size range
c_radio={'style':'TRadiobutton'}
c_check={'style':'TCheckbutton'}
c_wlabel={'style':'white.TLabel'}   #double check if this needs to be so..
c_entry={'style':'TEntry'}
c_pentry={'style':'plastikEntry'}
c_notebook={'style':'TNotebook'}
c_hiddenNotebook={'style':'hidden.TNotebook'}

TIMS_bgB='grey75'#'maroon4' #BORDER of normal window (made with guimaker)
master_cfg_defaults={'relief':TIMS_relief,'bd':TIMS_bd,'bg':TIMS_bgB}
cfg_frame_defaults={'padx':TIMS_padx,'pady':TIMS_pady}
cfg_guimaker_frame=dict(master_cfg_defaults, **cfg_frame_defaults)
                
TIMS_padxW=10       #OUTTER PROGRAM BORDER (for whole app not just sections made with guimaker)
TIMS_padyW=10
cfg_outter_frame_defaults={'padx':TIMS_padxW,'pady':TIMS_padyW,'bg':TIMS_bgB}   #w for window this is the outer border, 
cfg_outter_frame=dict(master_cfg_defaults, **cfg_outter_frame_defaults)
c_buttonMain={'style':'Toolbutton'} #(same colour button as background fore beldning) #old was main.button

#Random
c_optionMenuButton ={'bg':TIMS_bgButton,'fg':TIMS_fgButton} #option menu drop down style buttons, no ttk #TBD, DELETE THIS


#######################################
#Book display Behavior
#######################################
#~ TIMS_bg2='steelblue4'    
TIMS_bg2='gray3'    
TIMS_bd2=0
TIMS_fg2='white'
TIMS_heading2='helvetica 16'
TIMS_font2=('Arial', 12)
#~ TIMS_font2='georgia 9'
TIMS_relief2=tk.FLAT
TIM_padx2 = 10
TIM_pady2 = 10

TIMS_bgA='white'    #ACTIVE STATE, stats off disabled
TIMS_bgD='grey84'           #Disabled State
TIMS_fgA='black'
TIMS_reliefA='groove'
TIMS_bdA=1
TIMS_bgP='gold' #sash color
        

#~ c_book_button={'style':'TButton'}
#~ c_label={'style':'TLabel'}
#~ c_radio={'style':'TRadiobutton'}

master_cfg_defaults={'relief':TIMS_relief2,'bd':TIMS_bd2,'bg':TIMS_bg2}
master_grid_defaults={'sticky': 'w', 'padx':3,'pady':3}
master_pack_defaults={'fill':'both', 'expand':'yes'}
cfg_heading1={'columnspan':2,'ipady':3} #used through gui for a small heading,

cfg_packR = dict(master_pack_defaults, **{'side':'right'})
cfg_packL = dict(master_pack_defaults, **{'side':'left'})
cfg_packT = dict(master_pack_defaults, **{'side':'top'})
cfg_packB = dict(master_pack_defaults, **{'side':'bottom'})

#used in gui menus
cfg_gui_default={}
cfg_grid_default={}
cfg_gui = dict(master_cfg_defaults, **cfg_gui_default)
cfg_grid = dict(master_grid_defaults, **cfg_grid_default)

cfg_gridE= dict(master_grid_defaults, **{'sticky': 'e'})
cfg_gridW= dict(master_grid_defaults, **{'sticky': 'w'})
cfg_gridEW= dict(master_grid_defaults, **{'sticky': 'ew'})
cfg_gridA= dict(master_grid_defaults, **{'sticky': 'nsew'})
#~ TIMS_bg2='steelblue4'
#~ TIMS_fgtext='white'
#~ TIMS_font2='helvetica 22'
#~ TIMS_relief2=SUNKEN  
#Window sizes overal
wgdp_Height=400

##################################
# DEFAULT FOR ALL BOOK TYPES - THE MAIN WIDGET
##################################

cfg_books_defaults={'padx':TIM_padx2,'pady':TIM_pady2, 'bg':TIMS_bg2,'highlightthickness':0}                # no ttk.text widget must use old style method
cfg_books_mainwidg = dict(master_cfg_defaults, **cfg_books_defaults)
c_book_frame = {'style':'books.TFrame'} #for some reason padding not working in gui_maker so reverteing to old frame
c_mainwidg_label={'style':'books.TLabel'} #https://infohost.nmt.edu/tcc/help/pubs/tkinter/web/ttk-Frame.html

# used in pane gui maker
pane_pack_default={}
pane_pack = dict(master_pack_defaults, **pane_pack_default)
c_book_pane={'style':'books.TPanedwindow'}
c_book_entry={'style':'books.TEntry','font':TIMS_font2}         #bug with entry
c_book_entryHS={'style':'books.TEntry','font':TIMS_headingS}    #bug with entry
c_book_entryHM={'style':'books.TEntry','font':TIMS_headingM}    #bug with entry
c_book_label={'style':'books.TLabel'}
###########################
#BASEWINEDOW OUTERMOST FRAME 
###########################
TIMS_bg3='grey75'

cfg_frame_defaults={'padx':TIM_padx2,'pady':TIM_pady2, 'bg':TIMS_bg3}
cfg_basewin_frame=dict(master_cfg_defaults, **cfg_frame_defaults)

#####
# BASEWINDOW TOOLBARS 
#####
TIMS_bg4=TIMS_bg2
TIMS_relief4=tk.FLAT
c_toolBar_frame={'style':'basewinToolbar.TFrame'}
c_toolBar_button={'style':'basewinToolbar.ToggleButton','default':'normal'}
c_test_button={'style':'ToggleButton'}
c_test_button3={'style':'test.TButton'}
c_test_button2={'style':'test.Toolbutton'}

#~ c_test_button3={'style':'test.ToggleButton'}


class SimpleEntry(ttk.Entry):
    '''
    This Looks just liek a normal ttk Entry widget but it has a modified style
    so that you can change the background colour on windows z, only foreground
    and background options can be set,
    
    A frame has been packaged around it under a border attribute
    
    Not Themeinbg under windows 7 
    http://stackoverflow.com/questions/17635905/ttk-entry-background-colour,
    '''
    def __init__(self, parent,**kwargs):
        style = ttk.Style()
        self.border = ttk.Frame(parent, style='EntryBorder.TFrame')
        style.configure('EntryBorder.TFrame', background='black',relief='flat')
        style.layout("simple.TEntry", [('Entry.textarea', {'sticky': 'nswe'})])
        style.map("simple.TEntry", foreground=[('disabled', 'black'),('!disabled','white')],
                        background=[('disabled','white'),('!disabled','black')])         
        ttk.Entry.__init__(self, self.border,**kwargs)
        self.config(style='simple.TEntry')
        self.border.pack(fill='both',expand=1)
        
if __name__ == '__main__': 
    from tkinter import font
    #~ my = font.Font(family='Helvetica', size=12, weight='bold')

    s=ttk.Style()
    print(s.layout('TNotebook'))
    print(s.layout('TNotebook.Tab'))
    print(s.layout('TNotebook.Label'))
    
    #print(help(s))          http://www.tkdocs.com/tutorial/styles.html   http://www.tkdocs.com/tutorial/complex.html
    print(s.element_options('TNotebook.Tab'))
    print(s.element_options('TNotebook.label'))
    print(s.element_options('TNotebook.focus'))
    print(s.element_options('TNotebook.padding'))
#~ 
    #~ loadStyle(tk.Tk())
    #~ print(s.layout('TEntry'))
    #~ print()
    #~ print(s.element_options('TEntry.field'))
    #~ print(s.element_options('TEntry.textarea'))
    #~ print(s.element_options('TEntry.padding'))

    #~ print(s.layout('TButton'))
    #~ print()
    #~ print(s.element_options('TButton.focus'))
    #~ print(s.element_options('TButton.label'))
    #~ print(s.element_options('TButton.padding'))
    #~ print(s.element_options('TButton.field'))
    #~ print(s.element_options('TButton.textarea'))
    #~ print()
    #~ print(s.lookup('TButton','fieldbackground'))
    #~ print(s.lookup('TButton','background'))
    #~ print(s.lookup('TButton','image'))
    #~ 
    #~ print(s.layout('Button'))
    
    #~ print(s.layout('TLabel'))
    #~ print()
    #~ print(s.element_options('TLabel.border'))
    #~ print(s.element_options('TLabel.padding'))
    #~ print(s.element_options('TLabel.label'))
    
    #~ print(s.layout('Vertical.TScrollbar'))
    print()
    #~ print(s.element_options('TLabel.border'))
    #~ print(s.element_options('TLabel.padding'))
    #~ print(s.element_options('TLabel.label'))

    #~ print(s.layout('Sash'))
    #~ print()
    #~ print(s.element_options('TPanedwindow.background'))
    #~ print(s.element_options('TPanedwindow.padding'))
    #~ print(s.element_options('TPanedwindow.label'))
    #~ print(help(ttk.Panedwindow))
    #~ print(help(ttk.Frame))
    
    #~ print(help(ttk.Separator))
    #~ s.theme_use('clam')
    #~ print(s.theme_names())
    #~ a=ttk.Entry(t.Tk(),style='Entry')
    #~ print(a['style'])
    #~ 
    #~ def a():
        #~ a=1
        #~ def b():
            #~ nonlocal a
            #~ print(a)
            #~ a=2
            #~ 
        #~ 
        #~ 
        #~ b()
        #~ print(a)
        #~ 
    #~ a()
    
    #~ def outer():
        #~ a = 0
        #~ b = 1
#~ 
        #~ def inner():
            #~ print (a)
            #~ print (b)
            #~ b = 4
#~ 
        #~ inner()
#~ 
    #~ outer()
