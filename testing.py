import re
from itertools import islice

jclLines=['//IDCAMS1  EXEC PGM=%IDCAMS.',
'//SYSPRINT  DD SYSOUT=%N.              ',
'//SYSIN     DD *                                                                ',
' DELETE %IDXZK..K13A30AZ.PT%DAT2=0. PURGE                                       ',
' SET MAXCC=0                                                                    ',
'/*                                                                              ',
'//K13A30A1 EXEC %BATCHP.,%REG3.,                                                ',
'//             MBR=TK14530,PSB=AYX                                               ',
'//SYSPRINT  DD SYSOUT=%N.           ',
'//       PARM="XXX,GHJH,,,,"                                                     ',
'//EBAND     DD DSN=%IDXZK..K13A20BR.PT%DAT2=0.,                                 ',
'//             DISP=OLD                                                         ',
'//GVFEHL    DD DSN=%IDXZK..K13A20BQ.PT%DAT2=0.,                                 ',
'//             DISP=OLD                                                         ',
'//ABAND     DD DSN=%IDXZK..K13A30AZ.PT%DAT2=0.,       AN K13A42Z                ',
'//             DISP=(,CATLG,CATLG),                                             ',
'//             UNIT=DISK,                                                       ',
'//             MGMTCLAS=%DEL5.,                                                 ',
'//             DCB=%NFB255.,                                                    ',
'//             SPACE=(CYL,(550,99),RLSE)                                        ',
'//STEP01 EXEC PGM=IMSBATCH,',
'//     PARM=(DBB,IMSPGM,psbname,,,,,)',
'/*                                                                              ',
'//STEP02 EXEC PGM=FOCRRC00,',
'//     PARM=(ULU,                                                                ',
'//              FOCUSPGM,psbname,,,,,)                                            ',
'/*                                                                               ']
a=0
pgm=''
ims_util=['DFSRCC00','IMSBATCH','IMSDLI','FOCRRC00']
ims_set = False
for idx,line in enumerate(jclLines):
    if a < 1:
        mem = line.replace(",", " ")
        match = re.findall(r'(PGM=|PSB=|MBR=|PARM=)', line)
        if match:
            # print(match,len(match))
            for keyword in match:
                if keyword=='PARM=':
                    if ims_set:
                        ims_val = mem.split(keyword)[1].split()
                        if len(ims_val) >1:
                            psb,pgm = ims_val[0],ims_val[1]
                        else:
                            psb = ims_val[0]
                            for next_line in range(idx+1,len(jclLines)):
                                # print(jclLines[next_line])
                                ims_val = jclLines[next_line].replace(",", " ")
                                ims_val = ims_val.split()[1]
                                pgm = ims_val
                                # print('next pgm',ims_val)
                                break
                        ims_set = False
                        print('PSB',"=>",psb)
                else:
                    pgm = mem.split(keyword)[1].split()[0]
                print(keyword,"=>",pgm)
                
                if pgm in ims_util:
                     ims_set = True