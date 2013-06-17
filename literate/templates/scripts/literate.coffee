hljs.initHighlightingOnLoad()

console.log 'jQ'
console.log $

$(document).ready ->
    # code here will mainly be for switching between one-column and two-column layouts
    $('h1').click ->
        console.log 'clicked h1'
        $('body').toggleClass 'parallel'