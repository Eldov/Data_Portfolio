### **Desafio da SmarttBot** <br/> 
Vaga: Engenheiro de Dados Jr.<br/>
Candidata: Emili Veiga

*#Fiz uso do [Trello](https://trello.com/b/JoSEaRAx/smarttbot) para melhor organização do projeto.*<br/>


### **Dados/Tabelas** <br/>
Foram utilizadas 6 tabelas para a realização do projeto, sendo estas:

[Person_Person](https://trello.com/c/sDbklu37/4-personperson);<br/>
[Production_Product](https://trello.com/c/AvUL119B/6-productionproduct);<br/>
[Sales_Customer](https://trello.com/c/DAp74P41/8-salescustomer);<br/>
[Sales_SalesOrderDetail](https://trello.com/c/5wo7dXIm/10-salessalesorderdetail);<br/>
[Sales_SalesOrderHeader](https://trello.com/c/2l84cKOr/12-salessalesorderheader);<br/>
[Sales_SpecialOfferProduct](https://trello.com/c/rq0MFFJE/14-salesspecialofferproduct).<br/>

Os arquivos .CSV estavam inicialmente delimitados por ";".

Os arquivos terminados em _R a seguir se referem aos documentos com as mudanças que julguei necessárias já feitas:

[Person_Person_R](https://trello.com/c/FCHY0mYs/5-personpersonr);<br/>
[Production_Product_R](https://trello.com/c/Ix21nVSj/7-productionproductionr);<br/>
[Sales_Customer_R](https://trello.com/c/ZF6ECafA/9-salescustomerr);<br/>
[Sales_SalesOrderDetail_R](https://trello.com/c/9HniQHaJ/11-salessalesorderdetailr);<br/>
[Sales_SalesOrderHeader_R](https://trello.com/c/d7XYryvR/13-salessalesorderheaderr);<br/>
[Sales_SpecialOfferProduct_R](https://trello.com/c/3AyHtjX1/15-salesspecialofferproductr).<br/>

O .CSV da tabela Sales_SalesOrderDetail_R não foi anexado ao Trello por ter um peso maior que o permitido. No entanto, todos os arquivos estarão também neste repositório.

### **Modelagem** <br/>

Decidi utilizar o MySQL por ter mais familiaridade com este.
Foi criada uma Base de Dados a partir dos 6 arquivos já citados, cada um com pelo menos uma Primary Key e 3 das tabelas com suas respectivas Foreign Keys como já demonstrado em cada cartão no Trello.
O Diagrama EER resultante foi este:

![image](https://user-images.githubusercontent.com/21317788/163992966-53fd4a14-f20f-4317-aca9-2d44f85a48c0.png)

### **Ferramentas** <br/>

#### Excel: 
Utilizei o Excel para fazer algumas alterações nos arquivos .CSV, tive problemas ao tentar importa-los diretamente ao MySQL onde criaria uma base de dados. Também fiz delecão de algumas colunas e concatenei valores antes de fazer a importação. As tabelas estavam separadas em ";" e após o consumo, separadas em ",".

#### MySQL: 
Foi onde a maior parte do projeto foi feita. Como pode ver através do script SmarttBot MySQL Script, todas as respostas foram desenvolvidas lá, tabelas e base de dados criadas e importadas tanto para o PowerBI quanto para o Jupyter. O diagrama citado acima também foi feito através do MySQL e o arquivo chama-se Modelo SmarttBot.

#### Jupyter Notebook: 
Fiz a importação da Base de Dados do MySQL para o Jupyter. Bibliotecas como Pandas, foram usadas mas admito que não fiz muito o uso do mesmo. Por minha familiaridade ser maior com o SQL, preferi resolver as soluções primeiramente lá. Após feitas as queries, levei-as ao Jupyter. O arquivo usado chama-se SmarttBot Jupyter.

#### PowerBI: 
Fiz uso do PowerBI não só para visualizações finais mas para resolução dos problemas. Aproveitei a ferramenta para organizar meu raciocínio e pensar em como as queries deveriam ser escritas. A ideia de concatenar os nomes da Questão 3 veio de lá onde testei, através de uma fórmula DAX, a junção dos nomes.
O arquivo para visualização em PowerBI chama-se SmarttBot Visualização e pode-se encontra-lo neste repositório.

### **Questões** <br/>

**1. Escreva uma query que retorna a quantidade de linhas na tabela Sales.SalesOrderDetail pelo campo SalesOrderID, desde que tenham pelo menos três linhas de detalhes.**

**2. Escreva uma query que ligue as tabelas Sales.SalesOrderDetail, Sales.SpecialOfferProduct e Production.Product e retorne os 3 produtos (Name) mais vendidos (pela soma de OrderQty), agrupados pelo número de dias para manufatura (DaysToManufacture).**

**3. Escreva uma query ligando as tabelas Person.Person, Sales.Customer e Sales.SalesOrderHeader de forma a obter uma lista de nomes de clientes e uma contagem de pedidos efetuados.**

**4. Escreva uma query usando as tabelas Sales.SalesOrderHeader, Sales.SalesOrderDetail e Production.Product, de forma a obter a soma total de produtos (OrderQty) por ProductID e OrderDate.**

**5. Escreva uma query mostrando os campos SalesOrderID, OrderDate e TotalDue da tabela Sales.SalesOrderHeader. Obtenha apenas as linhas onde a ordem tenha sido feita durante o mês de setembro/2011 e o total devido esteja acima de 1.000. Ordene pelo total devido decrescente.**

As soluções podem ser encontradas tanto no script do MySQL quanto no script do Jupyter Notebook.
Infelizmente não consegui resolver a Questão 2. Meu código levava bastante tempo para carregar e retornava falha pela demora. Entendi que meu conhecimento só ia até ali e reconheço a necessidade de aprender mais. No mais, respondi todas as questões da melhor maneira que pude.
Outra coisa importante a salientar é que as respostas estão um pouco diferentes do MySQL para o Jupyter. Isso ocorreu pois no Jupyter, fiz uso do SQLite e algumas funções existentes no MySQL não existem no SQLite, logo, fiz substituições para as mesmas.

### **Considerações Finais** <br/>

Antes de mais nada, gostaria de agradecer pela chance de ter chegado até aqui no processo. Tenho estudado bastante e ter a oportunidade de testar meus conhecimentos de verdade foi muito bom. Percebi que tenho muito o que melhorar mas também vi o que consegui fazer.
Agradeço também pela paciência de ter lido até aqui e peço encarecidamente pelo feedback. Qualquer conselho ou dica de como eu posso melhorar será igualmente bem-vindo!
Por fim, quero dizer que se receber a oportunidade de fazer parte de seu time, continuarei estudando e melhorando a cada dia, não só por mim, mas para honrar a escolha dos senhores e o voto de confiança dado. Na minha opinião, a melhor forma de agradecer é retribuindo e este seria meu foco: me tornar uma boa integrante na equipe, de forma a ajudar a empresa a crescer mais e mais.
Concluindo, este foi meu projeto, espero que vocês gostem e que em caso de maiores dúvidas, sintam-se livres para me contatar!
