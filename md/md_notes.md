# Markdown 常用公式编辑
Markdown编辑器中用Latex语法来编辑公式方便高效，这里记录下常用的表示。
# 1.  基本用法
## 1.1 呈现位置
`$...$` 用来在在文本中嵌入显示，比如`$\sum_{i=0}^N{X_i}$`的效果为： $\sum_{i=0}^N{X_i}$ 其是嵌入在文本中间来呈现的。而`$$....$$`则为隔行居中显示， `$$\sum_{i=0}^N{X_i}$$`的显示效果：
$$
\sum_{i=0}^N{X_i}
$$
## 1.2 常用希腊字母表示
大写 | markdown | 小写 | markdown
-------|-------|-------|-------
$A$ | `$A$`  |  $\alpha$  | `$\alpha$`
$B$ | `$B$` |  $\beta$ | `$\beta$`
$\Gamma$ | `$\Gamma$` | $\gamma$ | `$\gamma$`
$\Delta$ | `$\Delta$` | $\delta$ | `$\delta$`
$E$ | `$E$` | $\epsilon$ | `$\epsilon$` 
$Z$ | `$Z$` | $\zeta$ | `$\zeta$`
$H$ | `$H$` | $\eta$ |  `$\eta$`       
$\Theta$ | `$\Theta$` | $\theta$ | `$\theta$` 
$K$ | `$K$` | $\kappa$ | `$kappa$`
$\Lambda$ | `$\Lambda$` | $\lambda$ | `$\lambda$`
$M$ | `$M$` | $\mu$ | `$\mu$`
$N$ | `$N$` | $\nu$ | `$\nu$`
$\Xi$ | `$\Xi$` | $\xi$ | `$\xi$`
$O$ | `$O$` | $\omicron$ | `$\omicron$`
$\Pi$ | `$\Pi$` | $\pi$ | `$\pi$`
$P$ | `$P$` | $\rho$ | `$\rho$`
$\Sigma$ | `$\Sigma$` | $\sigma$ | `$\sigma$`
$T$ | `$T$` | $\tau$ | `$\tau$`
$\Upsilon$ | `$\Upsilon$` | $\upsilon$ | `$\upsilon$`
$\Omega$ | `$\Omega$` | $\omega$ | `$\omega$`
$\Phi$ | `$\Phi$` | $\phi$ | `$\phi$`
$\Psi$ | `$\Psi$` | $\psi$ | `$\psi$`
$X$ | `$X$` | $\chi$ | `$\chi$`

首字母大写即为大写表示:     `$\Nu$` $\Nu$
加var前缀则斜体:   `$\vartheta$` $\vartheta$ 

## 1.3 上下标
_表示下标，^表示上标
源码 |呈现
----|----
`$x_1$` |  $x_1$ 
`$i^2$` |  $i^2$
`$\sum_{i=0}^{n}$` | $\sum_{i=0}^{n}$

## 1.4 矢量
利用\vec  和\overrightarrow （注意空格）
源码 | 呈现
----|----
`$\vec {a}$` | $\vec {a}$
$\vec {a+b}$ | $\vec {a+b}$
`$\overrightarrow {a+b}$` | $\overrightarrow {a+b}$

## 1.5 分组与括号
利用{}来进行分组，分组就是将{}内看做一个整体的意思， 比如不分组时`$10^20$` 效果为$10^20$
可以看到20被分隔开了，10的20次方正确的写法应该为`$10^{20}$`    效果：$10^{20}$
接下来是括号：

源码 | 呈现
:----|----
小括号`$(a+b+c)$` |   $(a+b+c)$
中括号`$[a\ b\ c]$` |   $[a\ b\ c]$
无空格 `$[a b c]$` |   $[a b c]$
尖括号`$< \overrightarrow {xyz}>$` | $< \overrightarrow {xyz}>$

## 1.6   求和，极限，积分，分式，根式
源码 | 呈现
:----|----
求和`$\sum_{i=1}^{N}{W_i*X_i+b_i}$`  |  $\sum_{i=1}^{N}{W_i*X_i+b_i}$
极限`$\lim_{x \to 0}{f(x)}$`|  $\lim_{x \to 0}{f(x)}$
积分`$\int_0^\infty{f(x)dx}$`| $\int_0^\infty{f(x)dx}$
分式`$\frac {x+y}{x_0+y_0}$`| $\frac {x+y}{x_0+y_0}$
根式`$\sqrt[x]{y}$` | $\sqrt[x]{y}$  
求导`$f^\prime$` | $f^\prime$ 

## 1.7  常用函数
源码 | 呈现
----|----
`$\sin{(w*x+b)}$`   |    $\sin{(w*x+b)}$
`$\cos{(w*x+b)}$`   |    $\cos{(w*x+b)}$
`$\tan{(w*x+b)}$`   |    $\tan{(w*x+b)}$
`$\ln{(w*x+b)}$`   |    $\ln{(w*x+b)}$
`$\max{(w*x+b)}$`   |    $\max{(w*x+b)}$
`$\min{(w*x+b)}$`   |    $\min{(w*x+b)}$
`$\lg$` | $\lg$ 
`$\log$` | $\log$ 
`\exp` | $\exp$ 

其他函数就按自己想象写就行了比如softmax 函数:
`$$softmax(x_i) = \frac {e^{x_i}}{\sum_{j=0}^N{e^x_j}}$$`
$$softmax(x_i) = \frac {e^{x_i}}{\sum_{j=0}^N{e^x_j}}$$

##  1.8  算式与特殊符号
源码 | 呈现 | 描述
----|---- | ----
`$\pm$`| $\pm$ | 正负号
`$\div$`| $\div$ | 除号
`$\times$`| $\times$ | 乘号
`$\otimes$`| $\otimes$ | 克罗内克积 
`$\bigotimes$`| $\bigotimes$ | 克罗内克积 
`$\mid$`| $\mid$ | 竖线
`$\cdot$`| $\cdot$ | 点
`$\cdots$`| $\cdots$ | 省略号
`$\vdots$`| $\vdots$ | 省略号 
`$\ddots$`| $\ddots$ | s省略号 
`$\circ$`| $\circ$ | 圈
`$\ast$`| $\ast$ | 星 
`$\nabla$`| $\nabla$ | 梯度 
` $\sum$`| $\sum$ | 求和 
`$\int$`| $\int$ | 求积分 
`$\iint$`| $\iint$ | 双重积分 
`$\oint$`| $\oint$ | 曲线积分 
` $\prod$`| $\prod$ | N元乘积 
`$\coprod$`| $\coprod$ | N元余积 
` $\leq$`| $\leq$ | 小于等于 
`$\neq$`| $\neq$ | 不等于 
`$\geq$`| $\geq$ | 大于等于 
`$\approx$`| $\approx$ | 约等于 
`$\infty$`|$\infty$ | 无穷 
`$\to$`|$\to$ | 趋势于 
`$\because$`|$\because$ | 因为 
`$\therefore$`|$\therefore$ | 所以 
`$\vee$`| $\vee$ | 逻辑或 
`$\wedge$`| $\wedge$ | 逻辑与 
`$\bigoplus$`| $\bigoplus$ | 异或 
`$\subset$`| $\subset$ | 子集 
`$\subseteq$`| $\subseteq$ | 真子集 
`$\not\subset$`| $\not\subset$  | 不属于 
`$\supset$`| $\supset$ | 
`$\supseteq$`| $\supseteq$ | 
`$\cup$`|  $\cup$ | 并集 
`$\cap$`| $\cap$ | 交集 
`$\in$`| $\in$ | 属于 
`$\notin$`| $\notin$ | 不属于 
`$\varnothing$`| $\varnothing$ | 
`$\emptyset$`| $\emptyset$ | 空集 
`$\forall$`| $\forall$ | 任意 
`$\exist$`| $\exist$ | 存在 
`$\lnot$`| $\lnot$ | 
`$\partial$`|$\partial$ | 
`$\hat{y}$`|$\hat{y}$ | 期望值 
`$\check{y}$`|$\check{y}$ |  
`$\overline{a+b+c+d}$`|$\overline{a+b+c+d}$ | 平均值 
`$\underline{a+b+c+d}$`|$\underline{a+b+c+d}$ |  
`\overbrace{a+\underbrace{b+c}_{1.0}+d}^{2.0}`|$\overbrace{a+\underbrace{b+c}_{1.0}+d}^{2.0}$ |  
`$\lbrace \rbrace$`|$\lbrace \rbrace$ |  

## 1.9  块
### 1.9.1 矩阵

`\begin{matrix}` 标识开始
`\end{matrix}`   标识结束
`pmatrix` 小括号外框
`bmatrix` 中括号外框
`Bmatrix` 大括号外框
`vmatrix` 单竖线外框
`Vmatrix` 双竖线外框

`\\` 行结尾
`&`元素分割
`\cdots` 横向省略号
`\vdots` 竖向省略号
`\ddots` 斜向省略号

例1：
$$
\begin{bmatrix}
a_{00}&a_{01}\\
a_{10}&a_{11}\\
\end{bmatrix}
$$
例2：
$$
A_{mn}=
\begin{vmatrix}
a_{00}&a_{01}&{\cdots}&{a_{0n}}\\
a_{10}&a_{11}&{\cdots}&{a_{1n}}\\
{\vdots}&{\vdots}&{\ddots}&{\vdots}\\
a_{m0}&a_{m1}&{\cdots}&{a_{mn}}\\
\end{vmatrix}
$$
### 1.9.2 分段函数

示例：
$$
X(m,n) =
\begin{cases}
x(n+1) & x \leq -1, \\
x(n) & -1 < x < 1, \\
x(n-1) & x \geq 1
\end{cases}
$$


## 1.10  方程组

例：
$$
\begin{cases}
a_1x+b_1y+c_1z=d_1\\
a_2x+b_2y+c_2z=d_2\\
a_3x+b_3y+c_3z=d_3\\
\end{cases}
$$

## 1.11 箭头符号

### 1.11.1 基本箭头

| 符号 | MarkDown |
| ---- | -------- |
| $\uparrow$ | `$\uparrow$` |
| $\Uparrow$ | `$\Uparrow$` |
| $\downarrow$ | `$\downarrow$` |
| $\Downarrow$ | `$\Downarrow$` |
| $\leftarrow$ | `$\leftarrow$` |
| $\Leftarrow$ | `$\Leftarrow$` |
| $\rightarrow$ | `$\rightarrow$` |
| $\Rightarrow$ | `$\Rightarrow$` |
| $\updownarrow$ | `$\updownarrow$` |
| $\Updownarrow$ | `$\Updownarrow$` |
| $\leftrightarrow$ | `$\leftrightarrow$` |

### 1.11.2 长箭头

| 符号 | MarkDown |
| ---- | -------- |
| $\longleftarrow$ | `$\longleftarrow$` |
| $\Longleftarrow$ | `$\Longleftarrow$` |
| $\longrightarrow$ | `$\longrightarrow$` |
| $\Longrightarrow$ | `$\Longrightarrow$` |
| $\longleftrightarrow$ | `$\longleftrightarrow$` |
| $\Longleftrightarrow$ | `$\Longleftrightarrow$` |

### 1.11.3 更多

| 符号 | MarkDown |
| ---- | -------- |
| $\twoheadrightarrow$ | `$\twoheadrightarrow$` |
| $\rightarrowtail$ | `$\rightarrowtail$` |
| $\looparrowright$ | `$\looparrowright$` |
| $\curvearrowright$ | `$\curvearrowright$` |
| $\circlearrowright$ | `$\circlearrowright$` |
| $\Rsh$ | `$\Rsh$` |
| $\multimap$ | `$\multimap$` |
| $\leftrightsquigarrow$ | `$\leftrightsquigarrow$` |
| $\rightsquigarrow$ | `$\rightsquigarrow$` |
| $\leadsto$ | `$\leadsto$` |
| $\nearrow$ | `$\nearrow$` |
| $\searrow$ | `$\searrow$` |
| $\swarrow$ | `$\swarrow$` |
| $\nwarrow$ | `$\nwarrow$` |
| $\nleftarrow$ | `$\nleftarrow$` |
| $\nrightarrow$ | `$\nrightarrow$` |
| $\nLeftarrow$ | `$\nLeftarrow$` |
| $\nRightarrow$ | `$\nRightarrow$` |
| $\nleftrightarrow$ | `$\nleftrightarrow$` |
| $\nLeftrightarrow$ | `$\nLeftrightarrow$` |
| $\dashrightarrow$ | `$\dashrightarrow$` |
| $\dashleftarrow$ | `$\dashleftarrow$` |
| $\leftleftarrows$ | `$\leftleftarrows$` |
| $\leftrightarrows$ | `$\leftrightarrows$` |
| $\Lleftarrow$ | `$\Lleftarrow$` |
| $\twoheadleftarrow$ | `$\twoheadleftarrow$` |
| $\leftarrowtail$ | `$\leftarrowtail$` |
| $\looparrowleft$ | `$\looparrowleft$` |
| $\curvearrowleft$ | `$\curvearrowleft$` |
| $\circlearrowleft$ | `$\circlearrowleft$` |
| $\Lsh$ | `$\Lsh$` |
| $\mapsto$ | `$\mapsto$` |
| $\hookleftarrow$ | `$\hookleftarrow$` |
| $\hookrightarrow$ | `$\hookrightarrow$` |
| $\upharpoonright$ | `$\upharpoonright$` |
| $\upharpoonleft$ | `$\upharpoonleft$` |
| $\downharpoonright$ | `$\downharpoonright$` |
| $\downharpoonleft$ | `$\downharpoonleft$` |
| $\leftharpoonup$ | `$\leftharpoonup$` |
| $\rightharpoonup$ | `$\rightharpoonup$` |
| $\leftharpoondown$ | `$\leftharpoondown$` |
| $\rightharpoondown$ | `$\rightharpoondown$` |
| $\upuparrows$ | `$\upuparrows$` |
| $\downdownarrows$ | `$\downdownarrows$` |
| $\rightrightarrows$ | `$\rightrightarrows$` |
| $\rightleftarrows$ | `$\rightleftarrows$` |
| $\rightrightarrows$ | `$\rightrightarrows$` |
| $\rightleftarrows$ | `$\rightleftarrows$` |
| $\rightleftharpoons$ | `$\rightleftharpoons$` |