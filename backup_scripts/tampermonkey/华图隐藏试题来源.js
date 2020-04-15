// ==UserScript==
// @name         华图隐藏试题来源
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Hide huatu sources of questions
// @author       Hansimov
// @match        http://v.huatu.com/tiku/analysis/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    let divs = document.getElementsByClassName("jiexi-item clearfix");

    // https://stackoverflow.com/a/13786423/8328786
    for (let x = 0; x < divs.length; x++) {
        let div = divs[x];
        let content = div.innerHTML;

        // https://stackoverflow.com/a/6629743/8328786
        if (content.includes("来源")) {
            div.style.display = 'none';
        }
    }
})();