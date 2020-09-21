document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll("#edit").forEach( (button) => {
        button.onclick = () => {
            body = button.offsetParent.children[1];
        
            // Create new textfield and fill it with previous values
            const editField = document.createElement("textarea");
            editField.rows = 10;
            editField.classList.add("form-control");
            editField.value = body.getElementsByTagName("p")[0].innerText
            body.appendChild(editField);

            body.getElementsByTagName("p")[0].classList.add("d-none")

            // Display Save and Cancel Button 
            const btnDiv = document.createElement("div")
            btnDiv.classList.add("container", "text-center", "mt-3")
            body.appendChild(btnDiv) 
            const saveBtn = document.createElement("button");
            saveBtn.classList.add("btn", "btn-success", "btn-sm", "mx-3")
            saveBtn.innerText = "Save"
            btnDiv.appendChild(saveBtn);
            const cancelBtn = document.createElement("button");
            cancelBtn.classList.add("btn", "btn-secondary", "btn-sm")
            cancelBtn.innerText = "Cancel"
            btnDiv.appendChild(cancelBtn);

        }
    })
})