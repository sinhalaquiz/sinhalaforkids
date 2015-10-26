"use strict";

function startLesson(letters, letterElem)
{
    var big_letter_ = document.getElementById(letterElem);
    var id_ = 0;

    big_letter_.innerHTML =
        '<a href="#" id="bigLetter" class="bigButton" onmousedown="onClickLetter(' + id_ + ');">' + letters[id_] + '</a>';
    return 'a';
}

