---
title: "03. YAML Basics for Playbooks"
slug: "03-yaml-basics"
estimated_time: 6
has_hands_on: false
---

## 03. YAML basics
            

#### Understanding YAML
            

              
- The `playbook` is usually written in [YAML](https://ja.wikipedia.org/wiki/YAML)
                format.
              
- Nevertheless, `playbooks` can be written in [JSON](https://en.wikipedia.org/wiki/JSON) format as well.
              
- In this lab we will be using only YAML format for `playbooks`.
              
- YAML is a text file that uses “Python-style” indentation to indicate nesting, which
                **does not require quotes** around most string values.
              
- Files should start with `---`.
              
- As **indentations have meanings**, they are extremely important!!!
              
- Indentation should be written using `space`, as using `tab` will result in an
                error.
              
- The level of indentation (using spaces, not tabs) is used to **denote structure**.
              
- Building the playbook using **Key-Value Pairs**, making them as dictionary in YAML that
                is represented in a simple `key`: `value` form.
              
- The `:` (colon) **must** be followed by a space.
              
- All members of a `list` are lines beginning at the **same indentation level**
                starting with a `-` (a dash and a space).
              
- As values can span multiple lines, using `|` or `>`, `playbooks`
                support **Multi-Line Strings**.
              
- Using a `Literal Block Scalar` [`|`] will include the newlines and any trailing
                spaces.
              
- Using a `Folded Block Scalar` [`>`] will fold new lines into spaces.
              
- **Boolean Values** (true/false) can be specified in several forms. For example, use a
                lowercase `true` or `false` boolean value in dictionaries in order to be
                compatible with default yamllint options.
              
- 
                

YAML is **case sensitive**, so be careful with your capitalization.
                

![Image](/static/assets/images/ansible-playbook-yaml.png)
