document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
  // Toggle Background of Selected item 
  document.querySelectorAll(".btn-outline-primary").forEach((button) => {
    button.onclick = () => {
      document.querySelectorAll(".btn-outline-primary").forEach((button) => {
        button.classList.remove("active")
      })
      button.classList.add("active")
    }
  })

  // By default, load the inbox
  load_mailbox('inbox');
  document.querySelector('#inbox').classList.add("active")
});


function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-details').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('form').onsubmit = send_email;
}


function send_email() {
  // Send Email via POST method using the API and log response
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      if (result.error) {
        console.log(result.error);
      };

      if (result.message){
        console.log(result.message);
        load_mailbox('sent');
      };

  }).catch(error => console.log("Fetch Failed: ", error));

  // Stop form from submitting and redirecting to a new page 
  return false
}


function view_email(id, mailbox) {
    // Show compose view and hide other views
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    const email_details = document.querySelector('#email-details')
    email_details.style.display = 'block';
    email_details.innerHTML = '';

    // Get Email 
    fetch(`/emails/${id}`)
    .then(response => response.json())
    .then(email => {
        console.log(email);

        // Write Email Information into the header
        const mailInfo = document.createElement("div")
        mailInfo.style.fontSize = "medium"
        mailInfo.className = "mb-3 border-bottom border-secondary"
        mailInfo.innerHTML = `<strong>From:</strong> ${email.sender} <br>` 
        mailInfo.innerHTML += `<strong>To:</strong> ${email.recipients} <br>` 
        mailInfo.innerHTML += `<strong>Subject:</strong> ${email.subject} <br>` 
        mailInfo.innerHTML += `<strong>Timestamp:</strong> ${email.timestamp} <br>`
        email_details.appendChild(mailInfo);

        // Add Div with Reply and Archive Button
        const btnDiv = document.createElement("div")
        btnDiv.className += "my-2"
        mailInfo.appendChild(btnDiv)

        // Reply Button 
        const reply = document.createElement("button")
        btnDiv.appendChild(reply)
        reply.className += "btn btn-sm btn-info"
        reply.innerText = "Reply"
        reply.onclick = () => {
          compose_email();
          document.querySelector('#compose-recipients').value = email.sender;
          document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
          document.querySelector('#compose-body').value = `\n\n\n-- On ${email.timestamp} ${email.sender} wrote: \n${email.body}`
        }

        // Archive Button - not visible in sent section
        if (mailbox != "sent"){
          const archive = document.createElement("button")
          btnDiv.appendChild(archive)
          archive.className += "btn btn-sm btn-secondary mx-2"
          if (email.archived) {
            archive.innerText = "Unarchive"
          } else {
            archive.innerText = "Archive"
          }
          archive.onclick = () => {
            if (email.archived) {
              archiveEmail(email.id, false)
            } else {
              archiveEmail(email.id, true)
            }
            load_mailbox("inbox")
          }
        }

        // Div for the Mail Body
        const mailSubect = document.createElement("div")
        mailSubect.style.whiteSpace = "pre-wrap"
        mailSubect.innerHTML = `${email.body}`
        email_details.appendChild(mailSubect)

        // Div with back to inbox button 
        const returnBtnDiv = document.createElement("div")
        email_details.appendChild(returnBtnDiv)
        returnBtnDiv.classList.add("text-center","mt-4")
        const returnBtn = document.createElement("button")
        returnBtnDiv.appendChild(returnBtn)
        returnBtn.className += "btn btn-sm btn-secondary"
        returnBtn.innerText = "Return To Inbox"
        returnBtn.onclick = () => {
          load_mailbox("inbox")
        }

        // Tag email as read 
        if (email.read != "true") {
          fetch(`/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                read: true
            })
          });
        }
    });
}


function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-details').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get emails for mailbox via API 
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      console.log(`in load_mailsbox ${mailbox}`, emails);
          
      // Display all Emails as divs
      emails.forEach(email => {
        const element = document.createElement("div");
        element.className += 'my-2 p-2 email'

        // Set Email Title
        element.innerHTML = `<div class="float-left"><strong>${email.sender}</strong><span class="mx-3">${email.subject}</span></div>`;
        element.innerHTML += `<div class="float-right">${email.timestamp}</div>`;
        element.innerHTML += '<div class="clearfix"></div>';

        // Change background if is not read 
        if (email.read) {
          element.style.backgroundColor = "white"
        } else {
          element.style.backgroundColor = "lightgray"
        }

        // View Email on Click 
        element.addEventListener("click", (event) => {
          console.log("This E-mail has been clicked!")
          view_email(email.id, mailbox);
        });
        document.querySelector("#emails-view").append(element);
      });
  });
}


function archiveEmail(id, bool) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: bool
    })
  })
} 