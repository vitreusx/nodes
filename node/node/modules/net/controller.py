from .models import Group, Member, Node

class CRUDException(Exception):
    pass

class Controller:
    def __init__(self, db):
        self.db = db

    def fetch_group(self, group):
        return Group.query.filter_by(name = group).first()
    
    def fetch_group_safe(self, group):
        grp = self.fetch_group(group)
        if not grp:
            raise CRUDException('Group not present.')
        return grp
    
    def create(self, group):
        if self.fetch_group(group):
            raise CRUDException('Group already present.')
        
        grp = Group(name = group)
        self.db.session.add(grp)
        self.db.session.commit()
    
    def destroy(self, group):
        grp = self.fetch_group(group)
        if not grp:
            raise CRUDException('Group not present.')

        self.db.session.delete(grp)
        self.db.session.commit()
    
    def fetch_node(self, addr):
        return Node.query.filter_by(addr = addr)

    def fetch_mem(self, grp, addr):
        return grp.members.filter(Node.addr == addr).one()

    def add_member(self, group, whom_addr, whom_alias):
        grp = self.fetch_group_safe(group)
        mem = self.fetch_mem(grp, whom_addr)
        if mem:
            raise CRUDException('Member present.')
        
        node = self.fetch_node(whom_addr) \
            or Node(addr = whom_addr, \
                    alias = whom_alias)
        grp.members.append(node)
        self.db.session.commit()
    
    def remove_member(self, group, whom_addr):
        grp = self.fetch_group_safe(group)
        mem = self.fetch_mem(grp, whom_addr)
        if not mem:
            raise CRUDException('Member not present.')

        grp.members.delete(self.fetch_node(whom_addr))
        self.db.session.commit()
    
    def list_members(self, group):
        grp = self.fetch_group_safe(group)
        return [{'addr': mem.addr, 'alias': mem.alias} 
                for mem in grp.members]
    
    def dump_group(self, group):
        return { 'name': group, 'members': self.list_members(group) }
    
    def update(self, dump):
        grp = self.fetch_group_safe(dump['name'])
        grp.members = []
        for mem in dump['members']:        
            node = self.fetch_node(mem['addr']) \
                or Node(addr = mem['addr'], \
                        alias = mem['alias'])
            grp.members.add(node)
        self.db.session.commit()
