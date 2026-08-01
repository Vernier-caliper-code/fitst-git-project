def parse_row(line:str,row_num:int):
    line=line.strip()
    if not line:
        return None
    parts=line.split(",")
    if len(parts)!=3:
        print(f"  [警告] 第 {row_num} 行列数不对，跳过: {line}")
        return None

    name,age_str,score_str=parts
    name=name.strip()

    if not name:
        print(f"  [警告] 第 {row_num} 行 name 为空，跳过")
        return None

    try:
        age=int(age_str.strip())
        score=float(score_str.strip())
    except ValueError as e:
        print(f"  [警告] 第 {row_num} 行数据类型错误 ({e})，跳过: {line}")
        return None

    return [name,age,score]

def main():
    csv_path="data.csv"
    valid_rows=[]

    try:
        with open(csv_path,"r",encoding="utf-8") as f:
            lines=f.readlines()
    except FileNotFoundError:
        print(f"错误：找不到文件 '{csv_path}'，请确认文件存在")
        return 
    except PermissionError:
        print(f"错误：找不到文件 '{csv_path}'，请确认文件存在")
        return
    print(f"共读取 {len(lines)} 行，开始逐行处理...\n")
    for i,line in enumerate(lines,start=1):
        if i==1:
            print(f"  第 {i} 行（表头）: {line.strip()}")
            continue

        result=parse_row(line,i)
        if result:
            name,age,score=result
            valid_rows.append(result)
            print(f"  第 {i} 行 [OK]: name={name}, age={age}, score={score}")


