'''
lexer
'''
  # import pprint
import ply.lex as lex
  # import ply.yacc as yacc
from ply.lex import TOKEN

tokens = [
    'ATTR_OP',
    'ATTR_En',
    'OP0_ATTR',
    'TYPE_ATTR',
    'ADDR_EXPR',
    'SPEC_ATTR',
    'SPEC_VALU',
    'CONSTRUCTOR',
    'QUAL',
    'FLOAT',
    'PSEUDO_TMPL',
    'STRG',
    "NODE",
#    "SPACE",
    'SPEC',

    "BUILTIN_FILE",
#    'SCOPE',
#    "INTCONST",
    'HXX_FILE',
    'ARTIFICIAL',
    'LANG',
#    'ERROR',
    'SIGNED',
    'LINK',
    'STRUCT',
    'ACC',
#    'DTYPE',
    'MEMBER',
#    'INTERNAL',
#    'STRG2',
    'OP',
    'NOTE',
#    'R'
]


def make_re(tstr):
    '''
    create a regex like a|b|c
    '''
    items = [
        x.strip().rstrip() for x in tstr.split()
    ]
    newre = r'(%s)' % '|'.join(items)
    # print newre
    return newre

import sys

# create parser rules
def create_rules(tstr):
    for token in tstr.split():
        token = token.upper()
        func = lambda x: x
        rule = "ntype : %s" % token
        func.__doc__ = rule
        current_module = sys.modules[__name__]
        name = "p_%s" % (token.lower())
        print "name %s(psr_val):\n    \'%s\'\n    return ntype_base(psr_val)\n" %(name, rule)
        setattr(current_module, name , func)


def emit_parser_rule(base_name, prefix):
    # parser
    rule = "%s_type : %s" % (prefix, base_name)
    parser_name = "p_%s" % (base_name.lower())
    print "def %s(psr_val):\n    \'%s\'\n    psr_val[0] = %s_base(psr_val)\n" %(parser_name, rule, prefix)

def make_tokens(prefix,pattern,val_func, tstr):
    '''
    create tokens
    * prefix for the token name
    * pattern to create for each token with one %s
    * val_fun to process the data
    * tstr for the tokens

    '''
    for x in tstr.split():
        item = x.strip().rstrip()
        regex = pattern % item
        func = lambda x : val_func(x)
        func.__doc__ = regex
        current_module = sys.modules[__name__]
        base_name = "%s_%s" % (prefix, item.upper())
        name = "t_%s" % (base_name)
        tokens.append(base_name)
        #print "created name %s regex %s"  %( name, regex )

        emit_parser_rule(base_name, prefix)

        #print "%s"  %( base_name )
        setattr(current_module, name , func)


def ntype_value(tok) :
    return tok 

make_tokens("NTYPE", "(%s)",ntype_value,"""
aggr_init_expr
alignof_expr
array_ref
array_type
arrow_expr
baselink
bind_expr
binfo
bit_and_expr
bit_ior_expr
bit_not_expr
bit_xor_expr
boolean_type
bound_template_template_parm
break_stmt
call_expr
case_label_expr
cast_expr
complex_type
component_ref
compound_expr
cond_expr
const_cast_expr
const_decl
continue_stmt
ctor_initializer
decl_expr
decltype_type
dl_expr
do_stmt
dotstar_expr
dynamic_cast_expr
enumeral_type
eq_expr
error_mark
expr_stmt
field_decl
for_stmt
function_decl
function_type
ge_expr
gt_expr
handler
identifier_node
if_stmt
indirect_ref
integer_cst
integer_type
label_decl
lang_type
le_expr
lshift_expr
lt_expr
member_ref
method_type
minus_expr
modop_expr
mult_expr
namespace_decl
ne_expr
negate_expr
nop_expr
nw_expr
offset_type
overload
parm_decl
plus_expr
pointer_type
postdecrement_expr
postincrement_expr
predecrement_expr
preincrement_expr
ptrmem_cst
real_cst
real_type
record_type
reference_type
reinterpret_cast_expr
return_expr
rshift_expr
scope_ref
sizeof_expr
statement_list
static_cast_expr
string_cst
switch_stmt
tag_defn
target_expr
template_decl
template_id_expr
template_parm_index
template_template_parm
template_type_parm
throw_expr
trait_expr
translation_unit_decl
tree_list
tree_vec
trunc_div_expr
trunc_mod_expr
truth_andif_expr
truth_not_expr
truth_orif_expr
try_block
type_decl
typeid_expr
typename_type
typeof_type
union_type
using_decl
using_stmt
var_decl
vector_type
void_type
while_stmt
""")
#make_token("NTYPE",NTYPES)

#t_NTYPE = r'%s\s?' % make_re(NTYPES)
# print(t_NTYPE)

t_PSEUDO_TMPL = 'pseudo|tmpl'
#t_DTYPE = 'long|int'

# can be used as a node type or a note
t_CONSTRUCTOR = 'constructor'


def t_STRG(tok):
    r'strg:\s+(.+)\s+lngt:\s\d+'
    strval = tok.lexer.lexmatch.group(2)
    # print ("CHECK:%s" % strval)
    tok.value = strval
    return tok

#t_STRG2 = r'.+\s+lngt:\s\d+?'

t_LANG = r'C\s'
#t_R = r'\sr\s'


def t_QUAL(tok):
    r'c\s|v\s|cv\s|r\s'
    strval = tok.value
    #print ("QUAL:%s" % strval)
    #tok.value = strval
    return tok


def t_NODE(tok):
    r'\@(\d+)'
    strval = tok.lexer.lexmatch.group(4)
    # print ("NODEID:%s" % strval)
    tok.value = strval
    return tok


def t_SPACE(tok):
    r'\s+'
    pass

#t_ERROR = 'error_mark'

@TOKEN(r'addr_expr\s?')
def t_ADDR_EXPR(tok) :
    tok.value = str(tok.lexer.lexmatch.group(6))
    #print("NTYPE ADDR EXPR %s " % tok.value)
    return tok

def t_OP0_ATTR(tok):
    r'(OP0)\s*:'
    #count_non_null(tok)
    tok.value = str(tok.lexer.lexmatch.group(28))
    #print("OP0_ATTR %s " % tok.value)
    return tok

def t_TYPE_ATTR(tok):
    r'type\s*:'
    tok.value = 'type'
    #print("TYPE_ATTR:%s" % tok.value)
    return tok


def t_ATTR_En(tok):
    '''(%s|E\d+)\s*:'''
    #print("ATTR:%s" % str(tok.lexer.lexmatch.groups()))
    #tok.value = tok.lexer.lexmatch.group(11
    tok.value = tok.value.replace(" :","")
    #print("ATTR:%s" % tok.value)
    #print("ATTREN:%s" % tok.value)
    return tok

def count_non_null(tok):
    count = 0 
    for v in tok.lexer.lexmatch.groups():
        if v is not None :
            print "check %s %d"  % (v, count)
        count = count + 1

def t_ATTR_OP(tok):
    '''(OP\d+)\s*:'''
    # count_non_null(tok)
    tok.value = tok.lexer.lexmatch.group(33)
    #print("ATTR:%s" % tok.value)
    #print("OPATTR:%s" % tok.value)
    return tok



def attr_val(tok):

    val = None
    #print("IN ATTR:%s" % tok.value)
    #print("UNMATCHED ATTR:%s" % tok.value)
    tok.value = tok.value.replace(":","")
    tok.value = tok.value.replace(" ","")
    return tok


make_tokens("ATTR", "%s\s*:",attr_val, '''
accs
addr
algn
alis
args
argt
base
bases
binf
body
bpos
chain
chan
clas
clnp
cls
cnst
cond
crnt
csts
ctor
dcls
decl
domn
else
elts
expr
flds
fn
fncs
hdlr
high
init
inst
lang
line
link
lngt
low
max
mbr
min
mngl
name
nmsp
note
nst
orig
parm
prec
prms
ptd
purp
qual
refd
retn
rslt
scpe
sign
size
spcs
srcp
sts
tag
then
unql
used
val
valu
vfld
''')

def t_SPEC_ATTR(tok):
    '''
    spec attr
    '''
    strval = tok.lexer.lexmatch.group(10)
    tok.value = strval
    # print "SPEC_ATTR:%s(%s)" % (t.type, strval)
    return tok

t_SPEC_ATTR.__doc__ = r'%s\s*:' % make_re('spec')

t_BUILTIN_FILE = r'\<built\-in\>:0'
t_HXX_FILE = r'(yes_no_type.hpp|' + \
             r'[\-\+A-Za-z_\-0-9]+(\.(h|hdl|txx|tcc|hpp|cxx|hxx))?):\d+'
t_SIGNED = 'signed|unsigned'
#t_SCOPE = r'\:\:'
#t_INTCONST = r'(\-)?\d+'
t_FLOAT = r'[+\-]?(?:0|[1-9]\d*)(?:\.\d*)?(?:[eE][+\-]?\d+)?'
t_ARTIFICIAL = r'artificial'
t_LINK = r'static|undefined|extern'
t_ACC = r'pub|priv|prot'
t_STRUCT = r'struct|union'
t_MEMBER = r'member|destructor|binfo|ptrmem'
t_NOTE = r'operator|conversion'
t_SPEC = r'spec\s'
t_SPEC_VALU = r'mutable|bitfield|pure|virt'


def op_token_value(tok) :
    '''
    OP token
    '''
    strval = tok.lexer.lexmatch.group(2)
    tok.value = strval
    # print "OP%s" % strval
    return tok

make_tokens("OPERATOR", r'operator\s+(%s)\s',op_token_value,"""
    add
    and
    andassign
    addr
    assign
    call
    compound
    delete
    deref
    div
    divassign
    eq
    ge
    gt
    le
    lnot
    lshift
    lshiftassign
    lt
    minus
    minusassign
    mult
    multassign
    ne
    neg
    new
    or
    orassign
    plus
    plusassign
    postdec
    postinc
    predec
    preinc
    rshift
    vecdelete
    vecnew
    xor
    xorassign
    not
    pos
    ref
    rshiftassign
    subs
""")


def t_error(t):
    raise TypeError("Unknown text '%s'" % (t.value, ))

lex.lex()
