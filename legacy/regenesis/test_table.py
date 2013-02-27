# -*- coding: utf-8 -*-

import unittest

import table


MIKROZENSUS_11111_0001 = """GENESIS-Tabelle: Temporär
Gebietsfläche: Bundesländer, Stichtag;;;;;;;;;;;;;
Feststellung des Gebietsstands;;;;;;;;;;;;;
Gebietsfläche (qkm);;;;;;;;;;;;;
;Stichtag;Stichtag;Stichtag;Stichtag;Stichtag;Stichtag;Stichtag;Stichtag;Stichtag;Stichtag;Stichtag;Stichtag;Stichtag
;31.12.1995;31.12.1996;31.12.1997;31.12.1998;31.12.1999;31.12.2000;31.12.2001;31.12.2002;31.12.2003;31.12.2004;31.12.2005;31.12.2006;31.12.2007
Baden-Württemberg;35752,50;35751,76;35751,85;35751,63;35751,36;35751,36;35751,64;35751,64;35751,65;35751,64;35751,65;35751,50;35751,40
Bayern;70550,87;70550,87;70548,00;70547,96;70547,81;70547,85;70549,93;70549,32;70549,19;70549,44;70551,57;70551,57;70551,56
Berlin;890,82;890,85;890,77;890,22;891,41;891,69;891,76;891,75;891,75;891,82;891,85;891,02;891,02
Thüringen;16171,12;16170,88;16171,57;16171,70;16171,85;16171,98;16171,94;16172,21;16172,14;16172,08;16172,10;16172,14;16172,10
Insgesamt;357022,31;357021,43;357020,79;357022,17;357020,22;357021,54;357022,90;357026,55;357030,32;357045,64;357092,90;357114,25;357104,07
_____
Gebietsfläche:
"Berlin (1995-2000): bezogen auf den Gebietsstand 01.01.2001;"
Rheinland-Pfalz: Landessumme ab 2004 einschl. des gemein-
"        schaftlichen deutsch-luxemburgischen Hoheitsgebiets;"
Sachsen (1995): bezogen auf den Gebietsstand 01.01.1996.
_____
(C)opyright Statistisches Bundesamt, Wiesbaden 2010
Stand: 22.04.2010 / 21:32:50"""

GEBURTENZIFFERN_12612_0102 = """GENESIS-Tabelle: Temporär
Geburtenziffern: Deutschland, Jahre, Altersjahre;;;;;;;;
Statistik der Geburten;;;;;;;;
Deutschland;;;;;;;;
Lebendgeborene je 1000 Frauen (Anzahl);;;;;;;;
;Jahr;Jahr;Jahr;Jahr;Jahr;Jahr;Jahr;Jahr
;2001;2002;2003;2004;2005;2006;2007;2008
15 Jahre;1,0;1,0;0,9;0,8;0,8;0,8;0,8;0,8
16 Jahre;3,1;3,2;3,0;2,8;2,6;2,6;2,5;2,6
17 Jahre;7,5;7,7;7,1;6,4;6,2;5,8;5,5;5,7
47 Jahre;0,2;0,1;0,2;0,2;0,2;0,2;0,2;0,2
48 Jahre;0,0;0,1;0,1;0,1;0,1;0,1;0,1;0,1
49 Jahre;0,0;0,0;0,0;0,0;0,1;0,1;0,1;0,1
_____
Durchschnittliches Alter:
Differenz zwischen Geburtsjahr des Kindes und Geburtsjahr
der Mutter.
_____
(C)opyright Statistisches Bundesamt, Wiesbaden 2010
Stand: 10.04.2010 / 21:25:57"""



class tableParserTest(unittest.TestCase):
    
    def _make_parser(self, data, table_id):
        structure, variables = table.load_structure(table_id)
        return table.tableParser(structure, variables, data)
    
    def setUp(self):
        pass
    
    def test_parse_geburtenziffern(self):
        parser = self._make_parser(GEBURTENZIFFERN_12612_0102, "12612-0102")
        parser.parse()
        assert False
    

if __name__ == '__main__':
    unittest.main()