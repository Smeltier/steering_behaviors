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

    def __init__(self, entity, ellipse: Ellipse, k1: float, k2: float, gamma: float = 0.1, episilon: float = 0.1) -> None:
        super().__init__(entity)
        self._ellipse = ellipse
        self._k1 = k1
        self._k2 = k2
        self._gamma = gamma
        self._epsilon = episilon

    def execute(self, delta_time: float) -> None:
        steering = self.get_steering()
        self.entity.apply_steering(steering, delta_time)

    def enter(self):
        pass
    
    def exit(self):
        pass

    def get_steering(self) -> SteeringOutput:
        """
        Calcula o vetor de controle u_i conforme a Equação (4) do artigo.
        
        A lei de controle é composta por:
        1. Força de Formação (-k1 * nabla U): Empurra o agente para minimizar o potencial.
        2. Força de Amortecimento (-k2 * v): Dissipa energia cinética.
        
        Returns:
            steering: SteeringOutput contendo a força linear resultante.
        """
        local_position = self.__world_to_local(self.entity.position)
        local_gradient = self._calculate_gradient(local_position)

        local_formation_force = -self._k1 * local_gradient
        global_formation_force = self.__local_to_world(local_formation_force)

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
        a, b = self._ellipse.a, self._ellipse.b
        distance = position.length()
        threshold: float = 1e-6

        if distance < threshold: 
            return 0.0
        
        elliptic_denominator = math.sqrt((x * b) ** 2 + (y * a) ** 2)
        if elliptic_denominator < threshold:
            return 0.0
        
        scale_factor = (a * b) / elliptic_denominator
        return distance * (1.0 - scale_factor)
    

    def _potential_U(self, position: pygame.Vector2) -> float:
        threshold: float = 1e-6
        distance = position.length()

        if distance < threshold:
            return 0.0
        
        phi_value = self._phi(position = position)
        return math.exp(-self._gamma * (phi_value ** 2))

    def _calculate_gradient(self, position: pygame.Vector2) -> pygame.Vector2:
        x_value_plus = self._potential_U(pygame.Vector2(position.x + self._epsilon, position.y))
        x_value_minus = self._potential_U(pygame.Vector2(position.x - self._epsilon, position.y))
        x_gradient = (x_value_plus - x_value_minus) / (2 * self._epsilon)

        y_value_plus = self._potential_U(pygame.Vector2(position.x, position.y + self._epsilon))
        y_value_minus = self._potential_U(pygame.Vector2(position.x, position.y - self._epsilon))
        y_gradient = (y_value_plus - y_value_minus) / (2 * self._epsilon)

        return pygame.Vector2((x_gradient, y_gradient))

    def __world_to_local(self, world_position: pygame.Vector2) -> pygame.Vector2:
        translated = world_position - self._ellipse.position
        return translated.rotate(-self._ellipse.rotation)
    
    def __local_to_world(self, local_position: pygame.Vector2) -> pygame.Vector2:
        return local_position.rotate(self._ellipse.rotation)
    
    # def _calculate_phi_gradient(self, position: pygame.Vector2) -> pygame.Vector2:
    #     threshold = 1e-6
    #     distance = position.length()

    #     if distance < threshold:
    #         return pygame.Vector2(0, 0)

    #     a, b = self._ellipse.a, self._ellipse.b
    #     x, y = position.x, position.y

    #     elliptic_denominator = math.sqrt((x * b)**2 + (y * a)**2)
    #     if elliptic_denominator < threshold:
    #         return pygame.Vector2(0, 0)

    #     common_factor = (a * b) / elliptic_denominator
    #     inner_derivative_scale = (a * b) / (elliptic_denominator**3)

    #     dphi_dx = (x / distance) * (1.0 - common_factor) \
    #             + distance * inner_derivative_scale * x * (b ** 2)

    #     dphi_dy = (y / distance) * (1.0 - common_factor) \
    #             + distance * inner_derivative_scale * y * (a ** 2)

    #     return pygame.Vector2(dphi_dx, dphi_dy)
    
    # def _calculate_gradient(self, position: pygame.Vector2, phi: float) -> pygame.Vector2:
    #     """ Calcula o Gradiente baseado na derivada analítica do Campo Escalar U. """
    #     threshold: float = 1e-6
    #     distance = position.length()

    #     if distance < threshold: 
    #         return pygame.Vector2(0, 0)

    #     a, b = self._ellipse.a, self._ellipse.b
    #     x, y = position.x, position.y
        
    #     elliptic_denominator = math.sqrt((x * b)**2 + (y * a)**2)
        
    #     exponential_term = math.exp(-self._gamma * (phi**2))
    #     du_dphi = -2.0 * self._gamma * phi * exponential_term

    #     common_factor = (a * b) / elliptic_denominator
    #     inner_derivative_scale = (a * b) / (elliptic_denominator**3)
        
    #     dphi_dx = (x / distance) * (1.0 - common_factor) + distance * (inner_derivative_scale * x * (b ** 2))
    #     dphi_dy = (y / distance) * (1.0 - common_factor) + distance * (inner_derivative_scale * y * (a ** 2))
        
    #     return du_dphi * pygame.Vector2(dphi_dx, dphi_dy)