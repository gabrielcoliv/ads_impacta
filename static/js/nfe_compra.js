document.addEventListener("DOMContentLoaded", function () {
  carregarFornecedores();
  carregarProdutos();

  document.getElementById("addItem").addEventListener("click", adicionarItem);
  document.getElementById("formNotaFiscal").addEventListener("submit", salvarNota);
});

function carregarFornecedores() {
  fetch("/fornecedores_json")
    .then(response => response.json())
    .then(data => {
      const select = document.getElementById("fornecedor_id");
      data.forEach(fornecedor => {
        const option = document.createElement("option");
        option.value = fornecedor.id;
        option.textContent = fornecedor.nome;
        select.appendChild(option);
      });
    })
    .catch(error => console.error("Erro ao carregar fornecedores:", error));
}

function carregarProdutos() {
  fetch("/produtos_json")
    .then(response => response.json())
    .then(data => {
      window.listaProdutos = data; // Armazena para usar ao adicionar itens
    })
    .catch(error => console.error("Erro ao carregar produtos:", error));
}

function adicionarItem() {
  const tbody = document.querySelector("#itensTable tbody");
  const tr = document.createElement("tr");

  const tdProduto = document.createElement("td");
  const selectProduto = document.createElement("select");
  selectProduto.classList.add("produto");
  window.listaProdutos.forEach(produto => {
    const option = document.createElement("option");
    option.value = produto.id;
    option.textContent = produto.nome;
    selectProduto.appendChild(option);
  });
  tdProduto.appendChild(selectProduto);

  const tdQuantidade = document.createElement("td");
  const inputQtd = document.createElement("input");
  inputQtd.type = "number";
  inputQtd.classList.add("quantidade");
  inputQtd.min = "0";
  inputQtd.step = "1";
  inputQtd.addEventListener("input", atualizarTotal);
  tdQuantidade.appendChild(inputQtd);

  const tdPreco = document.createElement("td");
  const inputPreco = document.createElement("input");
  inputPreco.type = "number";
  inputPreco.classList.add("preco");
  inputPreco.min = "0";
  inputPreco.step = "0.01";
  inputPreco.addEventListener("input", atualizarTotal);
  tdPreco.appendChild(inputPreco);

  const tdAcoes = document.createElement("td");
  const btnRemover = document.createElement("button");
  btnRemover.textContent = "Remover";
  btnRemover.type = "button";
  btnRemover.addEventListener("click", () => {
    tr.remove();
    atualizarTotal();
  });
  tdAcoes.appendChild(btnRemover);

  tr.appendChild(tdProduto);
  tr.appendChild(tdQuantidade);
  tr.appendChild(tdPreco);
  tr.appendChild(tdAcoes);

  tbody.appendChild(tr);
}

function atualizarTotal() {
  let total = 0;
  document.querySelectorAll("#itensTable tbody tr").forEach(row => {
    const qtd = parseFloat(row.querySelector(".quantidade").value) || 0;
    const preco = parseFloat(row.querySelector(".preco").value) || 0;
    total += qtd * preco;
  });
  document.getElementById("valor_total").value = total.toFixed(2);
}

function salvarNota(e) {
  e.preventDefault();

  const numero = document.getElementById("numero").value;
  const serie = document.getElementById("serie").value;
  const data_emissao = document.getElementById("data_emissao").value;
  const fornecedor_id = document.getElementById("fornecedor_id").value;
  const valor_total = document.getElementById("valor_total").value;

  const itens = [];
  document.querySelectorAll("#itensTable tbody tr").forEach(row => {
    const produto_id = row.querySelector(".produto").value;
    const quantidade = parseFloat(row.querySelector(".quantidade").value);
    const preco_unitario = parseFloat(row.querySelector(".preco").value);

    if (produto_id && quantidade && preco_unitario) {
      itens.push({ produto_id, quantidade, preco_unitario });
    }
  });

  const notaFiscal = {
    numero,
    serie,
    data_emissao,
    fornecedor_id,
    valor_total,
    itens
  };

  fetch("/nota_fiscal_compra", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(notaFiscal)
  })
    .then(res => {
      if (!res.ok) throw new Error("Erro ao salvar nota fiscal.");
      return res.json();
    })
    .then(data => {
      alert(data.mensagem || "Nota salva com sucesso!");
      window.location.href = "/nfe_lista"; // Redireciona após sucesso
    })
    .catch(error => {
      console.error("Erro:", error);
      alert("Erro ao salvar a nota fiscal.");
    });
}
