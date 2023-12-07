$(document).ready(function () {
  //alert("{{category}}");
  $('#category option:contains("{{current_category}}")').prop("selected",true);
});

function handleButtonClick() {
  {% if not session['id'] %}
    alert('로그인을 먼저하세요!');
  {% else %}
    window.location.href = '/reg_items';
  {% endif %}
}
       
function submitForm() {
  document.getElementById('rentForm').submit();
}
