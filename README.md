<h1 align="center">Steering Behaviors</h1>

---

Projeto de simulação de comportamentos de steering com Pygame.

O repositório combina:
- comportamentos clássicos de steering (seek, flee, arrive, wander, separation, cohesion, etc.);
- blending e prioridade de comportamentos;
- simulações de enxame (boids);
- planejamento de caminho em grade com A* e D* Lite;
- experimentos de formação com elipse e deformação por colisão.

## Tecnologias

- Python 3.10+
- Pygame 2.6.1

## Estrutura do projeto

```text
steering_behaviors/
  docs/          # diagrama de classes (PlantUML)
  simulations/   # scripts de simulação e demonstrações
  src/           # entidades, estados, máquinas e saídas de steering
  utils/         # D* Lite, grade, elipse e utilitários geométricos
```

## Instalação

1. Clone o repositório.

```bash
git clone https://github.com/Smeltier/steering_behaviors.git
```

2. Crie um ambiente virtual.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Instale as dependências.

```bash
pip install -r requirements.txt
```

## Simulações

A partir da raiz do projeto:

```bash
python3 simulations/reynolds_boids.py
python3 simulations/circle_simulation.py
python3 simulations/follow_with_state.py
python3 simulations/follow_with_a_star.py
python3 simulations/follow_with_d_star_lite.py
python3 simulations/d_star_lite_com_elipse.py
python3 simulations/d_star_lite_com_deformacao.py
python3 simulations/alvos_dinamicos_d_star.py
python3 simulations/deformacao_elipse.py
python3 simulations/deformacao_circulo.py
python3 simulations/mesclando_elipse_com_separation.py
```

## Comportamentos implementados

| Comportamento | Descrição breve |
| --- | --- |
| Seek | Move a entidade em direção ao alvo na maior aceleração possível. |
| Flee | Move a entidade para longe de um alvo ameaçador. |
| Arrive | Aproxima-se do alvo desacelerando ao entrar no raio de chegada. |
| Wander | Gera movimento exploratório contínuo com direção parcialmente aleatória. |
| Face | Ajusta a orientação da entidade para olhar para o alvo. |
| Align | Alinha a rotação da entidade com a orientação/rotação de referência. |
| Pursue | Persegue um alvo móvel prevendo sua posição futura. |
| Evade | Evita um perseguidor prevendo sua posição futura. |
| VelocityMatch | Ajusta a velocidade para ficar parecida com a de outra entidade. |
| Separation | Afasta agentes próximos para evitar aglomeração e colisões locais. |
| Cohesion | Puxa o agente para o centro do grupo para manter coesão. |
| SwarmState | Controla formação em enxame com campo potencial (ex.: elipse). |
| PathFollow | Segue uma sequência de waypoints definida previamente. |
| DStarPathFollow | Segue caminho gerado por D* Lite com replanning em ambiente dinâmico. |
| BlendedSteering | Combina múltiplos comportamentos por pesos em um único steering. |
| PrioritySteering | Avalia comportamentos por prioridade e usa o primeiro relevante. |
| MultiTargetSteering | Base para comportamentos que consideram múltiplos alvos/agentes. |
| CollisionAvoidance | Detecta risco de colisão e gera desvio preventivo. |
| MaintainRadius | Mantém distância radial desejada em relação a um alvo/centro. |
| Attraction | Atrai o agente para regiões/alvos conforme função de atração. |

## Licença

Distribuído sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.
