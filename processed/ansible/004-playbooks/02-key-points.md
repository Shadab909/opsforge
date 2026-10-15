---
title: "02. Key Architecture & Execution Points"
slug: "02-key-points"
estimated_time: 5
has_hands_on: false
---

## 02. Key points
            
            
              

                
-  **Structure**
              

              
              

                
- A playbook is composed of one or more `plays`, in an **ordered list**
                  (Sequence).
                
- 
                  

Each play executes **part** of the overall goal of the playbook, running one or more
                    tasks, whereas each task calls an `Ansible module`.
                
                
- 
Execution****
                
              

              
              

                
- `Playbooks` runs in sequential order, from top to bottom.
                
- Within each `play`, tasks also run in a sequential order, from top to bottom.
                
- 
                  

`Playbooks` containing multiple `plays` can orchestrate **multi-machine
                      deployments**.
                
                
- 
Functionality****
                
              

              
              

                
- 
                  

`Playbooks` can declare **configurations** and **orchestrate
                      steps** of any manual ordered process, on **multiple** sets of machines, in a
                    pre-defined order, while launching tasks, either synchronously or asynchronously.
                
                
- 
Use Cases****
                
              

              
              

                
- `Playbooks` are regularly used to automate IT infrastructure, networks, security systems
                  and code repositories (like GitHub).
                
- 
                  

IT staff can also use playbooks to program applications, services, server nodes and other devices.
                  
                
                
- 
Reusability****
                
              

              
              

                
- The `conditions`, `variables` and `tasks` within playbooks can be
                  saved, shared or reused indefinitely.
                
- This makes it easier for IT teams to codify operational knowledge and ensure that the same actions
                  are performed consistently across different environments.
