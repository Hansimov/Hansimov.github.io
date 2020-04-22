// ==UserScript==
// @name        前往leetcode中文站
// @description 前往leetcode中文站
// @match       *://leetcode.com/*
// @exclude     *://leetcode.com/*/discuss/*
// @grant       GM_addStyle
// ==/UserScript==

/*--- Create a button in a container div.  It will be styled and
    positioned with CSS.
*/
var zNode       = document.createElement ('div');
zNode.innerHTML = '<button id="lc-cn-btn" type="button">'
                + '前往中文站</button>'
                ;
zNode.setAttribute ('id', 'lc-cn-btn-container');
document.body.appendChild (zNode);

//--- Activate the newly added button.
document.getElementById ("lc-cn-btn").addEventListener (
    "click", ButtonClickAction, false
);

function ButtonClickAction (zEvent) {
    var zNode       = document.createElement ('p');
    var pathname_L = location.pathname.split('/');
    if (location.hostname=="leetcode.com") {
        window.open("https://leetcode-cn.com"+pathname_L.slice(0,3).join('/')+"/solution");
    }
    document.getElementById ("lc-cn-btn-container").appendChild(zNode);
}

//--- Style our newly added elements using CSS.
GM_addStyle ( `
    #lc-cn-btn-container {
        position:               absolute;
        top:                    70px;
        left:                   430px;
        font-size:              15px;
        // background:             cyan;
        // border:                 3px outset black;
        margin:                 3px;
        opacity:                0.5;
        z-index:                1100;
        // padding:                5px px;
    }
    #lc-cn-btn {
        cursor:                 pointer;
    }
    #lc-cn-btn-container p {
        color:                  red;
        background:             white;
    }
` );