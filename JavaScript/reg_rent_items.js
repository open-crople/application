var keyword_box=document.getElementById("key");
var newTag=document.createElement("label");

function addTag(){
		var newTag=document.createElement("label");
		var delete_button=document.createElement("button");
		delete_button.type="button";
		delete_button.addEventListener("click",deleteTag);
		newTag.id="hashtag";
		newTag.innerHTML="#"+document.getElementsByTagName("form")[0].keyword.value;
		delete_button.innerHTML="X";
		keyword_box.appendChild(newTag);
		newTag.appendChild(delete_button);
}

function deleteTag(){
		keyword_box.removeChild(this.parentNode);
}
