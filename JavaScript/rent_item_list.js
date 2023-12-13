function submitForm() {
    document.getElementById('rentForm').submit();
}

function handleButtonClick() {
    {% if not session['id'] %}
    alert('로그인을 먼저하세요!');
     {% else %}
     window.location.href = '/reg_items';
      {% endif %}
}
