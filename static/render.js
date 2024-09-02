const Login_zone = document.querySelector('.login_input_zone');
const login_title = document.querySelector('#login_title');


// Cria um objeto com os dados de login do usuario
let user_login = {
    Name: "nome do usuario",
    Password: "password do usuario",
    Pergunta_Seguranca: "pergunta de segurança",
    Resposta: "resposta da pergunta de segurança",
}

function delete_login_data() {

    // reinicia o objeto com os dados de login do usuario
    user_login = {
        Name: "nome do usuario",
        Password: "password do usuario",
        Pergunta_Seguranca: "pergunta de segurança",
        Resposta: "resposta da pergunta de segurança",
    }
    
}

// Função que atualiza o formulário de login com os inputs para a pergunta de segurança e a resposta
// e atualiza o objeto com o primeira parte dos dados de login o Nome e a Senha
function login_part1(event) {
    event.preventDefault(); // Prevenir o comportamento padrão do formulário

    // Capturar os valores dos inputs
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    
    let usuario_a_verificar = {
        Name: username,
        Password: password,
        login_process: "part1"
    }

    //Envia os Dados para o endereço que vai enviar para o DB
    
    fetch('http://127.0.0.1:5000/Secure_Login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(usuario_a_verificar)
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Erro: erro no envio da lista_atual', error));

    // atualiza o formulário de login mostrando os inputs para a pergunta de segurança e a resposta
    Login_zone.innerHTML = `
    <input type="text" id="pergunta_seguranca" name="pergunta_seguranca" placeholder="Sua Pergunta de segurança">
    <input type="password" id="Resposta" name="Resposta" placeholder="Resposta">
    <div class="button-group">
        <button type="submit" name="action" value="login" onclick="login_part2(event)" class="btn btn-primary">Entrar</button>
    </div>
`
}

function login_part2(event) {
    event.preventDefault(); // Prevenir o comportamento padrão do formulário


    // Capturar os valores dos inputs
    let pergunta_seguranca = document.getElementById('pergunta_seguranca').value;
    let Resposta = document.getElementById('Resposta').value;

    // Atualiza o objeto com os dados de login com os novos dados, pergunta_segurança e resposta
    let usuario_a_verificar = {
        Name: pergunta_seguranca,
        resposta_Secreta: Resposta,
        login_process: "part2"
    }

    //Envia os Dados para o endereço que vai enviar para o DB
    
    fetch('http://127.0.0.1:5000/Secure_Login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(usuario_a_verificar)
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Erro: erro no envio da lista_atual', error));

    // por motivos de segurança, os dados do usuario seram alterados
    delete_login_data()
}


function Show_register_form() {

    login_title.innerHTML = "Registrar";

    // atualiza o formulário de login com a pergunta de segurança e resposta
    Login_zone.innerHTML = `
    <input type="text" id="username" name="username" placeholder="Nome">
    <input type="password" id="password" name="password" placeholder="Senha">
    <input type="text" id="pergunta_seguranca" name="pergunta_seguranca" placeholder="Sua Pergunta de segurança">
    <input type="password" id="Resposta" name="Resposta" placeholder="Resposta">
    <div class="button-group">
        <button type="submit" name="action" value="login" class="btn btn-danger" onclick="Register(event)">Registrar</button>
    </div>
    `
}

function Register(event) {
    event.preventDefault(); // Prevenir o comportamento padrão do formulário

    // Capturar os valores dos inputs
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;
    let pergunta_seguranca = document.getElementById('pergunta_seguranca').value;
    let Resposta = document.getElementById('Resposta').value;

    // Verifica se todos os campos foram preenchidos
    if (username == "" || password == "" || pergunta_seguranca == "" || Resposta == "") {
        alert("Preencha todos os campos")
        return
    }

    let Nova_Conta = {
        Name: username,
        Password: password,
        Pergunta_Seguranca: pergunta_seguranca,
        resposta_Secreta: Resposta,
    }

    console.log(Nova_Conta)
    
    //Envia os Dados para o endereço que vai enviar para o DB
    fetch('http://127.0.0.1:5000/Register_New_Account', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(Nova_Conta)
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Erro: erro no envio da lista_atual', error));
}

// Envia informações para o servidor
function enviar_Lista_Atual() {

    // Pega a lista atual
    let insert_list = {
        user_id: "exemplo_user_id",  // Este ID será substituído pelo backend
        created_at: new Date().toISOString(),
        items: lista_atual,
        total_price: calcularTotal()
    };

    // Envia informações para o endereço que vai enviar para o DB
    fetch('http://127.0.0.1:5000/send_to_DB', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(insert_list)
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error('Erro: erro no envio da lista_atual', error));
}
