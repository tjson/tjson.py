# TJSON for Python

A python implementation for TJSON: Tagged JSON with Rich Types.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/anupsv/tjson-Python/master/LICENSE)

https://www.tjson.org/

## Installation

Coming soon

## Usage

### Parsing

To parse a TJSON document:

```python
>> from pytjson import tjson
>> my_tjson = tjson()
>> my_tjson.parse('{"foo:s":"bar"}')
{'foo': 'bar'}
```
The following describes how TJSON types map onto Python types during parsing:

 * **Unicode Strings**: parsed as Python's `String` with `Encoding::UTF_8`
 * **Binary Data**: parsed as python `bytes`
 * **Integers**: parsed as python `Int`
 * **Floats** (i.e. JSON number literals): parsed as python `float`
 * **Timestamps**: parsed as python `datetime.datetime`
 * **Arrays**: parsed as python `list`
 * **Objects**: parsed as `TJSON::Object` (a subclass of `::Dict`)
 
 ### Generating

To generate TJSON from Ruby objects, use the `TJSON.generate` method:

```python
>> from pytjson.tjson import tjson
>> my_tjson = tjson()
>> my_tjson.generate({"foo" => "bar"})
{"foo:s:"bar"}
```
