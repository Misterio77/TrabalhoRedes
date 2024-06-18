---
lang: pt_BR
title: Ensino de redes com ferramentas "as-code"
subtitle: SCC5797 - Seminário
author: Gabriel Fontes (10856803)
documentclass: beamer
theme: Antibes
fontsize: 10pt
---

# Motivação

## Dificuldades em ferramentas imperativas

- Dificuldade em reproduzir uma rede
    - Passos manuais
    - Inconsistências (e.g. precisar ficar rebootando)

## Vantagens da abordagem "as-code"

- Cooperação: compartilhar soluções entre alunos
- Reproduzir problemas facilmente, ao invés de lutar com a ferramenta
- Possibilitar projetos mais complexos
    - Graças à ferramentas de engenharia de software (VCS, testes automáticos, etc)

# Objetivos

## Research Question

> É viável utilizar "as-code" no ensino de redes?

# Metodologia

## Revisão da literatura de "as-code"

- Levantar o estado da arte em ferramentas para declarar redes como código
    - Descrição e configurações de equipamentos em rede
- Simuladores, VMs, ferramentas de "as-code"
    - Não basta apenas configurar máquinas, deve existir uma forma de simular elas como um todo

## Busca por "as-code" no ensino de redes

- Por enquanto, só encontrei artigos sobre "as-code" em contexto de ensino de cloud (onde "as-code" é nativo), não no curso usual de redes
- Comparar com ferramentas tradicionais imperativas (e.g. packet tracer)
    - Quais as vantagens e desvantagens?
    - Formas mais declarativas de usar ferramentas existentes?
        - GNS3

## Construção de PoC

- Explorar viabilidade técnica implementando uma PoC

## Feedback

- Aplicar ferramenta no ensino
- Colher feedback, por meio de entrevista

## Questões

- Facilita plágio?
- As ferramentas são leaky abstractions?
    - Receio de se tornar "aula sobre ferramenta X"
- Alunos tem maturidade suficiente (e.g. VCS) para os benefícios serem tangíveis?

# Prova de conceito

## Startup configuration (imperativo)

Criar nó usando API do GNS3:
```
POST https://gns3.m7.rs/v2/projects/xxx/templates/yyy
{
    "node_type": "dynamips",
    "name": "r0"
}
```

Configuração via arquivo + netcat
```
ipv6 unicast-routing
interface fastethernet 0/0
 no ip address
 ipv6 address 2001::1/64
 ipv6 ospf 1 area 0
 no shut
!
```

```
nc -t -w 5 gns3.m7.rs 5001 < ospf.cfg
```

## Esboço terraform

Imperativo:

```hcl
resource "gns3_node" "r0" {
    project = "xxx"
    template = "yyy"
    type = "dynamips"
    startup_commands = ./ospf.cfg
}
```

## Esboço terraform

Declarativo:

```hcl
resource "packettracer_router_cisco" "r0" {
    project = "xxx"
    ipv6 {
        unicast-routing = true
    }
    interface "fastethernet 0/0" {
        ipv6 {
            address = "2001::1/64"
            ospf "1" {
                area = 0
            }
        }
    }
}
```

# Cronograma

## Cronograma

Planeja-se uma execução em 3 meses.

1. Revisão da literatura
    - "as-code" no ensino de redes
    - "as-code" em simuladores de rede
2. Levantar ferramentas para uma PoC
    - No momento o candidato esperado é GNS3
3. Construir PoC
    - Imperativa
    - Declarativa
4. Avaliar viabilidade testando com alunos

| Mes\\Etapa | 1 | 2 | 3 | 4 |
|------------|---|---|---|---|
|  1         | x | x |   |   |
|  2         |   | x | x |   |
|  3         |   |   | x | x |


# Considerações Finais

## Thanks!

:)
