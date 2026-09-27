# Controle de Frota

Documentação de análise e modelagem para um sistema web de controle de saída e retorno de veículos corporativos, desenvolvido em PHP e MySQL.

## Objetivo

Controlar a utilização de carros, caminhões e motocicletas. Antes de liberar uma saída, o sistema identifica o motorista, valida a CNH e a disponibilidade do veículo e registra data/hora, quilometragem, placa e destino. No retorno, registra a data/hora e a quilometragem final, encerra a saída e devolve o veículo à condição disponível.

## Perfis de acesso

| Perfil | Responsabilidades |
|---|---|
| Administrador | Mantém usuários, funcionários e veículos; consulta todas as saídas e relatórios. |
| Porteiro | Registra e encerra as saídas; consulta veículos e motoristas para a operação da portaria. |

## Regras de negócio essenciais

1. Uma saída só pode ser aberta para veículo com status `DISPONIVEL`.
2. O motorista deve estar ativo, possuir CNH cadastrada e com validade igual ou posterior à data da saída.
3. A categoria da CNH precisa ser compatível com a categoria exigida pelo veículo.
4. Um veículo só pode ter uma saída aberta por vez.
5. A quilometragem de retorno não pode ser menor que a quilometragem de saída.
6. Ao abrir uma saída, o veículo fica `EM_USO`; ao encerrá-la, volta a `DISPONIVEL`.
7. Veículos em `MANUTENCAO` ou `INATIVO` não podem ser liberados.
8. Somente Administradores alteram cadastros estruturais e acessos; Administradores e Porteiros realizam o registro operacional das saídas.

## Artefatos

| Arquivo | Conteúdo |
|---|---|
| `docs/diagrams/01-casos-de-uso.puml` | Escopo funcional e atores. |
| `docs/diagrams/02-diagrama-de-classes.puml` | Modelo UML de domínio. |
| `docs/diagrams/03-diagrama-de-pacotes.puml` | Arquitetura lógica em camadas/módulos. |
| `docs/diagrams/04-sequencia-saida-retorno.puml` | Fluxo principal de abertura e encerramento. |
| `docs/diagrams/05-modelo-entidade-relacionamento.puml` | Modelo lógico do banco. |
| `docs/diagrams/06-diagrama-de-implantacao.puml` | Arquitetura de implantação (VPS, containers web/db, volume). |
| `docs/diagrams/07-diagrama-devops.puml` | Arquitetura DevOps / pipeline CI-CD (GitHub Actions, GHCR, deploy). |
| `database/schema.sql` | DDL MySQL 8+ para criação do banco. |
| `docs/MODELAGEM.md` | Decisões e instruções para gerar as imagens. |

Os arquivos `.puml` podem ser renderizados localmente com PlantUML ou pelo editor/preview PlantUML do VS Code. As imagens geradas devem ser versionadas em `docs/diagrams/rendered/` quando forem inseridas no PDF da avaliação.
