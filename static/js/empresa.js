document.addEventListener("DOMContentLoaded", () => {
    carregarEmpresas();

    document.getElementById("empresa-form").addEventListener("submit", async (event) => {
        event.preventDefault();

        const nome = document.getElementById("nome").value;
        const cnpj = document.getElementById("cnpj").value;
        const endereco = document.getElementById("endereco").value;
        const telefone = document.getElementById("telefone").value;
        const email = document.getElementById("email").value;

        await fetchAPI("/empresas", "POST", { nome, cnpj, endereco, telefone, email });
        carregarEmpresas();
    });
});

async function carregarEmpresas() {
    const empresas = await fetchAPI("/empresas");
    const lista = document.getElementById("empresa-list");
    lista.innerHTML = "";

    empresas.forEach((empresa) => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${empresa.nome}</td>
            <td>${empresa.cnpj}</td>
            <td>${empresa.endereco}</td>
            <td>${empresa.telefone}</td>
            <td>${empresa.email}</td>
            <td>
                <button onclick="excluirEmpresa(${empresa.id})">Excluir</button>
            </td>
        `;
        lista.appendChild(row);
    });
}

async function excluirEmpresa(id) {
    await fetchAPI(`/empresas/${id}`, "DELETE");
    carregarEmpresas();
}
