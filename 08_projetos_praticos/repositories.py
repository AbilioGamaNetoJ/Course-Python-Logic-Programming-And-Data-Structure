"""
Módulo de Repositórios e Validadores
====================================

Este módulo contém as implementações de repositórios para persistência de dados
e validadores para garantir a integridade dos dados no sistema de gestão.

Estruturas de Dados Utilizadas:
- Dict: Para armazenamento principal dos dados (O(1) para busca por ID)
- defaultdict: Para índices automáticos sem verificação de existência
- Set: Para conjuntos de IDs nos índices (operações de interseção eficientes)
- threading.RLock: Para thread-safety em operações concorrentes

Padrões de Design:
- Repository Pattern: Abstração do acesso a dados
- Strategy Pattern: Diferentes estratégias de validação
- Template Method: Interface comum para repositórios
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Set
from collections import defaultdict
import threading

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config


# ================================
# INTERFACES ABSTRATAS
# ================================

class RepositorioBase(ABC):
    """
    Interface base para repositórios.
    
    Define o contrato que todos os repositórios devem seguir,
    permitindo diferentes implementações (memória, banco de dados, etc.)
    """
    
    @abstractmethod
    def criar(self, entidade: Any) -> str:
        """Cria uma nova entidade e retorna seu ID."""
        pass
    
    @abstractmethod
    def buscar(self, id: str) -> Optional[Any]:
        """Busca uma entidade por ID."""
        pass
    
    @abstractmethod
    def listar(self, filtros: Dict[str, Any] = None) -> List[Any]:
        """Lista entidades com filtros opcionais."""
        pass
    
    @abstractmethod
    def atualizar(self, id: str, dados: Dict[str, Any]) -> bool:
        """Atualiza uma entidade."""
        pass
    
    @abstractmethod
    def deletar(self, id: str) -> bool:
        """Deleta uma entidade."""
        pass


class ValidadorBase(ABC):
    """
    Interface base para validadores.
    
    Implementa o padrão Strategy para diferentes tipos de validação.
    """
    
    @abstractmethod
    def validar(self, dados: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Valida dados e retorna (válido, lista_erros).
        
        Args:
            dados: Dicionário com os dados a serem validados
            
        Returns:
            Tuple[bool, List[str]]: (é_válido, lista_de_erros)
        """
        pass


# ================================
# IMPLEMENTAÇÃO DE REPOSITÓRIO
# ================================

class RepositorioMemoria(RepositorioBase):
    """
    Repositório em memória com índices otimizados.
    
    Características:
    - Armazenamento principal: Dict[str, Any] - O(1) para busca por ID
    - Índices automáticos: defaultdict para campos comuns - O(1) para busca por campo
    - Thread-safe: RLock para operações concorrentes
    - Busca eficiente: Usa índices quando disponíveis, senão busca linear
    
    Estrutura dos índices:
    _indices[campo][valor] = Set[id] - permite interseções eficientes para filtros múltiplos
    """
    
    def __init__(self, classe_entidade):
        """
        Inicializa o repositório.
        
        Args:
            classe_entidade: Classe das entidades que serão armazenadas
        """
        self.classe_entidade = classe_entidade
        self._dados: Dict[str, Any] = {}
        self._indices: Dict[str, Dict[Any, Set[str]]] = defaultdict(lambda: defaultdict(set))
        self._lock = threading.RLock()
    
    def criar(self, entidade: Any) -> str:
        """
        Cria uma nova entidade.
        
        Complexidade: O(1) para inserção + O(k) para índices (k = número de campos indexados)
        """
        with self._lock:
            self._dados[entidade.id] = entidade
            self._atualizar_indices(entidade.id, entidade)
            return entidade.id
    
    def buscar(self, id: str) -> Optional[Any]:
        """
        Busca uma entidade por ID.
        
        Complexidade: O(1) - acesso direto ao dicionário
        """
        return self._dados.get(id)
    
    def listar(self, filtros: Dict[str, Any] = None) -> List[Any]:
        """
        Lista entidades com filtros opcionais.
        
        Complexidade:
        - Sem filtros: O(n) - retorna todas as entidades
        - Com filtros indexados: O(k) onde k é o número de entidades que atendem aos filtros
        - Com filtros não indexados: O(n) - busca linear
        """
        if not filtros:
            return list(self._dados.values())
        
        # Usar índices para filtros eficientes
        ids_resultado = None
        
        for campo, valor in filtros.items():
            if campo in self._indices:
                # Busca O(1) no índice
                ids_campo = self._indices[campo].get(valor, set())
                if ids_resultado is None:
                    ids_resultado = ids_campo.copy()
                else:
                    # Interseção de sets - O(min(len(ids_resultado), len(ids_campo)))
                    ids_resultado &= ids_campo
            else:
                # Filtro sem índice - busca linear O(n)
                ids_filtro = {
                    id for id, entidade in self._dados.items()
                    if hasattr(entidade, campo) and getattr(entidade, campo) == valor
                }
                if ids_resultado is None:
                    ids_resultado = ids_filtro
                else:
                    ids_resultado &= ids_filtro
        
        return [self._dados[id] for id in (ids_resultado or [])]
    
    def atualizar(self, id: str, dados: Dict[str, Any]) -> bool:
        """
        Atualiza uma entidade.
        
        Complexidade: O(k) onde k é o número de campos indexados
        """
        with self._lock:
            if id not in self._dados:
                return False
            
            entidade = self._dados[id]
            self._remover_indices(id, entidade)
            
            # Atualizar campos
            for campo, valor in dados.items():
                if hasattr(entidade, campo):
                    setattr(entidade, campo, valor)
            
            self._atualizar_indices(id, entidade)
            return True
    
    def deletar(self, id: str) -> bool:
        """
        Deleta uma entidade.
        
        Complexidade: O(k) onde k é o número de campos indexados
        """
        with self._lock:
            if id not in self._dados:
                return False
            
            entidade = self._dados[id]
            self._remover_indices(id, entidade)
            del self._dados[id]
            return True
    
    def _atualizar_indices(self, id: str, entidade: Any):
        """
        Atualiza índices para uma entidade.
        
        Cria índices automáticos para campos comuns que são frequentemente
        usados em buscas e filtros.
        """
        # Campos que são automaticamente indexados para busca eficiente
        campos_indexados = ['nome', 'email', 'categoria', 'status', 'tipo', 'cliente_id']
        
        for campo in campos_indexados:
            if hasattr(entidade, campo):
                valor = getattr(entidade, campo)
                if valor is not None:
                    self._indices[campo][valor].add(id)
    
    def _remover_indices(self, id: str, entidade: Any):
        """
        Remove entidade dos índices.
        
        Percorre todos os índices e remove o ID da entidade.
        """
        for campo_dict in self._indices.values():
            for valor_set in campo_dict.values():
                valor_set.discard(id)  # discard não gera erro se ID não existir
    
    def contar(self) -> int:
        """
        Retorna o número de entidades.
        
        Complexidade: O(1)
        """
        return len(self._dados)
    
    def buscar_por_campo(self, campo: str, valor: Any) -> List[Any]:
        """
        Busca entidades por um campo específico.
        
        Complexidade:
        - Com índice: O(k) onde k é o número de entidades com o valor
        - Sem índice: O(n) busca linear
        """
        if campo in self._indices:
            ids = self._indices[campo].get(valor, set())
            return [self._dados[id] for id in ids]
        
        # Busca linear se não há índice
        return [
            entidade for entidade in self._dados.values()
            if hasattr(entidade, campo) and getattr(entidade, campo) == valor
        ]


# ================================
# VALIDADORES
# ================================

class ValidadorCliente(ValidadorBase):
    """
    Validador para dados de cliente.
    
    Regras de negócio:
    - Nome é obrigatório
    - Email deve ter formato válido (contém @)
    - Telefone deve ter pelo menos 10 dígitos
    - Limite de crédito não pode ser negativo
    """
    
    def validar(self, dados: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Valida dados do cliente."""
        erros = []
        
        # Nome obrigatório
        if not dados.get('nome', '').strip():
            erros.append("Nome é obrigatório")
        
        # Email válido (validação básica)
        email = dados.get('email', '')
        if email and '@' not in email:
            erros.append("Email inválido")
        
        # Telefone
        telefone = dados.get('telefone', '')
        if telefone and len(telefone) < 10:
            erros.append("Telefone deve ter pelo menos 10 dígitos")
        
        # Limite de crédito
        limite = dados.get('limite_credito', config.business.default_credit_limit)
        if limite < 0:
            erros.append("Limite de crédito não pode ser negativo")
        
        return len(erros) == 0, erros


class ValidadorProduto(ValidadorBase):
    """
    Validador para dados de produto.
    
    Regras de negócio:
    - Nome é obrigatório
    - Preço deve ser maior que zero
    - Estoque não pode ser negativo
    - Estoque mínimo não pode ser negativo
    """
    
    def validar(self, dados: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Valida dados do produto."""
        erros = []
        
        # Nome obrigatório
        if not dados.get('nome', '').strip():
            erros.append("Nome é obrigatório")
        
        # Preço válido
        preco = dados.get('preco', 0)
        if preco <= 0:
            erros.append("Preço deve ser maior que zero")
        
        # Estoque
        estoque = dados.get('estoque', 0)
        if estoque < 0:
            erros.append("Estoque não pode ser negativo")
        
        # Estoque mínimo
        estoque_min = dados.get('estoque_minimo', config.business.min_stock_level)
        if estoque_min < 0:
            erros.append("Estoque mínimo não pode ser negativo")
        
        return len(erros) == 0, erros


class ValidadorPedido(ValidadorBase):
    """
    Validador para dados de pedido.
    
    Regras de negócio:
    - Cliente é obrigatório
    - Pedido deve ter pelo menos um item
    - Cada item deve ter produto, quantidade > 0 e preço > 0
    """
    
    def validar(self, dados: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Valida dados do pedido."""
        erros = []
        
        # Cliente obrigatório
        if not dados.get('cliente_id'):
            erros.append("Cliente é obrigatório")
        
        # Itens obrigatórios
        itens = dados.get('itens', [])
        if not itens:
            erros.append("Pedido deve ter pelo menos um item")
        
        # Validar cada item
        for i, item in enumerate(itens):
            if not item.get('produto_id'):
                erros.append(f"Item {i+1}: Produto é obrigatório")
            
            quantidade = item.get('quantidade', 0)
            if quantidade <= 0:
                erros.append(f"Item {i+1}: Quantidade deve ser maior que zero")
            
            preco = item.get('preco_unitario', 0)
            if preco <= 0:
                erros.append(f"Item {i+1}: Preço deve ser maior que zero")
        
        return len(erros) == 0, erros