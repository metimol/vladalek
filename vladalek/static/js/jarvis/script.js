document.addEventListener('DOMContentLoaded', () => {
	const msgerInput = document.getElementById('msger-input')
	const msgerChat = document.getElementById('msger-chat')
	const msgerForm = document.getElementById('msger-inputarea')
	const button = document.getElementById('button_send')
	
	// Icons made by Freepik from www.flaticon.com
	const BOT_IMG = "https://cdn-icons-png.flaticon.com/512/86/86494.png";
	const PERSON_IMG = "https://cdn-icons-png.flaticon.com/512/86/86483.png";
	const BOT_NAME = "Jarvis";
	const PERSON_NAME = "User";
	
	button.addEventListener("click", () => {
	  const msgText = msgerInput.value;
	  if (!msgText) return;
	
	  appendMessage(PERSON_NAME, PERSON_IMG, "right", msgText);
	  msgerInput.value = "";
	
	  botResponse(msgText);
	});
	
	msgerInput.addEventListener("keypress", function(event) {
	  if (event.key === "Enter") {
	    event.preventDefault();
	    button.click();
	  }
	});
	
	function appendMessage(name, img, side, text) {
	  //   Simple solution for small apps
	  const msgHTML = `
	    <div class="msg ${side}-msg">
	      <div class="msg-img" style="background-image: url(${img})"></div>
	
	      <div class="msg-bubble">
	        <div class="msg-info">
	          <div class="msg-info-name">${name}</div>
	          <div class="msg-info-time">${formatDate(new Date())}</div>
	        </div>
	
	        <div class="msg-text">${text}</div>
	      </div>
	    </div>
	  `;
	
	  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
	  msgerChat.scrollTop += 500;
	}
	
	function botResponse(text) {
		var data = JSON.stringify({"password": "apijarvisapiapi20050510", "text": text});
		fetch("", {
			  credentials: "same-origin",
		    mode: "same-origin",
		    method: "post",
		    headers: { "Content-Type": "application/json" },
		    body: data
		})
				.then(resp => {
		       if (resp.status === 200) {
		           return resp.json()
		        } else {
		           console.log("Status: " + resp.status)
		           return Promise.reject("server")
			      }
			   })
			   .then(dataJson => {
			       appendMessage(BOT_NAME, BOT_IMG, "left", dataJson.text)
			   })
			   .catch(err => {
			       if (err === "server") return
			       console.log(err)
			   })
	}
	
	function formatDate(date) {
	  const h = "0" + date.getHours();
	  const m = "0" + date.getMinutes();
	
	  return `${h.slice(-2)}:${m.slice(-2)}`;
	}
})