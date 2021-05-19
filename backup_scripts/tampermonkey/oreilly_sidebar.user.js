// ==UserScript==
// @name         O'Reilly Sidebar
// @namespace    http://tampermonkey.net/
// @version      21.05.19
// @description  Add sidebar to O'Reilly books
// @author       Hansimov
// @match        https://learning.oreilly.com/*
// @icon         https://www.google.com/s2/favicons?domain=oreilly.com
// @require      https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js
// @grant        GM_addStyle
// ==/UserScript==

(function() {
    'use strict';
    let sidebar_width = 320;
    let sidebar_margin_left = 10;
    let sidebar_left = 10;
    let sidebar_top = 80;

    var page_style = `
        code, span {
            color:blue;
            background-color:#f9f9f9;
        }
        a {
            color:#0d0 !important;
        }
        em {
            font-weight:bold !important;
        }
        h5,h6 {
            font-style:normal !important;
            font-weight:bold !important;
            color:brown !important;
        }

        // Hide and modify unneccessary elements

        #js-subscribe-nag {
            display:none;
        }
        .adders.expandUp {
            display:none;
        }

        .sbo-reading-menu.sbo-menu-top {
            background-color: transparent;
            border:none;
        }
        .sbo-reading-menu.sbo-menu-top sbo-toc-container.toc-menu, .sbo-title.ss-list {
            display:none;
        }
        .prev.nav-link, .next.nav-link {
            width:150px;
            opacity:0.1;
            border:none;
        }
        .prev.nav-link:hover, .next.nav-link:hover {
            opacity:0.8;
        }

        .interface-control-btns.js-bitlist.js-reader {
            opacity:0.1;
        }
        .interface-control-btns.js-bitlist.js-reader:hover {
            opacity:0.8;
        }
        .topbar.t-topbar, js-site-nav {
            background-color:transparent;
            border:none;
            display:none;
        }

        .l0.nav-icn {
            opacity:0.1;
        }
        .l0.nav-icn:hover {
            opacity:0.8;
        }
        .l1.nav-icn {
            display:none;
        }

        .toc-contents, .toc-contents.open, .toc-contents.open:hover {
            margin-left:auto;
            left: auto;
            margin-right: 0;
            right: 0;
            width: 500px;
            opacity: 1;
            background-color: transparent;
            transition-duration: 0s;
            border:none;
        }
        .toc-contents {
            opacity: 0.0;
        }
        .toc-contents::-webkit-scrollbar {
            display: none;
        }
        .toc-contents.open:hover {
            opacity: 1;
        }

        .minutes {
            color:black !important;
        }

        .cyxy-trs-source.cyxy-trs-target {
            background: #fffaaa !important;
        }
    `;

    function add_sidebar() {
        $("body").append(`
        <div class="toc-contents open" id="_sidebar" tabindex="-1" style="max-height: 1090px;">
            <div class="sbo-toc" id="_sidebar_toc">
            </div>
        </div>
        `);
        let sidebar_toc = $("#_sidebar_toc");

        // ToDo: "Fluent Python" need to use `getElementsByClassName("sect1")`
        try {
            let h1 = document.getElementsByTagName("h1")[1];
            sidebar_toc.append(`
                <p style="white-space:nowrap;"><a href="#${h1.id}">${h1.textContent}</ol>
            `);
        } catch (e) {
            console.log("No h1 elements!");
        }
        try {
            let h2 = Array.prototype.slice.call(document.getElementsByTagName("h2")).slice(0,-2);
            console.log("h2:", h2.length);
            for (let i=0; i<h2.length; ++i) {
                let h2_tmp = h2[i];
                sidebar_toc.append(`
                    <p style="white-space:nowrap;"><a href="#${h2_tmp.id}" >${h2_tmp.textContent}</p>
                `);
            }
        } catch (e) {
            console.log("No h2 elements!");
        }
        /*
        try {
            let h3 = Array.prototype.slice.call(document.getElementsByTagName("h3"));
            console.log(h3.length);
            for (let i=0; i<h2.length; ++i) {
                let h2_tmp = h2[i];
                sidebar_toc.append(`
                    <ol style="white-space:nowrap;"><a href="#${h3_tmp.id}" >${h2_tmp.textContent}</ol>
                `);
            }
        } catch (e) {
            console.log("No h3 elements!");
        }
        */
    }

    function update_sidebar() {
        try {
             $("#_sidebar").remove();
            add_sidebar();
        } catch (e) {}
    }

    var sidebar_style = `
        #_sidebar {
            margin-right: auto;
            right: auto;
            margin-left: ${sidebar_margin_left}px;
            left: ${sidebar_left}px;
            top:  ${sidebar_top}px;
            width: ${sidebar_width}px;
        }

        #_sidebar_toc > p > a, .sbo-toc > a {
            color:black !important;
            opacity: 1;
        }
        #_sidebar::hover {
            opacity:0.1;
        }
        #sbo-rt-content {/* must placed here (after page loaded) */
            /* margin-left: calc(${sidebar_width}px - ${sidebar_left}px - ${sidebar_margin_left}px); */
            margin-left: ${sidebar_width}px;
        }
    `;

    window.addEventListener('load', function() {
        GM_addStyle(page_style);
        add_sidebar();
        GM_addStyle(sidebar_style);
    }, false);

    var prev_url = location.href.split("#")[0];

    window.addEventListener('popstate', function (event) {
        var new_url = location.href.split("#")[0];
        if (!(prev_url === new_url)) {
             update_sidebar();
       }
        prev_url = new_url;
    });

})();