function realBuying() {
    $.ajax({
        type: 'POST',
        url: '/update_buy/{{name}}/',
        data: {
            price: '{{data.price}}',
            seller: '{{data.seller}}',
            img_path: '{{data.img_path}}',
            isBuy: "Y"
        },
        success: function (response) {
            changeConfirm(name);
            window.open("{{data.openkakao}}");
            location.reload(true);
        }
    });
}

function changeConfirm() {
    $.ajax({
        type: 'POST',
        url: '/confirm_buying/{{name}}/'
    });
}

function disableScroll() {
    document.body.style.overflow = 'hidden';
}

function enableScroll() {
    document.body.style.overflow = 'visible';
}

$(function () {
    $("#confirm").click(function () {
        realBuying();
        modalClose();
        enableScroll();
    });
    $("#modal-open").click(function () {
        {% if session['id'] %}
            $("#popup").css('display', 'flex').hide().fadeIn();
            disableScroll();
        {% else %}
            alert('로그인을 먼저하세요!');
            window.location.href = '/login';
        {% endif %}
    });
    $("#close").click(function () {
        modalClose();
        enableScroll();
    });
    function modalClose() {
        $("#popup").fadeOut();
    }
    $("#img-bigger").click(function () {
        $("#img-popup").css('display', 'flex').hide().fadeIn();
        disableScroll();
    });
    $("#img-close").click(function () {
        imgModalClose();
        enableScroll();
    });
    function imgModalClose() {
        $("#img-popup").fadeOut();
    }
});

function showHeart() {
    $.ajax({
        type: 'GET',
        url: '/show_heart/{{name}}/',
        data: {},
        success: function (response) {
            let myHeart = response['my_heart'];
            if (myHeart['interested'] == 'Y') {
                $("#heart").css("color", "red").attr("onclick", "unlike()");
            } else {
                $("#heart").css("color", "grey").attr("onclick", "like()");
            }
        }
    });
}

function like() {
    $.ajax({
        type: 'POST',
        url: '/like/{{name}}/',
        data: {
            interested: "Y"
        },
        success: function (response) {
            alert(response['msg']);
            window.location.reload();
        }
    });
}

function unlike() {
    $.ajax({
        type: 'POST',
        url: '/unlike/{{name}}/',
        data: {
            interested: "N"
        },
        success: function (response) {
            alert(response['msg']);
            window.location.reload();
        }
    });
}

$(document).ready(function () {
    showHeart();
});
