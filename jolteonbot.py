#################################################
#if there is any problem, don't tell me QAQ     #
#                       --chokasama             #
#################################################

import discord
import asyncio
import pandas
import random
import time
import functools
from math import sqrt, pow, floor

weather_boost = {   "extreme"       : [],
                    "sunny"         : ["grass", "fire", "ground"],
                    "clear"         : ["grass", "fire", "ground"],
                    "partly-cloudy" : ["normal","rock"],
                    "partly cloudy" : ["normal","rock"],
                    "cloudy"        : ["fairy", "fighting", "poison"],
                    "wind"          : ["dragon", "psychic", "flying"],
                    "fog"           : ["ghost", "dark"],
                    "snow"          : ["ice", "steel"],
                    "rain"          : ["water", "electric", "bug"],
                    "windy"         : ["dragon", "psychic", "flying"],
                    "foggy"         : ["ghost", "dark"],
                    "snowy"         : ["ice", "steel"],
                    "rainy"         : ["water", "electric", "bug"],
                    }
diff_form = {
    351: [0,4],
    386: [4,4],
    413: [8,3],
    479: [11,6],
    487: [17,2],
    492: [19,2],
    555: [21,2],
    641: [23,2],
    642: [25,2],
    645: [27,2],
    646: [29,3],
    648: [32,2],
    658: [34,2],
    681: [36,2],
    710: [38,4],
    711: [42,4],
    718: [46,3],
    720: [49,2],
    741: [51,4],
    745: [55,3],
    746: [58,2],
    774: [60,2],
    800: [62,4],
}

mega_form ={
    3: [0,1],
    6: [1,2],
    9: [3,1],
    15: [4,1],
    18: [5,1],
    65: [6,1],
    80: [7,1],
    94: [8,1],
    115: [9,1],
    127: [10,1],
    130: [11,1],
    142: [12,1],
    150: [13,2],
    181: [15,1],
    208: [16,1],
    212: [17,1],
    214: [18,1],
    229: [19,1],
    248: [20,1],
    254: [21,1],
    257: [22,1],
    260: [23,1],
    282: [24,1],
    302: [25,1],
    303: [26,1],
    306: [27,1],
    308: [28,1],
    310: [29,1],
    319: [30,1],
    323: [31,1],
    334: [32,1],
    354: [33,1],
    359: [34,1],
    362: [35,1],
    373: [36,1],
    376: [37,1],
    380: [38,1],
    381: [39,1],
    382: [40,1],
    383: [41,1],
    384: [42,1],
    428: [43,1],
    445: [44,1],
    448: [45,1],
    460: [46,1],
    475: [47,1],
    531: [48,1],
    719: [49,1],
}

alola_form = [19,
              20,
              26,
              27,
              28,
              37,
              38,
              50,
              51,
              52,
              53,
              74,
              75,
              76,
              88,
              89,
              103,
              105]

color_map = {
    'normal'    : 0xD1D1C4,
    'fire'      : 0xFF4500,
    'water'     : 0x1E90FF,
    'grass'     : 0x32CD32,
    'electric'  : 0xFFFF00,
    'ice'       : 0xAFEEEE,
    'ghost'     : 0x483D8B,
    'poison'    : 0x800080,
    'dark'      : 0x392A00,
    'fighting'  : 0xA52A2A,
    'psychic'   : 0xFF1493,
    'fairy'     : 0xFFB6C1,
    'dragon'    : 0x7B68EE,
    'ground'    : 0xDAA520,
    'rock'      : 0xDEB887,
    'flying'    : 0xB0C4DE,
    'bug'       : 0x9ACD32,
    'steel'     : 0xC0C0C0,
}

game_on = {}

dfmc = pandas.read_excel('charge_moves.xlsx')
dfmf = pandas.read_excel('fast_moves.xlsx')
df = pandas.read_excel('national_pokedex.xlsx')
dfdiff = pandas.read_excel('form_diff.xlsx')
dfmega = pandas.read_excel('mega_form.xlsx')
dfalola = pandas.read_excel('alola_form.xlsx')

def isweather(str):
    if str.lower() in weather_boost:
        return True
    else:
        return False

def weather_trans(str):
    if str.lower() in weather_boost:
        return str.lower()
    else:
        return 'extreme'

def if_boost(weather = 'extreme', type = 'unknown'):
    if type.lower() in weather_boost.get(weather):
        return True
    else:
        return False

def move_dps_calc(move_num, movef = 'c', weather = 'extreme', type_p = 'unknown'):
    '''calculates move dps under stb and weather boost'''
    return_val = ['0.0', False, False] #default value

    if movef == 'c':
        data  = dfmc;
    elif movef == 'f':
        data = dfmf;
    else:
        return return_val #unrecognized move type

    type_m = data['type'][move_num].lower()
    dps = float(data['dps'][move_num])
    stb = False
    boost = False
    #boost calc
    if if_boost(weather, type_m):
        boost = True
        if dps != 0:
            dps = float(data['dps'][move_num])*int(int(data['power'][move_num])*1.2)/int(data['power'][move_num])
    #stb calc
    if type_m in type_p.lower():
        stb = True
        dps *= 1.2

    dps_string = "%.1f" %dps
    return_val = [dps_string, stb, boost]
    return return_val

def movestr(dex_num, type_p, weather = 'extreme'):
    '''form the string consists of moves'''
    
    # no move stats avalible for gen 4 or after
    if dex_num > 386:
        return ''
    
    fast_moves = df['fast move no'][dex_num-1].strip().split(',')
    charge_moves = df['charge move no'][dex_num-1].strip().split(',')
    legacy_fast = []
    legacy_charge = []
    # detect if legacy move exists
    if str(df['legacy fast no'][dex_num-1]) != 'nan':
        legacy_fast = df['legacy fast no'][dex_num-1].strip().split(',')
    if str(df['legacy charge no'][dex_num-1]) != 'nan':
        legacy_charge= df['legacy charge no'][dex_num-1].strip().split(',')

    fast_moves_str = 'fast move(DPS): '
    charge_moves_str = 'charge move(DPS): '
    legacy_fast_str = 'legacy fast(DPS): '
    legacy_charge_str ='legacy charge(DPS): '

    for move in fast_moves:
        move = move.strip()
        if move!='':
            move_num = int(move)
            move_name = dfmf['name'][move_num]
            move_stat = move_dps_calc(move_num,'f',weather,type_p)
            if move_stat[2] == True:
                fast_moves_str += '**'+move_name.title()+'('+move_stat[0]+')** '
            else:
                fast_moves_str += move_name.title()+'('+move_stat[0]+') '
    fast_moves_str += '\n'

    for move in charge_moves:
        move = move.strip()
        if move!='':
            move_num = int(move)
            move_name = dfmc['name'][move_num]
            move_stat = move_dps_calc(move_num,'c',weather,type_p)
            if move_stat[2] == True:
                charge_moves_str += '**'+move_name.title()+'('+move_stat[0]+')** '
            else:
                charge_moves_str += move_name.title()+'('+move_stat[0]+') '
    charge_moves_str += '\n'

    if legacy_fast != []:
        for move in legacy_fast:
            move = move.strip()
            if move!='':
                move_num = int(move)
                move_name = dfmf['name'][move_num]
                move_stat = move_dps_calc(move_num,'f',weather,type_p)
                if move_stat[2] == True:
                    legacy_fast_str += '**'+move_name.title()+'('+move_stat[0]+')** '
                else:
                    legacy_fast_str += move_name.title()+'('+move_stat[0]+') '
        legacy_fast_str += '\n'
    else: legacy_fast_str = ''

    if legacy_charge != []:
        for move in legacy_charge:
            move = move.strip()
            if move!='':
                move_num = int(move)
                move_name = dfmc['name'][move_num]
                move_stat = move_dps_calc(move_num,'c',weather,type_p)
                if move_stat[2] == True:
                    legacy_charge_str += '**'+move_name.title()+'('+move_stat[0]+')** '
                else:
                    legacy_charge_str += move_name.title()+'('+move_stat[0]+') '
        legacy_charge_str += '\n'
    else: legacy_charge_str = ''
    return fast_moves_str+charge_moves_str+legacy_fast_str+legacy_charge_str

def pokestat_diff(dex_num, form_num, weather = 'extreme'):
    '''form the string consists of different form pokemon description'''
    format_str = u'name: %s\n中文名: %s\ntype: %s\nbase hp: %s\nbase att: %s\nbase def: %s\nlv30maxcp: %d\n%slv40maxcp: %d\n孵蛋/raid 参考:\nlv20maxcp: %d\nlv20mincp: %d\n%s%s\n'
    format_25 = '**lv25maxcp: %d**\n**lv25mincp: %d**\n'
    error_exp = ['error','',0]
    if dex_num not in diff_form:
        return error_exp
    elif form_num >= diff_form[dex_num][1]:
        return error_exp
    else:
        new_dex = diff_form[dex_num][0]+form_num
        hp = dfdiff['base hp'][new_dex]
        atk = dfdiff['base attack'][new_dex]
        defence = dfdiff['base defence'][new_dex]
        type_p = dfdiff['type'][new_dex].split()
        
        type_p_new = ''
        lvl_boost = False
        color = 0
        # weather boosted type formatting
        for type_1 in type_p:
            if type_1.strip().lower() != '':
                if if_boost(weather, type_1.strip().lower()):
                    type_p_new += '**'+type_1.strip().title()+'** '
                    lvl_boost = True
                else:
                    type_p_new += type_1.strip().title()+' '
                if color == 0:
                    color = color_map[type_1.strip().lower()]
            else: pass
        type_p = type_p_new
        
        cpm_20 = 0.597400010000000
        cpm_25 = 0.667934000000000
        cpm_30 = 0.731700000000000
        cpm_35 = 0.761563840000000
        cpm_40 = 0.790300000000000
        mincp_20 = floor((atk+10)*sqrt(defence+10)*sqrt(hp+10)*pow(cpm_20,2)/10);
        maxcp_20 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_20,2)/10);
        mincp_25 = floor((atk+10)*sqrt(defence+10)*sqrt(hp+10)*pow(cpm_25,2)/10);
        maxcp_25 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_25,2)/10);
        maxcp_30 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_30,2)/10);
        maxcp_35 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_35,2)/10);
        maxcp_40 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_40,2)/10);
        
        name_en = dfdiff['Name'][new_dex].title()
        name_ch = dfdiff['chName'][new_dex].strip().title()
        
        move_str = movestr(dex_num, type_p, weather)
        dex_str = dfdiff['url'][new_dex]
        
        lvl25_str = ''
        lvl35_str = ''
        
        # show lvl35 lvl25 stats only when boosted
        if lvl_boost:
            lvl25_str = format_25%(maxcp_25,mincp_25)
            lvl35_str = '**lv35maxcp: %d**\n'%maxcp_35
        
        result = [format_str %(name_en,name_ch,type_p,str(hp),str(atk),str(defence),maxcp_30,lvl35_str, maxcp_40,maxcp_20,mincp_20,lvl25_str,move_str), dex_str, color]
        return result


def pokestat_mega(dex_num, form_num, weather = 'extreme'):
    '''form the string consists of mega pokemon description'''
    format_str = u'name: %s\n中文名: %s\ntype: %s\nbase hp: %s\nbase att: %s\nbase def: %s\nlv30maxcp: %d\n%slv40maxcp: %d\n孵蛋/raid 参考:\nlv20maxcp: %d\nlv20mincp: %d\n%s%s\n'
    format_25 = '**lv25maxcp: %d**\n**lv25mincp: %d**\n'
    error_exp = ['error','',0]
    if dex_num not in mega_form:
        return error_exp
    elif form_num > mega_form[dex_num][1]:
        return error_exp
    elif form_num == 0:
        return pokestat(dex_num, weather)
    else:
        new_dex = mega_form[dex_num][0]+form_num-1
        hp = dfmega['base hp'][new_dex]
        atk = dfmega['base attack'][new_dex]
        defence = dfmega['base defence'][new_dex]
        
        # lazy me, '#' represents types same as normal form
        if dfmega['type'][new_dex].strip()!='#':
            type_p = dfmega['type'][new_dex].split()
        else:
            type_p = df['type'][dex_num-1].split()
        
        type_p_new = ''
        lvl_boost = False
        color = 0
        # weather boosted type formatting
        for type_1 in type_p:
            
            if type_1.strip().lower() != '':
                if if_boost(weather, type_1.strip().lower()):
                    type_p_new += '**'+type_1.strip().title()+'** '
                    lvl_boost = True
                else:
                    type_p_new += type_1.strip().title()+' '
                if color == 0:
                    color = color_map[type_1.strip().lower()]
            else: pass
        type_p = type_p_new
        
        cpm_20 = 0.597400010000000
        cpm_25 = 0.667934000000000
        cpm_30 = 0.731700000000000
        cpm_35 = 0.761563840000000
        cpm_40 = 0.790300000000000
        mincp_20 = floor((atk+10)*sqrt(defence+10)*sqrt(hp+10)*pow(cpm_20,2)/10);
        maxcp_20 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_20,2)/10);
        mincp_25 = floor((atk+10)*sqrt(defence+10)*sqrt(hp+10)*pow(cpm_25,2)/10);
        maxcp_25 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_25,2)/10);
        maxcp_30 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_30,2)/10);
        maxcp_35 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_35,2)/10);
        maxcp_40 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_40,2)/10);

        name_en = df['Name'][dex_num-1].title()
        if dfmega['abbr'][new_dex].strip()!='#':
            name_en += ' ('+dfmega['abbr'][new_dex].strip().title()+')'
        else:
            name_en += ' (Mega)'

        if dfmega['chName'][new_dex].strip()!='#':
            name_ch = dfmega['chName'][new_dex]
        else:
            name_ch = '超级'+df['offName'][dex_num-1]

        move_str = movestr(dex_num, type_p, weather)
        dex_str = dfmega['url'][new_dex]
        
        lvl25_str = ''
        lvl35_str = ''

        # show lvl35 lvl25 stats only when boosted
        if lvl_boost:
            lvl25_str = format_25%(maxcp_25,mincp_25)
            lvl35_str = '**lv35maxcp: %d**\n'%maxcp_35

        result = [format_str %(name_en,name_ch,type_p,str(hp),str(atk),str(defence),maxcp_30,lvl35_str, maxcp_40,maxcp_20,mincp_20,lvl25_str,move_str), dex_str, color]
        return result


def pokestat_alola(dex_num, weather = 'extreme'):
    '''form the string consists of alola pokemon description'''
    format_str = u'name: %s\n中文名: %s\ntype: %s\nbase hp: %s\nbase att: %s\nbase def: %s\nlv30maxcp: %d\n%slv40maxcp: %d\n孵蛋/raid 参考:\nlv20maxcp: %d\nlv20mincp: %d\n%s%s\n'
    format_25 = '**lv25maxcp: %d**\n**lv25mincp: %d**\n'
    error_exp = ['error','',0]
    if  dex_num not in alola_form:
        return error_exp
    else:
        dex_num_new = alola_form.index(dex_num)
        hp = dfalola['base hp'][dex_num_new]
        atk = dfalola['base attack'][dex_num_new]
        defence = dfalola['base defence'][dex_num_new]
        type_p = dfalola['type'][dex_num_new].split()
        type_p_new = ''
        lvl_boost = False
        color = 0
        # weather boosted type formatting
        for type_1 in type_p:
            if type_1.strip().lower() != '':
                if if_boost(weather, type_1.strip().lower()):
                    type_p_new += '**'+type_1.strip().title()+'** '
                    lvl_boost = True
                else:
                    type_p_new += type_1.strip().title()+' '
                if color == 0:
                    color = color_map[type_1.strip().lower()]
            else: pass
        type_p = type_p_new
        # cp calculation
        cpm_20 = 0.597400010000000
        cpm_25 = 0.667934000000000
        cpm_30 = 0.731700000000000
        cpm_35 = 0.761563840000000
        cpm_40 = 0.790300000000000
        mincp_20 = floor((atk+10)*sqrt(defence+10)*sqrt(hp+10)*pow(cpm_20,2)/10);
        maxcp_20 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_20,2)/10);
        mincp_25 = floor((atk+10)*sqrt(defence+10)*sqrt(hp+10)*pow(cpm_25,2)/10);
        maxcp_25 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_25,2)/10);
        maxcp_30 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_30,2)/10);
        maxcp_35 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_35,2)/10);
        maxcp_40 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_40,2)/10);
        name_en = 'Alola '+df['Name'][dex_num-1].title()
        name_ch = '阿罗拉'+df['chName'][dex_num-1]
        # no move avalible for alola form pokemon now...
        #move_str = movestr(dex_num, type_p, weather)
        move_str = ''
        dex_str = dfalola['url'][dex_num_new]

        lvl25_str = ''
        lvl35_str = ''

        # show lvl35 lvl25 stats only when boosted
        if lvl_boost:
            lvl25_str = format_25%(maxcp_25,mincp_25)
            lvl35_str = '**lv35maxcp: %d**\n'%maxcp_35
        result = [format_str %(name_en,name_ch,type_p,str(hp),str(atk),str(defence),maxcp_30,lvl35_str, maxcp_40,maxcp_20,mincp_20,lvl25_str,move_str), dex_str, color]
        return result



def pokestat(dex_num, weather = 'extreme'):
    '''form the string consists of pokemon description'''
    format_str = u'name: %s\n中文名: %s\ntype: %s\nbase hp: %s\nbase att: %s\nbase def: %s\nlv30maxcp: %d\n%slv40maxcp: %d\n孵蛋/raid 参考:\nlv20maxcp: %d\nlv20mincp: %d\n%s%s\n'
    format_25 = '**lv25maxcp: %d**\n**lv25mincp: %d**\n'
    error_exp = ['不知道呢 <:huaji:341240709405343745>','',0]
    if  dex_num>806:
        return error_exp
    else:
        hp = df['base hp'][dex_num-1]
        atk = df['base attack'][dex_num-1]
        defence = df['base defence'][dex_num-1]
        type_p = df['type'][dex_num-1].split()
        type_p_new = ''
        lvl_boost = False
        color = 0
        #weather boosted type formatting
        for type_1 in type_p:
            
            if type_1.strip().lower() != '':
                if if_boost(weather, type_1.strip().lower()):
                    type_p_new += '**'+type_1.strip().title()+'** '
                    lvl_boost = True
                else:
                    type_p_new += type_1.strip().title()+' '
                if color == 0:
                    color = color_map[type_1.strip().lower()]
            else: pass
        type_p = type_p_new
        # cp calculation
        cpm_20 = 0.597400010000000
        cpm_25 = 0.667934000000000
        cpm_30 = 0.731700000000000
        cpm_35 = 0.761563840000000
        cpm_40 = 0.790300000000000
        mincp_20 = floor((atk+10)*sqrt(defence+10)*sqrt(hp+10)*pow(cpm_20,2)/10);
        maxcp_20 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_20,2)/10);
        mincp_25 = floor((atk+10)*sqrt(defence+10)*sqrt(hp+10)*pow(cpm_25,2)/10);
        maxcp_25 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_25,2)/10);
        maxcp_30 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_30,2)/10);
        maxcp_35 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_35,2)/10);
        maxcp_40 = floor((atk+15)*sqrt(defence+15)*sqrt(hp+15)*pow(cpm_40,2)/10);
        name_en = df['Name'][dex_num-1].title()
        
        if name_en.strip() == "Farfetch'D":
            name_en = "Farfetch'd"
        #don't ask me why i do that...
        
        name_ch = df['chName'][dex_num-1]
        move_str = movestr(dex_num, type_p, weather)
        # form picture url
        dex_str = "%03d"%dex_num
        dex_str = 'https://assets.pokemon.com/assets/cms2/img/pokedex/full/'+dex_str+'.png'

        lvl25_str = ''
        lvl35_str = ''

        # show lvl35 lvl25 stats only when boosted
        if lvl_boost:
            lvl25_str = format_25%(maxcp_25,mincp_25)
            lvl35_str = '**lv35maxcp: %d**\n'%maxcp_35
        result = [format_str %(name_en,name_ch,type_p,str(hp),str(atk),str(defence),maxcp_30,lvl35_str, maxcp_40,maxcp_20,mincp_20,lvl25_str,move_str), dex_str, color]
        return result

def movestat(move_number, flag='f', weather = 'extreme'):
    '''form the string consists of pokemon move description'''
    formatf = 'fast move: %s\ntype: %s\npower: %s\ndps: %s\neps: %s\ntime: %s\n'
    formatc = 'charge move: %s\ntype: %s\npower: %s\ndps: %s\ndpe: %s\ntime: %s\n'
    
    if flag == 'c':
        data  = dfmc;
        format_str = formatc
        eps = data['dpe'][move_number-1]
        time = data['time'][move_number-1]
    elif flag == 'f':
        data = dfmf;
        format_str = formatf
        eps = data['eps'][move_number-1]
        time = str(data['time'][move_number-1])+'s'
    else:
        return '' #unrecognized move type
    
    name=data['name'][move_number-1].title()
    type_1=data['type'][move_number-1].title()
    power=data['power'][move_number-1]
    boost_power = str(power)
    energy=data['energy'][move_number-1]
    dps=move_dps_calc(move_number-1,flag,weather)[0]
    #weather boost formatting
    if if_boost(weather,type_1):
        type_1 = '**'+type_1+'**'
        boost_power = '**'+boost_power+'+'+str(int(power/5))+'**'
        power = int(power)+int(power)/5
        dps = '**'+dps+'**'
        # dpe can be boosted, too
        if flag == 'c':
            epsdata = power/(-data['energy'][move_number-1])
            eps = '**%.2f**' % epsdata
    
    return format_str % (name,type_1,boost_power,dps,eps,time)

def parse_arg(argstr):
    if '+' in argstr:
        args = argstr.split('+')
    else:
        args = [argstr]
    weather = 'extreme'
    content = '1000'
    if len(args)>2:
        args = args[0:2]

    if len(args) == 1:
        content = args[0].lower().strip()
    else:
        if isweather(args[0].lower().strip()):
            weather = weather_trans(args[0].lower().strip())
            content = args[1].lower().strip()
        elif isweather(args[1].lower().strip()):
            weather = weather_trans(args[1].lower().strip())
            content = args[0].lower().strip()
        else:
            content = args[0].lower().strip()

    result = [content,weather]
    return result


#main program start

tokenstr = input('token: ')
print('entered\n')

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='type $h for help'))

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    
    if message.content.startswith('$pg '):
        # pokemon description search process starts
        
        # prohibit using this function in $game
        if game_on.get(message.channel) != None and game_on.get(message.channel) == True:
            await client.send_message(message.channel, '不许作弊呢～<:huaji:341240709405343745>')
            return
        

        
        input_str=message.content[4:]
        content,weather = parse_arg(input_str)
        msg_send = ''
        image_exist = False

        if content == '':
            msg_send="不知道呢 <:huaji:341240709405343745>"


        if str(content).isdigit():
            dex_num = int(content)
        else:
            for i in range(0,len(df['chName'])):
                if content == df['Name'][i].lower() or content == str(df['chName'][i]).lower() or content == str(df['offName'][i]).lower() or content == str(df['alterName'][i]).lower():
                    dex_num = int(df['dex number'][i])
                    #message_out=pokestat(dex_number)
                    #await client.send_message(message.channel,message_out)
                    break
            else:
                msg_send = "不知道呢 <:huaji:341240709405343745>"

        if msg_send == '':
            if dex_num in mega_form:
                # for pokemon has mega/primal form
                msg_2 = '这个精灵有超级进化／原始回归形态哦～'
                if mega_form[dex_num][1]==1:
                    msg_2 += ' type $0 for normal, $1 for mega/primal'
                else:
                    msg_2 += ' type $0 for normal, $1 for mega X, $2 for mega Y'
                await client.send_message(message.channel, msg_2)
                msg = await client.wait_for_message(timeout = 30, author = message.author, channel = message.channel)
                if not msg:
                    await client.send_message(message.channel,'不理我？不理你了哦～')
                    return
                type_d = msg.content[1:]
                
                if type_d == '':
                    msg_send = "不知道呢 <:huaji:341240709405343745>"
                elif ord('0')<=ord(type_d[0])<= ord('0')+mega_form[dex_num][1]:
                    msg_send,url_str,color = pokestat_mega(dex_num,ord(type_d[0])-ord('0'),weather)
                    e = discord.Embed(colour = color)
                    e.set_image(url=url_str)
                    image_exist = True
                elif type_d == '-1' and dex_num == 384:
                    msg_send,url_str,color = pokestat(10,weather)
                    e = discord.Embed(colour = color)
                    e.set_image(url=url_str)
                    image_exist = True
                else:
                    msg_send = "不知道呢 <:huaji:341240709405343745>"
            elif dex_num in diff_form:
                # for pokemon has more than one form
                msg_2 = '这个精灵有多种形态哦～ '
                for i in range(diff_form[dex_num][1]):
                    msg_2 += 'type $'+str(i)+' for '+dfdiff['abbr'][diff_form[dex_num][0]+i]+', '
                
                msg_2 = msg_2[:-2]
                await client.send_message(message.channel, msg_2)
                msg = await client.wait_for_message(timeout = 30, author = message.author, channel = message.channel)
                if not msg:
                    await client.send_message(message.channel,'不理我？不理你了哦～')
                    return
                type_d = msg.content[1:]

                if type_d == '':
                    msg_send = "不知道呢 <:huaji:341240709405343745>"
                elif ord('0')<=ord(type_d[0])<= ord('0')+diff_form[dex_num][1]:
                    msg_send,url_str,color = pokestat_diff(dex_num,ord(type_d[0])-ord('0'),weather)
                    e = discord.Embed(colour = color)
                    e.set_image(url=url_str)
                    image_exist = True
                else:
                    msg_send = "不知道呢 <:huaji:341240709405343745>"
            elif dex_num in alola_form:
                # for pokemon has alola form
                msg_2 = '这个精灵有阿罗拉的样子哦～ type $0 for normal, $1 for alola form'
                await client.send_message(message.channel, msg_2)
                msg = await client.wait_for_message(timeout = 30, author = message.author, channel = message.channel)
                if not msg:
                    await client.send_message(message.channel,'不理我？不理你了哦～')
                    return

                type_d = msg.content[1:]

                if type_d == '':
                    msg_send = "不知道呢 <:huaji:341240709405343745>"
                elif type_d[0] == '1':
                    msg_send,url_str,color = pokestat_alola(dex_num,weather)
                    e = discord.Embed(colour = color)
                    e.set_image(url=url_str)
                    image_exist = True
                elif type_d[0] == '0':
                    msg_send,url_str,color = pokestat(dex_num,weather)
                    e = discord.Embed(colour = color)
                    e.set_image(url=url_str)
                    image_exist = True
                else:
                    msg_send = "不知道呢 <:huaji:341240709405343745>"
            else:
                msg_send,url_str,color = pokestat(dex_num,weather)
                if url_str != '':
                    e = discord.Embed(colour = color)
                    e.set_image(url=url_str)
                    image_exist = True
        if image_exist:
            await client.send_message(message.channel,msg_send,embed = e)
        else:
            await client.send_message(message.channel,msg_send)


    elif message.content.startswith('hi jolteon'):
        # greeting
        await client.send_message(message.channel,'{0.author.mention} 你好，我是萌萌哒雷伊布，要疼爱我哦～'.format(message))

    elif message.content.startswith('$pgm '):
        # pokemon move description search
        input_str = message.content[5:]
        content,weather = parse_arg(input_str)
        for i in range(0,len(dfmf['name'])):
            if content == str(dfmf['name'][i]):
                move_number = i+1
                msg_send=movestat(move_number,'f',weather)
                #await client.send_message(message.channel,message_out)
                break
        else:
            for j in range(0,len(dfmc['name'])):
                if content == str(dfmc['name'][j]):
                    move_number = j+1
                    msg_send = movestat(move_number,'c',weather)
                    #await client.send_message(message.channel,message_out)
                    break
            else:
                msg_send = "没见过的技能呢～"
        await client.send_message(message.channel,msg_send)

    elif message.content.startswith('$h'):
        # help
        input_str = message.content[2:]
        if input_str.strip() == '':
            await client.send_message(message.channel,"输入\"$pg 宝可梦名称/编号\"查询pgo中宝可梦的(预测)数据\n输入\"$pgm 技能名称\"查询pgo中技能的数据\n输入\"$game\"看看有什么奇怪的事情发生:see_no_evil:")
        elif input_str.strip().lower() == 'pg':
            await client.send_message(message.channel,"输入\"$pg 宝可梦名称/编号(+天气)\"查询pgo中宝可梦的(预测)数据,名称可用中英文,天气可省略或使用英文天气")
        elif input_str.strip().lower() == 'pgm':
            await client.send_message(message.channel,"输入\"$pgm 技能名称/编号(+天气)\"查询pgo中技能数据,名称仅限英文,天气可省略或使用英文天气")
        elif input_str.strip().lower() == 'game':
            await client.send_message(message.channel,"输入\"$game\"开始辣鸡的我是谁游戏,游戏中不能作弊哦～\n输入\"$quit\"结束当前游戏")

    elif message.content.startswith('$game'):
        flag = False
        if message.content[5:] == ' v2':
            flag = True
        # who am i game
        if game_on.setdefault(message.channel,False):
            await client.send_message(message.channel,'游戏已开始，请先输入"$quit"结束已有游戏再开始新游戏')
            return
        game_on[message.channel] = True
        total = 0
        scoreboard = {}
        # maximum rounds = 30
        while total < 30:
            time.sleep(1.5)
            dex_num_ran = random.randint(1, 806)
            dex_str = "%03d"%dex_num_ran
            
            if flag:
                # send the picture first to get an url for it
                m_tmp = await client.send_file(message.channel, 'out/'+dex_str+'.png')
            
            dex_str = 'https://assets.pokemon.com/assets/cms2/img/pokedex/full/'+dex_str+'.png'
            hint_str = '_ '*len(str(df['chName'][dex_num_ran-1]))
            hint_str = hint_str[:-1]
            e = discord.Embed(title='猜猜我是谁?',colour=0x20DF80)
            if flag:
                e.set_image(url=m_tmp.attachments[0]['url'])
            else:
                e.set_image(url=dex_str)
            e.set_footer(text = hint_str)
            msg_quiz = await client.send_message(message.channel, embed = e)
            # time.sleep(0.2)
            if flag:
                await client.delete_message(m_tmp)
            start_time = time.time()
            now_time = start_time
            edited = False
            quit_game = False
            # maximum waiting time for one round: 30s
            while now_time-start_time < 30:
                now_time = time.time()
                # change hints at about 15s
                if now_time-start_time > 15 and not edited:
                    hint_str = ''
                    for i in range(len(str(df['chName'][dex_num_ran-1]))):
                        # give hint on every three characters
                        if i%3 == 1:
                            hint_str += str(df['chName'][dex_num_ran-1])[i]+' '
                        else:
                            hint_str += '_ '
                    e.set_footer(text = hint_str)
                    await client.edit_message(msg_quiz, embed = e)
                    edited = True
                guess = await client.wait_for_message(timeout = 2,channel = message.channel)
                if not guess:
                    continue
                else:
                    guess_1 = guess.content
                    if guess_1.strip() == '$quit':
                        #quit when this round ends
                        quit_game = True
                    if guess_1.strip().lower() == df['Name'][dex_num_ran-1].lower() or guess_1.strip().lower() == str(df['chName'][dex_num_ran-1]).lower() or guess_1.strip().lower() == str(df['offName'][dex_num_ran-1]).lower():
                        scoreboard.setdefault(guess.author,0)
                        scoreboard[guess.author] += 1
                        e_corr = discord.Embed(title=guess.author.name+' 答对了哦～', description ='正确答案:',colour=0x20DF80)
                        e_corr.set_image(url = dex_str)
                        e_corr.set_footer(text = df['Name'][dex_num_ran-1].title()+' '+df['chName'][dex_num_ran-1]+'\n')
                        await client.send_message(message.channel,embed = e_corr)
                        break
            else:
                e_wrong = discord.Embed(title='time up~', description ='正确答案:',colour=0xFF6347)
                e_wrong.set_image(url = dex_str)
                e_wrong.set_footer(text = df['Name'][dex_num_ran-1].title()+' '+df['chName'][dex_num_ran-1]+'\n')
                await client.send_message(message.channel,embed = e_wrong)
            # end the game when some player get 10 pts
            if scoreboard and max(scoreboard.values()) == 10:
                score_title = 'game over~\n'
                break
            # end the game when '$quit' shows up
            elif quit_game:
                score_title = '游戏中止\n'
                break
            total += 1
        else:
            score_title = 'game over~\n'
        # compare function for ordering scoreboard
        def user_compare(user_1,user_2):
            if scoreboard[user_1]>scoreboard[user_2]:
                return -1
            elif scoreboard[user_1]<scoreboard[user_2]:
                return 1
            else:
                return 0
        users = list(scoreboard.keys())
        users.sort(key=functools.cmp_to_key(user_compare))
        scorestr = ''
        for user in users:
            scorestr += user.name+': '+str(scoreboard[user])+'\n'
        e_score = discord.Embed(title=score_title, description =scorestr,colour=0x20DF80)
        await client.send_message(message.channel,embed = e_score)
        game_on[message.channel] = False


client.run(tokenstr)