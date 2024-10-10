'''
Date: 2024-09-30 19:28:57
LastEditors: BHM-Bob 2262029386@qq.com
LastEditTime: 2024-10-09 21:06:26
Description: RRCS calculation in PyMOL, RRCS is from article "Common activation mechanism of class A GPCRs": https://github.com/elifesciences-publications/RRCS/blob/master/RRCS.py
'''
from typing import Dict, Tuple

import pandas as pd
from pymol import cmd


def _test_close(dict_coord: Dict[str, Dict[int, Tuple[float, float, float, float]]],
                ires: str, jres: str):
    for iatom in dict_coord[ires]:
        (ix, iy, iz, iocc) = dict_coord[ires][iatom]
        for jatom in dict_coord[jres]:                  
            (jx, jy, jz, jocc) = dict_coord[jres][jatom]
            dx = abs(ix-jx)
            dy = abs(iy-jy)
            dz = abs(iz-jz)
            if dx < 4.63 and dy < 4.63 and dz < 4.63:
                return True
    return False

def _calcu_score(dict_coord: Dict[str, Dict[int, Tuple[float, float, float, float]]],
                 atomnum2name: Dict[int, str], ires: str, jres: str,
                 check_name: bool, score_count: int):
    total_score = 0
    for iatom in dict_coord[ires]:
        if check_name and atomnum2name[iatom] in ['N', 'CA', 'C', 'O']:
            continue
        (ix, iy, iz, iocc) = dict_coord[ires][iatom]
        for jatom in dict_coord[jres]:
            if check_name and atomnum2name[jatom] in ['N', 'CA', 'C', 'O']:
                continue
            (jx, jy, jz, jocc) = dict_coord[jres][jatom]
            d2 = (ix-jx)**2 + (iy-jy)**2 + (iz-jz)**2
            if d2 >= 21.4369:  # 4.63*4.63 = 21.4369
                score = 0
            elif d2 <= 10.4329:  # 3.23*3.23 = 10.4329
                score = 1.0*iocc*jocc
            else:
                score = (1-(d2**0.5 - 3.23)/1.4)*iocc*jocc
            total_score += score
            score_count[0] += 1
    return total_score

def calcu_RRCS(model: str):
    dict_coord = {} # dict to store coordinates. dict_coord[res][atom] = (x, y, z, occupancy)
    cmd.iterate_state(1, model, 'dict_coord.setdefault(f"{chain}:{resi}:{resn}", {}).setdefault(index, (x, y, z, q))', space={'dict_coord': dict_coord})
    atomnum2name = {} # map atom number to atom name, in order to find N, CA, C, O
    cmd.iterate(model, 'atomnum2name[index] = name', space={'atomnum2name': atomnum2name})
    contact_score = {} # dict to store final results. contact_score[ires][jres] = contact_score.
    score_count = [0] # 66320
    # calcu RRCS score for each residue pair
    for ires in dict_coord:
        ires_num = int(ires.split(':')[1])
        contact_score[ires] = {}
        # find jres if it has any atom close to ires
        for jres in dict_coord:
            jres_num = int(jres.split(':')[1])
            contact_score[ires][jres] = 0
            # skip because alreadly calculated
            if jres_num <= ires_num:
                continue
            # skip if jres has no atom close to ires
            if not _test_close(dict_coord, ires, jres):
                continue
            # calculate RRCS score for ires and jres
            contact_score[ires][jres] = _calcu_score(dict_coord, atomnum2name, ires, jres,
                                                     check_name= abs(ires_num - jres_num) < 5, score_count=score_count)
    # convert dict to DataFrame
    contact_df = pd.DataFrame(data={k:list(v.values()) for k,v in contact_score.items()},
                              index=contact_score.keys(), columns=contact_score.keys())
    return contact_df

if __name__ == '__main__':
    cmd.reinitialize()
    cmd.load('data_tmp/pdb/RECEPTOR.pdb', 'receptor')
    from mbapy.base import TimeCosts
    @TimeCosts(3)
    def test_calcu(idx):
        calcu_RRCS('receptor')
    test_calcu()