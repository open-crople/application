var cancelButton = document.getElementById("cancelReview");

cancelButton.addEventListener("click", function() {
    var confirmation = confirm("리뷰 작성을 취소하시겠습니까?");
    if (confirmation) {
        history.back();
    }
});
    
var submitButton = document.getElementById("submitReview");

submitButton.addEventListener("click", function() {
    var itemName = "{{ name }}";
    localStorage.setItem('reviewSubmittedForItem', itemName);
    alert("리뷰가 입력되었습니다.");
    
    disableButton(itemName);
});
    
function disableButton(item) {
    var reviewButton = document.getElementById("review_" + item);
    if (reviewButton && !reviewButton.disabled) { // 이미 비활성화된 버튼인지 확인
        reviewButton.disabled = true;
        reviewButton.style.backgroundColor = '#CCCCCC';
        reviewButton.style.cursor = 'not-allowed';
        localStorage.setItem('disabledReviewButton_' + item, 'disabled');
    }
}
    
window.onload = function() {
    var reviewSubmittedForItem = localStorage.getItem('reviewSubmittedForItem');
    var disabledButton = document.getElementById("review_" + reviewSubmittedForItem);
    
    // 저장된 상품 리뷰가 있을 경우 해당 상품 버튼을 비활성화
    if (reviewSubmittedForItem) {
        disableButton(reviewSubmittedForItem);
    }
};
