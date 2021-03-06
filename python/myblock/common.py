#/usr/bin/env python

# constant variables
MAX_X = 12
MAX_Y = 20

BLOCK_WIDTH = 22
BLOCK_HEIGHT = 22

NUM_LEVELS = 20
NUM_HIGHSCORE = 10

# start level value
START_LEVEL_VALUE = 6

# Global variables
game_area = None
next_block_area = None
game_over = True
game_pause = False
current_x = 0
current_y = 0
current_block = 0
current_frame = 0
current_score = 0
current_level = 0
current_lines = 0
next_block = 0
next_frame = 0
options = {"level":6, "noise_l":0, "noise_h":0, "shw_nxt":False}

blocks_pixmap = None
# XPM 
blocks_xpm = [
"176 22 198 2",
"  	c None",
". 	c #000000",
"+ 	c #6161EC",
"@ 	c #6161F0",
"# 	c #6161E8",
"$ 	c #6161E3",
"% 	c #6161DF",
"& 	c #6161D5",
"* 	c #2F4891",
"= 	c #61ED62",
"- 	c #61EF62",
"; 	c #61EB62",
"> 	c #61E962",
", 	c #61E662",
"' 	c #61E262",
") 	c #61DD62",
"! 	c #61D962",
"~ 	c #61BD62",
"{ 	c #437F0B",
"] 	c #EF6162",
"^ 	c #EB6162",
"/ 	c #ED6162",
"( 	c #E96162",
"_ 	c #E46162",
": 	c #E26162",
"< 	c #DB6162",
"[ 	c #D96162",
"} 	c #9B1C09",
"| 	c #EDEDEC",
"1 	c #EFEFF0",
"2 	c #EBEBEC",
"3 	c #E9E9E8",
"4 	c #E4E4E3",
"5 	c #E2E2E3",
"6 	c #DBDBDA",
"7 	c #D9D9DA",
"8 	c #BDBDBC",
"9 	c #727272",
"0 	c #ED61EC",
"a 	c #EF61F0",
"b 	c #EB61EC",
"c 	c #E961E8",
"d 	c #E661E8",
"e 	c #E461E3",
"f 	c #E261E3",
"g 	c #DD61DF",
"h 	c #D961DA",
"i 	c #9B039B",
"j 	c #61EDEC",
"k 	c #61EFF0",
"l 	c #61EBEC",
"m 	c #61E9E8",
"n 	c #61E6E8",
"o 	c #61E4E3",
"p 	c #61E2E3",
"q 	c #61DDDF",
"r 	c #61D9DA",
"s 	c #61BDBC",
"t 	c #039B93",
"u 	c #EDED62",
"v 	c #EFEF62",
"w 	c #EBEB62",
"x 	c #E9E962",
"y 	c #E6E662",
"z 	c #E4E462",
"A 	c #E2E262",
"B 	c #DDDD62",
"C 	c #D9D962",
"D 	c #9B9903",
"E 	c #6161DA",
"F 	c #6161C6",
"G 	c #61E062",
"H 	c #61DB62",
"I 	c #61D462",
"J 	c #61C262",
"K 	c #61B562",
"L 	c #E06162",
"M 	c #DD6162",
"N 	c #D66162",
"O 	c #C26162",
"P 	c #E0E0DF",
"Q 	c #DDDDDF",
"R 	c #D6D6D5",
"S 	c #C5C5C6",
"T 	c #B5B5B6",
"U 	c #E061DF",
"V 	c #DB61DA",
"W 	c #D461D5",
"X 	c #C561C6",
"Y 	c #61E0DF",
"Z 	c #61DBDA",
"` 	c #61D4D5",
" .	c #61C5C6",
"..	c #61B5B6",
"+.	c #E0E062",
"@.	c #DBDB62",
"#.	c #D4D462",
"$.	c #C5C562",
"%.	c #6161D0",
"&.	c #6161C1",
"*.	c #61D662",
"=.	c #61D162",
"-.	c #61CF62",
";.	c #61C062",
">.	c #D46162",
",.	c #CF6162",
"'.	c #C06162",
").	c #F1F1F0",
"!.	c #D4D4D5",
"~.	c #CFCFD0",
"{.	c #CCCCCB",
"].	c #C0C0C1",
"^.	c #D661D5",
"/.	c #CF61D0",
"(.	c #D161D0",
"_.	c #CC61CB",
":.	c #C061C1",
"<.	c #61D6D5",
"[.	c #61D1D0",
"}.	c #61CCCB",
"|.	c #61C0C1",
"1.	c #D6D662",
"2.	c #D1D162",
"3.	c #CCCC62",
"4.	c #C0C062",
"5.	c #6161CB",
"6.	c #61CC62",
"7.	c #61B262",
"8.	c #D16162",
"9.	c #CC6162",
"0.	c #E6E6E8",
"a.	c #D1D1D0",
"b.	c #B2B2B1",
"c.	c #61CFD0",
"d.	c #61C2C1",
"e.	c #61B2B1",
"f.	c #CFCF62",
"g.	c #C2C262",
"h.	c #6161BC",
"i.	c #61E462",
"j.	c #61B062",
"k.	c #BD6162",
"l.	c #B0B0B1",
"m.	c #BD61BC",
"n.	c #61B0B1",
"o.	c #BDBD62",
"p.	c #61CA62",
"q.	c #CA6162",
"r.	c #CACACB",
"s.	c #CA61CB",
"t.	c #61CACB",
"u.	c #CACA62",
"v.	c #C76162",
"w.	c #BA6162",
"x.	c #C7C7C6",
"y.	c #C761C6",
"z.	c #C7C762",
"A.	c #61BA62",
"B.	c #61AD62",
"C.	c #E66162",
"D.	c #BABABC",
"E.	c #ADADAC",
"F.	c #BA61BC",
"G.	c #61BABC",
"H.	c #61ADAC",
"I.	c #BABA62",
"J.	c #61C762",
"K.	c #C56162",
"L.	c #61C7C6",
"M.	c #61C562",
"N.	c #61AA62",
"O.	c #B86162",
"P.	c #AAAAAC",
"Q.	c #61AAAC",
"R.	c #6161B6",
"S.	c #61B862",
"T.	c #B8B8B6",
"U.	c #B861B6",
"V.	c #61B8B6",
"W.	c #B8B862",
"X.	c #B26162",
"Y.	c #C2C2C1",
"Z.	c #C261C1",
"`.	c #B261B1",
" +	c #B2B262",
".+	c #6161B1",
"++	c #6161AC",
"@+	c #B56162",
"#+	c #B06162",
"$+	c #AD6162",
"%+	c #AA6162",
"&+	c #B561B6",
"*+	c #B061B1",
"=+	c #AD61AC",
"-+	c #AA61AC",
";+	c #B5B562",
">+	c #B0B062",
",+	c #ADAD62",
". . . . . . . . . . . . . . . . . . . . . . + @ @ + @ @ + + + # # # $ $ $ $ $ $ % & & * = = - - - - ; ; = > > > , , ' ' ' ) ) ! ~ { ] ] ] ] ] ] ^ / / ( ( ( _ _ _ : : : < [ [ } | | 1 | | 2 2 | 3 3 3 4 4 4 5 5 5 6 6 7 8 9 0 a a 0 a a b 0 0 c c c d e e f f f g h h i j j k j j k l j m m m n n o p p p q q r s t u v v v v v w u u x x x y z z A A A B C C D ",
". . . . . . . . . . . . . . . . . . . . . . @ + + + # # $ # # % $ $ % % % E E E & F F * - - - ; ; > , , , G G G ) ) ! ! H I I J K { / ] ] ^ ( ( _ _ _ L L L M < < [ < < N O O } 1 1 | 2 2 4 4 4 P P P Q Q 6 7 7 6 R R S T 9 a a a b c c e e e U U U g V V h V V W X X i k k k l l m o o Y Y Y q q q r r Z ` `  ...t v v v w x x y y y +.+.+.B B B C @.@.#.$.$.D ",
". . . . . . . . . . . . . . . . . . . . . . @ + + % % % % % % E & & & & & %.%.%.%.&.&.* - - ; G G ) ) ) ) H H *.I I =.=.=.-.-.;.K { ] ( ( L L L L < < [ [ [ N >.>.,.,.,.,.'.'.} ).).2 P P P P 6 7 7 7 R R !.~.~.~.{.{.].T 9 a b b U U U U V V h ^.^.^.W W /.(.(._.:.:.i k k l Y Y Y Y Z r r <.` ` ` [.[.[.}.}.|...t v w w +.B B B B B @.1.1.#.#.#.2.2.2.3.4.4.D ",
". . . . . . . . . . . . . . . . . . . . . . @ + + % % % % % % E & & & & & %.%.%.%.&.&.* - - ; G G ) ) ) ) H H *.I I =.=.=.-.-.;.K { ] ( ( L L L L < < [ [ [ N >.>.,.,.,.,.'.'.} ).).2 P P P P 6 7 7 7 R R !.~.~.~.{.{.].T 9 a b b U U U U V V h ^.^.^.W W /.(.(._.:.:.i k k l Y Y Y Y Z r r <.` ` ` [.[.[.}.}.|...t v w w +.B B B B B @.1.1.#.#.#.2.2.2.3.4.4.D ",
". . . . . . . . . . . . . . . . . . . . . . + # # % % % E E E & & & & & & %.%.%.5.&.&.* - - , G G G ) ) H *.*.! *.*.-.-.=.6.6.;.7.{ ] ( ( L M M < M M [ N N >.>.>.8.8.8.9.'.'.} | | 0.P P 6 6 Q 7 7 R !.!.!.a.a.a.{.{.].b.9 0 c c U g g V g g h h h W ^.^.(././._.:.:.i j j m Y Y q Z q r r r <.<.<.c.c.[.}.}.d.e.t v y y +.+.+.B @.@.1.C C 1.1.1.f.2.2.3.g.g.D ",
". . . . . . . . . . . . . . . . . . . . . . + # # % E E % E E E & & & %.%.%.5.5.5.h.h.* = = i.) ) H ) ) H ! ! *.I I -.-.-.-.-.;.7.{ / _ _ L < < < [ [ [ N N N 8.8.,.,.,.9.'.'.} | | 4 Q Q 6 6 7 7 7 R R R a.~.~.~.~.~.].b.9 b e e g V V V h h h ^.^.W (.(.(./././.:.:.i l l o q q Z Z r r r <.` ` ` c.c.c.}.}.|.e.t u z z B @.@.B @.@.C 1.1.#.#.#.f.f.f.3.4.4.D ",
". . . . . . . . . . . . . . . . . . . . . . + # # % E E % E E E & & & %.%.%.5.5.5.h.h.* = = i.) ) H ) ) H ! ! *.I I -.-.-.-.-.;.7.{ / _ _ L < < < [ [ [ N N N 8.8.,.,.,.9.'.'.} | | 4 Q Q 6 6 7 7 7 R R R a.~.~.~.~.~.].b.9 b e e g V V V h h h ^.^.W (.(.(./././.:.:.i l l o q q Z Z r r r <.` ` ` c.c.c.}.}.|.e.t u z z B @.@.B @.@.C 1.1.#.#.#.f.f.f.3.4.4.D ",
". . . . . . . . . . . . . . . . . . . . . . + $ $ % E E E E E & & & %.& & %.%.%.%.&.&.* = = i.) ) H ! ! H *.*.*.I I =.=.6.-.-.~ j.{ / _ _ M < < [ < < N >.>.8.>.>.8.9.9.,.k.k.} | | 4 Q Q 7 7 6 R R !.a.a.!.a.a.{.~.~.8 l.9 0 e e g h h h V V ^.W W W W W /._._./.m.m.i j j o q q Z Z Z <.<.` ` ` ` [.[.}.c.c.s n.t u z z B @.@.C @.@.1.1.1.#.#.#.2.3.3.f.o.o.D ",
". . . . . . . . . . . . . . . . . . . . . . # % % E E E E E E & & & %.%.%.5.%.%.F h.h.* > > ' ! ! H ! ! *.I I *.=.=.6.6.-.p.p.~ j.{ ( : : < < < [ N N N N N 8.,.,.9.,.,.q.'.'.} 0.0.5 6 6 7 7 R R R R a.a.~.~.~.~.r.r.8 l.9 d f f V V V h ^.^.^.W W (.(.(./././.s.m.m.i n n p r r r r <.<.<.` [.[.[.c.c.c.t.t.s n.t x A A C @.@.C 1.1.#.1.1.2.2.2.f.f.f.u.o.o.D ",
". . . . . . . . . . . . . . . . . . . . . . # % % E E E E E E & & & %.%.%.5.%.%.F h.h.* > > ' ! ! H ! ! *.I I *.=.=.6.6.-.p.p.~ j.{ ( : : < < < [ N N N N N 8.,.,.9.,.,.q.'.'.} 0.0.5 6 6 7 7 R R R R a.a.~.~.~.~.r.r.8 l.9 d f f V V V h ^.^.^.W W (.(.(./././.s.m.m.i n n p r r r r <.<.<.` [.[.[.c.c.c.t.t.s n.t x A A C @.@.C 1.1.#.1.1.2.2.2.f.f.f.u.o.o.D ",
". . . . . . . . . . . . . . . . . . . . . . # % % E & & & & & & & & %.%.%.%.5.5.5.&.&.* , , G ! ! *.*.*.*.*.*.I =.=.-.-.p.p.p.~ j.{ ( L L N N N >.N N >.>.>.8.8.8.,.9.9.v.w.w.} 3 3 P R R !.!.R !.!.!.a.a.a.{.{.r.x.x.8 l.9 c U U ^.^.^.W W W W W W W /./._.s.s.y.m.m.i m m Y r r <.` <.` ` ` [.[.c.}.}.}.t.t.s n.t y +.+.C 1.1.1.1.1.1.#.#.2.f.f.3.3.3.z.o.o.D ",
". . . . . . . . . . . . . . . . . . . . . . # E E & & & & %.%.& %.%.%.5.5.5.5.5.F h.h.* , , ) *.*.I *.*.=.I I =.=.=.-.-.p.p.p.A.B.{ C.M M N N N >.>.>.>.8.8.,.9.9.,.9.9.q.w.w.} 0.0.Q R R !.!.!.!.!.a.~.~.{.~.~.{.r.r.D.E.9 d g g ^.^.^.^.W W W /./.(._._./._._.s.F.F.i n n q <.<.<.` [.` ` [.[.[.}.}.}.t.t.t.G.H.t y B B 1.#.#.1.2.2.#.2.2.2.3.3.3.3.3.u.I.I.D ",
". . . . . . . . . . . . . . . . . . . . . . # E E & & & & %.%.& %.%.%.5.5.5.5.5.F h.h.* , , ) *.*.I *.*.=.I I =.=.=.-.-.p.p.p.A.B.{ C.M M N N N >.>.>.>.8.8.,.9.9.,.9.9.q.w.w.} 0.0.Q R R !.!.!.!.!.a.~.~.{.~.~.{.r.r.D.E.9 d g g ^.^.^.^.W W W /./.(._._./._._.s.F.F.i n n q <.<.<.` [.` ` [.[.[.}.}.}.t.t.t.G.H.t y B B 1.#.#.1.2.2.#.2.2.2.3.3.3.3.3.u.I.I.D ",
". . . . . . . . . . . . . . . . . . . . . . $ % % & %.%.%.& & %.%.%.5.%.%.5.5.5.F h.h.* i.i.) I I I =.=.I =.=.-.6.6.p.p.p.J.J.~ B.{ _ M M >.8.8.8.8.8.,.,.,.,.,.,.q.q.q.K.w.w.} 4 4 Q !.!.a.a.a.~.~.~.~.~.~.r.r.r.S S D.E.9 e g g W (.(.(.(.(.(.(.(._././.s.s.s.X F.F.i o o Z ` ` [.` ` [.[.c.}.}.c.}.}.t.L.L.s n.t z B B #.#.#.2.#.#.2.f.f.3.f.f.3.u.u.$.I.I.D ",
". . . . . . . . . . . . . . . . . . . . . . $ E E %.& & %.%.%.%.%.%.5.5.5.5.F F F h.h.* ' ' ) =.=.I =.=.=.-.-.-.6.6.6.6.J.M.M.A.N.{ : M M 8.>.>.8.8.8.,.9.9.9.q.q.q.v.v.v.O.O.} 5 5 6 a.a.a.a.a.~.~.{.{.{.r.r.r.x.S S D.P.9 f V V (.(.(.(././._._._._.s.s.s.y.y.X F.F.i p p Z [.[.[.[.[.c.c.c.}.}.t.}.}.L. . .G.Q.t A B B 2.#.#.2.2.2.f.f.f.3.u.u.u.z.z.z.I.I.D ",
". . . . . . . . . . . . . . . . . . . . . . $ E E %.& & %.%.%.%.%.%.5.5.5.5.F F F h.h.* ' ' ) =.=.I =.=.=.-.-.-.6.6.6.6.J.M.M.A.N.{ : M M 8.>.>.8.8.8.,.9.9.9.q.q.q.v.v.v.O.O.} 5 5 6 a.a.a.a.a.~.~.{.{.{.r.r.r.x.S S D.P.9 f V V (.(.(.(././._._._._.s.s.s.y.y.X F.F.i p p Z [.[.[.[.[.c.c.c.}.}.t.}.}.L. . .G.Q.t A B B 2.#.#.2.2.2.f.f.f.3.u.u.u.z.z.z.I.I.D ",
". . . . . . . . . . . . . . . . . . . . . . % E E %.%.%.5.%.%.5.5.5.5.5.5.F F F F R.R.* ) ) ! =.=.-.-.-.-.6.6.p.6.6.J.J.M.J.J.S.B.{ L [ [ 8.8.8.,.,.,.q.9.9.q.q.q.v.v.v.K.w.w.} P P 7 ~.~.~.~.~.r.r.{.{.{.r.x.x.S x.x.T.E.9 U h h /.(.(./././._._._._.s.s.y.y.y.y.U.U.i Y Y r c.c.c.}.c.t.t.t.}.}.t.L.L. .L.L.V.n.t B C C 2.f.f.f.f.f.3.u.u.3.u.u.z.z.z.$.W.W.D ",
". . . . . . . . . . . . . . . . . . . . . . % & & 5.%.%.5.5.5.%.5.5.F F F F F F F R.R.* ) ) I 6.6.6.6.6.p.-.-.p.J.J.J.J.M.J.J.A.N.{ M N N q.9.9.9.9.9.,.q.q.v.K.K.K.K.K.K.w.w.} P P R {.{.{.{.{.~.~.r.x.x.S x.x.S x.x.T.P.9 U ^.^._._._./._._./.s.s.y.X X X X X y.F.F.i Y Y <.}.}.c.}.}.c.c.t.L.L. .L.L. . . .V.H.t B #.#.3.3.3.3.u.u.f.u.u.z.z.z.$.z.z.$.W.W.D ",
". . . . . . . . . . . . . . . . . . . . . . % & & 5.%.%.5.5.5.%.5.5.F F F F F F F R.R.* ) ) I 6.6.6.6.6.p.-.-.p.J.J.J.J.M.J.J.A.N.{ M N N q.9.9.9.9.9.,.q.q.v.K.K.K.K.K.K.w.w.} P P R {.{.{.{.{.~.~.r.x.x.S x.x.S x.x.T.P.9 U ^.^._._._./._._./.s.s.y.X X X X X y.F.F.i Y Y <.}.}.c.}.}.c.c.t.L.L. .L.L. . . .V.H.t B #.#.3.3.3.3.u.u.f.u.u.z.z.z.$.z.z.$.W.W.D ",
". . . . . . . . . . . . . . . . . . . . . . E %.%.&.&.&.&.h.h.h.h.h.h.h.h.h.h.h.h.R.R.* ) ) -.J J ;.;.;.;.~ ~ ~ A.A.A.A.S.S.S.7.N.{ M ,.,.O '.'.'.k.k.k.k.k.w.w.w.w.O.O.O.X.X.} 6 6 ~.Y.Y.].].8 8 8 D.D.D.D.T.T.T.T.T.T P.9 V /./.Z.:.:.:.m.m.m.F.F.F.F.F.F.U.U.U.`.`.i Z Z c.d.d.|.|.s s s s G.G.G.G.G.V.G.G.e.Q.t B f.f.g.4.4.4.4.4.o.o.o.I.I.I.I.W.W.I. + +D ",
". . . . . . . . . . . . . . . . . . . . . . & h.h..+R.R..+.+.+.+++++.+++++++++++++++++* I I A.7.7.K 7.7.7.j.j.j.7.7.B.B.B.N.N.j.B.{ >.w.w.X.@+@+X.#+#+#+#+#+#+$+$+$+$+$+%+$+$+} !.!.D.b.b.b.b.l.l.l.l.l.l.E.E.E.E.P.P.E.E.9 W F.F.`.&+&+`.*+*+*+*+*+*+=+=+=+=+=+-+=+=+i ` ` G.e.e.....e.n.n.n.e.e.H.H.H.H.H.H.H.H.t #.I.I. +;+;+ + + +>+>+>+>+,+,+,+,+,+,+,+,+D ",
". . . . . . . . . . . . . . . . . . . . . . * * * * * * * * * * * * * * * * * * * * * * { { { { { { { { { { { { { { { { { { { { { { } } } } } } } } } } } } } } } } } } } } } } 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 9 i i i i i i i i i i i i i i i i i i i i i i t t t t t t t t t t t t t t t t t t t t t t D D D D D D D D D D D D D D D D D D D D D D "]


