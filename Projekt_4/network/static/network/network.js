document.addEventListener('DOMContentLoaded', () => {
    // Add Edit button functionality for all buttons
    document.querySelectorAll("#edit").forEach( (button) => {
        showEditButtons(button);
    })

    // Like button functionality
    document.querySelectorAll("#likeBtn").forEach( (button) => {
        button.onclick = () => {
            likePost(button);
        }
    })

    // Follow/Unfollow button functionality 
    document.querySelectorAll("#followBtn").forEach( (button) => {
        button.onclick = () => {
            fetch("/api/follow", {
                method: 'PUT',
                body: JSON.stringify({
                    profile_id: profile_id
                })
            })

            const followBtn = document.querySelector("#followBtn")
            if (followBtn.innerText === "Follow") {
                followBtn.innerText = "Unfollow"
            } else {
                followBtn.innerText = "Follow"
            }
        }
    })

})


function showEditButtons(button) {
    button.onclick = () => {
        const body = button.offsetParent.children[1];
    
        // Disable all edit buttons while editing 
        document.querySelectorAll("#edit").forEach( (button) => {
            button.disabled = true
        })

        // Create new textfield and fill it with previous values
        const editField = document.createElement("textarea");
        editField.rows = 7;
        editField.classList.add("form-control");
        editField.value = body.getElementsByTagName("p")[0].innerText
        body.appendChild(editField);

        // Hide previous content
        prevPost = body.getElementsByTagName("p")[0]
        prevPost.classList.add("d-none")

        // Display Save and Cancel Button 
        const btnDiv = document.createElement("div")
        btnDiv.classList.add("container", "text-center", "mt-3")
        body.appendChild(btnDiv) 
        const saveBtn = document.createElement("button");
        btnDiv.appendChild(saveBtn);
        saveBtn.classList.add("btn", "btn-success", "btn-sm", "mx-3")
        saveBtn.innerText = "Save"
        saveBtn.onclick = () => {
            const post_id = button.parentNode.querySelector("#post_id").value
            saveChanges(post_id, editField.value)
            prevPost.innerHTML = editField.value
            finishEditing(prevPost, editField, btnDiv);
        }
        const cancelBtn = document.createElement("button");
        btnDiv.appendChild(cancelBtn);
        cancelBtn.classList.add("btn", "btn-secondary", "btn-sm")
        cancelBtn.innerText = "Cancel"
        cancelBtn.onclick = () => {
            finishEditing(prevPost, editField, btnDiv);
        }
    }
}


function saveChanges(id, content){
    fetch(`/posts/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          content: content
        })
    })
} 


function finishEditing(prevPost, editField, btnDiv) {
    // display content again and remove buttons and edit field
    prevPost.classList.remove("d-none")
    editField.remove()
    btnDiv.remove()
    // Enable all Edit buttons after editing 
    document.querySelectorAll("#edit").forEach( (button) => {
        button.disabled = false
    })
}


function likePost(button) {
    const post_id = button.parentNode.offsetParent.querySelector("#post_id").value
    fetch(`/api/posts/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
          like: true
        })
    })

    // Change like icon and count, where fa class == like & far == not like 
    const num_likes = button.parentNode.querySelector("#num_likes")
    const symbolClasses = button.parentNode.querySelector("#likeBtn").querySelector("i").classList
    if (symbolClasses.contains("fa")) {
        num_likes.innerText = parseInt(num_likes.innerText) - 1
        symbolClasses.remove("fa")
        symbolClasses.add("far")
    } else {
        num_likes.innerText = parseInt(num_likes.innerText)  + 1
        symbolClasses.remove("far")
        symbolClasses.add("fa")
    }
}