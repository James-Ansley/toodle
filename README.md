# Moodle TOML

Moodle TOML is a small transpiler that converts human-readable text and TOML
file formats representing Moodle questions to Moodle XML.

Moodle TOML also supports the Coderunner question type.

> Note: Moodle TOML is in alpha and significant API changes are likely.
> Currently, only Coderunner python questions and short answers are supported

## Install

    pip install moodle-toml

## Usage

Moodle TOML provides a `parser.to_xml` function that takes the Path of a
question suite and returns a Moodle XML file. A question suite is a directory
structure where non-question directories are treated as categories, and
questions are directories containing several text-based configuration files.
These formats are described below.

### Categories

Moodle TOML relies on parsing directory trees to determine question categories.
Each non-question directory is treated as a category. For example, if given the
following directory structure:

```text
questions
└── revision
    ├── programming
    │   ├── simple_area_calculation
    │   │   └── ...
    │   ├── simple_string_split_and_case
    │   │   └── ...
    │   └── simple_unit_conversion
    │       └── ...
    └── tracing
        └── string
            └── ...
```

Moodle TOML would generate a Moodle XML file containing a top-level category
"revision" which would contain two sub-categories "programming" and "tracing"
and so on. The root directory "questions" is not considered a category.

### Questions

Questions are represented as directories that contain a `config.toml` file. The
config file contains the basic configuration of the question such as question
type, and tags, along with question-specific configuration. Additional files
contain additional information such as `prompt.md` that contains the question
prompt and `answer.py` for Conderunner questions that contains the question
answer. The directory name is used as the question name.

For example, a Coderunner question would have the following directory structure:

```text
fizzbuzz
├── answer.py
├── config.toml
└── prompt.md
```

#### Config.toml

The question configuration is currently limited with only basic options
supported. The config.toml file has the following structures:

##### Coderunner

```toml
qtype = "coderunner"
coderunnertype = "..."  # from coderunner. e.g. "python3_w_input"
tags = ["...", "..."]  # any strings

precheck = "..."  # from coderunner. e.g. "examples"

[[testcases]]
example = true | false
display = "..."  # from coderunner e.g. "SHOW" | "HIDE"
testcode = '''...'''  # any testcode
stdin = '''...'''  # any stdin string
expected = '''...'''  # any string
```

##### Short Answer

```toml
qtype = "shortanswer"
tags = ["...", "..."]  # any strings

penalty_percent = 25  # any float | int
case_sensitivity = true | false

[[answers]]
text = '...'  # any string
grade = 100  # any int in 0..100
feedback = ''  # any string
```

### Example

Consider the following directory structure:
```text
questions
└── rectangle
    ├── answer.py
    ├── config.toml
    └── prompt.md
```

With the files:

`config.toml`:
```toml
qtype = "coderunner"
coderunnertype = "python3_w_input"
tags = ["beginner", "linear math", "area calculation"]

precheck = "examples"

[[testcases]]
example = true
display = "SHOW"
testcode = ''''''
stdin = '''10
10'''
expected = '''Enter the base of the rectangle in centimetres: 10
Enter the height of the rectangle in centimetres: 10
The area of the rectangle is 100.00cm^2'''

[[testcases]]
example = true
display = "SHOW"
testcode = ''''''
stdin = '''12.5
5.5'''
expected = '''Enter the base of the rectangle in centimetres: 12.5
Enter the height of the rectangle in centimetres: 5.5
The area of the rectangle is 68.75cm^2'''

[[testcases]]
example = false
display = "SHOW"
testcode = ''''''
stdin = '''0
10'''
expected = '''Enter the base of the rectangle in centimetres: 0
Enter the height of the rectangle in centimetres: 10
The area of the rectangle is 0.00cm^2'''

[[testcases]]
example = false
display = "SHOW"
testcode = ''''''
stdin = '''100
200'''
expected = '''Enter the base of the rectangle in centimetres: 100
Enter the height of the rectangle in centimetres: 200
The area of the rectangle is 20000.00cm^2'''

[[testcases]]
example = false
display = "SHOW"
testcode = ''''''
stdin = '''15
1'''
expected = '''Enter the base of the rectangle in centimetres: 15
Enter the height of the rectangle in centimetres: 1
The area of the rectangle is 15.00cm^2'''

[[testcases]]
example = false
display = "SHOW"
testcode = ''''''
stdin = '''0
0'''
expected = '''Enter the base of the rectangle in centimetres: 0
Enter the height of the rectangle in centimetres: 0
The area of the rectangle is 0.00cm^2'''

[[testcases]]
example = false
display = "HIDE"
testcode = ''''''
stdin = '''25
2.5'''
expected = '''Enter the base of the rectangle in centimetres: 25
Enter the height of the rectangle in centimetres: 2.5
The area of the rectangle is 62.50cm^2'''
```

`prompt.md`

```markdown
A rectangle's area can be calculated using the following formula:

$$ area = base * height $$

Write a program that prompts the user to enter the base and height of a
rectangle in centimetres. The program should then print the area of the
rectangle to two decimal places.

Refer to the example testcases below for the required prompts and format of the
message to be displayed with the rectangle area.

Note: The two values entered can be floating point values and will be valid
non-negative numbers.
```

`answer.py`

```python
base = float(input("Enter the base of the rectangle in centimetres: "))
height = float(input("Enter the height of the rectangle in centimetres: "))

area = base * height

print(f"The area of the rectangle is {area:.2f}cm^2")
```

Calling the following python program:

`main.py`:

```python
from pathlib import Path

from moodle_toml.parser import to_xml

xml = to_xml(Path("questions"))
with open("import.xml", "w") as f:
    f.write(xml)
```

Would generate the following Moodle XML:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<quiz>
    <question type="coderunner">
    <name>
        <text>rectangle</text>
    </name>
    <coderunnertype>python3_w_input</coderunnertype>
    <precheck>2</precheck>
    <questiontext format="html">
        <text><![CDATA[<p>A rectangle's area can be calculated using the following formula:</p>
<p>$$ area = base * height $$</p>
<p>Write a program that prompts the user to enter the base and height of a
rectangle in centimetres. The program should then print the area of the
rectangle to two decimal places.</p>
<p>Refer to the example testcases below for the required prompts and format of the
message to be displayed with the rectangle area.</p>
<p>Note: The two values entered can be floating point values and will be valid
non-negative numbers.</p>]]></text>
    </questiontext>
    <answer><![CDATA[base = float(input("Enter the base of the rectangle in centimetres: "))
height = float(input("Enter the height of the rectangle in centimetres: "))

area = base * height

print(f"The area of the rectangle is {area:.2f}cm^2")
]]></answer>
    <answerboxlines>7</answerboxlines>
    <generalfeedback format="html">
        <text></text>
    </generalfeedback>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.0000000</penalty>
    <hidden>0</hidden>
    <idnumber></idnumber>
    <prototypetype>0</prototypetype>
    <allornothing>1</allornothing>
    <penaltyregime>0, 0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50</penaltyregime>
    <hidecheck>0</hidecheck>
    <showsource>0</showsource>
    <answerboxcolumns>100</answerboxcolumns>
    <answerpreload></answerpreload>
    <globalextra></globalextra>
    <useace></useace>
    <resultcolumns></resultcolumns>
    <template></template>
    <iscombinatortemplate></iscombinatortemplate>
    <allowmultiplestdins></allowmultiplestdins>
    <validateonsave>1</validateonsave>
    <testsplitterre></testsplitterre>
    <language></language>
    <acelang></acelang>
    <sandbox></sandbox>
    <grader></grader>
    <cputimelimitsecs></cputimelimitsecs>
    <memlimitmb></memlimitmb>
    <sandboxparams></sandboxparams>
    <templateparams></templateparams>
    <hoisttemplateparams>1</hoisttemplateparams>
    <templateparamslang>None</templateparamslang>
    <templateparamsevalpertry>0</templateparamsevalpertry>
    <templateparamsevald>{}</templateparamsevald>
    <twigall>0</twigall>
    <uiplugin></uiplugin>
    <uiparameters></uiparameters>
    <attachments>0</attachments>
    <attachmentsrequired>0</attachmentsrequired>
    <maxfilesize>10240</maxfilesize>
    <filenamesregex></filenamesregex>
    <filenamesexplain></filenamesexplain>
    <displayfeedback>1</displayfeedback>
    <giveupallowed>0</giveupallowed>
    <testcases>
        <testcase testtype="0" useasexample="{example}" hiderestiffail="0"
                  mark="1.0">
            <display>
                <text>SHOW</text>
            </display>
            <testcode>
                <text></text>
            </testcode>
            <stdin>
                <text>10
10</text>
            </stdin>
            <expected>
                <text>Enter the base of the rectangle in centimetres: 10
Enter the height of the rectangle in centimetres: 10
The area of the rectangle is 100.00cm^2</text>
            </expected>
            <extra>
                <text></text>
            </extra>
        </testcase>
        <testcase testtype="0" useasexample="{example}" hiderestiffail="0"
                  mark="1.0">
            <display>
                <text>SHOW</text>
            </display>
            <testcode>
                <text></text>
            </testcode>
            <stdin>
                <text>12.5
5.5</text>
            </stdin>
            <expected>
                <text>Enter the base of the rectangle in centimetres: 12.5
Enter the height of the rectangle in centimetres: 5.5
The area of the rectangle is 68.75cm^2</text>
            </expected>
            <extra>
                <text></text>
            </extra>
        </testcase>
        <testcase testtype="0" useasexample="{example}" hiderestiffail="0"
                  mark="1.0">
            <display>
                <text>SHOW</text>
            </display>
            <testcode>
                <text></text>
            </testcode>
            <stdin>
                <text>0
10</text>
            </stdin>
            <expected>
                <text>Enter the base of the rectangle in centimetres: 0
Enter the height of the rectangle in centimetres: 10
The area of the rectangle is 0.00cm^2</text>
            </expected>
            <extra>
                <text></text>
            </extra>
        </testcase>
        <testcase testtype="0" useasexample="{example}" hiderestiffail="0"
                  mark="1.0">
            <display>
                <text>SHOW</text>
            </display>
            <testcode>
                <text></text>
            </testcode>
            <stdin>
                <text>100
200</text>
            </stdin>
            <expected>
                <text>Enter the base of the rectangle in centimetres: 100
Enter the height of the rectangle in centimetres: 200
The area of the rectangle is 20000.00cm^2</text>
            </expected>
            <extra>
                <text></text>
            </extra>
        </testcase>
        <testcase testtype="0" useasexample="{example}" hiderestiffail="0"
                  mark="1.0">
            <display>
                <text>SHOW</text>
            </display>
            <testcode>
                <text></text>
            </testcode>
            <stdin>
                <text>15
1</text>
            </stdin>
            <expected>
                <text>Enter the base of the rectangle in centimetres: 15
Enter the height of the rectangle in centimetres: 1
The area of the rectangle is 15.00cm^2</text>
            </expected>
            <extra>
                <text></text>
            </extra>
        </testcase>
        <testcase testtype="0" useasexample="{example}" hiderestiffail="0"
                  mark="1.0">
            <display>
                <text>SHOW</text>
            </display>
            <testcode>
                <text></text>
            </testcode>
            <stdin>
                <text>0
0</text>
            </stdin>
            <expected>
                <text>Enter the base of the rectangle in centimetres: 0
Enter the height of the rectangle in centimetres: 0
The area of the rectangle is 0.00cm^2</text>
            </expected>
            <extra>
                <text></text>
            </extra>
        </testcase>
        <testcase testtype="0" useasexample="{example}" hiderestiffail="0"
                  mark="1.0">
            <display>
                <text>HIDE</text>
            </display>
            <testcode>
                <text></text>
            </testcode>
            <stdin>
                <text>25
2.5</text>
            </stdin>
            <expected>
                <text>Enter the base of the rectangle in centimetres: 25
Enter the height of the rectangle in centimetres: 2.5
The area of the rectangle is 62.50cm^2</text>
            </expected>
            <extra>
                <text></text>
            </extra>
        </testcase>
    </testcases>
    <tags>
        <tag>
            <text>beginner</text>
        </tag>
        <tag>
            <text>linear math</text>
        </tag>
        <tag>
            <text>area calculation</text>
        </tag>
    </tags>
</question>
</quiz>
```
