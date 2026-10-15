---
title: "01. What are Playbooks?"
slug: "01-what-are-playbooks"
estimated_time: 5
has_hands_on: false
---

## 01. What are playbooks?
            

              
- In the previous labs, we have executed an `Ansible ad-hoc command` which invoked modules.
              
              
- While ad-hoc commands are useful for quick tasks, real-world scenarios require more complex
                orchestration.
              
- This is where `Ansible playbooks` come to the rescue.
              
- `Ansible playbooks` are essentially **blueprints of automation tasks** written
                in `YAML` format.
              
- They are used to **automate tasks on remote hosts** in a structured, repeatable manner.
              
            

            

#### Ad-hoc Commands vs Playbooks

| Aspect | Ad-hoc Commands | Playbooks |
| --- | --- | --- |
| Use Case | Quick one-time tasks | Complex multi-step workflows |
| Repeatability | Limited | Fully repeatable |
| Version Control | Difficult | Easy (YAML files) |
| Documentation | Poor | Self-documenting |
| Orchestration | Single task | Multiple tasks, multiple hosts |
| Conditionals | Not supported | Full support |
| Error Handling | Basic | Advanced |

            

#### Why Use Playbooks?
            

              
- **Repeatability**: Run the same tasks consistently across environments
              
- **Reusability**: Share playbooks across teams and projects
              
- **Orchestration**: Coordinate complex multi-machine deployments
              
- **Version Control**: Track changes to your automation
              
- **Documentation**: YAML format is self-documenting
              
- **Idempotency**: Safe to run multiple times
              
- **Error Handling**: Built-in error handling and rollback capabilities
