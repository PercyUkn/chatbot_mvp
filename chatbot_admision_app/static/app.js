class Chatbox {
    constructor(){
        this.args =  {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];

    }

    display() {

        const {openButton, chatBox, sendButton} = this.args;
        openButton.addEventListener('click',()=> this.toggleState(chatBox))
        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        const node = chatBox.querySelector('input')
        node.addEventListener("keyup", ({key})=> {
            if (key == "Enter"){
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox){

        this.state = !this.state;

        // Muestra u oculta el chatbox
        if (this.state){
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox){
        let textField = chatbox.querySelector('input');
        let text1 = textField.value;
        if (text1 === ""){
            return;
        }

        let msg1 = {name:"User", message: text1};
        this.messages.push(msg1)

        // POST y GET request
        fetch($SCRIPT_ROOT + '/predict', { // Usa el SCRIPT ROOT para evitar hardcoding
            method: 'POST',
            body: JSON.stringify({message: text1}),
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(r => r.json())
            .then(r => {
                let msg2 = {name: "Sam", message: r.answer} // Utiliza Sam para identificar al chatbot en el método updateChatText
                this.messages.push(msg2);
                this.updateChatText(chatbox);
                textField.value = '';
            }).catch((error)=>{ // Error en la recepción de la respuesta del chatbot
                console.error('Error', error);
                this.updateChatText(chatbox)
                textField.value = ''
        });

    }

    updateChatText(chatbox){

        let html = '';
        this.messages.slice().reverse().forEach(function(item,){
            if (item.name === "Sam"){ // Si es el chatbot
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else // Si es mensaje del usuario
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
        })

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;

    }

}

const chatbox = new Chatbox();
chatbox.display();