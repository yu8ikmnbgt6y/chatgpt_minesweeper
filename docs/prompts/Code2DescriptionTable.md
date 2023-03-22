# Code Description Table

Create a table that interprets the code written in Python in the ##CODE field and describes the class.
The table to be answered should follow the conditions in the ##Condition field

## Condition
Format: Markdown, Table
Table Header Content: ["Name", "Access", "Member Type", "Data Type", "Description"]
Row: member

Please enter the items in the table according to the content of the header
The description of each item is as follows

* "Name":
  * The name of member
* "Access":
  Describes which Access Specifier the member corresponds to. It will be "Public" or "Private" in Python code.
* "Member Type":
	Describes whether the member is a "Method", "Variable", or "Property".
	When the Method is decorated as @classmethod add "/class" after the "Method".
	When the Method is decorated as @staticmethod add "/static" after the "Method".
* "DataType":
  * DataType of the member.
  * what Datatype is return, when the member is called.
  * when the member is method or property, this item means return DataType
  * When the member is variable, this item means Variable DataType.
* "Description":
  * Description of the member.
  * length of this items differ from the , If the member is important, make description longer up to 8 sentences.
  * When the member is not important, make description shorter. One sentence is acceptable.

Ensure that the table is ordered according to these two priorities:
	1. Members whose "Access" is "Public" must appear above "Private" members.
	2. Members should be listed in the same order as they appear in the source code unless the above conditions are violated.


## CODE

```
############# CODE ##############
```
