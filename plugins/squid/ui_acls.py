from ajenti import apis
from ajenti.com import *
from ajenti.ui import *

class SquidACLs(Plugin):
    implements(apis.squid.IPluginPart)
    
    weight = 20
    title = 'ACLs'

    tab = 0
    cfg = 0
    parent = None
        
    def init(self, parent, cfg, tab):
        self.parent = parent
        self.cfg = cfg
        self.tab = tab
        parent._shuffling_acls = False

    def get_ui(self):
        t = UI.DataTable()
        t.appendChild(UI.DataTableRow(UI.Label(text='Type'), UI.Label(text='Parameters'), UI.Label(), header=True))
        for a in self.cfg.acls:
            t.appendChild(
                UI.DataTableRow(
                    UI.Label(text=a[0]), 
                    UI.Label(text=a[1]), 
                    UI.Label()
                )
              )
        frm = UI.FormBox(t, miscbtnid='shuffle_acls', miscbtn='Shuffle', id='frmACLs')
        vc = UI.VContainer(frm)
        
        if self.parent._shuffling_acls:
            vc.vnode(self.get_ui_acls_shuffler())
            
        return vc
      
    def get_ui_acls_shuffler(self):
        li = UI.SortList(id='list')
        for p in self.cfg.acls:
            s = ' '.join(p)
            li.appendChild(UI.SortListItem(UI.Label(text=s), id=s))
      
        return UI.DialogBox(li, title='Shuffle ACLs', id='dlgACLs')

    def on_click(self, event, params, vars=None):
        if params[0] == 'shuffle_acls':
            self.parent._tab = self.tab
            self.parent._shuffling_acls = True

    def on_submit(self, event, params, vars=None):
        if params[0] == 'dlgACLs':
            self.parent._tab = self.tab
            if vars.getvalue('action', '') == 'OK':
                l = vars.getvalue('list', '').split('|')
                self.cfg.acls = []
                for s in l:
                    n = s.split(' ')[0]
                    v = ' '.join(s.split(' ')[1:])
                    self.cfg.acls.append((n, v))
                self.cfg.save()
            self.parent._shuffling_acls = False

