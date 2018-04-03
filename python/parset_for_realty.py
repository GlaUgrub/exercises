import re

tag = "Дата появл"
NUM_DELIM = 16
    
def IsLow(string):
    if (string.count(';') < NUM_DELIM):
        return True
    return False
        
def IsBad(string, substring):
    if string[:len(substring)] == substring:
        return True
    return False
        
def IsComment(string):
    if (string.count(";;;;;;;;;;;;;;;;")) and (string[0] != ';'):
        return True
    return False
    
def IsEmpty(string):
    if string == ";;;;;;;;;;;;;;;;\n":
        return True
    return False
    
def IsSecondRow(string):
    splitted = string.split(';')
    if (not IsComment(string)) and (not IsEmpty(string)) and (splitted[1] == '') and (splitted[3] == ''):
        return True
    return False
    
def IsGood(string):
    if (IsComment(string)) or (IsEmpty(string)) or (IsSecondRow(string)):
        return False
    return True
    
def CleanUp(input, output):
    line = next(input, False)
    while line:
        if (IsBad(line, tag)):
            line = next(input, False)
            continue
        full_line = line
        if (IsLow(line)):
            full_line = line[0:-1]
            line = next(input, False)
            while (IsLow(full_line)) and line:
                full_line += (" " + line[0:-1])
                if not IsLow(full_line):
                    full_line += "\n"
                    break
                line = next(input, False)
        output.write(full_line)
        line = next(input, False)
        
def FindNextGood(strings, strings_total, idx):
    if (idx > strings_total):
        idx = strings_total
    while idx < strings_total:
        if IsGood(strings[idx]):
            break
        idx += 1
    return idx
    
def RemoveEOL(string):
    if len(string) == 0:
        return string
    if string[len(string) - 1] == '\n':
        if len(string) == 1:
            return ""
        return string[0:-1]
    return string
    
def FormatDates(cur_date):
    dates = re.findall(r'\d+.\d+.\d+',cur_date)
    return ','.join(dates)
    
def JustNumbers(string):
    result = cur_field.replace(' ','')
    m = re.search(r'\d+',result)
    if m != None:
        result = m.group()
    return result
    
def WrapWithQuotes(string):
    if (len(string)) == 0:
        return string
    if (string[0] == "\"") and (string[len(string) - 1] == "\""):
        return string
    if (string[0] == "\"") and (string[len(string) - 1] == "\n") and (string[len(string) - 2] == "\""):
        return string
    if string[len(string) - 1] == "\n":
        return "\"" + string[0:-1] + "\"" + "\n"
    return "\"" + string + "\""

input_file = open("1_UTF8.csv", 'r', encoding='utf-8')
output_file = open("out0", 'w', encoding='utf-8')

CleanUp(input_file, output_file)

output_file.close()
input_file.close()

input_file = open("out0", 'r', encoding='utf-8')

all_lines = []
for line in input_file:
    all_lines.append(line)

line_idx = 0
lines_total = len(all_lines)
processed_lines = []
while line_idx < lines_total:
    next_good = FindNextGood(all_lines, lines_total, line_idx)
    if next_good == lines_total:
        break
    next_next_good = FindNextGood(all_lines, lines_total, next_good + 1)
    lines_between = next_next_good - next_good
    processed_line = all_lines[next_good]
    cur_line_idx = 1
    while cur_line_idx < lines_between:
        cur_line = all_lines[next_good + cur_line_idx]
        if IsSecondRow(cur_line):
            # print("Base one: " + processed_line)
            # print("Sparse one: " + cur_line)
            splitted_base = processed_line.split(';')
            splitted_cur = cur_line.split(';')
            for i in range(len(splitted_base)):
                if (splitted_cur[i] != '') and (splitted_cur[i] != '\n'):
                    splitted_base[i] = splitted_base[i] + " " + splitted_cur[i]
            processed_line = ';'.join(splitted_base)
        if IsComment(cur_line):
            comment_extracted = cur_line.replace(';;;;;;;;;;;;;;;;','')
            processed_line = RemoveEOL(processed_line) + ';' + comment_extracted
        cur_line_idx += 1
    processed_lines.append(processed_line)
    line_idx = next_next_good
    
init_dict = {'date':0, 'operation':1, 'use and class':2, 'type':3, 'type of contract':4, 'room number':5, 'square range':6, 'ground square':7, 'price':8, 'price for m2':9, 'floors':10, 'metro':11, 'dummy':12, 'time and way':13, 'address':14, 'phones':15, 'status':16, 'comment':17}
target_dict = {'date':0, 'operation':1, 'use':2, 'type':3, 'class':4, 'type of contract':5, 'room number':6, 'square':7, 'min square':8, 'floor':9, 'floor number':10, 'metro':11, 'time':12, 'way':13, 'street':14, 'house':15, 'first phone':16, 'second phone':17, 'price':18, 'price for m2':19, 'comment':20}
init_to_targer_map = {'1':1, '3':3, '4':5, '5':6, '11':11, '17':21}

# for line in processed_lines:
    # output_file.write(line)
    
target_lines_excel = []
target_lines_crm = []
for idx in range(len(processed_lines)):
    target_splitted = []
    for i in range(22):
        target_splitted.append('')
    cur_line = processed_lines[idx]
    cur_splitted = cur_line.split(';', NUM_DELIM + 1)
    for idx_in_line in range(len(cur_splitted)):
        if idx_in_line == init_dict['date']: # get dates
            target_splitted[target_dict['date']] = WrapWithQuotes(FormatDates(cur_splitted[idx_in_line]))
        if idx_in_line == init_dict['use and class']: # get type and office class
            cur_field = cur_splitted[idx_in_line]
            use = cur_field
            office_class = ''
            m = re.search('кл.*',cur_field)
            if m != None:
                office_class = m.group()
                use = cur_field.replace(office_class,'')
                office_class = office_class[3:]
                use = use.replace(' ','')
            target_splitted[target_dict['use']] = WrapWithQuotes(use)
            target_splitted[target_dict['class']] = WrapWithQuotes(office_class)
        if idx_in_line == init_dict['square range']: # get min and max square
            cur_field = cur_splitted[idx_in_line]
            min = ''
            total = ''
            m = re.match(r'\d+-', cur_field)
            if m != None:
                min = m.group().replace('-','') 
                m = re.search(r'- \d+', cur_field)
                total = m.group().replace('- ','')
            else:
                total = cur_field
            target_splitted[target_dict['square']] = WrapWithQuotes(total)
            target_splitted[target_dict['min square']] = WrapWithQuotes(min)
        if idx_in_line == init_dict['price']: # get price
            cur_field = cur_splitted[idx_in_line] 
            target_splitted[target_dict['price']] = WrapWithQuotes(JustNumbers(cur_field))
        if idx_in_line == init_dict['price for m2']: # get price for m2
            cur_field = cur_splitted[idx_in_line] 
            target_splitted[target_dict['price for m2']] = WrapWithQuotes(JustNumbers(cur_field))
        if idx_in_line == init_dict['floors']: # get floor and number of floors
            cur_field = cur_splitted[idx_in_line]
            floors=''
            floor=''
            m = re.search(r'/\d+',cur_field)
            if m != None:
                floors = m.group().replace('/','')
            m = re.match(r'[0-9-]+/',cur_field)
            if m != None:
                floor = m.group().replace('/','')
            target_splitted[target_dict['floor']] = WrapWithQuotes(floor)
            target_splitted[target_dict['floor number']] = WrapWithQuotes(floors)
        if idx_in_line == init_dict['time and way']: # get time and way
            cur_field = cur_splitted[idx_in_line]
            time = ''
            way = ''
            m = re.search(r'\d+', cur_field)
            if m != None:
                time = m.group()
            m = re.search(r'\D+', cur_field)
            if m != None:
                way = m.group()
                if way == 'П':
                    way = 'пешком'
                if way == 'Т':
                    way = 'транспортом'
            target_splitted[target_dict['time']] = WrapWithQuotes(time)
            target_splitted[target_dict['way']] = WrapWithQuotes(way)
        if idx_in_line == init_dict['address']: # get address
            cur_field = cur_splitted[idx_in_line]
            street = cur_field
            house = ''
            m = re.search(', д.*',cur_field)
            if m != None:
                house = m.group()
                street = cur_field.replace(house,'')
                house = house.replace(', ','')
            target_splitted[target_dict['street']] = WrapWithQuotes(street)
            target_splitted[target_dict['house']] = WrapWithQuotes(house)
        if idx_in_line == init_dict['phones']: # get phones
            cur_field = cur_splitted[idx_in_line]
            home = cur_field
            mob = ''
            m = re.search(r'\d\(\d\d\d\)\d\d\d-\d\d\d\d', cur_field)
            if m != None:
                home = m.group()            
            home_removed = cur_field.replace(home,'')
            m = re.search(r'\d\(\d\d\d\)\d\d\d-\d\d\d\d', home_removed)
            if m != None:
                mob = m.group()
            target_splitted[target_dict['first phone']] = WrapWithQuotes(home)
            target_splitted[target_dict['second phone']] = WrapWithQuotes(mob)
        else:
            if str(idx_in_line) in init_to_targer_map:
                target_splitted[init_to_targer_map[str(idx_in_line)]] = WrapWithQuotes(cur_splitted[idx_in_line])
    print(target_splitted)
    target_lines_excel.append(';'.join(target_splitted))
    target_lines_crm.append(','.join(target_splitted))

output_file_crm = open("out_final_crm.csv", 'w', encoding='utf-8')
output_file_excel = open("out_final_excel.csv", 'w', encoding='cp1251')

for line in target_lines_excel:
    output_file_excel.write(line)
for line in target_lines_crm:
    output_file_crm.write(line)

input_file.close()
output_file_excel.close()
output_file_crm.close()


