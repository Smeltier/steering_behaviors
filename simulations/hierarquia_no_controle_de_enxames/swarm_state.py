import math
import pygame

from simulations.hierarquia_no_controle_de_enxames.ellipse import Ellipse
from src.states.state import State
from src.outputs.steering_output import SteeringOutput

class SwarmState(State):
    """
    Implementa o controle hierárquico baseado em Campos Potenciais Artificiais (APF).
    
    Esta classe realiza a lei de controle definida na Equação (4) do artigo,
    forçando o agente a convergir para uma formação geométrica definida pela
    abstração 'a = (g, s)'.

    Reference:
        Santos, V. G., & Chaimowicz, L. (2011). Uso de Hierarquias no Controle de Enxames Robóticos.
    """        

    _ellipse: Ellipse
    _k1: float
    _k2: float
    _gamma: float
    _epsilon: float
    DEFAULT_EPSILON: float = 0.1
    DEFAULT_GAMMA: float = 2.0

    def __init__(self, entity, ellipse: Ellipse, k1: float, k2: float) -> None:
        super().__init__(entity)
        self._ellipse = ellipse
        self._k1 = k1
        self._k2 = k2

        self._epsilon = self.DEFAULT_EPSILON
        self._gamma = self.DEFAULT_GAMMA

    def enter(self) -> None:
        pass

    def exit(self) -> None:
        pass

    def execute(self, delta_time: float) -> None:
        steering = self.get_steering()
        self.entity.apply_steering(steering, delta_time)

    def get_steering(self) -> SteeringOutput:
        """
        Calcula o vetor de controle u_i conforme a Equação (4) do artigo.
        
        A lei de controle é composta por:
        1. Força de Formação (-k1 * nabla U): Empurra o agente para minimizar o potencial.
        2. Força de Amortecimento (-k2 * v): Dissipa energia cinética.
        
        Returns:
            steering: SteeringOutput contendo a força linear resultante.
        """

        local_position = self._world_to_local(self.entity.position)
        local_gradient = self._calculate_gradient(local_position)

        local_formation_force = -self._k1 * local_gradient
        global_formation_force = self._local_to_world(local_formation_force)

        damping_force = -self._k2 * self.entity.velocity

        total_force = global_formation_force + damping_force

        steering = SteeringOutput()

        steering.linear = total_force
        steering.angular = 0

        return steering

    def _phi(self, position: pygame.Vector2) -> float:
        """
        Calcula a função phi(q_i, a) conforme a Equação (2) do artigo.

        Mapeia a posição da entidade para sua distância radial relativa à curva implícita
        c(x,y) = 0 definida pela elipse.
        
        Args:
            position: Posição local da entidade (relativa ao centro da elipse).
            
        Returns:
            Valor escalar de distância. Retorna 0 se estiver na origem.
        """

        x, y = position.x, position.y
        a = self._ellipse.a
        b = self._ellipse.b

        distance = position.length()
        if distance == 0: 
            return 0
        
        denominator = math.sqrt((x * b) ** 2 + (y * a) ** 2)
        if denominator == 0:
            return 0
        
        term = (a * b) / denominator
        return distance * (1 - term)
    
    def _potential_U(self, position: pygame.Vector2) -> float:
        """
        Calcula o Campo Potencial Escalar U(q_i, a) conforme a Equação (3) do artigo.

        Gera uma superfície em forma de 'bacia' onde:
        - U = 0 no centro (estável).
        - U = exp(-gamma * phi ^ 2).
        
        Args:
            position: Posição local do robô.
            
        Returns:
            Valor escalar do potencial.
        """

        threshold = 1e-9
        if abs(position.x) < threshold and abs(position.y) < threshold:
            return 0.0

        phi_value = self._phi(position)
        return math.exp(-self._gamma * (phi_value ** 2))
    
    def _calculate_gradient(self, position: pygame.Vector2) -> pygame.Vector2:
        """
        Aproxima o gradiente (nabla U) usando Diferenças Finitas Centrais.

        O gradiente aponta na direção de maior crescimento do potencial (para a borda).
        A lei de controle usará o negativo deste vetor.

        Args:
            position: Posição local onde o gradiente será avaliado.
            
        Returns:
            Vetor representando [dU/dx, dU/dy].
        """

        x_value_plus = self._potential_U(pygame.Vector2(position.x + self._epsilon, position.y))
        x_value_minus = self._potential_U(pygame.Vector2(position.x - self._epsilon, position.y))
        x_gradient = (x_value_plus - x_value_minus) / (2 * self._epsilon)

        y_value_plus = self._potential_U(pygame.Vector2(position.x, position.y + self._epsilon))
        y_value_minus = self._potential_U(pygame.Vector2(position.x, position.y - self._epsilon))
        y_gradient = (y_value_plus - y_value_minus) / (2 * self._epsilon)

        return pygame.Vector2((x_gradient, y_gradient))
    
    def _world_to_local(self, world_position: pygame.Vector2) -> pygame.Vector2:
        """ Converte coordenadas do referencial Global para o referencial da Abstração. """
        translated = world_position - self._ellipse.position
        return translated.rotate(-self._ellipse.rotation)
    
    def _local_to_world(self, local_position: pygame.Vector2) -> pygame.Vector2:
        """ Converte vetores do referencial da Abstração de volta para o Global. """
        return local_position.rotate(self._ellipse.rotation)