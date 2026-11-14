# Readable form of main.py (the exact 4,089-byte file submitted to the
# make.fun tiny-chess competition, server-graded Elo 1654, 5W/0D/1L).
# main.py is that file verbatim: LZMA-compressed + base85-encoded, exec'd at
# runtime so the whole engine fits the 4,096-byte limit. This file is the
# decompressed engine, included so the design can be read directly.
# It is 7,145 bytes — over the limit on its own, which is the whole point.

import json,os,random,urllib.request as U
W,L=0,1;P,N,B,R,Q,K=1,2,3,4,5,6
A,C,D,H=1<<17,1<<18,1<<19,1<<20
V=(0,100,320,330,500,900,0)
r=(33,31,18,14,-14,-18,-31,-33);x=(1,-1,16,-16,15,17,-15,-17)
m=(15,17,-15,-17);o=(1,-1,16,-16);I=(Q,R,B,N);S=((r,0),(m,1),(o,1),(m+o,1),(x,0))
M=100000
c=[15]*128
c[0],c[7],c[4],c[112],c[119],c[116]=13,14,12,7,11,3
J=[s for s in range(128)if s%16<8]
g=random.Random(2654435769).getrandbits
e=[[g(64)for _ in range(128)]for _ in range(16)]
O=g(64);E=[g(64)for _ in range(16)];F=[g(64)for _ in range(8)]
b="DDDDEFF@ECBDDDDHEEFIFFHJNNNNDDDD:<>><@DE>EFG>DGH>EGH>DFG<@DD:<>>@BBBBEDDBFFFBDFFBEEFBDEFBDDD@BBBDDDECDDDCDDDCDDDCDDDCDDDEFFFDDDDHJFDHHDDB@@@@>><><<:><<:><<:><<::>>>>>DD>BHJ>BJL>BJL>BHJ>@BD:<>@"
p="@BBCCBB@BDEDDDDBBEEEEEDBDDEEEEDCCDEEEEDCBDEEEEDBBDDDDDDB@BBCCBB@"
T=[tuple(5*ord(b[32*i+4*r+min(f,7-f)])-340 for r in range(8)for f in range(8))for i in range(6)]+[tuple(5*ord(c)-340 for c in p)]
u=[0]+T[:4]+T[6:]+T[4:6];i=6400
def a(f):
 p=[[0]*128,W,0,-1,0,1,[-1,-1],0,[]];b=p[0];pa=f.split();rw=pa[0].split("/");h=0
 for r in range(8):
  c=0
  for ch in rw[r]:
   if ch.isdigit():c+=int(ch)
   else:
    t=" pnbrqk".index(ch.lower());co=ch.islower();q=(7-r)*16+c;b[q]=t|(co<<3);h^=e[b[q]][q]
    if t==K:p[6][co]=q
    c+=1
 p[1]=pa[1]!="w"
 p[2]=sum(1<<"KQkq".index(c)for c in pa[2]if c in "KQkq")
 if pa[3]!="-":p[3]=(int(pa[3][1])-1)*16+ord(pa[3][0])-97
 p[4]=int(pa[4])
 if p[1]==L:h^=O
 h^=E[p[2]]
 if p[3]!=-1:h^=F[p[3]&7]
 p[7]=h;return p
def y(p,q,by):
 b=p[0];e=by<<3
 for d in(15,17):
  t=q+(d if by==L else-d)
  if not t&136 and b[t]==(P|e):return 1
 for d in r:
  t=q+d
  if not t&136 and b[t]==(N|e):return 1
 for d in x:
  t=q+d
  if not t&136 and b[t]==(K|e):return 1
 for i,d in enumerate(m+o):
  t=q+d
  while not t&136:
   pc=b[t]
   if pc:
    if pc==(Q|e)or pc==((B,R)[i>3]|e):return 1
    break
   t+=d
 return 0
def d(p,co=False):
 b=p[0];u=p[1];t=u^1;o=[]
 for fr in J:
  pc=b[fr]
  if not pc or(pc>>3)!=u:continue
  ty=pc&7
  if ty==P:
   fw=16-32*u;rk=fr>>4;la=6-5*u;st=1+5*u;on=fr+fw
   if b[on]==0:
    if rk==la:
     for pr in I:o.append(fr|(on<<7)|(pr<<14))
    elif not co:
     o.append(fr|(on<<7));tw=on+fw
     if rk==st and b[tw]==0:o.append(fr|(tw<<7)|H)
   for d in(fw-1,fw+1):
    to=fr+d
    if to&136:continue
    tg=b[to]
    if tg and(tg>>3)==t:
     if rk==la:
      for pr in I:o.append(fr|(to<<7)|(pr<<14)|A)
     else:o.append(fr|(to<<7)|A)
    elif to==p[3]:o.append(fr|(to<<7)|A|C)
   continue
  offs,sl=S[ty-2]
  for d in offs:
   to=fr+d
   while not to&136:
    tg=b[to]
    if tg:
     if(tg>>3)==t:o.append(fr|(to<<7)|A)
     break
    if not co:o.append(fr|(to<<7))
    if not sl:break
    to+=d
  if ty==K and not co:
   ba=112*u;kg=ba+4
   if p[6][u]==kg and not y(p,kg,t):
    for r,ps,qs,tg in((1+3*u,(5,6),(5,6),6),(2+6*u,(3,2,1),(3,2),2)):
     if p[2]&r and all(b[ba+x]==0 for x in ps)and not any(y(p,ba+x,t)for x in qs):o.append(kg|((ba+tg)<<7)|D)
 return o
def z(p,m):
 b=p[0];fr=m&127;to=(m>>7)&127;pc=b[fr];u=p[1]
 cq=to-16+32*u if m&C else to;cp=b[cq]
 p[8].append((m,cp,p[2],p[3],p[4],p[7]))
 if cp:p[7]^=e[cp][cq];b[cq]=0
 p[7]^=e[pc][fr];b[fr]=0
 pr=(m>>14)&7;pl=pr|(u<<3)if pr else pc;b[to]=pl;p[7]^=e[pl][to]
 if pc&7==K:p[6][u]=to
 if m&D:
  rf=fr-4+7*(to>fr);rt=fr-1+2*(to>fr);rk=b[rf]
  p[7]^=e[rk][rf];b[rf]=0;b[rt]=rk;p[7]^=e[rk][rt]
 p[7]^=E[p[2]];p[2]&=c[fr]&c[to];p[7]^=E[p[2]]
 if p[3]!=-1:p[7]^=F[p[3]&7]
 p[3]=-1
 if m&H:
  ep=P|((u^1)<<3)
  for s in(1,-1):
   if not(to+s)&136 and b[to+s]==ep:p[3]=(fr+to)>>1
  if p[3]!=-1:p[7]^=F[p[3]&7]
 p[4]=0 if pc&7==P or cp else p[4]+1
 p[1]=u^1;p[7]^=O
 x=y(p,p[6][u],u^1)
 if x:f(p)
 return not x
def f(p):
 m,cp,ca,ep,hm,h=p[8].pop();b=p[0];fr=m&127;to=(m>>7)&127
 p[1]^=1;u=p[1];pl=b[to];pc=P|(u<<3)if(m>>14)&7 else pl
 b[fr]=pc;b[to]=0
 if pc&7==K:p[6][u]=fr
 if cp:b[to-16+32*u if m&C else to]=cp
 if m&D:rf=fr-4+7*(to>fr);rt=fr-1+2*(to>fr);b[rf]=b[rt];b[rt]=0
 p[2:5]=ca,ep,hm
 p[7]=h
def v(p):
 o=[]
 for m in d(p):
  if z(p,m):f(p);o.append(m)
 return o
def h(m):
 fr=m&127;to=(m>>7)&127;pr=(m>>14)&7;a="abcdefgh"
 return f"{a[fr&7]}{fr//16+1}{a[to&7]}{to//16+1}{' pnbrqk'[pr]if pr else ''}"
def j(p):
 b=p[0];sc=0;np=0;bp=[0,0];ka=[0,0]
 for q in J:
  pc=b[q]
  if not pc:continue
  t=pc&7;co=pc>>3;r=q>>4;rl=(r if co==W else 7-r)*8+(q&7)
  if t==K:ka[co]=rl;continue
  v=V[t]+u[t][rl];sc+=v if co==W else-v
  if t!=P:np+=V[t]
  if t==B:bp[co]+=1
 ph=np if np<i else i
 kg=lambda r:(u[K][r]*ph+u[7][r]*(i-ph)+3200)//i
 sc+=kg(ka[W])-kg(ka[L])
 sc+=30*((bp[0]>1)-(bp[1]>1))
 return sc*(1-2*p[1])
G=[]
def k(p,dp,al,be,pl):
 if pl>0 and(p[4]>=100 or l(p)):return 0
 G[0]+=1
 if G[0]>=G[1]>0:G[2]=1;return 0
 if dp<=0 or pl>=64:
  ck=y(p,p[6][p[1]],p[1]^1);bt=-M-1
  if pl>=64:return j(p)
  if not ck:
   st=j(p)
   if st>=be:return st
   bt=st
   if st>al:al=st
  mv=s(p,d(p,not ck),pl);lg=0
  for m in mv:
   if not z(p,m):continue
   lg+=1;sc=-k(p,0,-be,-al,pl+1);f(p)
   if G[2]:return 0
   if sc>bt:bt=sc
   if sc>=be:return sc
   if sc>al:al=sc
  if ck and lg==0:return-M+pl
  return bt
 e=G[3].get(p[7]);tt=e[0]if e else 0
 if e and e[2]>=dp:
  x=e[1]
  if x>M-64:x-=pl
  elif x<-M+64:x+=pl
  if e[3]==1 or(e[3]==2 and x>=be)or(e[3]==3 and x<=al):return x
 a0=al;mv=s(p,d(p),pl,tt);lg=0;bt=-M-1;n=0
 ki=G[4];hi=G[5]
 for m in mv:
  if not z(p,m):continue
  lg+=1;hi.append(p[7]);r=(lg>2 and dp>2 and not m&A and not(m>>14)&7)*(1+(lg>8));sc=-k(p,dp-1-r,-be,-al,pl+1)
  if r and al<sc<be:sc=-k(p,dp-1,-be,-al,pl+1)
  hi.pop();f(p)
  if G[2]:return 0
  if sc>bt:bt=sc;n=m
  if sc>al:al=sc
  if al>=be:
   if not m&A and not(m>>14)&7 and ki[pl*2]!=m:ki[pl*2+1]=ki[pl*2];ki[pl*2]=m
   break
 if lg==0:return-M+pl if y(p,p[6][p[1]],p[1]^1)else 0
 x=bt
 if x>M-64:x+=pl
 elif x<-M+64:x-=pl
 G[3][p[7]]=(n,x,dp,3 if bt<=a0 else(2 if bt>=be else 1))
 return bt
def l(p):
 h=G[5];n=len(h)
 for i in range(n-3,max(0,n-1-p[4])-1,-2):
  if h[i]==p[7]:return 1
 return 0
def s(p,mv,pl,tt=0):
 b=p[0];ki=G[4];k0=ki[pl*2];k1=ki[pl*2+1];o=[]
 for i,m in enumerate(mv):
  x=0
  if m&A:tg=b[(m>>7)&127];x=M+10*V[(tg&7)or P]-(b[m&127]&7)
  pr=(m>>14)&7
  if pr:x+=2*M+V[pr]
  if x==0:x=50000 if m==k0 else 40000 if m==k1 else 0
  if m==tt:x=10*M
  o.append((x*1000-i,m))
 o.sort(reverse=True)
 return[m for _,m in o]
def n(p,hi,nn):
 G[:]=[0,0,0,{},[0]*128,list(hi)]
 if not G[5]or G[5][-1]!=p[7]:G[5].append(p[7])
 mv=v(p)
 od0=[(0,m)for m in mv]
 for d in range(1,65):
  G[1]=nn*(d>1);al=-M-1
  for i,(x0,m)in enumerate(od0):
   z(p,m);G[5].append(p[7]);sc=-k(p,d-1,-M-1,-al,1);G[5].pop();f(p)
   if G[2]:break
   od0[i]=(sc,m)
   if sc>al:al=sc
  if G[2]:break
  od0.sort(key=lambda t:-t[0]);bs,m0=od0[0];bd=d
  if bs>=M-64:break
 return m0,bs,bd,G[0]
t=70000
X=os.environ.get("MAKEFUN_ENV_URL")
def w(pa,bo):return json.load(U.urlopen(X+pa,json.dumps(bo).encode()))
def q():
 while(g:=w("/game",{}))["status"]!="done":
  while g["status"]=="your_move":
   p=a(g["fen"]);hp=a(g["start_fen"]);hi=[hp[7]]
   for u in g["moves"]:
    for m in v(hp):
     if h(m)==u:break
    else:break
    z(hp,m);hi.append(hp[7])
   m=n(p,hi,t)[0];u=h(m)
   g=w("/move",{"game":g["game"],"move":u})
q()