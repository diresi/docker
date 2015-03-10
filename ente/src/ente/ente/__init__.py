# Copyright (C) 2006-2014 VisoTech Softwareentwicklungsges.m.b.H.
#
# This file is part of ENTE, an in-memory graph database.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""simple access to several ente functions plus some convenience functions.
"""
import re
import functools
import types
import sys

import visotech
import bound_nb
nb = bound_nb.nb

# Vars for Up and Down
DOWN = nb.DOWN
UP = nb.UP

################################################################################
# util

def normalize_leg(leg):
    """Expands a single edge specification to a list of edges

    Possible leg parameter configurations

    :param leg: The legs, consisting of direction, number of steps, and possible edges
    :type  leg: tuple(number,int)|tuple(number,int,int)|tuple(number,int,str|list)|tuple(number,int,int,str|list)

    Examples:
    direction, num_walks
    direction, num_walks, edges
    direction, min_walks, max_walks, edges
    edges may be either a string or a list of strings
    """
    le = len(leg)
    if le == 2:
        return (leg[0], leg[1], leg[1])
    elif le == 3:
        if not isinstance(leg[2], int):
            return (leg[0], leg[1], leg[1], leg[2] if isinstance(leg[2], list) else [leg[2]])
        else:
            return (leg[0], leg[1], leg[2])
    elif le == 4:
        return (leg[0], leg[1], leg[2], leg[3] if isinstance(leg[3], list) else [leg[3]])
    raise IndexError("normalize_leg has wrong parameter: %r " % leg)


def normalize_legs(legs):
    """This utility function must be used before an itinerary is handed off to PyENTE
    """
    if isinstance(legs, list):
        return map(normalize_leg, legs)
    else:
        return [normalize_leg(legs)]

def fast_walk(id, walk, filter_expr = None, visit_expr = None):
    """ take id or [id] as first param, walk like PyNQL, filter is a function
    """
    legs = normalize_legs(walk)
    if not isinstance(id, list):
        id = [id]
    res = []
    for i in id:
        res.extend([r[0] for r in nb.walk(i, legs, filter_expr, visit_expr)])
    return res

def fwf(nt=None, name=None, info=None):
    is_nt = re.compile(nt).match if nt else None
    is_name = re.compile(name).match if name else None
    is_info = re.compile(info).match if info else None
    def fw_match(nid, fd):
        return bool((not is_nt or is_nt(fd.nodetypestring)) and (not is_name or is_name(fd.name)) and (not is_info or is_info(fd.info)))
    return fw_match

def e_version():
    return getattr(nb, "version", (1, 2))

################################################################################
# tx encapsulation
class aborting(object):
    def __init__(self, tx):
        self.tx = tx
    def __enter__(self):
        return self.tx
    def __exit__(self, *exc_info):
        self.tx.abort()

class committing(object):
    def __init__(self, tx):
        self.tx = tx
    def __enter__(self):
        return self.tx
    def __exit__(self, type, value, traceback):
        if type is None:
            self.tx.commit()
        else:
            self.tx.abort()

class implicit_tx(object):
    def __init__(self, nb, branch_id):
        self.nb = nb
        self.branch_id = branch_id
    def __enter__(self):
        self._old_tx = self.nb.get_implicit_tx()
        new_tx = nb.begin(self.branch_id)
        self.nb.set_implicit_tx(new_tx)
        return new_tx
    def __exit__(self, *exc_info):
        self.nb.set_implicit_tx(self._old_tx)

def encapsulate_call(nb, call):
    def call_with_tx(nb, call, par, kw):
        old_tx = nb.get_implicit_tx()
        if old_tx:
            try:
                old_branch = old_tx.get_branch_id()
            except (AttributeError, RuntimeError), e:
                old_branch = 0
        else:
            old_branch = 0
        try:
            tx = nb.begin(old_branch)
            nb.set_implicit_tx(tx)
            try:
                r = call(*par, **kw)
                tx.commit()
                return r
            except:
                __, e, tb = sys.exc_info()
                try:
                    tx.abort()
                except:
                    pass
                raise e, None, tb
        finally:
            nb.set_implicit_tx(old_tx)
    return lambda *a, **kw: call_with_tx(nb, call, a, kw)

def encapsulate_abortable_call(nb, call):
    def call_with_tx(nb, call, par, kw):
        old_tx = nb.get_implicit_tx()
        try:
            old_branch = old_tx.get_branch_id()
        except (RuntimeError, AttributeError):
            old_branch = 0
        with implicit_tx(nb, old_branch) as tx:
            with aborting(tx):
                return call(*par, **kw)
    return lambda *a, **kw: call_with_tx(nb, call, a, kw)

def tx_encaps(f):
    return encapsulate_call(nb, f)

def tx_abort_encaps(f):
    return encapsulate_abortable_call(nb, f)

def tx_encaps_if_necessary(f):
    @functools.wraps(f)
    def wrapper(*a, **kw):
        tx = nb.get_implicit_tx()
        func = f if (tx and tx.is_active()) else tx_encaps(f)
        return func(*a, **kw)
    return wrapper

def tx_encaps_in_branch(branch_id = None, commit = True, force_new_tx = True):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*a, **kw):
            otx = nb.get_implicit_tx()
            if not force_new_tx and otx and otx.is_active() and otx.get_branch_id() == branch_id:
                # no need to start a new transaction
                return f(*a, **kw)
            try:
                tx = nb.begin() if branch_id is None else nb.begin(branch_id)
                nb.set_implicit_tx(tx)
                res = f(*a, **kw)
                if commit:
                    tx.commit()
                else:
                    tx.abort()
                return res
            finally:
                nb.set_implicit_tx(otx)
        return wrapper
    return decorator

def run_in_trunk(f):
    return tx_encaps_in_branch(branch_id = 0, force_new_tx = False)(f)

################################################################################
# tx hooks
class Hooker(object):
    def __init__(self):
        self.hooks = []

    def hook(self, tx):
        for func, data in self.hooks:
            func(tx, data)

    def add(self, hook, data):
        self.hooks.append((hook, data))

def tx_register_hook(tx, hook_func, data):
    """Adds a hook callback to the list of registered hooks. It will
       receive 'data' as its second argument, the first being the
       transaction.
       There is no duplicate checking. Every function will be invoked
       the exact number of times it was registered.
    """
    h = tx.get_precommit_hook()
    if h is None:
        hooker = Hooker()
        tx.set_precommit_hook(hooker.hook)
    else:
        assert type(h) is types.MethodType
        assert h.im_func is Hooker.hook.im_func
        hooker = h.im_self
    hooker.add(hook_func, data)

def tx_get_hooks(tx):
    """Returns a list [(hook_func, data), ...].
       Don't change the list!
    """
    h = tx.get_precommit_hook()
    if h is None:
        return []
    assert type(h) is types.MethodType
    assert h.im_func is Hooker.hook.im_func
    return h.im_self.hooks

################################################################################
# ente shortcuts:
def e_nid(x):
    """Returns the .id attribute of 'x' or, if no such attribute exists just 'x'.
       This is useful to normalize the access to PyNQL(Dummy)Nodes and node ids.
    """
    nid = getattr(x, "id", x)
    return (nid or 0)

def e_node_exists(x):
    """ Returns True if x (or x.id) refers to an existing node, False otherwise.
    """
    return nb.node_exists(e_nid(x))

def e_xnid(x):
    """Returns the node id of x, if such a node exists, None otherwise.
    """
    return e_nid(x) if e_node_exists(x) else None

def e_nids(xs):
    """Returns a list of existing node ids. 'xs' can be a single element or an
       iterable.
       Useful to normalize inputs to fast_walk.
    """
    try:
        it = iter(xs)
    except TypeError:
        it = iter([xs])
    return [e_nid(x) for x in it if e_node_exists(x)]

def e_node(x):
    """ Returns the ENTE Node for x if such a node exists, None otherwise.
    """
    nid = e_nid(x)
    if e_node_exists(nid):
        return nb.node_from_id(nid)
    return None

def e_sub_node(nid, name):
    return e_xnid(nb.get_subnode(e_node(nid), name))

def legacy_e_val(nid, name = None):
    """ Returns the value of NVAL 'name', similar to E.node(nid).NAME, or the
    node.data if 'name' is None.
    """
    # E.nb.get_value() seems slightly faster than E.nb.get_subnode()
    n = nb.node_from_id(nid)
    if name is not None:
        n = nb.get_value(n, name)
    return n.data

def e_set_val(nid, val, name = None):
    """ Sets the value of NVAL 'name', similar to E.node(nid).NAME = val, or
    node.data = val if 'name' is None.
    """
    # E.nb.get_value() seems slightly faster than E.nb.get_subnode()
    n = nb.node_from_id(nid)
    if name is not None:
        n = nb.get_value(n, name)
    n.data = val
    nb.update_node(n)

def e_name(x):
    """ Returns the node.name for x if such a node exists, None otherwise.
    """
    return getattr(e_node(x), "name", None)

def e_info(x):
    """ Returns the node.info for x if such a node exists, None otherwise.
    """
    return getattr(e_node(x), "info", None)

def e_nt(x):
    """ Returns the node.nodetypestring for x if such a node exists, None otherwise.
    """
    n = e_node(x)
    if n:
        return e_node(n.type_id).name
    return None

def e_nti(x):
    """ Returns the node.info of the node template of x if such a node exists, None otherwise.
        Useful to format messages containing a human readable nodetype description.
    """
    n = e_node(x)
    if n:
        return e_node(n.type_id).info
    return None

def e_link_nodes(parents, childs, et, before=None, after=None, ignore_duplicate_links=False):
    """ Links all 'parents' with all 'childs' via 'et'.
        'parents' and 'childs' are normalized via e_nids(), thus can be single items or iterables,
        node ids and/or node objects.
        'before' and 'after' are mutually exclusive and can be used to set a reference node before/after
        the new links shall be inserted. These references are again normalized via e_nids() and are
        evaluated for each parent, only valid child nodes to each parent are evaluated.
        If 'ignore_duplicate_links' is True, the function checks whether some of the 'childs' are already
        linked from a parent via 'et' and ignores these nodes.
    """
    assert not (before and after), "e_link_nodes: before and after are mutually exclusive"

    parents = e_nids(parents)
    childs  = e_nids(childs)
    for p in parents:
        # if we are told to ignore duplicate links we build a list of current child nodes
        existing_links = set(fast_walk(p, (DOWN, 1, et))) if ignore_duplicate_links else set()

        # see whether we want to insert the childs midst of the other child nodes
        pkids_after = []
        if before or after:
            pkids = fast_walk(p, (DOWN, 1, et))
            pii = dict([(pk, i) for i, pk in enumerate(pkids)])
            # find the insertion index
            commons = set(pkids) & set(e_nids(before or after))
            iindex = None
            if before:
                # find the first child node also in before
                iindex = min([pii[c] for c in commons]) if commons else None
            elif after:
                # find the last child node also in after
                iindex = max([pii[c] for c in commons]) + 1 if commons else None
            if iindex is not None:
                pkids_after = pkids[iindex:]

        # unlink kids that should follow the new nodes:
        e_unlink_nodes(p, pkids_after, et)
        # and link them all again, in different order
        for n in [c for c in childs if c not in existing_links] + pkids_after:
            nb.link_nodes(p, n, et)

def e_unlink_nodes(parents, childs, et = None):
    """Unlinks all 'childs' from all 'parents' using edge 'et', or all edges if
    'et' is left None.
    Both 'parents' and 'childs' are normalized via e_nids().
    """
    parents = e_nids(parents)
    childs  = e_nids(childs)
    for p in parents:
        for c in childs:
            nb.unlink_nodes(p, c, et)

e_create_kw = set(["info", "name", "value", "tx_info", "tx_data"])
def e_create_node(nt, p=None, et=None, temp=False, empty=False, **kw):
    """creates a new node of type 'nt'
       if 'p' is given, it specifies the parent node
       if 'et' is given, it specifies the edge type to link 'p' -> new node,
               if not given, 'H' is used.
       if 'temp' is True, a temporary node is created.
       if 'empty' is True, no child nodes are created.
       about 'kw':
           if 'info' is in kw, the node info is set
           if 'name' is in kw, the node name is set
           if 'value' is in kw, the node value is set
    """
    nid = nb.create_node(nt, temp, empty)
    if p:
        if et is None:
            et = "H"
        e_link_nodes(p, nid, et)

    if kw:
        kw = dict(kw)
        n = e_node(nid)
        if "info" in kw:
            n.info = kw.pop("info")
        if "name" in kw:
            n.name = kw.pop("name")
        if "value" in kw:
            n.data = kw.pop("value")
        nb.update_node(n)

        # set node translation
        if "tx_info" in kw or "tx_data" in kw:
            tx_info, tx_data = nb.get_node_translation(nid)
            if "tx_info" in kw:
                tx_info = kw.pop("tx_info")
            if "tx_data" in kw:
                tx_data = kw.pop("tx_data")
            nb.set_node_translation(nid, tx_info, tx_data)

        assert not kw, "invalid paramters: %s" % (kw.keys(),)
    return nid

def e_set_translation(nid, tx_info = None, tx_data = None):
    for nid in e_nids(nid):
        cur_tx_data = nb.get_node_translation(nid)
        new_tx_data = (cur_tx_data[0] if tx_info is None else tx_info,
                       cur_tx_data[1] if tx_data is None else tx_data)
        nb.set_node_translation(nid, *new_tx_data)

def e_set_info(nid, info, tx_info = False):
    n = e_node(nid)
    n.info = info
    nb.update_node(n)
    e_set_translation(nid, tx_info = tx_info)

def e_copy_nodes(nodes, temp=False):
    """copies the given node ids, optional making temporary nodes
    """
    nids = []
    for nid in e_nids(nodes):
        nids.append(nb.copy_node(nid, temp))
    return nids

def e_delete_nodes(nodes):
    """Deletes all 'nodes'.
    """
    # traverese and check each node separately since we don't know
    # the node structure (we use e_nids() to listify 'nodes')
    for n in e_nids(nodes):
        if e_node_exists(n):
            nb.delete_node(e_nid(n))

################################################################################
# walking around

def e_walk(nids, *a, **kw):
    return fast_walk(e_nids(nids), *a, **kw)

NOYIELD = 0
YIELD = 1
def e_find(specs, root = None, dt_quirks = False):
    """
    Further description in FB cases (excerpt) 25196, 26550, 27870

    :param specs:
    lines = nb.find(pid, specs, dt_quirks)
    specs := [spec]
    spec  := (itin, match, flags)
    itin  := [leg]
    leg   := (nts, ets, name)  # None -> alles
    match := (val1, val2, op)

        val1 and val2 are constant values for the operator, and usually
        only val1 is used to compare against the node value(?)  however
        the INRANGE operator uses both values

    flags := (YIELD|NOYIELD) |

        if YIELD is set, a node id is returned if this spec matches.

    lines := [line]
    line  := (node_id for flags & yield, ...)

    The op in match is defined as in:
    filter_op_funcs = {
    "EQ"         : lambda x, val1, val2 : x  == val1,
    "NE"         : lambda x, val1, val2 : x  != val1,
    "GT"         : lambda x, val1, val2 : x  >  val1,
    "GE"         : lambda x, val1, val2 : x  >= val1,
    "LT"         : lambda x, val1, val2 : x  <  val1,
    "LE"         : lambda x, val1, val2 : x  <= val1,
    "INRANGE"    : lambda x, val1, val2 : (x >= val1) and (x <= 2),
    "INSTRING"   : lambda x, val1, val2 : (val1 or "").lower() in (x or "").lower(),
    "STARTSWITH" : lambda x, val1, val2 : (x or "").lower().startswith((val1 or "").lower()),
    "ENDSWITH"   : lambda x, val1, val2 : (x or "").lower().endswith((val1 or "").lower()),
    "REMATCH"    : lambda x, val1, val2 : bool(re.match(val1 or "", x or "", re.MULTILINE | re.DOTALL)),
    }

    """
    if root is None:
        root = nb.root()

    result = nb.find(root, specs, dt_quirks)

    num_yields = len([s for s in specs if s[2] & YIELD])
    if num_yields == 1:
        result = [x[0] for x in result]
    return result

if not nb.is_vtappd():
    e_val = legacy_e_val
else:
    def init_nb():
        reload(bound_nb)
        global nb, e_val
        nb = bound_nb.nb
        if e_version() < (1, 4, 44):
            e_val = legacy_e_val
        else:
            e_val = bound_nb.get_subnode_val
