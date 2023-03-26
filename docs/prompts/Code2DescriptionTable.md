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
	Describes whether the member is a "Method", "Attribute" or "Property".
	When the Method is decorated as @classmethod add "/class" after the "Method".
	When the Method is decorated as @staticmethod add "/static" after the "Method".
* "DataType":
  * DataType of the member.
  * Describe what Datatype is returned when the member is called.
  * If the member is a method or property, this item means the return value's DataType.
  * If the member is a attribute, this item means the member's own DataType.
* "Description":
  * Description of the member.
  * The length of this item depends on the importance of the member.
  * If the member is of high importance, the description should be longer, up to 8 sentences.
  * IF the member is not important, make description shorter. One sentence is acceptable.

Ensure that the table is ordered according to these two priorities:
	1. Members whose 'access' is 'public' must appear above those whose access is 'private'.
	2. Members should be listed in the same order as they appear in the source code unless the above conditions are violated.


## CODE

```
############# CODE ##############
```
