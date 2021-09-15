---
title: 'Line ChatBot'
disqus: hackmd
---

Line ChatBot
===

## Table of Contents

[TOC]

Line 模擬器
---
可以在模擬器上面看到即時建構的模組
https://developers.line.biz/flex-simulator/

結構介紹
---
透過callback監聽post request，於line developer得到line_chatbot_api，每個chatbot只有一組api，要保管好。
也可以得到WebHookHandler。

FlexSendMessage: show一個自選表單
TextSendMessage: 回傳文字訊息

## Appendix and FAQ

* 文件內要有Procfile:讓程式知道要開啟app.py

###### tags: `Line Developer` `ChatBot`
