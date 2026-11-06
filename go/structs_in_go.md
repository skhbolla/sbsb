---
title: "Structs in Go" 
description: "structs_in_go"
date: 2026-05-25
updated: 2026-05-25
tags: [""]
draft: true
---


So basically structs follow the below rules in C:

1. Structs are a way to create a custom data type, we do this by using the struct keyboard
2. struct x {} means that we are creating a custom data type x using struct .. any fields defined inside {} are the members
3. Since we created a blueprint (a data type) , we now need a way to actually use it.. creating a integer is done via int x; so similarly we assume that using struct_name x would work, but instead we are forced to use struct struct_name x to let the compiler know that we are talking about a struct we defined
4. If we know that we are not going to ever use the struct to initialize a new variable, then therer is no point in creating a name for the struct. So we use anonymous structs instead ie.. struct {member definition} x = {initializtion}. THis is logically same as doing struct name {mem def}; struct name x = {init} except that we are wasting a identifier unnecessarily
5. Since using the struct keyword over and over again is shitty, we use typedef to create alias for struct x as y

Am i right?

Nested Structs

Embedded Structs

Struct methods