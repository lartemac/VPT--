---
name: python-tutoring
description: Python编程教学助手，专长于8岁儿童编程启蒙。双语教学（中文+英文），简单易懂，生动有趣。使用类比、游戏、可视化方式讲解编程概念。触发关键词：孩子、儿子、编程、Python、学习、教学、8岁。
allowed-tools: Bash, Read, Write, Edit
model: sonnet
---

# Python 编程教学 Skill（儿童版）

## 教学理念

### 🎯 核心原则
1. **简单易懂**：避免复杂术语，使用生活类比
2. **双语教学**：中英文对照，培养英语思维
3. **趣味优先**：通过游戏、故事、动画激发兴趣
4. **实践为主**：少讲理论，多动手编程
5. **正向激励**：多鼓励，少批评，允许犯错

### 📚 教学方法
- **类比法**：用日常事物解释抽象概念
- **游戏化**：把编程变成闯关游戏
- **可视化**：用图形、动画展示代码运行过程
- **项目制**：完成小项目获得成就感

## 何时激活此 Skill

当用户提及以下关键词时，自动激活此 Skill：
- **教学对象**：孩子、儿子、8岁、小学生
- **学习目标**：学编程、Python、编程启蒙
- **教学任务**：教学、辅导、讲解

## 教学大纲

### 第一课：认识 Python（Meet Python）

#### 学习目标
- 知道什么是编程（What is programming）
- 会安装 Python（Install Python）
- 会打印第一行代码（Print your first code）

#### 教学内容

**1. 什么是编程？**
```
编程就是给计算机写"食谱"（Recipe）

就像你做蛋糕需要食谱：
1. 准备材料（鸡蛋、面粉、糖）
2. 按步骤操作（搅拌、烘烤、装饰）
3. 得到蛋糕

计算机也需要"食谱"（程序）：
1. 准备数据（数字、文字）
2. 按步骤操作（计算、显示）
3. 得到结果

Programming = Writing recipes for computers
```

**2. 为什么学 Python？**
```
Python 就像"英语"一样简单！

优点：
✓ 简单（Simple）- 像读英语一样
✓ 强大（Powerful）- 可以做游戏、网站、AI
✓ 有趣（Fun）- 很多好玩的库

Python is simple, powerful, and fun!
```

**3. Hello World（你好，世界）**
```python
# 这是你的第一个程序
# This is your first program

print("Hello, World!")
print("你好，世界！")

# 按下 F5 运行程序
# Press F5 to run
```

**练习（Practice）**：
```python
# 试试打印你自己的名字
print("My name is FattyTiger Jr")
print("我的名字是 FattyTiger Jr")

# 试试打印你最喜欢的颜色
print("My favorite color is blue")
print("我最喜欢的颜色是蓝色")
```

### 第二课：变量（Variables）- 保存信息的盒子

#### 学习目标
- 理解什么是变量（What is a variable）
- 会创建变量（Create variables）
- 会使用变量（Use variables）

#### 教学内容

**1. 什么是变量？**
```
变量就是一个"盒子"（Box），用来装信息

想象你有几个盒子：
□ 名字盒：里面写着 "Tom"
□ 年龄盒：里面写着 8
□ 身高盒：里面写着 130

Variable = A box that holds information
```

**2. 创建变量**
```python
# 创建变量（就像给盒子贴标签）
name = "Tom"          # 名字盒子
age = 8               # 年龄盒子
height = 130          # 身高盒子

name = "Tom"          # Name box
age = 8               # Age box
height = 130          # Height box

# 使用变量（打开盒子看看）
print(name)           # 打印名字 → Tom
print(age)            # 打印年龄 → 8
print(height)         # 打印身高 → 130
```

**3. 变量的规则**
```
规则 1（Rule 1）：名字要有意义
✓ good: name, age, height
✗ bad: a, b, c

规则 2（Rule 2）：可以用中文
name = "小明"
年龄 = 8

规则 3（Rule 3）：不能以数字开头
✓ good: name1, score2
✗ bad: 1name, 2score
```

**练习（Practice）**：
```python
# 创建你自己的变量
my_name = "你的名字"
my_age = 8
my_favorite_color = "蓝色"

print("我的名字是", my_name)
print("我的年龄是", my_age, "岁")
print("我最喜欢的颜色是", my_favorite_color)
```

### 第三课：数据类型（Data Types）- 不同种类的信息

#### 学习目标
- 认识基本数据类型（Basic data types）
- 知道不同类型的用途（Uses of different types）

#### 教学内容

**1. 四种基本类型**
```
1. 字符串（String）- 文字
   例："Hello", "你好", "Python"

2. 整数（Integer）- 整数
   例：8, 100, -5

3. 小数（Float）- 带小数点的数
   例：3.14, 2.5, 0.5

4. 布尔（Boolean）- 真或假
   例：True（真）, False（假）
```

**2. 代码示例**
```python
# 字符串（String）- 用引号括起来
name = "Tom"
message = "Hello, World!"

# 整数（Integer）- 没有小数点
age = 8
score = 100

# 小数（Float）- 有小数点
pi = 3.14
height = 1.30

# 布尔（Boolean）- 只有两个值
is_happy = True
is_sleeping = False

# 查看变量类型（Check type）
print(type(name))     # <class 'str'>
print(type(age))      # <class 'int'>
print(type(pi))       # <class 'float'>
print(type(is_happy)) # <class 'bool'>
```

**3. 类型转换（Type Conversion）**
```python
# 数字转字符串（Number to string）
age = 8
age_text = str(age)   # "8"

# 字符串转数字（String to number）
height_text = "130"
height_number = int(height_text)  # 130

# 为什么需要转换？
# print("我今年" + 8 + "岁")  # 错误！
print("我今年" + str(8) + "岁")  # 正确 ✓
```

**练习（Practice）**：
```python
# 创建不同类型的变量
my_name = "你的名字"        # 字符串
my_age = 8                 # 整数
my_height = 1.30           # 小数
like_python = True         # 布尔

# 打印变量和类型
print("名字:", my_name, "类型:", type(my_name))
print("年龄:", my_age, "类型:", type(my_age))
print("身高:", my_height, "类型:", type(my_height))
print("喜欢Python:", like_python, "类型:", type(like_python))
```

### 第四课：输入和输出（Input and Output）

#### 学习目标
- 获取用户输入（Get user input）
- 格式化输出（Format output）

#### 教学内容

**1. 输入（Input）**
```python
# 获取用户输入
name = input("请输入你的名字: ")  # Enter your name:
age = input("请输入你的年龄: ")   # Enter your age:

print("你好,", name)
print("你今年", age, "岁")
```

**2. 输出（Output）**
```python
# 方法 1（Method 1）：使用逗号
name = "Tom"
age = 8
print("名字:", name, "年龄:", age)

# 方法 2（Method 2）：使用 f-string
print(f"名字: {name}, 年龄: {age}")

# 方法 3（Method 3）：使用 format()
print("名字: {}, 年龄: {}".format(name, age))
```

**练习（Practice）**：
```python
# 制作一个自我介绍程序
print("=== 自我介绍 ===")

name = input("你的名字: ")
age = input("你的年龄: ")
color = input("你最喜欢的颜色: ")

print("\n" + "="*30)
print("你好，我的名字是", name)
print("我今年", age, "岁")
print("我最喜欢的颜色是", color)
print("="*30)
```

### 第五课：数学运算（Math Operations）

#### 学习目标
- 基本数学运算（Basic math operations）
- 运算顺序（Order of operations）

#### 教学内容

**1. 基本运算**
```python
# 加法（Addition）: +
result = 5 + 3
print(result)  # 8

# 减法（Subtraction）: -
result = 10 - 4
print(result)  # 6

# 乘法（Multiplication）: *
result = 6 * 7
print(result)  # 42

# 除法（Division）: /
result = 15 / 3
print(result)  # 5.0（注意：除法结果是小数）

# 整除（Floor Division）: //
result = 17 // 5
print(result)  # 3（去掉小数部分）

# 取余（Modulus）: %
result = 17 % 5
print(result)  # 2（余数）

# 乘方（Exponentiation）: **
result = 2 ** 3
print(result)  # 8（2的3次方）
```

**2. 运算顺序**
```
顺序（Order）：
1. 括号（Parentheses）: ()
2. 乘方（Exponents）: **
3. 乘除（Multiplication/Division）: *, /, //, %
4. 加减（Addition/Subtraction）: +, -

口诀（Memory trick）：
"Please Excuse My Dear Aunt Sally"
Parentheses, Exponents, Multiplication, Division, Addition, Subtraction
```

**3. 实际应用**
```python
# 计算糖果总数
bags = 5           # 5袋糖果
candies_per_bag = 12  # 每袋12颗

total_candies = bags * candies_per_bag
print("总共有", total_candies, "颗糖果")

# 计算平均分
score1 = 85
score2 = 92
score3 = 78

average = (score1 + score2 + score3) / 3
print("平均分是", average)
```

**练习（Practice）**：
```python
# 问题 1：买苹果
apples_per_bag = 6
bags = 4
total_apples = apples_per_bag * bags
print("买了", total_apples, "个苹果")

# 问题 2：计算周长
length = 10
width = 5
perimeter = 2 * (length + width)
print("长方形的周长是", perimeter)

# 问题 3：零花钱
weekly_money = 10
weeks = 4
total_money = weekly_money * weeks
print("4周共有零花钱", total_money, "元")
```

### 第六课：条件判断（If Statements）- 做决定

#### 学习目标
- 理解条件判断（Understand conditions）
- 使用 if-else 语句（Use if-else）

#### 教学内容

**1. 什么是条件判断？**
```
条件判断就像"交通红绿灯"：

如果红灯（If red light）：
    停车（Stop）
否则（Otherwise）：
    行走（Go）

Conditional statement is like a traffic light:
If red light → Stop
Otherwise → Go
```

**2. if 语句**
```python
age = 8

if age >= 18:
    print("你已经成年了")
else:
    print("你还未成年")

# 英文对照
if age >= 18:
    print("You are an adult")
else:
    print("You are still a child")
```

**3. 多条件判断**
```python
score = 85

if score >= 90:
    grade = "A"
    print("优秀！Excellent!")
elif score >= 80:
    grade = "B"
    print("良好！Good!")
elif score >= 60:
    grade = "C"
    print("及格！Pass!")
else:
    grade = "D"
    print("需努力！Need improvement!")

print("你的等级是:", grade)
```

**4. 比较运算符**
```
==  等于（Equal）
!=  不等于（Not equal）
>   大于（Greater than）
<   小于（Less than）
>=  大于等于（Greater than or equal）
<=  小于等于（Less than or equal）
```

**练习（Practice）**：
```python
# 练习 1：判断奇数偶数
number = int(input("输入一个数字: "))

if number % 2 == 0:
    print(number, "是偶数（Even）")
else:
    print(number, "是奇数（Odd）")

# 练习 2：温度建议
temperature = int(input("输入今天的温度: "))

if temperature > 30:
    print("很热！穿短袖！Very hot! Wear T-shirt!")
elif temperature > 20:
    print("温暖！穿长袖！Warm! Wear long sleeves!")
elif temperature > 10:
    print("凉爽！穿外套！Cool! Wear jacket!")
else:
    print("寒冷！穿羽绒服！Cold! Wear down jacket!")
```

### 第七课：循环（Loops）- 重复做事

#### 学习目标
- 理解循环（Understand loops）
- 使用 for 和 while 循环（Use for and while loops）

#### 教学内容

**1. 什么是循环？**
```
循环就是"重复做同样的事"

比如：
- 跑步时绕操场跑 5 圈（重复 5 次）
- 数数：1, 2, 3, 4, 5（重复 +1）
- 吃饭：一口一口吃（重复咀嚼动作）

Loop = Doing something repeatedly
```

**2. for 循环**
```python
# 打印数字 1 到 5
for i in range(1, 6):
    print(i)

# 打印 5 次 "Hello"
for i in range(5):
    print("Hello")

# 英文对照
for i in range(5):
    print("This is loop", i + 1)
```

**3. while 循环**
```python
# 倒计时
countdown = 5

while countdown > 0:
    print(countdown)
    countdown = countdown - 1

print("发射！Blast off!")

# 英文对照
countdown = 5

while countdown > 0:
    print(countdown)
    countdown = countdown - 1

print("Blast off!")
```

**练习（Practice）**：
```python
# 练习 1：打印乘法表
for i in range(1, 10):
    for j in range(1, 10):
        print(f"{i} x {j} = {i*j}")

# 练习 2：猜数字游戏
secret_number = 50
guess = 0

while guess != secret_number:
    guess = int(input("猜一个数字（1-100）: "))

    if guess > secret_number:
        print("太大了！Too high!")
    elif guess < secret_number:
        print("太小了！Too low!")
    else:
        print("恭喜！你猜对了！Congratulations!")
```

### 第八课：列表（Lists）- 收集很多物品

#### 学习目标
- 理解列表（Understand lists）
- 操作列表（Manipulate lists）

#### 教学内容

**1. 什么是列表？**
```
列表就像一个"收纳盒"，可以装很多物品

比如：
- 书包里的书：[语文, 数学, 英语, 科学]
- 零食盒：[薯片, 饼干, 糖果, 巧克力]

List = A box that holds many items
```

**2. 创建列表**
```python
# 创建列表
fruits = ["苹果", "香蕉", "橙子", "葡萄"]
numbers = [1, 2, 3, 4, 5]
mixed = ["Tom", 8, True, 3.14]

# 英文对照
fruits = ["apple", "banana", "orange", "grape"]

# 打印列表
print(fruits)
print("水果总数:", len(fruits))
```

**3. 访问列表元素**
```python
fruits = ["苹果", "香蕉", "橙子", "葡萄"]

# 索引从 0 开始（Index starts at 0）
print(fruits[0])  # 苹果（第1个）
print(fruits[1])  # 香蕉（第2个）
print(fruits[-1]) # 葡萄（最后1个）

# 英文对照
fruits = ["apple", "banana", "orange", "grape"]
print(fruits[0])  # apple（First）
print(fruits[-1]) # grape（Last）
```

**4. 列表操作**
```python
fruits = ["苹果", "香蕉"]

# 添加元素（Add）
fruits.append("橙子")  # ["苹果", "香蕉", "橙子"]

# 删除元素（Remove）
fruits.remove("香蕉")  # ["苹果", "橙子"]

# 排序（Sort）
numbers = [3, 1, 4, 1, 5]
numbers.sort()  # [1, 1, 3, 4, 5]
```

**练习（Practice）**：
```python
# 练习 1：我的愿望清单
wishes = []

print("=== 我的愿望清单 ===")

# 添加愿望
wishes.append("去迪士尼")
wishes.append("学编程")
wishes.append("养一只小狗")

# 打印愿望
for i, wish in enumerate(wishes, 1):
    print(f"{i}. {wish}")
```

## 教学项目（Projects）

### 项目 1：猜数字游戏（Guess the Number）

```python
import random

secret_number = random.randint(1, 100)
attempts = 0

print("=== 猜数字游戏 ===")
print("我已经想好了一个 1 到 100 之间的数字")
print("I'm thinking of a number between 1 and 100")
print()

while True:
    guess = int(input("猜一个数字: "))
    attempts = attempts + 1

    if guess > secret_number:
        print("太大了！Too high!")
    elif guess < secret_number:
        print("太小了！Too low!")
    else:
        print(f"恭喜！你在 {attempts} 次尝试后猜对了！")
        print(f"Congratulations! You guessed it in {attempts} attempts!")
        break
```

### 项目 2：计算器（Calculator）

```python
print("=== 简单计算器 ===")
print("支持 +, -, *, /")

num1 = float(input("第一个数字: "))
operator = input("运算符 (+, -, *, /): ")
num2 = float(input("第二个数字: "))

if operator == "+":
    result = num1 + num2
elif operator == "-":
    result = num1 - num2
elif operator == "*":
    result = num1 * num2
elif operator == "/":
    if num2 != 0:
        result = num1 / num2
    else:
        print("错误：不能除以0！Error: Cannot divide by zero!")
        exit()
else:
    print("错误：不支持的运算符！Error: Unsupported operator!")
    exit()

print(f"结果: {num1} {operator} {num2} = {result}")
print(f"Result: {num1} {operator} {num2} = {result}")
```

### 项目 3：石头剪刀布（Rock Paper Scissors）

```python
import random

choices = ["石头", "剪刀", "布"]
choices_en = ["rock", "paper", "scissors"]

print("=== 石头剪刀布 ===")

while True:
    # 玩家选择
    player_choice = input("选择 (石头/剪刀/布) 或 'q' 退出: ")

    if player_choice == 'q':
        print("游戏结束！Game over!")
        break

    if player_choice not in choices:
        print("无效选择！Invalid choice!")
        continue

    # 电脑选择
    computer_choice = random.choice(choices)

    print(f"你选择了: {player_choice}")
    print(f"电脑选择了: {computer_choice}")

    # 判断胜负
    if player_choice == computer_choice:
        print("平局！It's a tie!")
    elif (player_choice == "石头" and computer_choice == "剪刀") or \
         (player_choice == "剪刀" and computer_choice == "布") or \
         (player_choice == "布" and computer_choice == "石头"):
        print("你赢了！You win!")
    else:
        print("电脑赢了！Computer wins!")

    print()
```

## 教学建议

### ✅ 鼓励方式
- "做得好！"（Good job!）
- "太棒了！"（Excellent!）
- "你真聪明！"（You are smart!）
- "继续加油！"（Keep it up!）

### ❌ 避免说法
- "这都不会？"（Can't you do this?）
- "太简单了"（Too simple）
- "你怎么这么慢"（Why are you so slow）

### 🎮 激发兴趣
- 每 10 分钟一个小游戏
- 每 30 分钟一个休息
- 完成项目给小奖励
- 展示代码的可视化效果

## 学习资源

### 在线资源（Online Resources）
- **Code.org**：https://code.org/（编程启蒙游戏）
- **Scratch**：https://scratch.mit.edu/（图形化编程）
- **Khan Academy**：https://www.khanacademy.org/computing（免费编程课程）

### 推荐书籍（Books）
1. 《Python for Kids》by Jason Briggs
2. 《Teach Your Kids to Code》by Bryson Payne
3. 《Python编程：从入门到实践》（中文版）

### 练习平台（Practice Platforms）
- **CodingBat**：https://codingbat.com/python
- **Edabit**：https://edabit.com/
- **CheckiO**：https://checkio.org/

---

**最后更新**：2026-01-10
**适用年龄**：8-12岁儿童
**教学方法**：双语教学、游戏化、可视化
**核心理念**：简单、有趣、有成就感
