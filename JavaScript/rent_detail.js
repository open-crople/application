 function openBigPicture() {
     window.open("big_picture.html", "_blank");
 }
        
function realbuying() {
    $.ajax({type: 'POST',
            url: '/update_rent/{{name}}/',
            data: {
                price : '{{data.price}}',
                seller: '{{data.seller}}',
                img_path: '{{data.img_path}}',
                isRent: "Y"},
            success: function (response) {
                window.open("{{data.openkakao}}")
            }
           });
}
    
function disableScroll() {
    // body 요소의 overflow를 hidden으로 변경하여 스크롤 비활성화
    document.body.style.overflow = 'hidden';
}

function enableScroll() {
    // body 요소의 overflow를 다시 visible로 변경하여 스크롤 활성화
    document.body.style.overflow = 'visible';
}   
        
$(function(){
    $("#rent-confirm").click(function(){
        realbuying(); //모달 닫기 함수 호출
        modalClose();
        disableScroll();
        //컨펌 이벤트 처리
    });
    
    $("#modal-open").click(function(){   
        {% if session['id'] %}
        $("#popup").css('display','flex').hide().fadeIn();
         //팝업을 flex속성으로 바꿔준 후 hide()로 숨기고 다시 fadeIn()으로 효과
         disableScroll();
         {% else %}
         alert('로그인을 먼저하세요!');
          window.location.href='/login';
          {% endif %}
          });
          
          $("#rent-close").click(function(){
              modalClose(); //모달 닫기 함수 호출
              disableScroll();
          });
          
          function modalClose(){
              $("#popup").fadeOut(); //페이드아웃 효과
          }
          
          $("#img-bigger").click(function(){        
              $("#img-popup").css('display','flex').hide().fadeIn();
              disableScroll();
              //팝업을 flex속성으로 바꿔준 후 hide()로 숨기고 다시 fadeIn()으로 효과
          });
          
          $("#img-close").click(function(){
              imgmodalClose(); //모달 닫기 함수 호출
              enableScroll();
          });
          
          function imgmodalClose(){
              $("#img-popup").fadeOut(); //페이드아웃 효과
          }
         });
         
         function showHeart() {
             $.ajax({
                 type: 'GET',
                 url: '/show_heart/{{name}}/',
                 data: {},
                 success: function (response){
                     let my_heart = response['my_heart'];
                     if (my_heart['interested'] == 'Y'){
                         $("#heart").css("color", "red");
                         $("#heart").attr("onclick", "unlike()");
                     }
                     else {
                         $("#heart").css("color", "grey");
                         $("#heart").attr("onclick", "like()");
                     }
                 }
             });
         }
         function like(){
             $.ajax({type: 'POST',
                     url: '/like/{{name}}/',
                     data: {
                         interested : "Y"},
                     success: function (response) {
                         alert(response['msg']);
                         window.location.reload()
                     }
                    });
         }
         
         function unlike(){
             $.ajax({
                 type: 'POST',
                 url: '/unlike/{{name}}/',
                 data: {interested : "N"},
                 success: function (response) {
                     alert(response['msg']);
                     window.location.reload()
                 }
             });
         }
         
         $(document).ready(function () {
             showHeart();
         });
