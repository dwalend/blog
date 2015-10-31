---
layout: post
title: apply(config:Config) !
comments: True
---

# What I needed

Working with some older code at work I became really frustrated with the obfuscation and distant separation between where config keys were declared, values were loaded, and where the values were finally used. I started on a path to give case classes that were configured via Typesafe Config apply() methods that simply took configs.

# What I wanted
# Suspicious of implicit
# But this seemed OK
