# Modelagem do Sistema de Controle de Frota

## Limites do sistema

O sistema controla a **saída** e o **retorno** de veículos próprios da empresa. Uma saída possui apenas um veículo e um motorista. O `Porteiro` é o usuário que efetiva o lançamento na portaria; ele pode ser diferente do motorista. Funcionários motoristas não precisam necessariamente ter uma conta de acesso ao sistema.

O ciclo de vida da saída é:

```text
DISPONIVEL (veículo) -> abrir saída -> EM_USO -> encerrar saída -> DISPONIVEL
```

Se houver manutenção ou desativação, o Administrador deve alterar o status do veículo, impedindo novas liberações.

## Diagramas incluídos

1. **Casos de uso** — define os atores, permissões e validações obrigatórias.
2. **Classes** — representa o domínio PHP, atributos, operações e cardinalidades.
3. **Pacotes** — é o diagrama UML de arquitetura solicitado na avaliação. Ele separa apresentação, aplicação, domínio, infraestrutura e persistência.
4. **Sequência** — detalha a transação mais crítica: abertura da saída e seu encerramento.
5. **Entidade-relacionamento** — espelha o modelo físico/lógico implementado em MySQL.

## Como renderizar

Com PlantUML instalado, na raiz do repositório:

```bash
plantuml -tpng docs/diagrams/*.puml
```

Ou utilize a extensão PlantUML do VS Code e execute **Export Current Diagram**. Para o PDF, insira principalmente o diagrama de pacotes, o diagrama de implantação/DevOps (a serem elaborados pelo grupo), e o MER; os demais diagramas são documentação complementar importante.

## Decisões de banco de dados

- A tabela `usuario` contém somente quem opera o sistema. `funcionario` contém todos os colaboradores aptos ou não a dirigir.
- A tabela `saida_veiculo` conserva a quilometragem inicial e final para fins de auditoria; a quilometragem atual do veículo é atualizada em conjunto no encerramento.
- A coluna gerada `veiculo_em_uso_id` recebe o identificador do veículo apenas para saídas abertas e possui índice único. Assim, o banco também impede duas saídas abertas simultâneas para o mesmo veículo.
- As validações que dependem do momento atual (CNH válida), da categoria e da alteração sincronizada de status/quilometragem devem ser feitas no serviço PHP dentro de uma transação. O índice único é uma proteção adicional contra concorrência.

## Dados que ainda podem ser definidos pelo grupo

- nomes dos três integrantes e URL do repositório;
- política de categorias de CNH por tipo de veículo (o modelo aceita `categoria_cnh_minima`);
- necessidade de anexos, abastecimentos, manutenções e rastreamento GPS, que não fazem parte do escopo inicial.
