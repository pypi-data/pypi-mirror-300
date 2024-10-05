import{c as rt,g as mt,s as _t,a as kt,b as xt,D as vt,B as bt,E as wt,j as St,aQ as Lt,h as Y,i as Et}from"./index-a5d3e69d.js";import{o as At}from"./ordinal-ba9b4969.js";import"./init-77b53fdd.js";function Tt(t){for(var n=t.length/6|0,i=new Array(n),l=0;l<n;)i[l]="#"+t.slice(l*6,++l*6);return i}const Mt=Tt("4e79a7f28e2ce1575976b7b259a14fedc949af7aa1ff9da79c755fbab0ab");function ot(t,n){let i;if(n===void 0)for(const l of t)l!=null&&(i<l||i===void 0&&l>=l)&&(i=l);else{let l=-1;for(let u of t)(u=n(u,++l,t))!=null&&(i<u||i===void 0&&u>=u)&&(i=u)}return i}function yt(t,n){let i;if(n===void 0)for(const l of t)l!=null&&(i>l||i===void 0&&l>=l)&&(i=l);else{let l=-1;for(let u of t)(u=n(u,++l,t))!=null&&(i>u||i===void 0&&u>=u)&&(i=u)}return i}function Z(t,n){let i=0;if(n===void 0)for(let l of t)(l=+l)&&(i+=l);else{let l=-1;for(let u of t)(u=+n(u,++l,t))&&(i+=u)}return i}function Nt(t){return t.target.depth}function Pt(t){return t.depth}function Ct(t,n){return n-1-t.height}function dt(t,n){return t.sourceLinks.length?t.depth:n-1}function It(t){return t.targetLinks.length?t.depth:t.sourceLinks.length?yt(t.sourceLinks,Nt)-1:0}function G(t){return function(){return t}}function lt(t,n){return H(t.source,n.source)||t.index-n.index}function at(t,n){return H(t.target,n.target)||t.index-n.index}function H(t,n){return t.y0-n.y0}function J(t){return t.value}function Ot(t){return t.index}function $t(t){return t.nodes}function zt(t){return t.links}function ct(t,n){const i=t.get(n);if(!i)throw new Error("missing: "+n);return i}function ut({nodes:t}){for(const n of t){let i=n.y0,l=i;for(const u of n.sourceLinks)u.y0=i+u.width/2,i+=u.width;for(const u of n.targetLinks)u.y1=l+u.width/2,l+=u.width}}function jt(){let t=0,n=0,i=1,l=1,u=24,k=8,g,m=Ot,s=dt,o,c,p=$t,b=zt,y=6;function x(){const e={nodes:p.apply(null,arguments),links:b.apply(null,arguments)};return E(e),L(e),A(e),N(e),S(e),ut(e),e}x.update=function(e){return ut(e),e},x.nodeId=function(e){return arguments.length?(m=typeof e=="function"?e:G(e),x):m},x.nodeAlign=function(e){return arguments.length?(s=typeof e=="function"?e:G(e),x):s},x.nodeSort=function(e){return arguments.length?(o=e,x):o},x.nodeWidth=function(e){return arguments.length?(u=+e,x):u},x.nodePadding=function(e){return arguments.length?(k=g=+e,x):k},x.nodes=function(e){return arguments.length?(p=typeof e=="function"?e:G(e),x):p},x.links=function(e){return arguments.length?(b=typeof e=="function"?e:G(e),x):b},x.linkSort=function(e){return arguments.length?(c=e,x):c},x.size=function(e){return arguments.length?(t=n=0,i=+e[0],l=+e[1],x):[i-t,l-n]},x.extent=function(e){return arguments.length?(t=+e[0][0],i=+e[1][0],n=+e[0][1],l=+e[1][1],x):[[t,n],[i,l]]},x.iterations=function(e){return arguments.length?(y=+e,x):y};function E({nodes:e,links:f}){for(const[h,r]of e.entries())r.index=h,r.sourceLinks=[],r.targetLinks=[];const a=new Map(e.map((h,r)=>[m(h,r,e),h]));for(const[h,r]of f.entries()){r.index=h;let{source:_,target:v}=r;typeof _!="object"&&(_=r.source=ct(a,_)),typeof v!="object"&&(v=r.target=ct(a,v)),_.sourceLinks.push(r),v.targetLinks.push(r)}if(c!=null)for(const{sourceLinks:h,targetLinks:r}of e)h.sort(c),r.sort(c)}function L({nodes:e}){for(const f of e)f.value=f.fixedValue===void 0?Math.max(Z(f.sourceLinks,J),Z(f.targetLinks,J)):f.fixedValue}function A({nodes:e}){const f=e.length;let a=new Set(e),h=new Set,r=0;for(;a.size;){for(const _ of a){_.depth=r;for(const{target:v}of _.sourceLinks)h.add(v)}if(++r>f)throw new Error("circular link");a=h,h=new Set}}function N({nodes:e}){const f=e.length;let a=new Set(e),h=new Set,r=0;for(;a.size;){for(const _ of a){_.height=r;for(const{source:v}of _.targetLinks)h.add(v)}if(++r>f)throw new Error("circular link");a=h,h=new Set}}function P({nodes:e}){const f=ot(e,r=>r.depth)+1,a=(i-t-u)/(f-1),h=new Array(f);for(const r of e){const _=Math.max(0,Math.min(f-1,Math.floor(s.call(null,r,f))));r.layer=_,r.x0=t+_*a,r.x1=r.x0+u,h[_]?h[_].push(r):h[_]=[r]}if(o)for(const r of h)r.sort(o);return h}function z(e){const f=yt(e,a=>(l-n-(a.length-1)*g)/Z(a,J));for(const a of e){let h=n;for(const r of a){r.y0=h,r.y1=h+r.value*f,h=r.y1+g;for(const _ of r.sourceLinks)_.width=_.value*f}h=(l-h+g)/(a.length+1);for(let r=0;r<a.length;++r){const _=a[r];_.y0+=h*(r+1),_.y1+=h*(r+1)}O(a)}}function S(e){const f=P(e);g=Math.min(k,(l-n)/(ot(f,a=>a.length)-1)),z(f);for(let a=0;a<y;++a){const h=Math.pow(.99,a),r=Math.max(1-h,(a+1)/y);$(f,h,r),M(f,h,r)}}function M(e,f,a){for(let h=1,r=e.length;h<r;++h){const _=e[h];for(const v of _){let U=0,j=0;for(const{source:F,value:K}of v.targetLinks){let W=K*(v.layer-F.layer);U+=T(F,v)*W,j+=W}if(!(j>0))continue;let V=(U/j-v.y0)*f;v.y0+=V,v.y1+=V,w(v)}o===void 0&&_.sort(H),C(_,a)}}function $(e,f,a){for(let h=e.length,r=h-2;r>=0;--r){const _=e[r];for(const v of _){let U=0,j=0;for(const{target:F,value:K}of v.sourceLinks){let W=K*(F.layer-v.layer);U+=R(v,F)*W,j+=W}if(!(j>0))continue;let V=(U/j-v.y0)*f;v.y0+=V,v.y1+=V,w(v)}o===void 0&&_.sort(H),C(_,a)}}function C(e,f){const a=e.length>>1,h=e[a];d(e,h.y0-g,a-1,f),I(e,h.y1+g,a+1,f),d(e,l,e.length-1,f),I(e,n,0,f)}function I(e,f,a,h){for(;a<e.length;++a){const r=e[a],_=(f-r.y0)*h;_>1e-6&&(r.y0+=_,r.y1+=_),f=r.y1+g}}function d(e,f,a,h){for(;a>=0;--a){const r=e[a],_=(r.y1-f)*h;_>1e-6&&(r.y0-=_,r.y1-=_),f=r.y0-g}}function w({sourceLinks:e,targetLinks:f}){if(c===void 0){for(const{source:{sourceLinks:a}}of f)a.sort(at);for(const{target:{targetLinks:a}}of e)a.sort(lt)}}function O(e){if(c===void 0)for(const{sourceLinks:f,targetLinks:a}of e)f.sort(at),a.sort(lt)}function T(e,f){let a=e.y0-(e.sourceLinks.length-1)*g/2;for(const{target:h,width:r}of e.sourceLinks){if(h===f)break;a+=r+g}for(const{source:h,width:r}of f.targetLinks){if(h===e)break;a-=r}return a}function R(e,f){let a=f.y0-(f.targetLinks.length-1)*g/2;for(const{source:h,width:r}of f.targetLinks){if(h===e)break;a+=r+g}for(const{target:h,width:r}of e.sourceLinks){if(h===f)break;a-=r}return a}return x}var tt=Math.PI,et=2*tt,D=1e-6,Dt=et-D;function nt(){this._x0=this._y0=this._x1=this._y1=null,this._=""}function gt(){return new nt}nt.prototype=gt.prototype={constructor:nt,moveTo:function(t,n){this._+="M"+(this._x0=this._x1=+t)+","+(this._y0=this._y1=+n)},closePath:function(){this._x1!==null&&(this._x1=this._x0,this._y1=this._y0,this._+="Z")},lineTo:function(t,n){this._+="L"+(this._x1=+t)+","+(this._y1=+n)},quadraticCurveTo:function(t,n,i,l){this._+="Q"+ +t+","+ +n+","+(this._x1=+i)+","+(this._y1=+l)},bezierCurveTo:function(t,n,i,l,u,k){this._+="C"+ +t+","+ +n+","+ +i+","+ +l+","+(this._x1=+u)+","+(this._y1=+k)},arcTo:function(t,n,i,l,u){t=+t,n=+n,i=+i,l=+l,u=+u;var k=this._x1,g=this._y1,m=i-t,s=l-n,o=k-t,c=g-n,p=o*o+c*c;if(u<0)throw new Error("negative radius: "+u);if(this._x1===null)this._+="M"+(this._x1=t)+","+(this._y1=n);else if(p>D)if(!(Math.abs(c*m-s*o)>D)||!u)this._+="L"+(this._x1=t)+","+(this._y1=n);else{var b=i-k,y=l-g,x=m*m+s*s,E=b*b+y*y,L=Math.sqrt(x),A=Math.sqrt(p),N=u*Math.tan((tt-Math.acos((x+p-E)/(2*L*A)))/2),P=N/A,z=N/L;Math.abs(P-1)>D&&(this._+="L"+(t+P*o)+","+(n+P*c)),this._+="A"+u+","+u+",0,0,"+ +(c*b>o*y)+","+(this._x1=t+z*m)+","+(this._y1=n+z*s)}},arc:function(t,n,i,l,u,k){t=+t,n=+n,i=+i,k=!!k;var g=i*Math.cos(l),m=i*Math.sin(l),s=t+g,o=n+m,c=1^k,p=k?l-u:u-l;if(i<0)throw new Error("negative radius: "+i);this._x1===null?this._+="M"+s+","+o:(Math.abs(this._x1-s)>D||Math.abs(this._y1-o)>D)&&(this._+="L"+s+","+o),i&&(p<0&&(p=p%et+et),p>Dt?this._+="A"+i+","+i+",0,1,"+c+","+(t-g)+","+(n-m)+"A"+i+","+i+",0,1,"+c+","+(this._x1=s)+","+(this._y1=o):p>D&&(this._+="A"+i+","+i+",0,"+ +(p>=tt)+","+c+","+(this._x1=t+i*Math.cos(u))+","+(this._y1=n+i*Math.sin(u))))},rect:function(t,n,i,l){this._+="M"+(this._x0=this._x1=+t)+","+(this._y0=this._y1=+n)+"h"+ +i+"v"+ +l+"h"+-i+"Z"},toString:function(){return this._}};function ht(t){return function(){return t}}function Bt(t){return t[0]}function Rt(t){return t[1]}var Ut=Array.prototype.slice;function Vt(t){return t.source}function Ft(t){return t.target}function Wt(t){var n=Vt,i=Ft,l=Bt,u=Rt,k=null;function g(){var m,s=Ut.call(arguments),o=n.apply(this,s),c=i.apply(this,s);if(k||(k=m=gt()),t(k,+l.apply(this,(s[0]=o,s)),+u.apply(this,s),+l.apply(this,(s[0]=c,s)),+u.apply(this,s)),m)return k=null,m+""||null}return g.source=function(m){return arguments.length?(n=m,g):n},g.target=function(m){return arguments.length?(i=m,g):i},g.x=function(m){return arguments.length?(l=typeof m=="function"?m:ht(+m),g):l},g.y=function(m){return arguments.length?(u=typeof m=="function"?m:ht(+m),g):u},g.context=function(m){return arguments.length?(k=m??null,g):k},g}function Yt(t,n,i,l,u){t.moveTo(n,i),t.bezierCurveTo(n=(n+l)/2,i,n,u,l,u)}function Gt(){return Wt(Yt)}function Ht(t){return[t.source.x1,t.y0]}function Qt(t){return[t.target.x0,t.y1]}function Xt(){return Gt().source(Ht).target(Qt)}var it=function(){var t=function(m,s,o,c){for(o=o||{},c=m.length;c--;o[m[c]]=s);return o},n=[1,9],i=[1,10],l=[1,5,10,12],u={trace:function(){},yy:{},symbols_:{error:2,start:3,SANKEY:4,NEWLINE:5,csv:6,opt_eof:7,record:8,csv_tail:9,EOF:10,"field[source]":11,COMMA:12,"field[target]":13,"field[value]":14,field:15,escaped:16,non_escaped:17,DQUOTE:18,ESCAPED_TEXT:19,NON_ESCAPED_TEXT:20,$accept:0,$end:1},terminals_:{2:"error",4:"SANKEY",5:"NEWLINE",10:"EOF",11:"field[source]",12:"COMMA",13:"field[target]",14:"field[value]",18:"DQUOTE",19:"ESCAPED_TEXT",20:"NON_ESCAPED_TEXT"},productions_:[0,[3,4],[6,2],[9,2],[9,0],[7,1],[7,0],[8,5],[15,1],[15,1],[16,3],[17,1]],performAction:function(s,o,c,p,b,y,x){var E=y.length-1;switch(b){case 7:const L=p.findOrCreateNode(y[E-4].trim().replaceAll('""','"')),A=p.findOrCreateNode(y[E-2].trim().replaceAll('""','"')),N=parseFloat(y[E].trim());p.addLink(L,A,N);break;case 8:case 9:case 11:this.$=y[E];break;case 10:this.$=y[E-1];break}},table:[{3:1,4:[1,2]},{1:[3]},{5:[1,3]},{6:4,8:5,15:6,16:7,17:8,18:n,20:i},{1:[2,6],7:11,10:[1,12]},t(i,[2,4],{9:13,5:[1,14]}),{12:[1,15]},t(l,[2,8]),t(l,[2,9]),{19:[1,16]},t(l,[2,11]),{1:[2,1]},{1:[2,5]},t(i,[2,2]),{6:17,8:5,15:6,16:7,17:8,18:n,20:i},{15:18,16:7,17:8,18:n,20:i},{18:[1,19]},t(i,[2,3]),{12:[1,20]},t(l,[2,10]),{15:21,16:7,17:8,18:n,20:i},t([1,5,10],[2,7])],defaultActions:{11:[2,1],12:[2,5]},parseError:function(s,o){if(o.recoverable)this.trace(s);else{var c=new Error(s);throw c.hash=o,c}},parse:function(s){var o=this,c=[0],p=[],b=[null],y=[],x=this.table,E="",L=0,A=0,N=2,P=1,z=y.slice.call(arguments,1),S=Object.create(this.lexer),M={yy:{}};for(var $ in this.yy)Object.prototype.hasOwnProperty.call(this.yy,$)&&(M.yy[$]=this.yy[$]);S.setInput(s,M.yy),M.yy.lexer=S,M.yy.parser=this,typeof S.yylloc>"u"&&(S.yylloc={});var C=S.yylloc;y.push(C);var I=S.options&&S.options.ranges;typeof M.yy.parseError=="function"?this.parseError=M.yy.parseError:this.parseError=Object.getPrototypeOf(this).parseError;function d(){var v;return v=p.pop()||S.lex()||P,typeof v!="number"&&(v instanceof Array&&(p=v,v=p.pop()),v=o.symbols_[v]||v),v}for(var w,O,T,R,e={},f,a,h,r;;){if(O=c[c.length-1],this.defaultActions[O]?T=this.defaultActions[O]:((w===null||typeof w>"u")&&(w=d()),T=x[O]&&x[O][w]),typeof T>"u"||!T.length||!T[0]){var _="";r=[];for(f in x[O])this.terminals_[f]&&f>N&&r.push("'"+this.terminals_[f]+"'");S.showPosition?_="Parse error on line "+(L+1)+`:
`+S.showPosition()+`
Expecting `+r.join(", ")+", got '"+(this.terminals_[w]||w)+"'":_="Parse error on line "+(L+1)+": Unexpected "+(w==P?"end of input":"'"+(this.terminals_[w]||w)+"'"),this.parseError(_,{text:S.match,token:this.terminals_[w]||w,line:S.yylineno,loc:C,expected:r})}if(T[0]instanceof Array&&T.length>1)throw new Error("Parse Error: multiple actions possible at state: "+O+", token: "+w);switch(T[0]){case 1:c.push(w),b.push(S.yytext),y.push(S.yylloc),c.push(T[1]),w=null,A=S.yyleng,E=S.yytext,L=S.yylineno,C=S.yylloc;break;case 2:if(a=this.productions_[T[1]][1],e.$=b[b.length-a],e._$={first_line:y[y.length-(a||1)].first_line,last_line:y[y.length-1].last_line,first_column:y[y.length-(a||1)].first_column,last_column:y[y.length-1].last_column},I&&(e._$.range=[y[y.length-(a||1)].range[0],y[y.length-1].range[1]]),R=this.performAction.apply(e,[E,A,L,M.yy,T[1],b,y].concat(z)),typeof R<"u")return R;a&&(c=c.slice(0,-1*a*2),b=b.slice(0,-1*a),y=y.slice(0,-1*a)),c.push(this.productions_[T[1]][0]),b.push(e.$),y.push(e._$),h=x[c[c.length-2]][c[c.length-1]],c.push(h);break;case 3:return!0}}return!0}},k=function(){var m={EOF:1,parseError:function(o,c){if(this.yy.parser)this.yy.parser.parseError(o,c);else throw new Error(o)},setInput:function(s,o){return this.yy=o||this.yy||{},this._input=s,this._more=this._backtrack=this.done=!1,this.yylineno=this.yyleng=0,this.yytext=this.matched=this.match="",this.conditionStack=["INITIAL"],this.yylloc={first_line:1,first_column:0,last_line:1,last_column:0},this.options.ranges&&(this.yylloc.range=[0,0]),this.offset=0,this},input:function(){var s=this._input[0];this.yytext+=s,this.yyleng++,this.offset++,this.match+=s,this.matched+=s;var o=s.match(/(?:\r\n?|\n).*/g);return o?(this.yylineno++,this.yylloc.last_line++):this.yylloc.last_column++,this.options.ranges&&this.yylloc.range[1]++,this._input=this._input.slice(1),s},unput:function(s){var o=s.length,c=s.split(/(?:\r\n?|\n)/g);this._input=s+this._input,this.yytext=this.yytext.substr(0,this.yytext.length-o),this.offset-=o;var p=this.match.split(/(?:\r\n?|\n)/g);this.match=this.match.substr(0,this.match.length-1),this.matched=this.matched.substr(0,this.matched.length-1),c.length-1&&(this.yylineno-=c.length-1);var b=this.yylloc.range;return this.yylloc={first_line:this.yylloc.first_line,last_line:this.yylineno+1,first_column:this.yylloc.first_column,last_column:c?(c.length===p.length?this.yylloc.first_column:0)+p[p.length-c.length].length-c[0].length:this.yylloc.first_column-o},this.options.ranges&&(this.yylloc.range=[b[0],b[0]+this.yyleng-o]),this.yyleng=this.yytext.length,this},more:function(){return this._more=!0,this},reject:function(){if(this.options.backtrack_lexer)this._backtrack=!0;else return this.parseError("Lexical error on line "+(this.yylineno+1)+`. You can only invoke reject() in the lexer when the lexer is of the backtracking persuasion (options.backtrack_lexer = true).
`+this.showPosition(),{text:"",token:null,line:this.yylineno});return this},less:function(s){this.unput(this.match.slice(s))},pastInput:function(){var s=this.matched.substr(0,this.matched.length-this.match.length);return(s.length>20?"...":"")+s.substr(-20).replace(/\n/g,"")},upcomingInput:function(){var s=this.match;return s.length<20&&(s+=this._input.substr(0,20-s.length)),(s.substr(0,20)+(s.length>20?"...":"")).replace(/\n/g,"")},showPosition:function(){var s=this.pastInput(),o=new Array(s.length+1).join("-");return s+this.upcomingInput()+`
`+o+"^"},test_match:function(s,o){var c,p,b;if(this.options.backtrack_lexer&&(b={yylineno:this.yylineno,yylloc:{first_line:this.yylloc.first_line,last_line:this.last_line,first_column:this.yylloc.first_column,last_column:this.yylloc.last_column},yytext:this.yytext,match:this.match,matches:this.matches,matched:this.matched,yyleng:this.yyleng,offset:this.offset,_more:this._more,_input:this._input,yy:this.yy,conditionStack:this.conditionStack.slice(0),done:this.done},this.options.ranges&&(b.yylloc.range=this.yylloc.range.slice(0))),p=s[0].match(/(?:\r\n?|\n).*/g),p&&(this.yylineno+=p.length),this.yylloc={first_line:this.yylloc.last_line,last_line:this.yylineno+1,first_column:this.yylloc.last_column,last_column:p?p[p.length-1].length-p[p.length-1].match(/\r?\n?/)[0].length:this.yylloc.last_column+s[0].length},this.yytext+=s[0],this.match+=s[0],this.matches=s,this.yyleng=this.yytext.length,this.options.ranges&&(this.yylloc.range=[this.offset,this.offset+=this.yyleng]),this._more=!1,this._backtrack=!1,this._input=this._input.slice(s[0].length),this.matched+=s[0],c=this.performAction.call(this,this.yy,this,o,this.conditionStack[this.conditionStack.length-1]),this.done&&this._input&&(this.done=!1),c)return c;if(this._backtrack){for(var y in b)this[y]=b[y];return!1}return!1},next:function(){if(this.done)return this.EOF;this._input||(this.done=!0);var s,o,c,p;this._more||(this.yytext="",this.match="");for(var b=this._currentRules(),y=0;y<b.length;y++)if(c=this._input.match(this.rules[b[y]]),c&&(!o||c[0].length>o[0].length)){if(o=c,p=y,this.options.backtrack_lexer){if(s=this.test_match(c,b[y]),s!==!1)return s;if(this._backtrack){o=!1;continue}else return!1}else if(!this.options.flex)break}return o?(s=this.test_match(o,b[p]),s!==!1?s:!1):this._input===""?this.EOF:this.parseError("Lexical error on line "+(this.yylineno+1)+`. Unrecognized text.
`+this.showPosition(),{text:"",token:null,line:this.yylineno})},lex:function(){var o=this.next();return o||this.lex()},begin:function(o){this.conditionStack.push(o)},popState:function(){var o=this.conditionStack.length-1;return o>0?this.conditionStack.pop():this.conditionStack[0]},_currentRules:function(){return this.conditionStack.length&&this.conditionStack[this.conditionStack.length-1]?this.conditions[this.conditionStack[this.conditionStack.length-1]].rules:this.conditions.INITIAL.rules},topState:function(o){return o=this.conditionStack.length-1-Math.abs(o||0),o>=0?this.conditionStack[o]:"INITIAL"},pushState:function(o){this.begin(o)},stateStackSize:function(){return this.conditionStack.length},options:{easy_keword_rules:!0},performAction:function(o,c,p,b){switch(p){case 0:return this.pushState("csv"),4;case 1:return 10;case 2:return 5;case 3:return 12;case 4:return this.pushState("escaped_text"),18;case 5:return 20;case 6:return this.popState("escaped_text"),18;case 7:return 19}},rules:[/^(?:sankey-beta\b)/,/^(?:$)/,/^(?:((\u000D\u000A)|(\u000A)))/,/^(?:(\u002C))/,/^(?:(\u0022))/,/^(?:([\u0020-\u0021\u0023-\u002B\u002D-\u007E])*)/,/^(?:(\u0022)(?!(\u0022)))/,/^(?:(([\u0020-\u0021\u0023-\u002B\u002D-\u007E])|(\u002C)|(\u000D)|(\u000A)|(\u0022)(\u0022))*)/],conditions:{csv:{rules:[1,2,3,4,5,6,7],inclusive:!1},escaped_text:{rules:[6,7],inclusive:!1},INITIAL:{rules:[0,1,2,3,4,5,6,7],inclusive:!0}}};return m}();u.lexer=k;function g(){this.yy={}}return g.prototype=u,u.Parser=g,new g}();it.parser=it;const Q=it;let X=[],q=[],B={};const qt=()=>{X=[],q=[],B={},wt()};class Kt{constructor(n,i,l=0){this.source=n,this.target=i,this.value=l}}const Zt=(t,n,i)=>{X.push(new Kt(t,n,i))};class Jt{constructor(n){this.ID=n}}const te=t=>(t=St.sanitizeText(t,rt()),B[t]||(B[t]=new Jt(t),q.push(B[t])),B[t]),ee=()=>q,ne=()=>X,ie=()=>({nodes:q.map(t=>({id:t.ID})),links:X.map(t=>({source:t.source.ID,target:t.target.ID,value:t.value}))}),se={nodesMap:B,getConfig:()=>rt().sankey,getNodes:ee,getLinks:ne,getGraph:ie,addLink:Zt,findOrCreateNode:te,getAccTitle:mt,setAccTitle:_t,getAccDescription:kt,setAccDescription:xt,getDiagramTitle:vt,setDiagramTitle:bt,clear:qt},pt=class st{static next(n){return new st(n+ ++st.count)}constructor(n){this.id=n,this.href=`#${n}`}toString(){return"url("+this.href+")"}};pt.count=0;let ft=pt;const re={left:Pt,right:Ct,center:It,justify:dt},oe=function(t,n,i,l){const{securityLevel:u,sankey:k}=rt(),g=Lt.sankey;let m;u==="sandbox"&&(m=Y("#i"+n));const s=u==="sandbox"?Y(m.nodes()[0].contentDocument.body):Y("body"),o=u==="sandbox"?s.select(`[id="${n}"]`):Y(`[id="${n}"]`),c=(k==null?void 0:k.width)??g.width,p=(k==null?void 0:k.height)??g.width,b=(k==null?void 0:k.useMaxWidth)??g.useMaxWidth,y=(k==null?void 0:k.nodeAlignment)??g.nodeAlignment,x=(k==null?void 0:k.prefix)??g.prefix,E=(k==null?void 0:k.suffix)??g.suffix,L=(k==null?void 0:k.showValues)??g.showValues;Et(o,p,c,b);const A=l.db.getGraph(),N=re[y],P=10;jt().nodeId(d=>d.id).nodeWidth(P).nodePadding(10+(L?15:0)).nodeAlign(N).extent([[0,0],[c,p]])(A);const S=At(Mt);o.append("g").attr("class","nodes").selectAll(".node").data(A.nodes).join("g").attr("class","node").attr("id",d=>(d.uid=ft.next("node-")).id).attr("transform",function(d){return"translate("+d.x0+","+d.y0+")"}).attr("x",d=>d.x0).attr("y",d=>d.y0).append("rect").attr("height",d=>d.y1-d.y0).attr("width",d=>d.x1-d.x0).attr("fill",d=>S(d.id));const M=({id:d,value:w})=>L?`${d}
${x}${Math.round(w*100)/100}${E}`:d;o.append("g").attr("class","node-labels").attr("font-family","sans-serif").attr("font-size",14).selectAll("text").data(A.nodes).join("text").attr("x",d=>d.x0<c/2?d.x1+6:d.x0-6).attr("y",d=>(d.y1+d.y0)/2).attr("dy",`${L?"0":"0.35"}em`).attr("text-anchor",d=>d.x0<c/2?"start":"end").text(M);const $=o.append("g").attr("class","links").attr("fill","none").attr("stroke-opacity",.5).selectAll(".link").data(A.links).join("g").attr("class","link").style("mix-blend-mode","multiply"),C=(k==null?void 0:k.linkColor)||"gradient";if(C==="gradient"){const d=$.append("linearGradient").attr("id",w=>(w.uid=ft.next("linearGradient-")).id).attr("gradientUnits","userSpaceOnUse").attr("x1",w=>w.source.x1).attr("x2",w=>w.target.x0);d.append("stop").attr("offset","0%").attr("stop-color",w=>S(w.source.id)),d.append("stop").attr("offset","100%").attr("stop-color",w=>S(w.target.id))}let I;switch(C){case"gradient":I=d=>d.uid;break;case"source":I=d=>S(d.source.id);break;case"target":I=d=>S(d.target.id);break;default:I=C}$.append("path").attr("d",Xt()).attr("stroke",I).attr("stroke-width",d=>Math.max(1,d.width))},le={draw:oe},ae=t=>t.replaceAll(/^[^\S\n\r]+|[^\S\n\r]+$/g,"").replaceAll(/([\n\r])+/g,`
`).trim(),ce=Q.parse.bind(Q);Q.parse=t=>ce(ae(t));const ye={parser:Q,db:se,renderer:le};export{ye as diagram};
